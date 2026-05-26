"""Handles Telegram bot commands sent by the admin (phone management)."""
from __future__ import annotations

import logging

from app.config import Settings
from app.models import Subject

logger = logging.getLogger(__name__)


class BotCommandHandler:
    """Polls getUpdates and responds to admin commands.

    Enabled only when ADMIN_CHAT_ID is set.
    Commands only execute when the sender's chat_id matches ADMIN_CHAT_ID.
    """

    def __init__(self, settings: Settings, orchestrator: object, telegram: object) -> None:
        self.settings = settings
        self.orchestrator = orchestrator  # PostOrchestrator
        self.telegram = telegram  # TelegramPoster
        self._offset: int = 0

    async def poll(self) -> None:
        """Called periodically by the scheduler to process pending commands."""
        if not self.settings.admin_chat_id or not self.settings.telegram_bot_token:
            return

        updates = await self.telegram.get_updates(self._offset)
        for update in updates:
            self._offset = update["update_id"] + 1
            await self._handle(update)

    async def _handle(self, update: dict) -> None:
        message = update.get("message") or update.get("edited_message", {})
        if not message:
            return

        text: str = (message.get("text") or "").strip()
        chat_id = str(message.get("chat", {}).get("id", ""))

        if chat_id != self.settings.admin_chat_id:
            return  # Ignore non-admin messages

        if not text.startswith("/"):
            return

        cmd, _, args = text.partition(" ")
        cmd = cmd.lower().split("@")[0]  # Strip bot username suffix

        try:
            if cmd == "/help":
                await self._cmd_help(chat_id)
            elif cmd == "/status":
                await self._cmd_status(chat_id)
            elif cmd == "/post":
                await self._cmd_post(chat_id, args.strip())
            elif cmd == "/start":
                await self._cmd_help(chat_id)
        except Exception as exc:
            logger.exception("Bot command %s failed.", cmd)
            await self.telegram.send_message_to(chat_id, f"❌ Error: {exc}")

    async def _cmd_help(self, chat_id: str) -> None:
        msg = (
            "<b>MedicoHelp Bot — Admin Commands</b>\n\n"
            "/status — Bot status &amp; next schedule\n"
            "/post — Trigger an immediate revision post\n"
            "/post anatomy — Post a specific subject\n"
            "/help — Show this help\n\n"
            "<i>Only messages from your ADMIN_CHAT_ID are processed.</i>"
        )
        await self.telegram.send_message_to(chat_id, msg)

    async def _cmd_status(self, chat_id: str) -> None:
        schedule = self.settings.post_schedule_times or f"every {self.settings.post_interval_hours}h"
        target = self.settings.telegram_chat_id or "not configured"
        provider = self.settings.ai_provider.upper()
        mode = "text-only" if self.settings.text_only_mode else "image poster"
        msg = (
            "✅ <b>MedicoHelp is running</b>\n\n"
            f"🕐 Schedule: <code>{schedule}</code> ({self.settings.timezone})\n"
            f"📬 Posting to: <code>{target}</code>\n"
            f"🤖 AI provider: {provider}\n"
            f"📄 Post mode: {mode}\n"
        )
        await self.telegram.send_message_to(chat_id, msg)

    async def _cmd_post(self, chat_id: str, args: str) -> None:
        subject: Subject | None = None
        if args:
            try:
                subject = Subject(args.lower().replace(" ", "_").replace("-", "_"))
            except ValueError:
                valid = ", ".join(s.value for s in Subject)
                await self.telegram.send_message_to(
                    chat_id,
                    f"❌ Unknown subject <code>{args}</code>.\nValid: {valid}",
                )
                return

        await self.telegram.send_message_to(chat_id, "⏳ Generating post…")
        try:
            result = await self.orchestrator.generate_planned_post(  # type: ignore[attr-defined]
                publish_to_telegram=True,
                subject_override=subject,
            )
            subj = result.content.subject.value if result.content.subject else "mixed"
            fmt = result.content.content_format.value
            await self.telegram.send_message_to(
                chat_id,
                f"✅ Posted! Subject: <b>{subj}</b> | Format: <b>{fmt}</b>",
            )
        except Exception as exc:
            await self.telegram.send_message_to(chat_id, f"❌ Generation failed: {exc}")
