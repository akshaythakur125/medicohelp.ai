import random
from dataclasses import dataclass

from app.models import ContentFormat, Difficulty, NewsTopic, PostLane, SlotType, Subject


@dataclass(frozen=True)
class PlannedPost:
    lane: PostLane
    subject: Subject | None = None
    content_format: ContentFormat | None = None
    news_topic: NewsTopic | None = None
    difficulty: Difficulty | None = None


class ContentStrategy:
    # 12-slot rotation — 2 full cycles/day at 6 slots/cycle
    _WEIGHTED_LANES = [
        PostLane.mcq_variant,       # slot 1  — varied MCQ from existing pool
        PostLane.poll_quiz,          # slot 2  — native Telegram quiz poll
        PostLane.pyq_concept,        # slot 3
        PostLane.flashcard,          # slot 4
        PostLane.quick_revision,     # slot 5
        PostLane.poll_quiz,          # slot 6
        PostLane.mnemonic,           # slot 7
        PostLane.image_based,        # slot 8
        PostLane.daily_pack,         # slot 9  — burst of 5 revision items
        PostLane.pyq_concept,        # slot 10
        PostLane.residency_tip,      # slot 11
        PostLane.exam_news,          # slot 12
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

    # Difficulty distribution: 30% easy, 40% moderate, 30% exam-level
    _DIFFICULTY_WEIGHTS = [Difficulty.easy] * 3 + [Difficulty.moderate] * 4 + [Difficulty.exam_level] * 3

    def __init__(self) -> None:
        self._cursor = 0
        self._subjects = list(Subject)

    def next_post(
        self,
        slot_type: SlotType | None = None,
    ) -> PlannedPost:
        if slot_type:
            return self._plan_slot(slot_type)

        lane = self._WEIGHTED_LANES[self._cursor % len(self._WEIGHTED_LANES)]
        self._cursor += 1
        return self._build_planned(lane)

    def _plan_slot(self, slot_type: SlotType) -> PlannedPost:
        """Map a 4-phase day slot to a planned post lane."""
        mapping = {
            SlotType.morning_revision: PostLane.quick_revision,
            SlotType.afternoon_mcq: PostLane.mcq_variant,
            SlotType.evening_revision: PostLane.flashcard,
            SlotType.nightly_weak_topic: PostLane.weak_topic_recall,
        }
        lane = mapping.get(slot_type, PostLane.quick_revision)
        return self._build_planned(lane)

    def _build_planned(self, lane: PostLane) -> PlannedPost:
        if lane == PostLane.residency_tip:
            return PlannedPost(lane=lane, news_topic=NewsTopic.residency)

        if lane == PostLane.exam_news:
            return PlannedPost(
                lane=lane,
                news_topic=random.choice([NewsTopic.neet_pg, NewsTopic.inicet]),
            )

        subject = self._subjects[(self._cursor - 1) % len(self._subjects)]
        content_format = self._FORMAT_MAP.get(lane, ContentFormat.rapid_revision)
        difficulty = random.choice(self._DIFFICULTY_WEIGHTS)
        return PlannedPost(
            lane=lane,
            subject=subject,
            content_format=content_format,
            difficulty=difficulty,
        )
