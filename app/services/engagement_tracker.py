from __future__ import annotations

import json
import logging
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Optional

from app.config import get_settings
from app.models import DailyChallenge, EngagementStats, GeneratedContent, WeeklyBattle

logger = logging.getLogger(__name__)

STREAK_CUTOFF_HOURS = 30


class EngagementTracker:
    def __init__(self, storage_dir: Optional[Path] = None) -> None:
        settings = get_settings()
        self.storage_dir = storage_dir or (settings.logs_dir / "engagement")
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._stats_file = self.storage_dir / "engagement_stats.json"
        self._challenge_file = self.storage_dir / "daily_challenge.json"
        self._battle_file = self.storage_dir / "weekly_battle.json"
        self._stats = self._load_stats()
        self._daily_challenge: Optional[DailyChallenge] = self._load_challenge()
        self._weekly_battle: Optional[WeeklyBattle] = self._load_battle()
        self._today = date.today().isoformat()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------
    def _load_stats(self) -> EngagementStats:
        if self._stats_file.exists():
            try:
                data = json.loads(self._stats_file.read_text())
                return EngagementStats(**data)
            except Exception as exc:
                logger.warning("Failed to load engagement stats: %s", exc)
        return EngagementStats()

    def _save_stats(self) -> None:
        self._stats_file.write_text(self._stats.model_dump_json(indent=2))

    def _load_challenge(self) -> Optional[DailyChallenge]:
        if self._challenge_file.exists():
            try:
                data = json.loads(self._challenge_file.read_text())
                return DailyChallenge(**data)
            except Exception as exc:
                logger.warning("Failed to load daily challenge: %s", exc)
        return None

    def _save_challenge(self) -> None:
        if self._daily_challenge:
            self._challenge_file.write_text(self._daily_challenge.model_dump_json(indent=2))
        elif self._challenge_file.exists():
            self._challenge_file.unlink(missing_ok=True)

    def _load_battle(self) -> Optional[WeeklyBattle]:
        if self._battle_file.exists():
            try:
                data = json.loads(self._battle_file.read_text())
                return WeeklyBattle(**data)
            except Exception as exc:
                logger.warning("Failed to load weekly battle: %s", exc)
        return None

    def _save_battle(self) -> None:
        if self._weekly_battle:
            self._battle_file.write_text(self._weekly_battle.model_dump_json(indent=2))
        elif self._battle_file.exists():
            self._battle_file.unlink(missing_ok=True)

    # ------------------------------------------------------------------
    # Streak
    # ------------------------------------------------------------------
    def update_streak(self) -> None:
        now = date.today().isoformat()
        last = self._stats.last_active_date
        if last == now:
            return
        try:
            if last and (date.fromisoformat(now) - date.fromisoformat(last)).days == 1:
                self._stats.current_streak += 1
            elif last and last != now:
                self._stats.current_streak = 1
            else:
                self._stats.current_streak = 1
        except (ValueError, TypeError):
            self._stats.current_streak = 1
        self._stats.last_active_date = now
        if self._stats.current_streak > self._stats.longest_streak:
            self._stats.longest_streak = self._stats.current_streak
        self._save_stats()

    def get_streak_message(self) -> Optional[str]:
        if self._stats.current_streak <= 0:
            return None
        if self._stats.current_streak == 1:
            return "🔥 Day 1 streak started! Keep going tomorrow!"
        if self._stats.current_streak < 7:
            return f"🔥 {self._stats.current_streak}-day streak! You're building momentum!"
        if self._stats.current_streak < 30:
            return f"⚡ {self._stats.current_streak}-day streak! Unstoppable!"
        if self._stats.current_streak < 100:
            return f"🏆 {self._stats.current_streak}-day streak! Legendary consistency!"
        return f"👑 {self._stats.current_streak}-day streak! You're a revision legend!"

    # ------------------------------------------------------------------
    # Daily Challenge
    # ------------------------------------------------------------------
    def set_daily_challenge(self, content: GeneratedContent) -> None:
        self._daily_challenge = DailyChallenge(
            date=self._today,
            content=content,
            completed=False,
            scores=[],
        )
        self._stats.daily_challenge_active = True
        self._stats.daily_challenge_content = content
        self._save_challenge()
        self._save_stats()

    def record_answer(self, correct: bool) -> None:
        if self._daily_challenge and self._daily_challenge.date == self._today:
            self._daily_challenge.scores.append(correct)
            self._stats.total_attempted += 1
            if correct:
                self._stats.total_correct += 1
            self._save_challenge()
            self._save_stats()

    def get_challenge_result(self) -> Optional[str]:
        if not self._daily_challenge or self._daily_challenge.date != self._today:
            return None
        scores = self._daily_challenge.scores
        if not scores:
            return "📝 Daily Challenge is live! Tap to answer."
        correct = sum(scores)
        total = len(scores)
        pct = (correct / total * 100) if total else 0
        if pct == 100:
            return f"🎯 Perfect score! {correct}/{total} correct — outstanding!"
        if pct >= 80:
            return f"💪 Great job! {correct}/{total} correct ({pct:.0f}%)!"
        if pct >= 50:
            return f"📚 Keep revising! {correct}/{total} correct ({pct:.0f}%)"
        return f"🔄 Review needed — {correct}/{total} correct ({pct:.0f}%). Try again tomorrow!"

    # ------------------------------------------------------------------
    # Weekly Battle
    # ------------------------------------------------------------------
    def start_weekly_battle(self) -> None:
        week_start = date.today().isoformat()
        self._weekly_battle = WeeklyBattle(week_start=week_start, active=True, scores={})
        self._stats.weekly_battle_active = True
        self._save_battle()
        self._save_stats()

    def score_battle_point(self, user_id: str = "default") -> None:
        if self._weekly_battle and self._weekly_battle.active:
            self._weekly_battle.scores[user_id] = self._weekly_battle.scores.get(user_id, 0) + 1
            self._stats.weekly_battle_score += 1
            self._save_battle()
            self._save_stats()

    def get_battle_leaderboard(self) -> Optional[str]:
        if not self._weekly_battle or not self._weekly_battle.active:
            return None
        scores = self._weekly_battle.scores
        if not scores:
            return "⚔️ Weekly Revision Battle is on! Answer questions to score points!"
        sorted_users = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        lines = ["🏆 *Weekly Revision Battle*", ""]
        for rank, (uid, pts) in enumerate(sorted_users[:10], 1):
            medal = {1: "🥇", 2: "🥈", 3: "🥉"}.get(rank, f"{rank}.")
            lines.append(f"{medal} User {uid}: {pts} pts")
        return "\n".join(lines)

    def end_battle(self) -> Optional[str]:
        result = self.get_battle_leaderboard()
        self._weekly_battle = None
        self._stats.weekly_battle_active = False
        self._stats.weekly_battle_score = 0
        self._save_battle()
        self._save_stats()
        return result

    # ------------------------------------------------------------------
    # Stats accessors
    # ------------------------------------------------------------------
    @property
    def stats(self) -> EngagementStats:
        return self._stats

    def accuracy_pct(self) -> float:
        if self._stats.total_attempted == 0:
            return 0.0
        return self._stats.total_correct / self._stats.total_attempted * 100
