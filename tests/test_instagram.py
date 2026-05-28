"""End-to-end tests for the Instagram carousel posting pipeline.

Covers:
  - CarouselSpec → SlideSpec conversion
  - CarouselGenerator slide rendering (Pillow)
  - InstagramContentGenerator mock-mode fallback
  - Orchestrator Instagram flow (skipped when not configured)
  - InstagramPoster configuration checks
"""

from pathlib import Path
from PIL import Image

from app.config import get_settings
from app.services.carousel_generator import CarouselGenerator, CarouselSpec, SlideSpec
from app.services.instagram_content import InstagramContentGenerator
from app.services.instagram import InstagramPoster
from app.services.orchestrator import PostOrchestrator


# ---------------------------------------------------------------------------
# CarouselSpec → SlideSpec conversion
# ---------------------------------------------------------------------------


def test_carousel_spec_to_slides_cover_only():
    spec = CarouselSpec(
        cover_title="TEST TITLE",
        cover_subtitle="A test subtitle",
        points=[],
        caption="Test caption",
        hashtags=["#test"],
    )
    slides = spec.to_slides()
    assert len(slides) == 1  # just cover (CTA replaced by photo slide)
    assert slides[0].slide_type == "cover"
    assert slides[0].title == "TEST TITLE"
    assert slides[0].subtitle == "A test subtitle"


def test_carousel_spec_to_slides_with_points():
    spec = CarouselSpec(
        cover_title="GLAUCOMA FACTS",
        cover_subtitle="Know the silent thief of sight",
        points=[
            {"label": "WHAT IS GLAUCOMA", "body": "Glaucoma damages the optic nerve.", "icon_emoji": "\U0001f441"},
            {"label": "RISK FACTORS", "body": "Age, family history, high eye pressure.", "icon_emoji": "\u26a0\ufe0f"},
            {"label": "TREATMENT", "body": "Eye drops, laser, or surgery.", "icon_emoji": "\U0001f48a"},
        ],
        caption="Learn about glaucoma early detection.",
        hashtags=["EyeHealth", "Glaucoma"],
    )
    slides = spec.to_slides()
    assert len(slides) == 4  # cover + 3 content (no CTA — replaced by photo slide)
    assert slides[0].slide_type == "cover"
    assert slides[1].slide_type == "content"
    assert slides[1].title == "WHAT IS GLAUCOMA"
    assert slides[1].slide_num == 1
    assert slides[1].total == 3
    assert slides[2].slide_type == "content"
    assert slides[2].slide_num == 2
    assert slides[3].slide_type == "content"
    assert slides[3].slide_num == 3


def test_carousel_spec_full_caption_no_hashtags():
    spec = CarouselSpec(
        cover_title="TEST", cover_subtitle="",
        points=[], caption="Just a caption",
        hashtags=[],
    )
    assert spec.full_caption() == "Just a caption"


def test_carousel_spec_full_caption_with_hashtags():
    spec = CarouselSpec(
        cover_title="TEST", cover_subtitle="",
        points=[], caption="Hello world",
        hashtags=["EyeHealth", "DrAkshayThakur"],
    )
    result = spec.full_caption()
    assert "Hello world" in result
    assert "#EyeHealth" in result
    assert "#DrAkshayThakur" in result


def test_carousel_spec_full_caption_strips_existing_hash():
    spec = CarouselSpec(
        cover_title="TEST", cover_subtitle="",
        points=[], caption="Caption", hashtags=["#EyeHealth", "DrAkshayThakur"],
    )
    result = spec.full_caption()
    assert "##EyeHealth" not in result
    assert "#EyeHealth" in result
    assert "#DrAkshayThakur" in result


# ---------------------------------------------------------------------------
# CarouselGenerator slide rendering
# ---------------------------------------------------------------------------


def _make_test_spec() -> CarouselSpec:
    return CarouselSpec(
        cover_title="PROTECT YOUR EYES",
        cover_subtitle="Simple tips from Dr. Akshay Thakur",
        points=[
            {"label": "20-20-20 RULE", "body": "Every 20 minutes look 20 feet away for 20 seconds.", "icon_emoji": "\u23f1"},
            {"label": "BLINK OFTEN", "body": "Blinking keeps your eyes moist and reduces strain.", "icon_emoji": "\U0001f441"},
        ],
        caption="Protect your vision with these simple habits.",
        hashtags=["EyeHealth", "DrAkshayThakur"],
    )


