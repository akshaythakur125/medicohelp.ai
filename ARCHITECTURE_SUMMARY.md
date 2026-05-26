# MedicoHelp.ai — Final Architecture Summary

## System Overview

MedicoHelp.ai is an autonomous medical education content delivery system that posts structured revision material to a Telegram channel four times daily. It operates without any external API dependency for its core content pipeline — all 190 topics across 19 MBBS subjects are pre-loaded from static Python files.

## Component Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        FastAPI (app/main.py)                     │
│  Health | Generate | Planned-Post | Pause/Resume | Stats/News   │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│                    PostOrchestrator                              │
│  (app/services/orchestrator.py)                                  │
│                                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────────┐   │
│  │ AIClient     │  │ SmartContent │  │ ContentStrategy       │   │
│  │ (library-    │  │ Engine       │  │ (autonomous rotation) │   │
│  │  first AI)   │  │ (SM-2 track) │  │                       │   │
│  └─────────────┘  └──────────────┘  │ • No consecutive subj  │   │
│  ┌─────────────┐  ┌──────────────┐  │ • Format mixing        │   │
│  │ Enrichment  │  │ Content      │  │ • Weak-topic priority  │   │
│  │ (engagement)│  │ Analytics    │  │ • Balanced schedule    │   │
│  └─────────────┘  └──────────────┘  └───────────────────────┘   │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────────┐   │
│  │ QualityGate │  │ RetryQueue   │  │ PostLogStore          │   │
│  │ (validation)│  │ (3 retries)  │  │ (file-based JSONL)    │   │
│  ┌──────────────────┐  ┌──────────────────┐  ┌─────────────┐    │
│  │ EngagementTracker │  │ EducationModes   │  │ MemoryAnchors│   │
│  │ (streaks/        │  │ (MBBS year/      │  │ (mnemonics/  │   │
│  │  challenges/     │  │  exam routing)   │  │  pearls/     │   │
│  │  weekly battles) │  │                  │  │  cross-refs) │   │
│  └──────────────────┘  └──────────────────┘  └─────────────┘    │
│  └─────────────┘  └──────────────┘  └───────────────────────┘   │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────────┐   │
│  │ Formatter   │  │ PosterGen    │  │ TelegramPoster        │   │
│  │ (Telegram   │  │ (Pillow)     │  │ (send_message/poll)   │   │
│  │  HTML)      │  │              │  │                       │   │
│  └─────────────┘  └──────────────┘  └───────────────────────┘   │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│              PostingScheduler (APScheduler)                      │
│  ┌──────────────────────────────────────────────────────────┐    │
│  │  08:00 Morning Revision     (quick_revision)             │    │
│  │  14:00 Afternoon MCQ        (mcq_variant / poll_quiz)   │    │
│  │  20:00 Evening Revision     (flashcard / mnemonic)       │    │
│  │  22:00 Nightly Weak Topic   (weak_topic_recall)         │    │
│  │  Every 30s  ──► Command polling                         │    │
│  │  Every 15m  ──► Retry queue processor                   │    │
│  └──────────────────────────────────────────────────────────┘    │
│  • Restart-safe: saves/recoveres pause state                    │
│  • Misfire grace: 300s                                          │
└──────────────────────────────────────────────────────────────────┘
```

## Data Flow (Single Post)

```
1. Cron trigger fires → PostingScheduler._run_job(slot_type)
2. PostOrchestrator.generate_planned_post(slot_type)
3. ContentStrategy.next_post(slot_type)
   ├── Checks weak provider (25% chance → prioritize weak subject)
   ├── Picks subject ≠ last subject (no consecutive repeats)
   ├── Picks lane from 12-slot rotation
   └── Returns PlannedPost(lane, subject, format, difficulty)
4. Route to lane handler (poll_quiz / mcq_variant / flashcard / etc.)
5. SmartContentEngine generates content
   ├── Anti-duplication: skip recently posted titles (set of 100)
   ├── Education mode filtering (skip excluded subjects)
   ├── Vignette validation (3-7 lines, clinical keywords)
   ├── Difficulty assignment (easy/moderate/exam_level from performance)
   └── Wrong-option analysis (8 distractor reason templates)
