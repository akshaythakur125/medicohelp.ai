"""Production simulation: simulate 7 days of posting to verify scheduler stability, content diversity, and no crashes.

Usage:
    python -m tests.simulate_production
"""
import asyncio
import random
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

sys.path.insert(0, "/workspaces/medicohelp.ai")

from app.config import get_settings
from app.models import EducationMode, SlotType, Subject
from app.services.orchestrator import PostOrchestrator

settings = get_settings()
orchestrator = PostOrchestrator(settings)

POSTS_PER_DAY = 4
SIMULATION_DAYS = 30
TOTAL_POSTS = POSTS_PER_DAY * SIMULATION_DAYS

LANE_COUNTER: dict[str, int] = {}
SUBJECT_COUNTER: dict[str, int] = {}
FORMAT_COUNTER: dict[str, int] = {}
ERRORS: list[str] = []
START_TIME = time.monotonic()
POSTED_TITLES: set[str] = set()  # Track all posted titles for dedup check
ENGAGEMENT_EVENTS: list[str] = []


def log(msg: str) -> None:
    ts = datetime.now(tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{ts}] {msg}")


async def simulate() -> int:
    log(f"Starting {SIMULATION_DAYS}-day simulation: {TOTAL_POSTS} posts")
    log(f"Library: {len(list(Subject))} subjects, {_count_library()} topics")
    log("=" * 60)

    # Clear state from previous runs
    for p in ["logs/analytics.json", "logs/performance.json", "logs/topic_history.json", "logs/scheduler_state.json"]:
        Path(p).unlink(missing_ok=True)

    slot_cycle = [
        ("Morning", SlotType.morning_revision),
        ("Afternoon", SlotType.afternoon_mcq),
        ("Evening", SlotType.evening_revision),
        ("Night", SlotType.nightly_weak_topic),
    ]

    for day in range(1, SIMULATION_DAYS + 1):
        log(f"\n--- Day {day} of {SIMULATION_DAYS} ---")

        # Daily challenge on days 5-25
        if 5 <= day <= 25 and day % 2 == 0:
            await _run_daily_challenge(day)

        # Education mode switch at day 10 and 20
        if day == 10:
            orchestrator.set_education_mode("first_year_mbbs")
            log("  ⚡ Education mode: first_year_mbbs")
        elif day == 20:
            orchestrator.set_education_mode("comprehensive")
            log("  ⚡ Education mode: comprehensive")

        # Weekly battle cycle
        if day % 7 == 0:
            await _run_battle_start(day)
        elif day % 7 == 1:
            await _run_battle_end(day)

        # Regular posting slots
        for slot_name, slot_type in slot_cycle:
            await _run_slot(day, slot_name, slot_type)

        log(f"Day {day} complete — {sum(LANE_COUNTER.values())}/{TOTAL_POSTS} total posts")

        # Spread performance data realistically — 60/40 correct/incorrect
        rand_correct = random.random() < 0.6
        for title in list(orchestrator._engine._performance.keys())[:5]:
            orchestrator._engine.record_performance(
                title=title,
                correct=rand_correct,
            )

    elapsed = time.monotonic() - START_TIME
    return _report(elapsed)


async def _run_daily_challenge(day: int) -> None:
    try:
        result = await orchestrator.generate_daily_challenge(publish_to_telegram=False)
        if result:
            ENGAGEMENT_EVENTS.append(f"Day {day}: Daily challenge posted — {result.content.title[:50]}")
            POSTED_TITLES.add(result.content.title)
            log(f"  ⭐ Daily challenge: {result.content.title[:50]}")
        else:
            log(f"  ⭐ Daily challenge: FAILED to generate")
    except Exception as exc:
        ERRORS.append(f"Day {day} Daily Challenge: {exc}")
        log(f"  ⭐ Daily challenge ERROR: {exc}")


async def _run_battle_start(day: int) -> None:
    try:
        if orchestrator._engagement.stats.weekly_battle_active:
            await orchestrator.end_weekly_battle(publish_to_telegram=False)
        await orchestrator.start_weekly_battle(publish_to_telegram=False)
        ENGAGEMENT_EVENTS.append(f"Day {day}: Weekly battle started")
        log(f"  ⚔️ Weekly battle started")
    except Exception as exc:
        log(f"  ⚔️ Weekly battle start ERROR: {exc}")


async def _run_battle_end(day: int) -> None:
    try:
        if orchestrator._engagement.stats.weekly_battle_active:
            result = orchestrator._engagement.end_battle()
            if result:
                ENGAGEMENT_EVENTS.append(f"Day {day}: Weekly battle ended")
                log(f"  ⚔️ Weekly battle ended")
    except Exception as exc:
        log(f"  ⚔️ Weekly battle end ERROR: {exc}")


