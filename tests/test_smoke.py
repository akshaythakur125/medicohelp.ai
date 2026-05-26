import asyncio

from app.config import get_settings
from app.models import ContentFormat, NewsTopic, PostLane, Subject
from app.services.content_strategy import ContentStrategy
from app.services.orchestrator import PostOrchestrator
from content.loader import ContentLibrary


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
            subject=Subject.anatomy,
            content_format=ContentFormat.rapid_revision,
            publish_to_telegram=False,
        )
    )

    assert result.content.title
    assert result.content.subject == Subject.anatomy
    assert result.content.caption
    assert result.content.high_yield_takeaway
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


def test_content_library_loads_all_subjects() -> None:
    lib = ContentLibrary()
    summary = lib.summary()
    missing = [s.value for s in Subject if summary.get(s.value, 0) == 0]
    assert not missing, f"Subjects with no content: {missing}"
    assert lib.total() >= 19 * 4, f"Expected ≥76 topics, got {lib.total()}"


def test_content_library_serves_by_subject_and_format() -> None:
    lib = ContentLibrary()
    content = lib.get(Subject.anatomy, ContentFormat.rapid_revision)
    assert content is not None
    assert content.subject == Subject.anatomy
    assert content.content_format == ContentFormat.rapid_revision


def test_content_library_fallback_on_unknown_format() -> None:
    """Library falls back gracefully when exact format+subject combo is missing."""
    lib = ContentLibrary()
    content = lib.get(Subject.anatomy, ContentFormat.image_based_question)
    assert content is not None  # Falls back to any anatomy topic


def test_content_strategy_rotates_premium_mix() -> None:
    strategy = ContentStrategy()
    planned = [strategy.next_post() for _ in range(12)]
    lanes = [item.lane for item in planned]

    # Verify all expected lane types appear in the 12-slot cycle
    assert PostLane.image_based in lanes
    assert PostLane.poll_quiz in lanes
    assert PostLane.pyq_concept in lanes
    assert PostLane.flashcard in lanes
    assert PostLane.quick_revision in lanes
    assert PostLane.mnemonic in lanes
    assert PostLane.daily_pack in lanes
    assert PostLane.residency_tip in lanes
    assert PostLane.exam_news in lanes
    assert len(lanes) == 12
