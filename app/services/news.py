import html
import logging
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from urllib.parse import quote_plus, urlparse

import httpx

from app.config import Settings
from app.models import ContentFormat, GeneratedContent, NewsItem, NewsTopic, PostLane

logger = logging.getLogger(__name__)


class NewsSweeper:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    async def fetch_latest(self, topic: NewsTopic) -> list[NewsItem]:
        query = self._query_for_topic(topic)
        url = f"https://news.google.com/rss/search?q={quote_plus(query)}&hl=en-IN&gl=IN&ceid=IN:en"
        async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
            response = await client.get(url)
            response.raise_for_status()

        items = self._parse_rss(response.text)
        return self._rank_and_limit(items)

    def build_content(self, topic: NewsTopic, items: list[NewsItem]) -> GeneratedContent:
        if not items:
            return self._fallback_content(topic)

        primary = items[0]
        topic_label = self._label(topic.value)
        bullets = "\n".join(f"- {item.title} ({item.source})" for item in items[:4])
        source_urls = [item.url for item in items[: self.settings.news_max_items]]
        caption = (
            f"{topic_label} latest update sweep\n\n"
            f"{bullets}\n\n"
            "Verify exam decisions only from official portals before acting on deadlines, counselling, or application changes.\n\n"
            f"Primary source/link: {primary.url}"
        )
        return GeneratedContent(
            title=f"{topic_label}: Latest Updates",
            caption=caption,
            hashtags=["#MedicoHelp", "#NEETPG" if topic == NewsTopic.neet_pg else "#INICET", "#MedicalStudents"],
            poster_text=primary.title[:280],
            image_prompt=f"Clean news update card for {topic_label} postgraduate medical exam updates.",
            visual_description="News update card with official notice/search result style layout",
            visual_labels=["Latest", "Verify", "Deadline", "Official source"],
            question=None,
            options=[],
            correct_answer=None,
            explanation=(
                "This update is generated from recent web/news feed results. Students should use it as an alert "
                "and confirm all actionable details on official exam portals."
            ),
            high_yield_takeaway="Treat this as an alert; verify dates and eligibility on official websites.",
            relevance_rationale=f"{topic_label} updates directly affect exam applications, admit cards, results, and counselling.",
            image_answerability="This is a news card, so the visual hierarchy highlights the latest headline and verification warning.",
            source_title=primary.title,
            source_url=primary.url,
            source_urls=source_urls,
            news_topic=topic,
            post_lane=PostLane.exam_news,
            content_format=ContentFormat.exam_news_update,
        )

    def build_residency_tip(self) -> GeneratedContent:
        return GeneratedContent(
            title="Residency Survival Tip",
            caption=(
                "Residency survival tip: Build a handoff ritual.\n\n"
                "Before leaving the ward, write the sickest patients first, pending reports second, and jobs that can wait last. "
                "Use closed-loop communication for critical tasks and document escalation clearly. This protects patients and "
                "also protects you during busy calls."
            ),
            hashtags=["#MedicoHelp", "#Residency", "#MedicalPG", "#ResidentLife"],
            poster_text="Handoff rule: sickest first, pending reports second, routine jobs last.",
            image_prompt="Realistic hospital resident handoff scene, checklist, ward desk, night duty educational visual.",
            visual_description="Resident handoff checklist at a hospital workstation",
            visual_labels=["Sickest first", "Pending reports", "Escalation", "Closed-loop"],
            question=(
                "A first-year resident is finishing a 24-hour duty and has six unstable tasks pending.\n"
                "Two patients need reassessment, one lab value is critical, and three routine discharge summaries remain.\n"
                "The next resident is busy in emergency and asks for a quick handoff.\n"
                "The unsafe approach is to list tasks randomly or mention only bed numbers.\n"
                "A safer handoff prioritizes clinical risk and makes ownership explicit.\n"
                "Which structure best reduces missed tasks during residency duty changes?"
            ),
            options=[
                "A. Sickest patients, pending reports, then routine jobs",
                "B. Routine paperwork first to reduce workload",
                "C. Only verbal handoff without written backup",
                "D. Wait for the next resident to discover pending tasks",
            ],
            correct_answer="A. Sickest patients, pending reports, then routine jobs",
            explanation=(
                "The safest handoff starts with unstable patients because delays can harm patients quickly. Pending reports "
                "come next because they may change management during the next shift. Routine administrative work should be "
                "clearly listed but should not bury urgent clinical risks. A written checklist plus closed-loop communication "
                "helps residents survive workload without losing patient safety."
            ),
            high_yield_takeaway="A good handoff is a patient-safety tool, not just a courtesy.",
            relevance_rationale="Handoffs are a daily survival skill for postgraduate residents and directly affect patient safety.",
            image_answerability="The card uses a checklist visual because prioritization is the core practical skill.",
            news_topic=NewsTopic.residency,
            post_lane=PostLane.residency_tip,
            content_format=ContentFormat.residency_survival_tip,
        )

    def _parse_rss(self, xml_text: str) -> list[NewsItem]:
        root = ET.fromstring(xml_text)
        items: list[NewsItem] = []
        for item in root.findall(".//item"):
            title = self._clean(item.findtext("title") or "")
            link = item.findtext("link") or ""
            published = item.findtext("pubDate")
            source_node = item.find("{*}source")
            source = source_node.text if source_node is not None and source_node.text else self._domain(link)
            summary = self._clean(item.findtext("description") or "")
            if not title or not link:
                continue
            if not self._is_recent(published):
                continue
            items.append(NewsItem(title=title, url=link, source=source, published=published, summary=summary))
        return items

    def _rank_and_limit(self, items: list[NewsItem]) -> list[NewsItem]:
        official_domains = ("natboard.edu.in", "nbe.edu.in", "aiimsexams.ac.in", "docs.aiimsexams.ac.in", "mcc.nic.in")

        def score(item: NewsItem) -> tuple[int, float]:
            domain = self._domain(item.url)
            official = 0 if any(official in domain for official in official_domains) else 1
            return (official, -self._published_timestamp(item.published))

        return sorted(items, key=score)[: self.settings.news_max_items]

    def _is_recent(self, published: str | None) -> bool:
        if not published:
            return True
        try:
            parsed = parsedate_to_datetime(published)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed >= datetime.now(timezone.utc) - timedelta(days=self.settings.news_lookback_days)
        except (TypeError, ValueError):
            return True

    def _published_timestamp(self, published: str | None) -> float:
        if not published:
            return 0
        try:
            parsed = parsedate_to_datetime(published)
            if parsed.tzinfo is None:
                parsed = parsed.replace(tzinfo=timezone.utc)
            return parsed.timestamp()
        except (TypeError, ValueError, OSError):
            return 0

    def _fallback_content(self, topic: NewsTopic) -> GeneratedContent:
        topic_label = self._label(topic.value)
        official = "https://natboard.edu.in" if topic == NewsTopic.neet_pg else "https://www.aiimsexams.ac.in"
        return GeneratedContent(
            title=f"{topic_label}: Verify Official Portal",
            caption=(
                f"No recent feed item was found for {topic_label} in the configured lookback window.\n\n"
                f"Check the official portal directly: {official}"
            ),
            hashtags=["#MedicoHelp", "#MedicalStudents"],
            poster_text=f"No recent {topic_label} news found. Verify the official portal directly.",
            visual_description="Official portal verification reminder card",
            visual_labels=["No recent item", "Verify", "Official portal", "Avoid rumors"],
            source_url=official,
            source_urls=[official],
            news_topic=topic,
            post_lane=PostLane.exam_news,
            content_format=ContentFormat.exam_news_update,
        )

    def _query_for_topic(self, topic: NewsTopic) -> str:
        queries = {
            NewsTopic.neet_pg: "NEET PG NBEMS latest notice OR counselling OR admit card OR result",
            NewsTopic.inicet: "INI CET AIIMS latest notice OR registration OR counselling OR result",
            NewsTopic.residency: "medical residency tips burnout handoff sleep postgraduate residents",
        }
        return queries[topic]

    def _clean(self, value: str) -> str:
        value = html.unescape(re.sub("<[^<]+?>", " ", value))
        return re.sub(r"\s+", " ", value).strip()

    def _domain(self, url: str) -> str:
        return urlparse(url).netloc.replace("www.", "")

    def _label(self, value: str) -> str:
        return value.replace("_", " ").upper() if value != "inicet" else "INI-CET"