async def _run_slot(day: int, slot_name: str, slot_type: SlotType) -> None:
    try:
        planned = orchestrator.content_strategy.next_post(slot_type=slot_type)
        lane = planned.lane.value if planned.lane else "unknown"
        subj = planned.subject.value if planned.subject else "unknown"

        result = await orchestrator.generate_planned_post(
            publish_to_telegram=False,
            slot_type=slot_type,
        )
        content = result.content
        fmt = content.content_format.value

        LANE_COUNTER[lane] = LANE_COUNTER.get(lane, 0) + 1
        SUBJECT_COUNTER[subj] = SUBJECT_COUNTER.get(subj, 0) + 1
        FORMAT_COUNTER[fmt] = FORMAT_COUNTER.get(fmt, 0) + 1

        title_short = (content.title or "")[:60]
        diff = content.difficulty or "?"
        if content.title:
            POSTED_TITLES.add(content.title)
        log(f"  [{slot_name:10s}] {subj:20s} | {lane:20s} | {fmt:20s} | {diff:12s} | {title_short}")
    except RuntimeError as exc:
        if "paused" in str(exc):
            orchestrator.resume()
            log(f"  [{slot_name:10s}] Posting was paused — auto-resumed")
    except Exception as exc:
        ERRORS.append(f"Day {day} {slot_name}: {exc}")
        log(f"  [{slot_name:10s}] ERROR: {exc}")


def _check_title_repeats() -> str:
    """Check for rapid repeats within the posted titles."""
    repeats = len(POSTED_TITLES)
    total = sum(LANE_COUNTER.values()) + len(ENGAGEMENT_EVENTS)
    if total == 0:
        return "No posts to check"
    unique_ratio = repeats / total if total > 0 else 0
    if unique_ratio > 0.8:
        return f"✅ Excellent diversity — {unique_ratio:.0%} unique titles"
    if unique_ratio > 0.6:
        return f"⚠ Acceptable diversity — {unique_ratio:.0%} unique titles"
    return f"❌ Poor diversity — {unique_ratio:.0%} unique titles ({repeats} unique / {total} total)"


def _report(elapsed: float) -> int:
    log("\n" + "=" * 60)
    log("SIMULATION COMPLETE")
    log("=" * 60)
    log(f"Duration: {elapsed:.2f}s for {sum(LANE_COUNTER.values())} posts")
    log(f"Errors: {len(ERRORS)}")

    log("\n--- Lane Distribution ---")
    for lane, count in sorted(LANE_COUNTER.items(), key=lambda x: -x[1]):
        log(f"  {lane:20s}: {count}")

    log("\n--- Subject Distribution ---")
    for subj, count in sorted(SUBJECT_COUNTER.items(), key=lambda x: -x[1]):
        log(f"  {subj:25s}: {count}")

    log("\n--- Format Distribution ---")
    for fmt, count in sorted(FORMAT_COUNTER.items(), key=lambda x: -x[1]):
        log(f"  {fmt:25s}: {count}")

    # Check for consecutive subject repeats
    log("\n--- Diversity Check ---")
    max_subj = max(SUBJECT_COUNTER.values()) if SUBJECT_COUNTER else 0
    min_subj = min(SUBJECT_COUNTER.values()) if SUBJECT_COUNTER else 0
    total_subj = len(SUBJECT_COUNTER)
    log(f"  Unique subjects posted: {total_subj}/19")
    log(f"  Max posts per subject: {max_subj}, Min: {min_subj}")
    if total_subj >= 15:
        log("  ✅ Subject diversity: GOOD")
    else:
        log(f"  ❌ Subject diversity: POOR — only {total_subj}/19 subjects used")

    log("\n--- Title Dedup Check ---")
    log(f"  {_check_title_repeats()}")
    log(f"  Total unique titles: {len(POSTED_TITLES)}")

    log("\n--- Engagement Events ---")
    log(f"  Total engagement events: {len(ENGAGEMENT_EVENTS)}")
    log(f"  Streak days: {orchestrator._engagement.stats.current_streak}")
    log(f"  Longest streak: {orchestrator._engagement.stats.longest_streak}")
    log(f"  Battle active: {orchestrator._engagement.stats.weekly_battle_active}")

    # Test education mode filtering
    log("\n--- Education Mode Test ---")
    mode_name = orchestrator.settings.education_mode
    log(f"  Final mode: {mode_name}")
    log(f"  Subjects used: {len(SUBJECT_COUNTER)}")

    log("\n--- Stability Check ---")
    if ERRORS:
        log(f"  ❌ {len(ERRORS)} errors occurred:")
        for e in ERRORS[:5]:
            log(f"     - {e}")
    else:
        log("  ✅ Zero errors — stable")

    log(f"\nTotal simulation time: {elapsed:.1f}s")
    log(f"Average per post: {elapsed / max(sum(LANE_COUNTER.values()), 1):.2f}s")

    if ERRORS:
        return 1
    return 0


def _count_library() -> int:
    try:
        from content.loader import get_library
        return get_library().total()
    except Exception:
        return 0


if __name__ == "__main__":
    exit_code = asyncio.run(simulate())
    sys.exit(exit_code)
