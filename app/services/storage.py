import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from app.config import Settings
from app.models import GeneratedContent

logger = logging.getLogger(__name__)


class PostLogStore:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self.posts_log = settings.logs_dir / "generated_posts.jsonl"
        self.errors_log = settings.logs_dir / "errors.jsonl"

    def save_post(self, content: GeneratedContent, poster_path: Path, telegram_posted: bool) -> None:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "content": content.model_dump(mode="json"),
            "poster_path": str(poster_path),
            "telegram_posted": telegram_posted,
        }
        self._append_jsonl(self.posts_log, payload)

    def save_error(self, message: str, context: dict[str, Any] | None = None) -> None:
        payload = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "message": message,
            "context": context or {},
        }
        self._append_jsonl(self.errors_log, payload)
        logger.error("%s | %s", message, context or {})

    def _append_jsonl(self, path: Path, payload: dict[str, Any]) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8") as file:
            file.write(json.dumps(payload, ensure_ascii=False) + "\n")
