"""Autonomous rotation engine: no consecutive subject repeats, format mixing, weak-topic prioritisation, balanced schedule."""
import logging
import random
from collections import deque
from dataclasses import dataclass
from typing import Callable

from app.models import ContentFormat, Difficulty, NewsTopic, PostLane, SlotType, Subject

logger = logging.getLogger(__name__)

_RECENT_WINDOW = 8


@dataclass(frozen=True)
class PlannedPost:
    lane: PostLane
    subject: Subject | None = None
    content_format: ContentFormat | None = None
    news_topic: NewsTopic | None = None
    difficulty: Difficulty | None = None


_SLOT_LANE_MAP: dict[SlotType, PostLane] = {
    SlotType.morning_revision: PostLane.quick_revision,
    SlotType.afternoon_mcq: PostLane.mcq_variant,
    SlotType.evening_revision: PostLane.flashcard,
    SlotType.nightly_weak_topic: PostLane.weak_topic_recall,
}

_NIGHT_REPLACEMENT_LANES = [
    PostLane.flashcard,
    PostLane.quick_revision,
    PostLane.poll_quiz,
]

_WEAK_TOPIC_DRAW_P = 0.25


class ContentStrategy:
    def __init__(self) -> None:
        self._cursor = 0
        self._subjects = list(Subject)
        self._last_subject: Subject | None = None
        self._recent_formats: deque[str] = deque(maxlen=_RECENT_WINDOW)
        self._posted_titles: set[str] = set()
        self._cycle_count = 0
        self._weak_provider: Callable[[], list[dict]] | None = None

    def set_weak_provider(self, provider: Callable[[], list[dict]]) -> None:
        self._weak_provider = provider

    def mark_posted(self, title: str) -> None:
        self._posted_titles.add(title)
        if len(self._posted_titles) > 500:
            self._posted_titles = set(list(self._posted_titles)[-250:])

    def is_posted(self, title: str) -> bool:
        return title in self._posted_titles

    def next_post(self, slot_type: SlotType | None = None) -> PlannedPost:
        if slot_type and slot_type == SlotType.nightly_weak_topic:
            weak = self._get_weak_post()
            if weak:
                return weak

        if slot_type:
            lane = _SLOT_LANE_MAP.get(slot_type)
            if lane:
                if lane == PostLane.weak_topic_recall:
                    weak = self._get_weak_post()
                    if weak:
                        return weak
                    lane = random.choice(_NIGHT_REPLACEMENT_LANES)
                return self._build_planned(lane, slot_type=slot_type)

        lane = self._WEIGHTED_LANES[self._cursor % len(self._WEIGHTED_LANES)]
        self._cursor += 1
        return self._build_planned(lane)

    def _get_weak_post(self) -> PlannedPost | None:
        if not self._weak_provider:
            return None
        try:
            weak_list = self._weak_provider()
            if not weak_list:
                return None
            target = weak_list[0]
            subject_val = target.get("subject")
            subj = next((s for s in Subject if s.value == subject_val), None) if subject_val else None
            return PlannedPost(
                lane=PostLane.weak_topic_recall,
                subject=subj,
                content_format=ContentFormat.rapid_revision,
                difficulty=Difficulty.exam_level,
            )
        except Exception as exc:
            logger.debug("Weak topic provider error: %s", exc)
        return None

    def _pick_subject(self) -> Subject:
        if random.random() < _WEAK_TOPIC_DRAW_P and self._weak_provider:
            try:
                weak_list = self._weak_provider()
                if weak_list:
                    filtered = [w for w in weak_list if w.get("subject")]
                    if filtered:
                        target = filtered[0]
                        subj = next((s for s in Subject if s.value == target["subject"]), None)
                        if subj:
                            self._last_subject = subj
                            return subj
            except Exception:
                pass

        candidates = [s for s in self._subjects if s != self._last_subject]
        if not candidates:
            candidates = self._subjects
        chosen = random.choice(candidates)
        self._last_subject = chosen
        return chosen

    def _pick_difficulty(self) -> Difficulty:
        return random.choice(self._DIFFICULTY_WEIGHTS)

    def _build_planned(self, lane: PostLane, slot_type: SlotType | None = None) -> PlannedPost:
        if lane == PostLane.residency_tip:
            return PlannedPost(lane=lane, news_topic=NewsTopic.residency)
        if lane == PostLane.exam_news:
            return PlannedPost(
                lane=lane,
                news_topic=random.choice([NewsTopic.neet_pg, NewsTopic.inicet]),
            )
        if lane == PostLane.weak_topic_recall:
            weak = self._get_weak_post()
            if weak:
                return weak

        subject = self._pick_subject()
        content_format = self._FORMAT_MAP.get(lane, ContentFormat.rapid_revision)
        difficulty = self._pick_difficulty()

        if content_format and content_format.value:
            self._recent_formats.append(content_format.value)

        return PlannedPost(
            lane=lane,
            subject=subject,
            content_format=content_format,
            difficulty=difficulty,
        )

    # ── Slot definitions ─────────────────────────────────────────────────

    _WEIGHTED_LANES = [
        PostLane.mcq_variant,
        PostLane.poll_quiz,
        PostLane.pyq_concept,
        PostLane.flashcard,
        PostLane.quick_revision,
        PostLane.poll_quiz,
        PostLane.mnemonic,
        PostLane.true_false,
        PostLane.daily_pack,
        PostLane.pyq_concept,
        PostLane.residency_tip,
        PostLane.exam_news,
    ]

    _FORMAT_MAP = {
        PostLane.image_based: ContentFormat.image_based_question,
        PostLane.pyq_concept: ContentFormat.pyq_concept,
        PostLane.quick_revision: ContentFormat.rapid_revision,
        PostLane.poll_quiz: ContentFormat.mcq,
        PostLane.flashcard: ContentFormat.flashcard,
        PostLane.mnemonic: ContentFormat.mnemonic,
        PostLane.daily_pack: ContentFormat.mcq,
        PostLane.mcq_variant: ContentFormat.mcq,
        PostLane.true_false: ContentFormat.true_false,
        PostLane.one_liner_recall: ContentFormat.one_liner_recall,
        PostLane.weak_topic_recall: ContentFormat.rapid_revision,
    }

    _DIFFICULTY_WEIGHTS = [Difficulty.easy] * 3 + [Difficulty.moderate] * 4 + [Difficulty.exam_level] * 3