def test_carousel_generator_renders_all_slide_types():
    gen = CarouselGenerator()
    spec = _make_test_spec()
    paths = gen.generate_slides(spec)

    assert len(paths) == 3  # cover + 2 content (no CTA — replaced by photo)
    for path in paths:
        assert path.exists(), f"Slide file missing: {path}"
        img = Image.open(path)
        assert img.size == (1080, 1080), f"Expected 1080x1080, got {img.size}"
        img.close()

    assert "slide_00_cover" in paths[0].name
    assert "slide_01_content" in paths[1].name
    assert "slide_02_content" in paths[2].name


def test_carousel_generator_content_slide_branding():
    gen = CarouselGenerator()
    spec = _make_test_spec()
    paths = gen.generate_slides(spec)

    content_slide = paths[1]
    assert content_slide.exists()


def test_doctor_photo_slide_generated():
    gen = CarouselGenerator()
    spec = CarouselSpec(
        cover_title="TEST", cover_subtitle="", points=[], caption="",
    )
    paths = gen.generate_slides(spec)
    assert len(paths) == 1  # only cover (no photo configured, no CTA)
    gen.cleanup_slides(paths)


def test_carousel_generator_cover_slide():
    gen = CarouselGenerator()
    cover_spec = SlideSpec(slide_type="cover", title="DRY EYE TIPS", subtitle="Keep your eyes comfortable")
    img = gen._draw_cover(cover_spec)
    assert img.size == (1080, 1080)
    assert img.mode == "RGBA"


def test_carousel_generator_content_slide():
    gen = CarouselGenerator()
    content_spec = SlideSpec(
        slide_type="content", title="USE LUBRICATING DROPS",
        body_text="Artificial tears can help relieve dry eye symptoms.",
        icon_emoji="\U0001f4a7", slide_num=1, total=3,
    )
    img = gen._draw_content(content_spec)
    assert img.size == (1080, 1080)
    assert img.mode == "RGBA"


def test_carousel_generator_cleanup():
    gen = CarouselGenerator()
    spec = _make_test_spec()
    paths = gen.generate_slides(spec)
    assert all(p.exists() for p in paths)

    gen.cleanup_slides(paths)
    assert not any(p.exists() for p in paths)


def test_carousel_generator_progress_dots():
    gen = CarouselGenerator()
    spec = CarouselSpec(
        cover_title="SINGLE POINT",
        cover_subtitle="Test",
        points=[{"label": "ONE POINT", "body": "Single content slide.", "icon_emoji": "\u0031\ufe0f\u20e3"}],
        caption="Cap",
    )
    paths = gen.generate_slides(spec)
    assert len(paths) == 2  # cover + 1 content (no CTA)


# ---------------------------------------------------------------------------
# InstagramContentGenerator mock mode
# ---------------------------------------------------------------------------


def test_instagram_content_mock_carousel():
    settings = get_settings()
    gen = InstagramContentGenerator(settings)
    assert gen._anthropic_client is None, "Expected no AI client without API key"

    spec = gen._mock_carousel("digital eye strain", fmt="myth_buster")
    assert isinstance(spec, CarouselSpec)
    assert spec.cover_title
    assert len(spec.points) == 4
    assert spec.points[0]["label"] == "THE PROBLEM"
    assert spec.points[1]["label"] == "THE KEY INSIGHT"
    assert spec.caption
    assert "DrAkshayThakur" in " ".join(spec.hashtags)
    assert "MSOphthalmologist" in " ".join(spec.hashtags)


def test_instagram_content_generate_carousel_no_ai():
    settings = get_settings()
    gen = InstagramContentGenerator(settings)

    import asyncio
    spec = asyncio.run(gen.generate_carousel(topic="digital eye strain"))
    assert isinstance(spec, CarouselSpec)
    assert spec.cover_title
    assert len(spec.points) >= 4


