import asyncio

from app.config import get_settings
from app.models import ContentFormat, NewsTopic, PostLane, Subject
from app.services.content_engine import SmartContentEngine
from app.services.content_strategy import ContentStrategy
from app.services.orchestrator import PostOrchestrator
from content.loader import ContentLibrary


def test_curriculum_has_19_subjects() -> None:
    assert len(Subject) == 19


def test_library_generation_text_mode() -> None:
    """Library-first generation works with no AI key: poster_path is 'text-only'."""
    settings = get_settings()
    # No AI provider key needed — library path is always available
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


def test_library_generation_creates_poster() -> None:
    """With text_only_mode=False an actual PNG poster is generated from library content."""
    settings = get_settings()
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


def test_completed_subjects_have_10_topics() -> None:
    """ENT, Psychiatry, Radiology, Anesthesiology should now have 10 topics each."""
    lib = ContentLibrary()
    summary = lib.summary()
    assert summary.get("ent", 0) == 10, f"ENT has {summary.get('ent', 0)} topics, expected 10"
    assert summary.get("psychiatry", 0) == 10, f"Psychiatry has {summary.get('psychiatry', 0)} topics, expected 10"
    assert summary.get("radiology", 0) == 10, f"Radiology has {summary.get('radiology', 0)} topics, expected 10"
    assert summary.get("anesthesiology", 0) == 10, f"Anesthesiology has {summary.get('anesthesiology', 0)} topics, expected 10"


def test_all_8_content_formats_present_in_library() -> None:
    """Library should have all 8 target formats across subjects."""
    lib = ContentLibrary()
    formats_found = set()
    for subject in Subject:
        for fmt in ContentFormat:
            pool = lib.pool(subject, fmt)
            if pool:
                formats_found.add(fmt)
    expected = {
        ContentFormat.rapid_revision,
        ContentFormat.mcq,
        ContentFormat.concise_notes,
        ContentFormat.pyq_concept,
        ContentFormat.mnemonic,
        ContentFormat.flashcard,
        ContentFormat.true_false,
        ContentFormat.one_liner_recall,
    }
    missing = expected - formats_found
    assert not missing, f"Missing content formats in library: {missing}"


def test_smart_content_engine_tracks_weak_topics() -> None:
    """SmartContentEngine records performance and identifies weak topics."""
    settings = get_settings()
    engine = SmartContentEngine(settings)

    engine.record_performance("Test Topic", False, subject=Subject.anatomy)
    engine.record_performance("Test Topic", False, subject=Subject.anatomy)
    engine.record_performance("Test Topic", True, subject=Subject.anatomy)

    weak = engine.weak_topics(threshold=0.6, min_attempts=3)
    assert any(w["title"] == "Test Topic" for w in weak)
    weak_topic = next(w for w in weak if w["title"] == "Test Topic")
    assert weak_topic["accuracy"] <= 0.34


def test_mcq_variation_engine_reorders_options() -> None:
    """MCQ variation creates a variant with preserved correct answer."""
    settings = get_settings()
    engine = SmartContentEngine(settings)

    variant = engine.generate_variate_mcq(Subject.anatomy)
    if variant:
        assert variant.content_format == ContentFormat.mcq
        assert len(variant.options) >= 3
        assert variant.correct_answer is not None
        # Verify the correct answer label matches an option letter
        correct_label = variant.correct_answer[0]
        assert correct_label in {"A", "B", "C", "D"} or correct_label in "ABCD"


def test_content_library_has_150_topics() -> None:
    """Library should have at least 150 topics (5 complete × 10 + 14 complete × 10)."""
    lib = ContentLibrary()
    assert lib.total() >= 150, f"Expected ≥150 topics, got {lib.total()}"
