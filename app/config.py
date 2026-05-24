from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    project_name: str = "MedicoHelp AI Auto Poster"
    openai_api_key: str | None = None
    gemini_api_key: str | None = None
    ai_provider: str = Field(default="openai", pattern="^(openai|gemini)$")
    ai_model: str = "gpt-4o-mini"
    generate_realistic_images: bool = False
    openai_image_model: str = "gpt-image-1"
    openai_image_size: str = "1024x1024"
    openai_image_quality: str = "medium"

    telegram_bot_token: str | None = None
    telegram_chat_id: str | None = None

    post_interval_hours: int = Field(default=6, ge=1)
    timezone: str = "Asia/Kolkata"
    run_scheduler: bool = True

    app_host: str = "0.0.0.0"
    app_port: int = 8000
    log_level: str = "INFO"
    allow_mock_ai: bool = True
    news_lookback_days: int = Field(default=14, ge=1)
    news_max_items: int = Field(default=6, ge=1, le=20)

    base_dir: Path = Path(__file__).resolve().parent.parent
    generated_dir: Path = base_dir / "generated"
    logs_dir: Path = base_dir / "logs"
    prompts_dir: Path = base_dir / "prompts"
    assets_dir: Path = base_dir / "assets"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.generated_dir.mkdir(parents=True, exist_ok=True)
    settings.logs_dir.mkdir(parents=True, exist_ok=True)
    settings.assets_dir.mkdir(parents=True, exist_ok=True)
    return settings