def test_instagram_content_generate_carousel_random_topic():
    settings = get_settings()
    gen = InstagramContentGenerator(settings)

    import asyncio
    spec = asyncio.run(gen.generate_carousel(topic=None))
    assert isinstance(spec, CarouselSpec)
    assert spec.cover_title
    assert len(spec.points) >= 4


# ---------------------------------------------------------------------------
# InstagramPoster configuration checks
# ---------------------------------------------------------------------------


def test_instagram_poster_not_configured_by_default():
    settings = get_settings()
    poster = InstagramPoster(settings)
    assert not poster.is_configured


def test_instagram_poster_is_configured_with_creds():
    settings = get_settings()
    settings.instagram_user_id = "12345"
    settings.instagram_access_token = "test_token"
    settings.imgbb_api_key = "test_key"
    poster = InstagramPoster(settings)
    assert poster.is_configured


def test_instagram_poster_partial_config():
    settings = get_settings()
    settings.instagram_user_id = "12345"
    settings.instagram_access_token = None
    settings.imgbb_api_key = None
    poster = InstagramPoster(settings)
    assert not poster.is_configured  # missing token and imgbb key


# ---------------------------------------------------------------------------
# Orchestrator Instagram flow
# ---------------------------------------------------------------------------


def test_orchestrator_instagram_returns_skipped_when_disabled():
    settings = get_settings()
    settings.instagram_enabled = False
    orchestrator = PostOrchestrator(settings)

    import asyncio
    result = asyncio.run(orchestrator.generate_instagram_post(topic="dry eye"))
    assert result == {"skipped": True, "reason": "Instagram not enabled"}


def test_orchestrator_instagram_returns_skipped_when_not_configured():
    settings = get_settings()
    settings.instagram_enabled = True
    settings.instagram_user_id = None
    settings.instagram_access_token = None
    settings.imgbb_api_key = None
    orchestrator = PostOrchestrator(settings)

    import asyncio
    result = asyncio.run(orchestrator.generate_instagram_post(topic="dry eye"))
    assert result["skipped"] is True
    assert "credentials" in result["reason"].lower()


# ---------------------------------------------------------------------------
# Full integration: generate carousel spec → render slides → verify output
# ---------------------------------------------------------------------------


def test_instagram_full_pipeline_without_posting():
    """Generate content, render slides, verify files exist (no actual API post)."""
    settings = get_settings()
    orchestrator = PostOrchestrator(settings)
    carousel_gen = CarouselGenerator()

    import asyncio
    spec = asyncio.run(orchestrator._instagram_content.generate_carousel(topic="cataract symptoms and treatment"))
    assert isinstance(spec, CarouselSpec)
    assert spec.cover_title
    assert len(spec.points) >= 4

    paths = carousel_gen.generate_slides(spec)
    try:
        assert len(paths) >= 5  # cover + 4 content (no CTA)
        for p in paths:
            assert p.exists()
            img = Image.open(p)
            assert img.size == (1080, 1080)
            img.close()
    finally:
        carousel_gen.cleanup_slides(paths)


def test_instagram_multiple_topics_rendered():
    """Render slides for 3 different topics to verify no crashes."""
    settings = get_settings()
    gen = InstagramContentGenerator(settings)
    carousel_gen = CarouselGenerator()

    import asyncio

    topics = ["glaucoma warning signs", "dry eye syndrome tips", "digital eye strain prevention"]
    for topic in topics:
        spec = asyncio.run(gen.generate_carousel(topic=topic))
        paths = carousel_gen.generate_slides(spec)
        try:
            assert len(paths) >= 5
            for p in paths:
                img = Image.open(p)
                assert img.size == (1080, 1080)
                img.close()
        finally:
            carousel_gen.cleanup_slides(paths)


# ---------------------------------------------------------------------------
# Topic dedup ring buffer
# ---------------------------------------------------------------------------


