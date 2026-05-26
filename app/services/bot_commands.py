"""Handles Telegram bot commands sent by the admin (phone management)."""
from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from app.models import ContentFormat, Difficulty, Subject

if TYPE_CHECKING:
    from app.config import Settings
    from app.services.orchestrator import PostOrchestrator
    from app.services.telegram import TelegramPoster

logger = logging.getLogger(__name__)

_SUBJECT_NAMES = {s.value: s.value.replace("_", " ").title() for s in Subject}
_FORMAT_NAMES = {f.value: f.value.replace("_", " ").title() for f in ContentFormat}


class BotCommandHandler:
    """Polls getUpdates and responds to admin commands.

    Enabled only when ADMIN_CHAT_ID is set.
    Commands only execute when the sender's chat_id matches ADMIN_CHAT_ID.
    """

    def __init__(
        self,
        settings: Settings,
        orchestrator: PostOrchestrator,
        telegram: TelegramPoster,
    ) -> None:
        self.settings = settings
        self.orchestrator = orchestrator
        self.telegram = telegram
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
            elif cmd == "/pause":
                await self._cmd_pause(chat_id)
            elif cmd == "/resume":
                await self._cmd_resume(chat_id)
            elif cmd == "/post_format":
                await self._cmd_post_format(chat_id, args.strip())
            elif cmd == "/stats":
                await self._cmd_stats(chat_id)
            elif cmd == "/weak":
                await self._cmd_weak(chat_id)
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
            "/post anatomy mcq — Post specific subject + format\n"
            "/pause — Pause all scheduled posting\n"
            "/resume — Resume scheduled posting\n"
            "/post_format mcq — Post a specific format across subjects\n"
            "/stats — Show engine stats &amp; weak topics\n"
            "/weak — Force a weak-topic recall post\n"
            "/help — Show this help\n\n"
            "<i>Only messages from your ADMIN_CHAT_ID are processed.</i>"
        )
        await self.telegram.send_message_to(chat_id, msg)

    async def _cmd_status(self, chat_id: str) -> None:
        schedule = self.settings.post_schedule_times or f"every {self.settings.post_interval_hours}h"
        target = self.settings.telegram_chat_id or "not configured"
        provider = self.settings.ai_provider.upper()
        mode = "text-only" if self.settings.text_only_mode else "image poster"
        paused = "⏸ PAUSED" if self.orchestrator.paused else "▶ RUNNING"

        stats_line = ""
        try:
            st = self.orchestrator.get_engine_stats()
            stats_line = (
                f"\n📚 Library: {st['library_topics']} topics | "
                f"Sent: {st['topics_sent']} | "
                f"Fresh: {st['topics_unseen']} unseen | "
                f"Weak: {st['weak_topics_count']}"
            )
        except Exception:
            pass

        msg = (
            f"<b>MedicoHelp Status — {paused}</b>\n\n"
            f"🕐 Schedule: <code>{schedule}</code> ({self.settings.timezone})\n"
            f"📬 Posting to: <code>{target}</code>\n"
            f"🤖 AI provider: {provider}\n"
            f"📄 Post mode: {mode}"
            f"{stats_line}\n"
        )
        await self.telegram.send_message_to(chat_id, msg)

    async def _cmd_post(self, chat_id: str, args: str) -> None:
        subject: Subject | None = None
        content_format: ContentFormat | None = None
        rest = args

        if rest:
            parts = rest.split()
            # First part: subject
            try:
                subject = Subject(parts[0].lower().replace(" ", "_").replace("-", "_"))
                rest = " ".join(parts[1:]).strip()
            except ValueError:
                subject = None
                rest = " ".join(parts)

            # Second part: format
            if rest:
                try:
                    content_format = ContentFormat(
                        rest.lower().replace(" ", "_").replace("-", "_")
                    )
                except ValueError:
                    await self.telegram.send_message_to(
                        chat_id,
                        f"❌ Unknown format <code>{rest}</code>.\n"
                        f"Valid: {', '.join(f.value for f in ContentFormat)}",
                    )
                    return

        await self.telegram.send_message_to(chat_id, "⏳ Generating post…")
        try:
            result = await self.orchestrator.generate_planned_post(
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

    async def _cmd_pause(self, chat_id: str) -> None:
        self.orchestrator.pause()
        await self.telegram.send_message_to(chat_id, "⏸ Posting paused. No scheduled posts will go out.")

    async def _cmd_resume(self, chat_id: str) -> None:
        self.orchestrator.resume()
        await self.telegram.send_message_to(chat_id, "▶ Posting resumed.")

    async def _cmd_post_format(self, chat_id: str, args: str) -> None:
        """Force a post of a specific content format."""
        if not args:
            valid = ", ".join(f.value for f in ContentFormat)
            await self.telegram.send_message_to(
                chat_id,
                f"Usage: /post_format <format>\nValid: {valid}",
            )
            return

        try:
            content_format = ContentFormat(args.lower().replace(" ", "_").replace("-", "_"))
        except ValueError:
            valid = ", ".join(f.value for f in ContentFormat)
            await self.telegram.send_message_to(
                chat_id,
                f"❌ Unknown format <code>{args}</code>.\nValid: {valid}",
            )
            return

        await self.telegram.send_message_to(chat_id, f"⏳ Generating {content_format.value} post…")
        try:
            from app.services.content_engine import SmartContentEngine
            from app.models import GeneratedContent

            engine = SmartContentEngine(self.settings)
            # Try library-based generation for smart formats
            subjects = list(Subject)
            content: GeneratedContent | None = None
            for subj in subjects:
                if content_format == ContentFormat.flashcard:
                    content = engine.generate_flashcard(subj)
                elif content_format == ContentFormat.true_false:
                    content = engine.generate_true_false(subj)
                elif content_format == ContentFormat.one_liner_recall:
                    content = engine.generate_one_liner(subj)
                elif content_format == ContentFormat.mcq:
                    content = engine.generate_variate_mcq(subj)
                else:
                    content = engine.generate(subj, content_format)
                if content:
                    break

            if not content:
                result = await self.orchestrator.generate_post(
                    content_format=content_format,
                    publish_to_telegram=True,
                )
            else:
                from app.services.formatter import format_for_telegram

                text = format_for_telegram(content)
                posted = await self.telegram.send_message(text) if text else False
                from pathlib import Path

                self.orchestrator.store.save_post(content, Path("text-only"), posted)

            await self.telegram.send_message_to(
                chat_id,
                f"✅ Posted <b>{content_format.value}</b> format!",
            )
        except Exception as exc:
            await self.telegram.send_message_to(chat_id, f"❌ Failed: {exc}")

    async def _cmd_stats(self, chat_id: str) -> None:
        try:
            st = self.orchestrator.get_engine_stats()
            weak_lines = ""
            for w in st.get("weak_topics", [])[:5]:
                weak_lines += (
                    f"  • {w['title'][:50]} — "
                    f"{w['accuracy']:.0%} acc ({w['total_attempts']} tries)"
                    f" | {w['days_since_last_seen']}d ago\n"
                )

            msg = (
                f"📊 <b>Engine Statistics</b>\n\n"
                f"📚 Library topics: {st['library_topics']}\n"
                f"📤 Topics sent: {st['topics_sent']}\n"
                f"✨ Unseen: {st['topics_unseen']}\n"
                f"📅 Sent last 7d: {st['sent_last_7_days']}\n"
                f"⚠ Weak topics: {st['weak_topics_count']}\n\n"
            )
            if weak_lines:
                msg += f"<b>Top Weak Topics:</b>\n{weak_lines}"

            # Per-subject breakdown
            msg += "\n<b>By Subject:</b>\n"
            for subj_val, count in sorted(st.get("by_subject", {}).items()):
                msg += f"  {_SUBJECT_NAMES.get(subj_val, subj_val)}: {count}\n"

            await self.telegram.send_message_to(chat_id, msg.strip())
        except Exception as exc:
            await self.telegram.send_message_to(chat_id, f"❌ Stats failed: {exc}")

    async def _cmd_weak(self, chat_id: str) -> None:
        """Force a weak-topic recall post."""
        await self.telegram.send_message_to(chat_id, "🔁 Finding weakest topic…")
        try:
            result = await self.orchestrator.generate_weak_topic_post(publish_to_telegram=True)
            await self.telegram.send_message_to(
                chat_id,
                f"✅ Weak topic posted: <b>{result.content.title[:60]}</b>",
            )
        except Exception as exc:
            await self.telegram.send_message_to(chat_id, f"❌ Weak topic post failed: {exc}")
