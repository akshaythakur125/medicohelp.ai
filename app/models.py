from enum import Enum

from pydantic import BaseModel, Field


class ContentCategory(str, Enum):
    """Legacy ophthalmology presets kept for older API calls."""

    neet_pg_mcq = "neet_pg_mcq"
    clinical_case = "clinical_case"
    retina_quiz = "retina_quiz"
    cataract_pearl = "cataract_pearl"
    glaucoma_fact = "glaucoma_fact"
    emergency_ophthalmology = "emergency_ophthalmology"


class Subject(str, Enum):
    anatomy = "anatomy"
    physiology = "physiology"
    biochemistry = "biochemistry"
    pathology = "pathology"
    pharmacology = "pharmacology"
    microbiology = "microbiology"
    forensic_medicine = "forensic_medicine"
    community_medicine = "community_medicine"
    general_medicine = "general_medicine"
    general_surgery = "general_surgery"
    obstetrics_gynecology = "obstetrics_gynecology"
    pediatrics = "pediatrics"
    ophthalmology = "ophthalmology"
    ent = "ent"
    orthopedics = "orthopedics"
    dermatology = "dermatology"
    psychiatry = "psychiatry"
    radiology = "radiology"
    anesthesiology = "anesthesiology"


class ContentFormat(str, Enum):
    mcq = "mcq"
    image_based_question = "image_based_question"
    concise_notes = "concise_notes"
    clinical_case = "clinical_case"
    rapid_revision = "rapid_revision"
    practical_viva = "practical_viva"
    exam_news_update = "exam_news_update"
    residency_survival_tip = "residency_survival_tip"
    pyq_concept = "pyq_concept"
    flashcard = "flashcard"
    true_false = "true_false"
    one_liner_recall = "one_liner_recall"
    mnemonic = "mnemonic"


class NewsTopic(str, Enum):
    neet_pg = "neet_pg"
    inicet = "inicet"
    residency = "residency"


class PostLane(str, Enum):
    image_based = "image_based"
    pyq_concept = "pyq_concept"
    quick_revision = "quick_revision"
    residency_tip = "residency_tip"
    exam_news = "exam_news"
    poll_quiz = "poll_quiz"
    flashcard = "flashcard"
    mnemonic = "mnemonic"
    daily_pack = "daily_pack"
    mcq_variant = "mcq_variant"
    weak_topic_recall = "weak_topic_recall"
    true_false = "true_false"
    one_liner_recall = "one_liner_recall"


class Difficulty(str, Enum):
    easy = "easy"
    moderate = "moderate"
    exam_level = "exam_level"


class SlotType(str, Enum):
    morning_revision = "morning_revision"
    afternoon_mcq = "afternoon_mcq"
    evening_revision = "evening_revision"
    nightly_weak_topic = "nightly_weak_topic"


class EducationMode(str, Enum):
    comprehensive = "comprehensive"
    first_year_mbbs = "first_year_mbbs"
    final_year_revision = "final_year_revision"
    neet_pg_revision = "neet_pg_revision"
    inicet_high_yield = "inicet_high_yield"
    emergency_5_min = "emergency_5_min"


FIRST_YEAR_SUBJECTS = {
    Subject.anatomy, Subject.physiology, Subject.biochemistry,
}
FINAL_YEAR_SUBJECTS = {
    Subject.general_medicine, Subject.general_surgery,
    Subject.obstetrics_gynecology, Subject.pediatrics,
}
NEET_PG_CORE_SUBJECTS = {
    Subject.pathology, Subject.pharmacology, Subject.microbiology,
    Subject.forensic_medicine, Subject.community_medicine,
    Subject.ophthalmology, Subject.ent, Subject.orthopedics,
    Subject.dermatology, Subject.psychiatry, Subject.radiology,
    Subject.anesthesiology,
}
EMERGENCY_5_MIN_FORMATS = {
    ContentFormat.rapid_revision, ContentFormat.flashcard,
    ContentFormat.one_liner_recall, ContentFormat.mnemonic,
}


