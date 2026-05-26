"""Analytics system: content usage tracking, subject frequency, weak-topic trends, engagement estimates."""
import json
import logging
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

from app.models import ContentFormat, GeneratedContent, Subject

logger = logging.getLogger(__name__)

_WINDOW_DAYS = 30


class ContentAnalytics:
    def __init__(self, logs_dir: Path) -> None:
        self._path = logs_dir / "analytics.json"
        self._data: dict[str, Any] = self._load()

    # ── Recording ────────────────────────────────────────────────────────

    def record_post(self, content: GeneratedContent) -> None:
        now = datetime.now(tz=timezone.utc).isoformat()
        subj = content.subject.value if content.subject else "unknown"
        fmt = content.content_format.value

        # Subject frequency
        self._data.setdefault("subject_frequency", {}).setdefault(subj, 0)
        self._data["subject_frequency"][subj] += 1

        # Format frequency
        self._data.setdefault("format_frequency", {}).setdefault(fmt, 0)
        self._data["format_frequency"][fmt] += 1

        # Daily post count
        day = now[:10]
        self._data.setdefault("daily_counts", {}).setdefault(day, 0)
        self._data["daily_counts"][day] += 1

        # Timeline
        self._data.setdefault("timeline", []).append({
            "timestamp": now,
            "subject": subj,
            "format": fmt,
            "title": content.title[:80],
        })
        self._data["timeline"] = self._data["timeline"][-500:]

        # Weak topic frequency
        for tag in (content.topic_tags or []):
            self._data.setdefault("tag_frequency", {}).setdefault(tag, 0)
            self._data["tag_frequency"][tag] += 1

        self._save()

    def record_weak_spotlight(self, title: str, accuracy: float, subject: str | None) -> None:
        now = datetime.now(tz=timezone.utc).isoformat()
        self._data.setdefault("weak_topic_spottlights", []).append({
            "timestamp": now,
            "title": title[:80],
            "accuracy": accuracy,
            "subject": subject or "unknown",
        })
        self._data["weak_topic_spottlights"] = self._data["weak_topic_spottlights"][-200:]
        self._save()

    # ── Queries ──────────────────────────────────────────────────────────

    def most_posted_subjects(self, top_n: int = 5) -> list[dict]:
        freq = self._data.get("subject_frequency", {})
        sorted_subjects = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [{"subject": s, "count": c} for s, c in sorted_subjects[:top_n]]

    def most_used_formats(self, top_n: int = 5) -> list[dict]:
        freq = self._data.get("format_frequency", {})
        sorted_fmts = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        return [{"format": f, "count": c} for f, c in sorted_fmts[:top_n]]

    def weak_subject_trends(self) -> list[dict]:
        spots = self._data.get("weak_topic_spottlights", [])
        if not spots:
            return []
        subj_counts: dict[str, int] = {}
        for s in spots:
            sub = s.get("subject", "unknown")
            acc = s.get("accuracy", 0)
            if sub:
                subj_counts.setdefault(sub, {"count": 0, "total_accuracy": 0.0})
                subj_counts[sub]["count"] += 1
                subj_counts[sub]["total_accuracy"] += acc
        result = []
        for sub, info in subj_counts.items():
            result.append({
                "subject": sub,
                "weak_spotlights": info["count"],
                "avg_accuracy": round(info["total_accuracy"] / info["count"], 2),
            })
        return sorted(result, key=lambda x: x["weak_spotlights"], reverse=True)

    def daily_post_rate(self, days: int = 7) -> dict:
        daily = self._data.get("daily_counts", {})
        now = datetime.now(tz=timezone.utc)
        result = {}
        for i in range(days):
            day = (now - timedelta(days=i)).strftime("%Y-%m-%d")
            result[day] = daily.get(day, 0)
        return result

    def estimated_engagement(self) -> dict:
        total = sum(self._data.get("daily_counts", {}).values())
        days_active = max(len(self._data.get("daily_counts", {})), 1)
        avg = round(total / days_active, 1) if days_active else 0
        return {
            "total_posts": total,
            "days_active": days_active,
            "avg_posts_per_day": avg,
            "unique_subjects_posted": len(self._data.get("subject_frequency", {})),
            "unique_formats_used": len(self._data.get("format_frequency", {})),
        }

    def report(self) -> dict:
        return {
            "most_posted_subjects": self.most_posted_subjects(),
            "most_used_formats": self.most_used_formats(),
            "weak_subject_trends": self.weak_subject_trends(),
            "daily_post_rate": self.daily_post_rate(),
            "engagement": self.estimated_engagement(),
            "recent_weak_spotlights": self._data.get("weak_topic_spottlights", [])[-5:],
        }

    # ── Persistence ──────────────────────────────────────────────────────

    def _load(self) -> dict[str, Any]:
        if self._path.exists():
            try:
                return json.loads(self._path.read_text(encoding="utf-8"))
            except Exception as exc:
                logger.warning("Could not read analytics data: %s", exc)
        return {}

    def _save(self) -> None:
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(
                json.dumps(self._data, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as exc:
            logger.warning("Could not save analytics data: %s", exc)
