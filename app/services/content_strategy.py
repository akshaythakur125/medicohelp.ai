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
    def __init__(self) -> None:
        self._cursor = 0
        self._subjects = list(Subject)
        self._weighted_lanes = [
            PostLane.image_based,
            PostLane.image_based,
            PostLane.pyq_concept,
            PostLane.quick_revision,
            PostLane.residency_tip,
            PostLane.exam_news,
        ]

    def next_post(self) -> PlannedPost:
        lane = self._weighted_lanes[self._cursor % len(self._weighted_lanes)]
        self._cursor += 1

        if lane == PostLane.residency_tip:
            return PlannedPost(lane=lane, news_topic=NewsTopic.residency)

        if lane == PostLane.exam_news:
            return PlannedPost(lane=lane, news_topic=random.choice([NewsTopic.neet_pg, NewsTopic.inicet]))

        subject = self._subjects[(self._cursor - 1) % len(self._subjects)]
        format_map = {
            PostLane.image_based: ContentFormat.image_based_question,
            PostLane.pyq_concept: ContentFormat.pyq_concept,
            PostLane.quick_revision: ContentFormat.rapid_revision,
        }
        return PlannedPost(lane=lane, subject=subject, content_format=format_map[lane])
