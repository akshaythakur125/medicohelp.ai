# MedicoHelp.ai — Final Project Status

## Project Overview

MedicoHelp.ai is an autonomous medical education content generator and Telegram poster built for NEET PG / INI-CET aspirants. It runs a 4-phase daily schedule — morning revision, afternoon MCQ, evening revision, nightly weak-topic recall — that rotates across 19 pre-clinical and clinical subjects without human intervention. The system operates in a **library-first** mode: a static MBBS content library of 190 topics across 8 formats provides the entire content pipeline with zero external API dependencies. When AI API keys (OpenAI, Gemini, or Anthropic) are configured, the engine upgrades to AI-generated clinical vignettes, adaptive SM-2 spaced repetition, and rich-image posters.

The project is fully containerized, deploys to any cloud platform (Render, Railway, Fly.io), and exposes a FastAPI REST API for health checks, manual generation, scheduler pause/resume, and analytics. A Telegram bot interface provides admin commands for real-time control. The system includes restart-safe persistence (scheduler state, retry queue, analytics logs survive container restarts), anti-duplication safeguards, and a 21-test integration suite that validates every module end-to-end. Core design goals were zero external dependencies for the content pipeline, resilience against API failures, and fully autonomous operation across time zones.

## Feature Matrix

| Feature | Status | Details |
|---|---|---|
| Content Library | ✅ Complete | 19 subjects, 190 topics (10 per subject), 8 content formats (rapid_revision, mcq, concise_notes, pyq_concept, mnemonic, flashcard, true_false, one_liner_recall). Library-first fallback means zero API calls at runtime. |
| Autonomous Rotation Engine | ✅ Complete | No consecutive subject repeats (tracks `_last_subject`), format mixing via `_recent_formats` deque (window=8), weak-topic prioritization with 60% draw probability (`_WEAK_TOPIC_DRAW_P = 0.6`), balanced round-robin cursor across 19 subjects. |
| SmartContentEngine | ✅ Complete | SM-2 spaced repetition (`_SPACED_REPETITION_DAYS = 7`), MCQ variation format mapping, vignette validation with `generate_vignette()`, three difficulty tiers (easy, moderate, exam_level), performance tracking with `_PERFORMANCE_DECAY_DAYS = 30`. |
| 4-Phase Day Scheduler | ✅ Complete | APScheduler-based with CronTrigger at 08:00 (morning_revision), 14:00 (afternoon_mcq), 20:00 (evening_revision), 22:00 (nightly_weak_topic). State persisted to `scheduler_state.json`; survives container restarts. Slot-lane mapping via `_SLOT_LANE_MAP`. |
| Engagement Content Enrichment | ✅ Complete | Subject-specific hook lines, exam tags, memory tricks, clinical pearls, Bloom's taxonomy integration via `enrich_for_engagement()`. Hooks defined per subject with randomized selection. |
| MCQ Engine | ✅ Complete | Clinical vignettes via `generate_vignette()`, misleading distractors with `generate_distractors()`, wrong-option analysis (`analyze_wrong_option()`), NEET PG framing, image-based question support. |
| Analytics System | ✅ Complete | Subject frequency, format usage, daily post counts, weak topic trends with 30-day sliding window, engagement estimates. Persisted to `analytics.json`. Retrievable via REST API. |
| Anti-Duplication Safeguards | ✅ Complete | Recent post tracking (`_recent_titles` deque), spaced repetition cooldown (7-day SM-2 cycles), weak-topic cooldown (3 days via `_WEAK_TOPIC_COOLDOWN_DAYS`), posted title dedup set (max 500 entries). |
| Emergency Recovery | ✅ Complete | Restart-safe scheduler state via JSON file, retry queue with 3 attempts (delays: 1min, 5min, 15min), corrupted content fallback in `ContentLibrary.get()` with format/subject relaxation, graceful degradation when AI providers are unavailable. |
| Telegram Bot Integration | ✅ Complete | 7 commands (`/start`, `/help`, `/status`, `/post`, `/pause`, `/resume`, `/stats`), poll support, rich-text HTML formatting via `format_for_telegram()`, admin controls with `admin_chat_id` whitelisting. |
| REST API | ✅ Complete | 7 endpoints: `/health` (status + scheduler state), `/generate` (single post), `/generate-all` (all subjects), `/generate-news` (exam news), `/planned-post` (next slot), `/pause-resume` (toggle), `/stats` + `/analytics` (usage data). |
| Test Suite | ✅ Complete | 21 pytest integration tests covering library loading, content strategy rotation, SmartContentEngine generation, orchestrator workflow, pause/resume lifecycle, analytics recording, enrichment application, retry queue processing, and weak-topic recall. |