6. Educational enhancement (memory anchor, clinical pearl, concept cross-ref)
7. Enrichment (hook line, exam tag, memory trick, Bloom's taxonomy)
8. Engagement tracking (streak update, daily challenge, battle scoring)
9. QualityGate validation (image-based only)
10. Formatter converts to Telegram HTML
11. TelegramPoster.send_message() or send_poll()
12. PostLogStore.save_post() to JSONL
13. SmartContentEngine.record_performance()
14. ContentAnalytics.record_post()
15. ContentStrategy.mark_posted()
```

## Automation Logic

| Concern | Mechanism | File |
|---------|-----------|------|
| Post timing | 4-phase CronTrigger (08/14/20/22 IST) | scheduler.py |
| Subject rotation | `_last_subject` tracking + `_pick_subject()` | content_strategy.py |
| Format mixing | 12-slot rotation with diverse lane types | content_strategy.py |
| Education mode filtering | Subject allowlist per MBBS year/exam target | education_modes.py |
| Weak topic surfacing | SM-2 accuracy tracking → lowest first | content_engine.py |
| Anti-duplication | `_dedup_recent` set (100 entries), 7-day cooldown, `_posted_titles` (500 entries) | content_engine.py, content_strategy.py |
| Spaced repetition | History-based cooldown (3-7 days), performance-weighted | content_engine.py |
| Difficulty distribution | Weighted 30/40/30 (easy/moderate/exam_level) | content_strategy.py |
| Memory anchors | Subject-specific mnemonics, clinical pearls, cross-references | content_engine.py |
| Streak tracking | Consecutive active days with milestone messages | engagement_tracker.py |
| Daily challenge | Daily MCQ posted at 09:00 IST with accuracy scoring | engagement_tracker.py |
| Weekly battle | Sunday-Monday revision competition with leaderboard | engagement_tracker.py |
| Failure recovery | 3 retries (1m/5m/15m), library fallback | retry_queue.py, orchestrator.py |
| Restart safety | State saved to JSON on shutdown, recovered on start | scheduler.py |

## Persistence Layer

| File | Format | Content |
|------|--------|---------|
| `logs/generated_posts.jsonl` | JSONL | Every post with content + metadata |
| `logs/errors.jsonl` | JSONL | Pipeline failures |
| `logs/performance.json` | JSON | SM-2 per-topic performance |
| `logs/topic_history.json` | JSON | Last-sent timestamp per topic |
| `logs/analytics.json` | JSON | Subject frequency, format usage, weak spotlights |
| `logs/retry_queue.json` | JSON | Pending retry tasks |
| `logs/engagement/engagement_stats.json` | JSON | Streak, accuracy, battle score |
| `logs/engagement/daily_challenge.json` | JSON | Current daily challenge state |
| `logs/engagement/weekly_battle.json` | JSON | Active weekly battle scores |
| `logs/scheduler_state.json` | JSON | Pause state, cursor position |
| `logs/scheduler_state.json` | JSON | Pause state across restarts |

## Deployment Strategy

**Recommended**: Single Docker container with bind-mounted `logs/` directory.

```bash
docker run -d \
  --name medicohelp-bot \
  --restart unless-stopped \
  --env-file .env \
  -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  medicohelp-ai
```

**Platforms**: Render (Web Service), Railway, Fly.io, Codespaces.

**Zero external API dependency**: Set `AI_PROVIDER=none` — all content from static library.

## Scaling Plan

| Scale Level | Changes Needed | Effort |
|------------|----------------|--------|
| **1-100 channels** | Add channel routing in orchestrator, multi-tenant config | Medium |
| **100-1000 channels** | PostgreSQL for analytics, Redis for job queue, separate scheduler workers | High |
| **1000+ channels** | Microservice split: content-api, scheduler, poster, analytics; message queue in-between | Very High |

## Key Design Decisions

1. **Content-first over AI-first**: Static library removes API cost, latency, and quality variance. AI is optional overlay.
2. **File-based persistence over PostgreSQL**: Simplifies initial deployment (no DB setup). Migration path exists.
3. **APScheduler over Celery**: Lighter weight for single-process deployment. Coalesce + max_instances=1 prevents overlaps.
4. **Enrichment as post-processing**: Engagement sections (hook, Bloom tag, exam tag) added after content generation so they don't interfere with validation.
5. **Anti-duplication at multiple levels**: Content dedup (sequence of 100), spaced repetition (7-day cooldown), and strategy-level tracking (500 titles) work together.

## File Inventory

```
app/
├── main.py                  (159 lines)  — FastAPI entry, startup validation
├── config.py                 (57 lines)  — Pydantic BaseSettings
├── models.py                (159 lines)  — All enums + data models
├── logging_config.py         (38 lines)  — Logging setup
└── services/
    ├── ai_client.py         (355 lines)  — Content generation (lib first, AI opt)
    ├── analytics.py         (140 lines)  — Content usage tracking
    ├── bot_commands.py      (260 lines)  — Telegram admin commands
    ├── content_engine.py    (672 lines)  — SM-2, generators, variations
    ├── content_strategy.py  (158 lines)  — Autonomous rotation engine
    ├── enrichment.py        (180 lines)  — Engagement sections, Bloom's taxonomy
    ├── formatter.py         (279 lines)  — Telegram HTML formatting
    ├── medical_image.py     (160 lines)  — AI image generation (optional)
    ├── news.py              (199 lines)  — Exam news + residency tips
    ├── orchestrator.py      (265 lines)  — Central orchestration hub
    ├── poster.py           (1139 lines)  — Pillow image poster (text-only default)
    ├── quality.py            (63 lines)  — Content validation
    ├── retry_queue.py       (115 lines)  — 3-retry failed post queue
    ├── scheduler.py         (165 lines)  — APScheduler + restart safety
    ├── storage.py            (52 lines)  — File-based persistence
    └── telegram.py           (90 lines)  — Telegram API client
content/
└── loader.py                 (96 lines)  — Content library loader
├── *.py (19 files)           — Subject content definitions
tests/
└── test_smoke.py           (306 lines)  — 21 integration tests
└── simulate_production.py  (158 lines)  — 7-day simulation harness
```

## Framework & Dependencies

- **Web framework**: FastAPI (async, auto-docs at /docs)
- **Scheduler**: APScheduler 3.x (AsyncIOScheduler)
- **Telegram**: httpx-based client (no python-telegram-bot dependency)
- **Content validation**: Pydantic v2 (Built-in model validation)
- **Persistence**: JSON/JSONL files (no database required)
- **Image generation**: Pillow (optional, text-only mode default)
- **AI integration**: Anthropic/OpenAI/Gemini SDKs (optional, library-only default)
- **Testing**: pytest (21 tests)
