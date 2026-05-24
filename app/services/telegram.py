import logging
from pathlib import Path

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.config import Settings

logger = logging.getLogger(__name__)


class TelegramPoster:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @property
    def configured(self) -> bool:
        return bool(self.settings.telegram_bot_token and self.settings.telegram_chat_id)

    @retry(
        retry=retry_if_exception_type((httpx.HTTPError, RuntimeError)),
        wait=wait_exponential(multiplier=1, min=2, max=20),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def send_photo(self, image_path: Path, caption: str) -> bool:
        if not self.configured:
            raise RuntimeError("Telegram bot token or chat id is missing.")

        url = f"https://api.telegram.org/bot{self.settings.telegram_bot_token}/sendPhoto"
        data = {
            "chat_id": self.settings.telegram_chat_id,
            "caption": caption[:1024],
            "parse_mode": "HTML",
        }
        async with httpx.AsyncClient(timeout=45) as client:
            with image_path.open("rb") as image_file:
                files = {"photo": (image_path.name, image_file, "image/png")}
                response = await client.post(url, data=data, files=files)
                response.raise_for_status()

        payload = response.json()
        if not payload.get("ok"):
            raise RuntimeError(f"Telegram API rejected request: {payload}")

        logger.info("Telegram post sent: %s", image_path)
        return True