## Codebase Structure

```
app/
├── main.py                 # FastAPI entry point, startup validation, REST endpoints
├── config.py               # Pydantic Settings from env vars with directory initialization
├── models.py               # All Pydantic models and enums (Subject, ContentFormat, SlotType, etc.)
├── logging_config.py       # Logging configuration
└── services/
    ├── ai_client.py        # AI generation client (library-first fallback, multi-provider)
    ├── analytics.py        # Content usage tracking with 30-day sliding window
    ├── bot_commands.py     # Telegram bot admin command handler
    ├── content_engine.py   # SmartContentEngine: SM-2, MCQ variation, vignette generation
    ├── content_strategy.py # Autonomous rotation engine with weak-topic prioritization
    ├── enrichment.py       # Engagement hooks, exam tags, memory tricks, clinical pearls
    ├── formatter.py        # Telegram HTML message formatting
    ├── medical_image.py    # AI-based medical image generation
    ├── news.py             # Exam news sweeper and residency tips
    ├── orchestrator.py     # Central PostOrchestrator wiring all services together
    ├── poster.py           # Pillow-based image poster generation
    ├── quality.py          # Content quality validation gate
    ├── retry_queue.py      # Failed-post retry system (3 attempts, exponential backoff)
    ├── scheduler.py        # APScheduler-based 4-phase daily scheduler
    ├── storage.py          # File-based post log persistence
    └── telegram.py         # Telegram HTTP API client
content/
├── loader.py               # Dynamic content library loader with LRU-cached singleton
├── anatomy.py              # 10 anatomy topics (rapid_revision, mcq, etc.)
├── physiology.py           # 10 physiology topics
├── biochemistry.py         # 10 biochemistry topics
├── pathology.py            # 10 pathology topics
├── pharmacology.py         # 10 pharmacology topics
├── microbiology.py         # 10 microbiology topics
├── forensic_medicine.py    # 10 forensic medicine topics
├── community_medicine.py   # 10 community medicine topics
├── general_medicine.py     # 10 general medicine topics
├── general_surgery.py      # 10 general surgery topics
├── obstetrics_gynecology.py# 10 OBG topics
├── pediatrics.py           # 10 pediatrics topics
├── ophthalmology.py        # 10 ophthalmology topics
├── ent.py                  # 10 ENT topics
├── orthopedics.py          # 10 orthopedics topics
├── dermatology.py          # 10 dermatology topics
├── psychiatry.py           # 10 psychiatry topics
├── radiology.py            # 10 radiology topics
└── anesthesiology.py       # 10 anesthesiology topics
tests/
└── test_smoke.py           # 21 integration tests covering all modules
```

## Test Summary

- **21 tests, all passing** — run with `pytest tests/ -v`
- Coverage areas:
  - Curriculum completeness (19 subjects, 190 topics, 8 formats)
  - Library-first generation (`test_library_generation_text_mode`)
  - Content strategy rotation (no consecutive repeats, format diversity, weak-topic draw)
  - SmartContentEngine (post generation, performance recording, weak topic identification)
  - PostOrchestrator end-to-end (daily packs, news generation, image-based posts)
  - Pause/resume lifecycle (`test_pause_resume_lifecycle`)
  - Analytics recording and retrieval
  - Enrichment application across formats
  - Retry queue enqueue/processing mechanics
  - Weak-topic recall post generation

