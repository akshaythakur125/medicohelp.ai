from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

_base_dir = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    project_name: str = "MedicoHelp AI Auto Poster"
    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    ai_provider: str = Field(default="none", pattern="^(openai|gemini|anthropic|none)$")
    ai_model: str = "gpt-4o-mini"
    anthropic_api_key: str | None = None
    generate_realistic_images: bool = False
    # OpenAI image settings
    openai_image_model: str = "gpt-image-1"
    openai_image_size: str = "1024x1024"
    openai_image_quality: str = "medium"
    # Gemini / Imagen image settings
    gemini_image_model: str = "imagen-3.0-generate-002"
    gemini_text_model: str = "gemini-2.0-flash"

    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None
    admin_chat_id: str | None = None

    # Instagram
    instagram_user_id: str | None = None
    instagram_access_token: str | None = None
    imgbb_api_key: str | None = None
    instagram_enabled: bool = False
    # Facebook App credentials (needed for auto-refreshing the 60-day access token)
    facebook_app_id: str | None = None
    facebook_app_secret: str | None = None

    post_interval_hours: int = Field(default=6, ge=1)
    post_schedule_times: str = ""  # Comma-separated HH:MM slots, e.g. "08:00,14:00,20:00"
    timezone: str = "Asia/Kolkata"
    run_scheduler: bool = True
    text_only_mode: bool = True  # Send rich-text messages instead of image posters
    posting_paused: bool = False  # Global pause for scheduled posting

    education_mode: str = Field(default="comprehensive", pattern="^(comprehensive|first_year_mbbs|final_year_revision|neet_pg_revision|inicet_high_yield|emergency_5_min)$")
    streak_window_hours: int = Field(default=24, ge=1)
    battle_weekday: int = Field(default=6, ge=0, le=6)  # 0=Monday, 6=Sunday
    challenge_hour: int = Field(default=9, ge=0, le=23)  # Hour for daily challenge post
    engagement_enabled: bool = True

    image_card_enabled: bool = True
    image_card_fallback_to_text: bool = True
    assets_images_dir: Path = _base_dir / "assets" / "images"
    image_index_path: Path = _base_dir / "assets" / "images" / "index.json"
    image_card_template: str = "rapid_revision"

    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"
    allow_mock_ai: bool = True
    news_lookback_days: int = Field(default=14, ge=1)
    news_max_items: int = Field(default=6, ge=1, le=20)

    base_dir: Path = _base_dir
    generated_dir: Path = _base_dir / "generated"
    logs_dir: Path = _base_dir / "logs"
    prompts_dir: Path = _base_dir / "prompts"
    assets_dir: Path = _base_dir / "assets"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.generated_dir.mkdir(parents=True, exist_ok=True)
    settings.logs_dir.mkdir(parents=True, exist_ok=True)
    settings.assets_dir.mkdir(parents=True, exist_ok=True)
    return settings
