import logging
from pathlib import Path

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from app.config import Settings

logger = logging.getLogger(__name__)

_TELEGRAM_API = "https://api.telegram.org/bot{token}/{method}"


class TelegramPoster:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    @property
    def configured(self) -> bool:
        return bool(self.settings.telegram_bot_token and self.settings.telegram_chat_id)

    def _api_url(self, method: str) -> str:
        return _TELEGRAM_API.format(token=self.settings.telegram_bot_token, method=method)

    @retry(
        retry=retry_if_exception_type((httpx.HTTPError, RuntimeError)),
        wait=wait_exponential(multiplier=1, min=2, max=20),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def send_photo(self, image_path: Path, caption: str) -> bool:
        if not self.configured:
            raise RuntimeError("Telegram bot token or chat id is missing.")

        data = {
            "chat_id": self.settings.telegram_chat_id,
            "caption": caption[:1024],
            "parse_mode": "HTML",
        }
        async with httpx.AsyncClient(timeout=45) as client:
            with image_path.open("rb") as image_file:
                files = {"photo": (image_path.name, image_file, "image/png")}
                response = await client.post(self._api_url("sendPhoto"), data=data, files=files)
                response.raise_for_status()

        payload = response.json()
        if not payload.get("ok"):
            raise RuntimeError(f"Telegram API rejected request: {payload}")

        logger.info("Telegram photo sent: %s", image_path)
        return True

    @retry(
        retry=retry_if_exception_type((httpx.HTTPError, RuntimeError)),
        wait=wait_exponential(multiplier=1, min=2, max=20),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def send_message(self, text: str) -> bool:
        """Send a rich-text HTML message to the configured chat."""
        return await self.send_message_to(self.settings.telegram_chat_id, text)

    async def send_message_to(self, chat_id: str | None, text: str) -> bool:
        """Send an HTML message to an arbitrary chat (e.g. admin DM)."""
        if not self.settings.telegram_bot_token:
            raise RuntimeError("Telegram bot token is missing.")
        if not chat_id:
            raise RuntimeError("chat_id is required.")

        payload = {
            "chat_id": chat_id,
            "text": text[:4096],
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(self._api_url("sendMessage"), json=payload)
            response.raise_for_status()

        data = response.json()
        if not data.get("ok"):
            raise RuntimeError(f"Telegram sendMessage rejected: {data}")

        logger.info("Telegram message sent to %s", chat_id)
        return True

    @retry(
        retry=retry_if_exception_type((httpx.HTTPError, RuntimeError)),
        wait=wait_exponential(multiplier=1, min=2, max=20),
        stop=stop_after_attempt(3),
        reraise=True,
    )
    async def send_poll(
        self,
        question: str,
        options: list[str],
        correct_option_id: int = 0,
        explanation: str = "",
        is_quiz: bool = True,
        open_period: int | None = None,
        chat_id: str | None = None,
    ) -> bool:
        """Send a native Telegram quiz or opinion poll."""
        if not self.settings.telegram_bot_token:
            raise RuntimeError("Telegram bot token is missing.")
        target = chat_id or self.settings.telegram_chat_id
        if not target:
            raise RuntimeError("chat_id is required.")

        payload: dict = {
            "chat_id": target,
            "question": question[:300],
            "options": [o[:100] for o in options[:10]],
            "is_anonymous": True,
            "type": "quiz" if is_quiz else "regular",
        }
        if is_quiz:
            payload["correct_option_id"] = correct_option_id
            if explanation:
                payload["explanation"] = explanation[:200]
                payload["explanation_parse_mode"] = "HTML"
        if open_period:
            payload["open_period"] = open_period

        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(self._api_url("sendPoll"), json=payload)
            response.raise_for_status()

        data = response.json()
        if not data.get("ok"):
            raise RuntimeError(f"Telegram sendPoll rejected: {data}")

        logger.info("Telegram poll sent to %s", target)
        return True

    async def send_visual_post(self, image_path: Path, full_text: str) -> bool:
        """Send AI medical image as photo then full educational text as a follow-up message."""
        lines = [l for l in full_text.split("\n") if l.strip()]
        short_caption = lines[0][:300] if lines else "🏥 MedicoHelp"
        await self.send_photo(image_path, short_caption)
        await self.send_message(full_text)
        return True

    async def send_message_with_keyboard(
        self,
        text: str,
        keyboard: list[list[dict]],
        chat_id: str | None = None,
    ) -> dict:
        """Send a message with an inline keyboard. Returns the sent message dict."""
        if not self.settings.telegram_bot_token:
            raise RuntimeError("Telegram bot token is missing.")
        target = chat_id or self.settings.telegram_chat_id
        if not target:
            raise RuntimeError("chat_id is required.")

        payload = {
            "chat_id": target,
            "text": text[:4096],
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
            "reply_markup": {"inline_keyboard": keyboard},
        }
        async with httpx.AsyncClient(timeout=30) as client:
            response = await client.post(self._api_url("sendMessage"), json=payload)
            response.raise_for_status()

        data = response.json()
        if not data.get("ok"):
            raise RuntimeError(f"Telegram sendMessage+keyboard rejected: {data}")

        logger.info("Telegram keyboard message sent to %s", target)
        return data.get("result", {})

    async def answer_callback_query(self, callback_query_id: str, text: str = "", show_alert: bool = False) -> bool:
        """Answer a callback query (inline keyboard button press)."""
        if not self.settings.telegram_bot_token:
            return False
        payload = {
            "callback_query_id": callback_query_id,
            "text": text[:200],
            "show_alert": show_alert,
        }
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(self._api_url("answerCallbackQuery"), json=payload)
        return response.json().get("ok", False)

    async def get_updates(self, offset: int = 0) -> list[dict]:
        """Fetch pending bot updates for command handling."""
        if not self.settings.telegram_bot_token:
            return []
        params = {"offset": offset, "timeout": 1, "limit": 10}
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                response = await client.get(self._api_url("getUpdates"), params=params)
                data = response.json()
            if data.get("ok"):
                return data.get("result", [])
        except Exception as exc:
            logger.debug("getUpdates error: %s", exc)
        return []