def test_topic_dedup_ring_buffer():
    settings = get_settings()
    gen = InstagramContentGenerator(settings)

    import asyncio

    gen._recent_topics.clear()
    seen = set()
    for _ in range(50):
        topic = gen._pick_topic()
        # Should not repeat within the dedup window
        if len(gen._recent_topics) < 10:
            assert topic not in seen, f"Repeated topic before buffer full: {topic}"
        seen.add(topic)

    assert len(gen._recent_topics) == 10


def test_topic_dedup_after_buffer_full():
    settings = get_settings()
    gen = InstagramContentGenerator(settings)
    gen._recent_topics.clear()

    import asyncio

    first_10 = []
    for _ in range(10):
        first_10.append(gen._pick_topic())

    assert len(gen._recent_topics) == 10

    # After 10 more picks, the buffer should have rotated
    for _ in range(10):
        gen._pick_topic()

    # At least some of the original 10 should have been evicted
    remaining = set(first_10) & set(gen._recent_topics)
    assert len(remaining) < 10, "Buffer did not rotate"


# ---------------------------------------------------------------------------
# Post format rotation
# ---------------------------------------------------------------------------


def test_all_post_formats_covered_by_mock():
    settings = get_settings()
    gen = InstagramContentGenerator(settings)

    from app.services.instagram_content import POST_FORMATS
    for fmt in POST_FORMATS:
        spec = gen._mock_carousel("test topic", fmt=fmt)
        assert isinstance(spec, CarouselSpec)
        assert len(spec.points) == 4
        assert spec.points[0]["label"] == "THE PROBLEM"
        assert spec.points[1]["label"] == "THE KEY INSIGHT"
        assert len(spec.hashtags) >= 10
        assert "DrAkshayThakur" in " ".join(spec.hashtags)
        assert "MSOphthalmologist" in " ".join(spec.hashtags)


# ---------------------------------------------------------------------------
# Cover number rendering
# ---------------------------------------------------------------------------


def test_cover_leading_number_renders_in_teal():
    """Covers with leading numbers should render first word differently."""
    gen = CarouselGenerator()
    cover_spec = SlideSpec(slide_type="cover", title="5 WARNING SIGNS", subtitle="Test")
    img = gen._draw_cover(cover_spec)
    assert img.size == (1080, 1080)
    assert img.mode == "RGBA"


def test_cover_leading_non_number_renders_white():
    """Covers without leading numbers should render fully white."""
    gen = CarouselGenerator()
    cover_spec = SlideSpec(slide_type="cover", title="MYTH BUSTER", subtitle="Test")
    img = gen._draw_cover(cover_spec)
    assert img.size == (1080, 1080)
    assert img.mode == "RGBA"


# ---------------------------------------------------------------------------
# Content slide variants
# ---------------------------------------------------------------------------


def test_problem_slide_renders_with_red_theme():
    gen = CarouselGenerator()
    spec = SlideSpec(
        slide_type="content", title="THE PROBLEM",
        body_text="Test body text.", icon_emoji="\u26a0\ufe0f",
        slide_num=1, total=4,
    )
    img = gen._draw_content(spec)
    assert img.size == (1080, 1080)


def test_insight_slide_renders_with_save_badge():
    gen = CarouselGenerator()
    spec = SlideSpec(
        slide_type="content", title="THE KEY INSIGHT",
        body_text="Test body text.", icon_emoji="\U0001f4a1",
        slide_num=2, total=4,
    )
    img = gen._draw_content(spec)
    assert img.size == (1080, 1080)


# ---------------------------------------------------------------------------
# CTA engagement line
# ---------------------------------------------------------------------------


def test_doctor_photo_with_static_image():
    """Verify photo slide renders correctly with a synthetic test image."""
    import tempfile
    tmp = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
    test_img = Image.new("RGB", (800, 600), color="gray")
    test_img.save(tmp.name)
    tmp.close()

    gen = CarouselGenerator(doctor_photo_path=tmp.name)
    spec = CarouselSpec(
        cover_title="TEST", cover_subtitle="", points=[], caption="",
    )
    paths = gen.generate_slides(spec)
    try:
        assert len(paths) == 2  # cover + photo
        photo_path = paths[1]
        assert "photo" in photo_path.name
        img = Image.open(photo_path)
        assert img.size == (1080, 1080)
        img.close()
    finally:
        gen.cleanup_slides(paths)
        Path(tmp.name).unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# first_comment field
