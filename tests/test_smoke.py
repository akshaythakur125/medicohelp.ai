import asyncio

from app.config import get_settings
from app.models import ContentFormat, NewsTopic, PostLane, Subject
from app.services.content_strategy import ContentStrategy
from app.services.orchestrator import PostOrchestrator


def test_curriculum_has_19_subjects() -> None:
    assert len(Subject) == 19


def test_mock_generation_text_mode() -> None:
    """In default text-only mode, poster_path is 'text-only' and no PNG is created."""
    settings = get_settings()
    settings.allow_mock_ai = True
    # text_only_mode=True is the default
    orchestrator = PostOrchestrator(settings)

    result = asyncio.run(
        orchestrator.generate_post(
            subject=Subject.pathology,
            content_format=ContentFormat.image_based_question,
            publish_to_telegram=False,
        )
    )

    assert result.content.title
    assert result.content.subject == Subject.pathology
    assert result.content.content_format == ContentFormat.image_based_question
    assert result.content.image_based_data
    assert result.content.question is not None
    assert len(result.content.question.splitlines()) >= 6
    assert result.content.explanation is not None
    assert len(result.content.explanation) > 180
    assert result.content.relevance_rationale
    assert result.content.image_answerability
    assert result.poster_path == "text-only"
    assert result.telegram_posted is False


def test_mock_generation_creates_poster() -> None:
    """With text_only_mode=False an actual PNG poster is generated."""
    settings = get_settings()
    settings.allow_mock_ai = True
    settings.text_only_mode = False
    orchestrator = PostOrchestrator(settings)

    result = asyncio.run(
        orchestrator.generate_post(
            subject=Subject.pathology,
            content_format=ContentFormat.image_based_question,
            publish_to_telegram=False,
        )
    )

    assert result.content.title
    assert result.poster_path.endswith(".png")
    assert result.telegram_posted is False


def test_residency_tip_generation_creates_post() -> None:
    settings = get_settings()
    orchestrator = PostOrchestrator(settings)

    result = asyncio.run(orchestrator.generate_news_post(topic=NewsTopic.residency, publish_to_telegram=False))

    assert result.content.news_topic == NewsTopic.residency
    assert result.content.content_format == ContentFormat.residency_survival_tip
    assert result.content.post_lane == PostLane.residency_tip
    assert "handoff" in result.content.caption.lower()
    assert result.poster_path.endswith(".png")


def test_content_strategy_rotates_premium_mix() -> None:
    strategy = ContentStrategy()
    planned = [strategy.next_post() for _ in range(6)]

    assert [item.lane for item in planned] == [
        PostLane.image_based,
        PostLane.image_based,
        PostLane.pyq_concept,
        PostLane.quick_revision,
        PostLane.residency_tip,
        PostLane.exam_news,
    ]