## Environment Requirements

| Variable | Description | Default | Required |
|---|---|---|---|
| `OPENAI_API_KEY` | OpenAI API key for AI generation | `None` | No (library fallback) |
| `GEMINI_API_KEY` | Google Gemini API key | `None` | No |
| `ANTHROPIC_API_KEY` | Anthropic API key | `None` | No |
| `AI_PROVIDER` | Active AI provider (`openai`, `gemini`, `anthropic`, `none`) | `none` | No |
| `AI_MODEL` | Model name for chosen provider | `gpt-4o-mini` | No |
| `GENERATE_REALISTIC_IMAGES` | Enable AI image generation | `False` | No |
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from @BotFather | `None` | Yes for Telegram features |
| `TELEGRAM_CHAT_ID` | Target Telegram channel/chat ID | `None` | Yes for Telegram posting |
| `ADMIN_CHAT_ID` | Admin chat ID for bot commands | `None` | No |
| `POST_INTERVAL_HOURS` | Hours between scheduled posts | `6` | No |
| `POST_SCHEDULE_TIMES` | Comma-separated override schedule (e.g. `08:00,14:00,20:00`) | `""` | No |
| `TIMEZONE` | Schedule timezone | `Asia/Kolkata` | No |
| `RUN_SCHEDULER` | Enable APScheduler on startup | `True` | No |
| `TEXT_ONLY_MODE` | Send rich-text instead of image posters | `True` | No |
| `POSTING_PAUSED` | Global pause for scheduled posting | `False` | No |
| `APP_HOST` | FastAPI bind address | `0.0.0.0` | No |
| `APP_PORT` | FastAPI port | `8000` | No |
| `LOG_LEVEL` | Logging verbosity | `INFO` | No |
| `ALLOW_MOCK_AI` | Enable mock AI responses for testing | `True` | No |
| `NEWS_LOOKBACK_DAYS` | Days to look back for exam news | `14` | No |
| `NEWS_MAX_ITEMS` | Max news items per sweep | `6` | No |

## Deployment Status

- **Container-ready**: Dockerfile in repo root using Python 3.11+ base image
- **Platform support**: Deployable to Render, Railway, Fly.io, and GitHub Codespaces without modification
- **Zero external dependencies for core pipeline**: The static content library (190 topics across 8 formats) produces fully functional posts with no AI API key, no database, no external services — the system runs on pure Python with FastAPI + APScheduler + Pillow
- **Telegram-only mode**: With `TEXT_ONLY_MODE=true` and no AI keys, the system generates rich-text Telegram messages from the static library and posts them on schedule — no image generation or external API calls required
- **Deployment guides**: See `DEPLOYMENT.md` and `DEPLOYMENT_READY.md` for platform-specific instructions

## Known Limitations

- The static content library, while comprehensive (190 topics), is finite — a single subject cycled daily will exhaust its 10 topics within ~2 weeks. SM-2 spaced repetition and weak-topic rotation mitigate repetition visibility, but long-term AI-powered generation is required for truly indefinite operation.
- Telegram bot commands work only when `ADMIN_CHAT_ID` is configured; there is no public-facing interactive mode for channel subscribers. Commands are processed via polling, not webhooks.
- The analytics system tracks usage counts and weak-topic performance but does not persist per-user engagement metrics (views, clicks, poll responses) since Telegram channels do not expose per-user data via the bot API.
- AI image generation (`GENERATE_REALISTIC_IMAGES`) requires OpenAI or Gemini API keys and increases operational cost; the default `TEXT_ONLY_MODE=true` skips image poster creation entirely.
- The scheduler uses in-memory APScheduler with file-based state persistence — for multi-replica deployments, a database-backed scheduler (e.g., APScheduler+SQLAlchemy) would be needed to prevent duplicate post conflicts.