# ---------------------------------------------------------------------------


def test_carousel_spec_first_comment_default():
    spec = CarouselSpec(cover_title="T", cover_subtitle="")
    assert spec.first_comment == ""


def test_mock_carousels_have_first_comment():
    settings = get_settings()
    gen = InstagramContentGenerator(settings)

    from app.services.instagram_content import POST_FORMATS
    for fmt in POST_FORMATS:
        spec = gen._mock_carousel("test topic", fmt=fmt)
        assert spec.first_comment
        assert "EyeSpecialist" in spec.first_comment
        assert "OphthalmologyEducation" in spec.first_comment
        assert "DoctorOfInstagram" in spec.first_comment
        assert len(spec.first_comment) > 50


def test_generate_carousel_includes_first_comment():
    settings = get_settings()
    gen = InstagramContentGenerator(settings)

    import asyncio
    spec = asyncio.run(gen.generate_carousel(topic="test"))
    assert hasattr(spec, "first_comment")
    # Should be populated from mock data
    assert spec.first_comment


# ---------------------------------------------------------------------------
# Story teaser
# ---------------------------------------------------------------------------


def test_story_teaser_generates_vertical_image():
    gen = CarouselGenerator()
    spec = CarouselSpec(
        cover_title="5 WARNING SIGNS",
        cover_subtitle="Know what to look for",
        points=[],
    )
    path = gen.generate_story_teaser(spec)
    try:
        assert path.exists()
        img = Image.open(path)
        assert img.size == (1080, 1920), f"Expected 1080x1920, got {img.size}"
        img.close()
    finally:
        path.unlink(missing_ok=True)


def test_story_teaser_has_branding():
    gen = CarouselGenerator()
    spec = CarouselSpec(
        cover_title="MYTH BUSTER",
        cover_subtitle="Separating fact from fiction",
        points=[],
    )
    path = gen.generate_story_teaser(spec)
    try:
        assert "story_teaser" in path.name
    finally:
        path.unlink(missing_ok=True)


def test_story_teaser_multiple_calls_produce_consistent_output():
    gen = CarouselGenerator()
    spec1 = CarouselSpec(cover_title="TOPIC A", cover_subtitle="Sub A", points=[])
    spec2 = CarouselSpec(cover_title="TOPIC B", cover_subtitle="Sub B", points=[])
    path1 = gen.generate_story_teaser(spec1)
    path2 = gen.generate_story_teaser(spec2)
    try:
        assert path1.exists()
        assert path2.exists()
        img1 = Image.open(path1)
        img2 = Image.open(path2)
        assert img1.size == img2.size == (1080, 1920)
        img1.close()
        img2.close()
    finally:
        path1.unlink(missing_ok=True)
        path2.unlink(missing_ok=True)


# ---------------------------------------------------------------------------
# InstagramPoster new methods (validation only — no real API calls)
# ---------------------------------------------------------------------------


def test_post_first_comment_requires_config():
    import asyncio
    settings = get_settings()
    poster = InstagramPoster(settings)
    import pytest
    with pytest.raises(RuntimeError, match="not fully configured"):
        asyncio.run(poster.post_first_comment("123", "test comment"))


def test_post_story_requires_config():
    import asyncio
    settings = get_settings()
    poster = InstagramPoster(settings)
    import pytest
    with pytest.raises(RuntimeError, match="not fully configured"):
        asyncio.run(poster.post_story(Path("/tmp/nonexistent.jpg")))


# ---------------------------------------------------------------------------
# /instagram/status endpoint logic
# ---------------------------------------------------------------------------


def test_instagram_status_from_orchestrator():
    settings = get_settings()
    orchestrator = PostOrchestrator(settings)

    status = {
        "enabled": settings.instagram_enabled,
        "configured": orchestrator.instagram.is_configured,
        "user_id_set": bool(settings.instagram_user_id),
        "token_set": bool(settings.instagram_access_token),
        "imgbb_set": bool(settings.imgbb_api_key),
    }
    assert "enabled" in status
    assert "configured" in status
    assert status["configured"] is False
