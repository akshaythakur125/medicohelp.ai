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
