import asyncio

from app.config import get_settings
from app.models import ContentFormat, Difficulty, NewsTopic, PostLane, SlotType, Subject
from app.services.content_engine import SmartContentEngine
from app.services.content_strategy import ContentStrategy
from app.services.orchestrator import PostOrchestrator
from content.loader import ContentLibrary


def test_curriculum_has_19_subjects() -> None:
    assert len(Subject) == 19


def test_library_generation_text_mode() -> None:
    """Library-first generation works with no AI key: poster_path is 'text-only'."""
    settings = get_settings()
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

    result = asyncio.run(
        orchestrator.generate_news_post(topic=NewsTopic.residency, publish_to_telegram=False)
    )

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

    assert PostLane.true_false in lanes
    assert PostLane.poll_quiz in lanes
    assert PostLane.pyq_concept in lanes
    assert PostLane.flashcard in lanes
    assert PostLane.quick_revision in lanes
    assert PostLane.mnemonic in lanes
    assert PostLane.daily_pack in lanes
    assert PostLane.residency_tip in lanes
    assert PostLane.exam_news in lanes
    assert PostLane.mcq_variant in lanes
    assert len(lanes) == 12


def test_content_strategy_slot_type_mapping() -> None:
    """Slot type mapping produces expected lanes."""
    strategy = ContentStrategy()
    morning = strategy.next_post(slot_type=SlotType.morning_revision)
    afternoon = strategy.next_post(slot_type=SlotType.afternoon_mcq)
    evening = strategy.next_post(slot_type=SlotType.evening_revision)

    assert morning.lane == PostLane.quick_revision
    assert afternoon.lane == PostLane.mcq_variant
    assert evening.lane == PostLane.flashcard

    # Nightly weak-topic falls back to a replacement lane when no weak provider set
    nightly = strategy.next_post(slot_type=SlotType.nightly_weak_topic)
    assert nightly.lane in (
        PostLane.flashcard, PostLane.quick_revision, PostLane.poll_quiz, PostLane.weak_topic_recall,
    )


def test_completed_subjects_have_10_topics() -> None:
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

    engine.record_performance("Test Topic A", False, subject=Subject.anatomy)
    engine.record_performance("Test Topic A", False, subject=Subject.anatomy)
    engine.record_performance("Test Topic A", True, subject=Subject.anatomy)

    weak = engine.weak_topics(threshold=0.6, min_attempts=3)
    assert any(w["title"] == "Test Topic A" for w in weak)
    weak_topic = next(w for w in weak if w["title"] == "Test Topic A")
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
        correct_label = variant.correct_answer[0]
        assert correct_label in {"A", "B", "C", "D"} or correct_label in "ABCD"


def test_mcq_variation_with_difficulty() -> None:
    """MCQ variation accepts a difficulty override."""
    settings = get_settings()
    engine = SmartContentEngine(settings)

    variant = engine.generate_variate_mcq(Subject.pharmacology, difficulty="exam_level")
    if variant:
        assert variant.difficulty == "exam_level"


def test_difficulty_tier_assignment() -> None:
    """Difficulty tier is assigned based on performance history."""
    settings = get_settings()
    engine = SmartContentEngine(settings)

    engine.record_performance("Known Topic", True, subject=Subject.anatomy)
    engine.record_performance("Known Topic", True, subject=Subject.anatomy)
    engine.record_performance("Known Topic", True, subject=Subject.anatomy)

    engine.record_performance("Hard Topic", False, subject=Subject.anatomy)
    engine.record_performance("Hard Topic", False, subject=Subject.anatomy)
    engine.record_performance("Hard Topic", False, subject=Subject.anatomy)

    diff_easy = engine.difficulty_for_topic("Known Topic")
    diff_hard = engine.difficulty_for_topic("Hard Topic")
    assert diff_easy == "easy"
    assert diff_hard == "exam_level"


def test_mcq_vignette_validation() -> None:
    """Vignette validation identifies well-formed vs poorly-formed MCQs."""
    settings = get_settings()
    engine = SmartContentEngine(settings)

    # Create a well-formed vignette
    from app.models import GeneratedContent

    good = GeneratedContent(
        title="Test MCQ Vignette",
        caption="A clinical vignette MCQ testing appendicitis knowledge for NEET-PG revision.",
        poster_text="Test scenario for appendicitis diagnosis",
        content_format=ContentFormat.mcq,
        question=(
            "A 35-year-old male presents with 3 days of right lower quadrant abdominal pain. "
            "He has nausea and anorexia. On examination, there is tenderness at McBurney's point "
            "with rebound tenderness. Temperature is 38.2°C. "
            "What is the most likely diagnosis?"
        ),
        options=["A. Acute appendicitis", "B. Acute cholecystitis", "C. Renal colic", "D. Perforated ulcer"],
        correct_answer="A. Acute appendicitis",
        high_yield_takeaway="McBurney's point tenderness + rebound = acute appendicitis.",
    )

    issue = engine.validate_mcq_vignette(good)
    assert issue is None, f"Expected no issue, got: {issue}"


def test_enrich_mcq_with_analysis_adds_wrong_option_reasons() -> None:
    """Wrong-option analysis adds explanations for distractors."""
    settings = get_settings()
    engine = SmartContentEngine(settings)

    from app.models import GeneratedContent

    mcq = GeneratedContent(
        title="Test MCQ Analysis",
        caption="Hemoptysis MCQ with wrong-option analysis for NEET-PG revision.",
        poster_text="Test analysis of hemoptysis MCQ options",
        content_format=ContentFormat.mcq,
        question="A 50-year-old smoker presents with hemoptysis. What is the most likely diagnosis?",
        options=["A. Tuberculosis", "B. Lung cancer", "C. Bronchiectasis", "D. Pneumonia"],
        correct_answer="B. Lung cancer",
        explanation="Lung cancer is common in smokers over 50 with hemoptysis.",
        high_yield_takeaway="Smoker with hemoptysis = lung cancer until proven otherwise.",
    )

    enriched = engine.enrich_mcq_with_analysis(mcq)
    assert enriched.explanation is not None
    assert "Why other options are wrong" in enriched.explanation


def test_orchestrator_pause_resume_controls() -> None:
    """Orchestrator supports pause/resume and engine stats."""
    settings = get_settings()
    orchestrator = PostOrchestrator(settings)

    assert not orchestrator.paused
    orchestrator.pause()
    assert orchestrator.paused
    orchestrator.resume()
    assert not orchestrator.paused


def test_orchestrator_engine_stats() -> None:
    """Engine stats are accessible from the orchestrator."""
    settings = get_settings()
    orchestrator = PostOrchestrator(settings)

    stats = orchestrator.get_engine_stats()
    assert "library_topics" in stats
    assert "weak_topics_count" in stats
    assert stats["library_topics"] >= 150


def test_weak_topic_recall_generates_post() -> None:
    """Weak topic recall generates a post without AI key."""
    settings = get_settings()
    orchestrator = PostOrchestrator(settings)

    # Record a performance so there's a weak topic
    orchestrator._engine.record_performance("Test Weak Topic", False, subject=Subject.anatomy)

    result = asyncio.run(orchestrator.generate_weak_topic_post(publish_to_telegram=False))
    assert result.content is not None
    assert result.poster_path == "text-only"


def test_content_library_has_150_topics() -> None:
    """Library should have at least 150 topics."""
    lib = ContentLibrary()
    assert lib.total() >= 150, f"Expected ≥150 topics, got {lib.total()}"
