import random
from dataclasses import dataclass

from app.models import ContentFormat, NewsTopic, PostLane, Subject


@dataclass(frozen=True)
class PlannedPost:
    lane: PostLane
    subject: Subject | None = None
    content_format: ContentFormat | None = None
    news_topic: NewsTopic | None = None


class ContentStrategy:
    # 12-slot rotation mixing all content types (2 full cycles ≈ 24 posts/day at 3×/day)
    _WEIGHTED_LANES = [
        PostLane.image_based,    # slot 1
        PostLane.poll_quiz,      # slot 2  — native Telegram quiz poll
        PostLane.pyq_concept,    # slot 3
        PostLane.flashcard,      # slot 4
        PostLane.quick_revision, # slot 5
        PostLane.poll_quiz,      # slot 6
        PostLane.mnemonic,       # slot 7
        PostLane.image_based,    # slot 8
        PostLane.daily_pack,     # slot 9  — burst of 5 revision items
        PostLane.pyq_concept,    # slot 10
        PostLane.residency_tip,  # slot 11
        PostLane.exam_news,      # slot 12
    ]

    _FORMAT_MAP = {
        PostLane.image_based: ContentFormat.image_based_question,
        PostLane.pyq_concept: ContentFormat.pyq_concept,
        PostLane.quick_revision: ContentFormat.rapid_revision,
        PostLane.poll_quiz: ContentFormat.mcq,
        PostLane.flashcard: ContentFormat.flashcard,
        PostLane.mnemonic: ContentFormat.mnemonic,
        PostLane.daily_pack: ContentFormat.mcq,
    }

    def __init__(self) -> None:
        self._cursor = 0
        self._subjects = list(Subject)

    def next_post(self) -> PlannedPost:
        lane = self._WEIGHTED_LANES[self._cursor % len(self._WEIGHTED_LANES)]
        self._cursor += 1

        if lane == PostLane.residency_tip:
            return PlannedPost(lane=lane, news_topic=NewsTopic.residency)

        if lane == PostLane.exam_news:
            return PlannedPost(
                lane=lane,
                news_topic=random.choice([NewsTopic.neet_pg, NewsTopic.inicet]),
            )

        subject = self._subjects[(self._cursor - 1) % len(self._subjects)]
        content_format = self._FORMAT_MAP.get(lane, ContentFormat.rapid_revision)
        return PlannedPost(lane=lane, subject=subject, content_format=content_format)
