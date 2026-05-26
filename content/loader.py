"""Static MBBS content library — used as fallback when no AI API key is set."""
from __future__ import annotations

import importlib
import logging
import random
from functools import lru_cache

from app.models import ContentFormat, GeneratedContent, Subject

logger = logging.getLogger(__name__)

_SUBJECT_MODULES: dict[Subject, str] = {
    Subject.anatomy: "content.anatomy",
    Subject.physiology: "content.physiology",
    Subject.biochemistry: "content.biochemistry",
    Subject.pathology: "content.pathology",
    Subject.pharmacology: "content.pharmacology",
    Subject.microbiology: "content.microbiology",
    Subject.forensic_medicine: "content.forensic_medicine",
    Subject.community_medicine: "content.community_medicine",
    Subject.general_medicine: "content.general_medicine",
    Subject.general_surgery: "content.general_surgery",
    Subject.obstetrics_gynecology: "content.obstetrics_gynecology",
    Subject.pediatrics: "content.pediatrics",
    Subject.ophthalmology: "content.ophthalmology",
    Subject.ent: "content.ent",
    Subject.orthopedics: "content.orthopedics",
    Subject.dermatology: "content.dermatology",
    Subject.psychiatry: "content.psychiatry",
    Subject.radiology: "content.radiology",
    Subject.anesthesiology: "content.anesthesiology",
}


class ContentLibrary:
    def __init__(self) -> None:
        self._topics: dict[Subject, list[GeneratedContent]] = {}
        self._load()

    def _load(self) -> None:
        for subject, module_name in _SUBJECT_MODULES.items():
            try:
                mod = importlib.import_module(module_name)
                self._topics[subject] = [GeneratedContent(**t) for t in mod.TOPICS]
            except Exception as exc:
                logger.warning("Could not load content for %s: %s", subject.value, exc)
                self._topics[subject] = []

    def get(
        self,
        subject: Subject | None = None,
        content_format: ContentFormat | None = None,
    ) -> GeneratedContent | None:
        pool = self._pool(subject, content_format)
        if not pool and content_format:
            pool = self._pool(subject, None)  # relax format, keep subject
        # Cross-subject fallback only when caller doesn't specify a subject
        if not pool and subject is None:
            pool = self._pool(None, content_format)
        if not pool and subject is None:
            pool = self._pool(None, None)
        return random.choice(pool) if pool else None

    def _pool(
        self,
        subject: Subject | None,
        content_format: ContentFormat | None,
    ) -> list[GeneratedContent]:
        items = (
            list(self._topics.get(subject, []))
            if subject
            else [t for ts in self._topics.values() for t in ts]
        )
        if content_format:
            items = [t for t in items if t.content_format == content_format]
        return items

    def pool(
        self,
        subject: Subject | None,
        content_format: ContentFormat | None,
    ) -> list[GeneratedContent]:
        """Public access to the filtered topic pool (used by SmartContentEngine)."""
        return self._pool(subject, content_format)

    def total(self) -> int:
        return sum(len(v) for v in self._topics.values())

    def summary(self) -> dict[str, int]:
        return {s.value: len(v) for s, v in self._topics.items()}


@lru_cache(maxsize=1)
def get_library() -> ContentLibrary:
    return ContentLibrary()
