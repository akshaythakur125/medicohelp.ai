"""SmartContentEngine: spaced repetition + offline format variation from the static library."""
from __future__ import annotations

import json
import logging
import random
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from app.models import ContentFormat, GeneratedContent, Subject

if TYPE_CHECKING:
    from app.config import Settings

logger = logging.getLogger(__name__)

_SPACED_REPETITION_DAYS = 7
_VARIATION_FORMATS = {
    ContentFormat.rapid_revision: ContentFormat.pyq_concept,
    ContentFormat.mcq: ContentFormat.rapid_revision,
    ContentFormat.concise_notes: ContentFormat.clinical_case,
    ContentFormat.pyq_concept: ContentFormat.rapid_revision,
}


class SmartContentEngine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._history_path = Path("logs/topic_history.json")
        self._history: dict[str, str] = self._load_history()

    def generate(self, subject: Subject, content_format: ContentFormat) -> GeneratedContent | None:
        """Return content with spaced repetition applied. Falls back to a variation if no fresh topic."""
        content = self._get_with_spaced_repetition(subject, content_format)
        if content:
            self._record(content)
            return content

        # All topics seen recently — try a format variation on any available topic
        variation = self._generate_variation(subject)
        if variation:
            self._record(variation)
            return variation

        return None

    def stats(self) -> dict:
        """Return statistics about the library and send history."""
        try:
            from content.loader import get_library
            lib = get_library()
            summary = lib.summary()
            total_lib = lib.total()
        except Exception:
            summary = {}
            total_lib = 0

        sent = set(self._history.keys())
        unseen = max(0, total_lib - len(sent))

        now = datetime.now(tz=timezone.utc)
        cutoff = now - timedelta(days=_SPACED_REPETITION_DAYS)
        recent = sum(
            1 for ts in self._history.values()
            if datetime.fromisoformat(ts) >= cutoff
        )

        return {
            "library_topics": total_lib,
            "topics_sent": len(sent),
            "topics_unseen": unseen,
            "sent_last_7_days": recent,
            "by_subject": summary,
        }

    # ── Internal helpers ───────────────────────────────────────────────────────

    def _get_with_spaced_repetition(
        self,
        subject: Subject,
        content_format: ContentFormat,
    ) -> GeneratedContent | None:
        try:
            from content.loader import get_library
            lib = get_library()
        except Exception as exc:
            logger.debug("Content library unavailable: %s", exc)
            return None

        now = datetime.now(tz=timezone.utc)
        cutoff = now - timedelta(days=_SPACED_REPETITION_DAYS)
        recently_seen = {
            title for title, ts in self._history.items()
            if datetime.fromisoformat(ts) >= cutoff
        }

        pool = lib.pool(subject, content_format)
        if not pool:
            pool = lib.pool(subject, None)

        fresh = [c for c in pool if c.title not in recently_seen]

        if fresh:
            return random.choice(fresh)

        if pool:
            # All seen — pick the least recently seen to minimise repetition
            def _last_seen(c: GeneratedContent) -> datetime:
                ts = self._history.get(c.title)
                if ts:
                    return datetime.fromisoformat(ts)
                return datetime.min.replace(tzinfo=timezone.utc)

            return min(pool, key=_last_seen)

        return None

    def _generate_variation(self, subject: Subject) -> GeneratedContent | None:
        """Create a new-angle variation from any available topic for the subject."""
        try:
            from content.loader import get_library
            lib = get_library()
        except Exception:
            return None

        pool = lib.pool(subject, None)
        if not pool:
            return None

        source = random.choice(pool)
        target_format = _VARIATION_FORMATS.get(source.content_format)
        if not target_format:
            return None

        if source.content_format == ContentFormat.rapid_revision:
            return self._rapid_to_pyq(source)
        if source.content_format == ContentFormat.mcq:
            return self._mcq_to_rapid(source)
        if source.content_format in (ContentFormat.concise_notes, ContentFormat.pyq_concept):
            return self._notes_to_case(source)
        return None

    def _rapid_to_pyq(self, source: GeneratedContent) -> GeneratedContent:
        intro = (
            "NEET-PG repeatedly tests this topic. "
            "Know the classic clue, the close mimic, and the one-liner takeaway.\n\n"
        )
        return GeneratedContent(
            title=f"{source.title} — PYQ Pattern",
            caption=(intro + source.caption)[:2000],
            hashtags=_swap_tag(source.hashtags, "RapidRevision", "PYQ"),
            poster_text=f"Previous year pattern: {source.poster_text}"[:320],
            image_prompt=source.image_prompt,
            high_yield_takeaway=source.high_yield_takeaway,
            subject=source.subject,
            content_format=ContentFormat.pyq_concept,
            post_lane=source.post_lane,
        )

    def _mcq_to_rapid(self, source: GeneratedContent) -> GeneratedContent:
        base = source.explanation or source.caption
        intro = f"Key concept from MCQ: {source.title}\n\n"
        caption = (intro + base)[:2000]
        return GeneratedContent(
            title=f"{source.title} — Rapid Notes",
            caption=caption,
            hashtags=_swap_tag(source.hashtags, "MCQ", "RapidRevision"),
            poster_text=f"Concept: {source.poster_text}"[:320],
            high_yield_takeaway=source.high_yield_takeaway,
            subject=source.subject,
            content_format=ContentFormat.rapid_revision,
            post_lane=source.post_lane,
        )

    def _notes_to_case(self, source: GeneratedContent) -> GeneratedContent:
        lines = [
            l.strip()[2:] for l in source.caption.split("\n")
            if l.strip().startswith("• ")
        ]
        clue = lines[0] if lines else source.poster_text
        scenario = (
            f"A patient presents with findings consistent with {source.title}. "
            f"The key clinical clue is: {clue} "
            f"What is the most appropriate next step in management?"
        )
        discussion = (source.high_yield_takeaway or "") + "\n\n" + source.caption
        return GeneratedContent(
            title=f"{source.title} — Case",
            caption=f"Clinical case based on: {source.title}\n\n{source.poster_text}"[:2000],
            hashtags=_swap_tag(source.hashtags, "ConciseNotes", "ClinicalCase"),
            poster_text=f"Case: {source.poster_text}"[:320],
            question=scenario[:1200],
            correct_answer=f"Investigate and manage {source.title}"[:200],
            explanation=discussion[:1600],
            high_yield_takeaway=source.high_yield_takeaway,
            subject=source.subject,
            content_format=ContentFormat.clinical_case,
            post_lane=source.post_lane,
        )

    def _record(self, content: GeneratedContent) -> None:
        self._history[content.title] = datetime.now(tz=timezone.utc).isoformat()
        self._save_history()

    def _load_history(self) -> dict[str, str]:
        if self._history_path.exists():
            try:
                return json.loads(self._history_path.read_text(encoding="utf-8"))
            except Exception as exc:
                logger.warning("Could not read topic history: %s", exc)
        return {}

    def _save_history(self) -> None:
        try:
            self._history_path.parent.mkdir(parents=True, exist_ok=True)
            self._history_path.write_text(
                json.dumps(self._history, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as exc:
            logger.warning("Could not save topic history: %s", exc)


def _swap_tag(tags: list[str], old: str, new: str) -> list[str]:
    """Replace a hashtag containing `old` with one containing `new`."""
    result = []
    replaced = False
    for t in tags:
        if old.lower() in t.lower() and not replaced:
            result.append(f"#{new}")
            replaced = True
        else:
            result.append(t)
    if not replaced:
        result.append(f"#{new}")
    return result