class GeneratedContent(BaseModel):
    title: str = Field(min_length=3, max_length=120)
    caption: str = Field(min_length=10, max_length=2000)
    hashtags: list[str] = Field(default_factory=list)
    poster_text: str = Field(min_length=5, max_length=320)
    image_prompt: str | None = None
    image_based_data: list[str] = Field(default_factory=list, max_length=8)
    visual_description: str | None = Field(default=None, max_length=800)
    visual_labels: list[str] = Field(default_factory=list, max_length=8)
    question: str | None = Field(default=None, max_length=1200)
    options: list[str] = Field(default_factory=list, max_length=6)
    correct_answer: str | None = Field(default=None, max_length=200)
    explanation: str | None = Field(default=None, max_length=1600)
    high_yield_takeaway: str | None = Field(default=None, max_length=320)
    relevance_rationale: str | None = Field(default=None, max_length=500)
    image_answerability: str | None = Field(default=None, max_length=500)
    source_title: str | None = Field(default=None, max_length=200)
    source_url: str | None = Field(default=None, max_length=800)
    source_urls: list[str] = Field(default_factory=list, max_length=6)
    news_topic: NewsTopic | None = None
    post_lane: PostLane | None = None
    subject: Subject | None = None
    content_format: ContentFormat
    category: ContentCategory | None = None
    difficulty: str | None = Field(default=None, max_length=10)
    topic_tags: list[str] = Field(default_factory=list, max_length=10)


class GenerateRequest(BaseModel):
    subject: Subject | None = None
    content_format: ContentFormat | None = None
    category: ContentCategory | None = None
    publish_to_telegram: bool = False


class GenerateAllSubjectsRequest(BaseModel):
    content_format: ContentFormat | None = None
    publish_to_telegram: bool = False


class NewsItem(BaseModel):
    title: str
    url: str
    source: str
    published: str | None = None
    summary: str | None = None


class NewsRequest(BaseModel):
    topic: NewsTopic = NewsTopic.neet_pg
    publish_to_telegram: bool = False


class GenerateResponse(BaseModel):
    content: GeneratedContent
    poster_path: str
    telegram_posted: bool


class NewsResponse(BaseModel):
    items: list[NewsItem]
    generated_post: GenerateResponse | None = None


class HealthResponse(BaseModel):
    status: str
    scheduler_running: bool
    posting_paused: bool = False
    ai_provider: str = "none"
    text_only_mode: bool = True


class StudentProfile(BaseModel):
    education_mode: EducationMode = EducationMode.comprehensive
    weak_subjects: list[Subject] = Field(default_factory=list)
    streak_days: int = 0
    last_active_date: str | None = None
    consecutive_posts_seen: int = 0
    daily_challenge_completed: bool = False
    weekly_battle_score: int = 0


class EngagementStats(BaseModel):
    current_streak: int = 0
    longest_streak: int = 0
    last_active_date: str | None = None
    daily_challenge_active: bool = False
    daily_challenge_content: GeneratedContent | None = None
    daily_challenge_expiry: str | None = None
    weekly_battle_active: bool = False
    weekly_battle_scores: dict[str, int] = Field(default_factory=dict)
    weekly_battle_score: int = 0
    weekly_battle_deadline: str | None = None
    total_correct: int = 0
    total_attempted: int = 0


class DailyChallenge(BaseModel):
    date: str
    content: GeneratedContent
    completed: bool = False
    scores: list[bool] = Field(default_factory=list)


class WeeklyBattle(BaseModel):
    week_start: str
    scores: dict[str, int] = Field(default_factory=dict)
    active: bool = True


class OverlayElement(BaseModel):
    element_type: str = "label"  # label, arrow, highlight, border, callout
    text: str = ""
    x: float = 0.0
    y: float = 0.0
    color: str = "#FF0000"
    font_size: int = 18
    arrow_direction: str | None = None  # up, down, left, right, auto


class ImageAsset(BaseModel):
    asset_id: str
    file_path: str
    md5_hash: str
    subject: str
    topic: list[str] = Field(default_factory=list)
    format: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    caption: str = ""
    attribution: str = ""
    width: int = 0
    height: int = 0
    file_size_bytes: int = 0


class ImageCardTemplate(BaseModel):
    template_id: str
    name: str
    card_format: str  # flashcard, mcq_infographic, rapid_revision, comparison
    width: int = 1080
    height: int = 1500
    background_color: str = "#FFFFFF"
    header_height: int = 80
    footer_height: int = 60
    text_color: str = "#1A1A2E"
    accent_color: str = "#0F3460"
    font_family: str = "DejaVuSans"


class ImageCardRequest(BaseModel):
    content: GeneratedContent
    template_id: str = "rapid_revision"
    overlays: list[OverlayElement] = Field(default_factory=list)
    highlight_color: str | None = None
    show_subject_badge: bool = True
    show_format_badge: bool = True
