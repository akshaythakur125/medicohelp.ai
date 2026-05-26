# Admin Guide

## Overview

This guide is for administrators and operators of the MedicoHelp.ai Telegram bot — an AI-powered medical education poster generator and Telegram auto-poster. The bot serves NEET-PG content across 19 subjects using a static content library with adaptive spaced repetition. It posts 4 times daily to a configured Telegram channel and exposes admin controls both via Telegram bot commands and REST API endpoints.

## Environment Variables

All variables are loaded from a `.env` file or platform dashboard at startup.

| Variable | Purpose | Default | Required |
|---|---|---|---|
| `TELEGRAM_BOT_TOKEN` | Telegram bot token from @BotFather | `None` | Yes |
| `TELEGRAM_CHAT_ID` | Target channel/group ID for posting | `None` | Yes |
| `ADMIN_CHAT_ID` | Admin Telegram user ID for bot commands | `None` | Yes (for bot commands) |
| `POST_SCHEDULE_TIMES` | Comma-separated HH:MM posting slots | `""` (uses default 08:00,14:00,20:00,22:00) | No |
| `POST_INTERVAL_HOURS` | Fallback interval if no schedule times set | `6` | No |
| `TIMEZONE` | Timezone for scheduler | `Asia/Kolkata` | No |
| `TEXT_ONLY_MODE` | Send formatted text instead of image posters | `True` | No |
| `AI_PROVIDER` | AI provider: `openai`, `gemini`, `anthropic`, or `none` | `none` | No |
| `AI_MODEL` | Model name for the selected AI provider | `gpt-4o-mini` | No |
| `OPENAI_API_KEY` | OpenAI API key | `None` | If AI_PROVIDER=openai |
| `GEMINI_API_KEY` | Gemini API key | `None` | If AI_PROVIDER=gemini |
| `ANTHROPIC_API_KEY` | Anthropic API key | `None` | If AI_PROVIDER=anthropic |
| `GENERATE_REALISTIC_IMAGES` | Enable DALL-E / Imagen image generation | `False` | No |
| `OPENAI_IMAGE_MODEL` | OpenAI image generation model | `gpt-image-1` | No |
| `OPENAI_IMAGE_SIZE` | Image size for OpenAI | `1024x1024` | No |
| `OPENAI_IMAGE_QUALITY` | Image quality for OpenAI | `medium` | No |
| `GEMINI_IMAGE_MODEL` | Imagen model for Gemini | `imagen-3.0-generate-002` | No |
| `GEMINI_TEXT_MODEL` | Gemini text model | `gemini-2.0-flash` | No |
| `RUN_SCHEDULER` | Whether to start the background scheduler | `True` | No |
| `POSTING_PAUSED` | Start the bot in paused state | `False` | No |
| `LOG_LEVEL` | Python log level | `INFO` | No |
| `APP_HOST` | FastAPI bind host | `0.0.0.0` | No |
| `APP_PORT` | FastAPI bind port | `8000` | No |
| `ALLOW_MOCK_AI` | Allow mock AI client for local development | `True` | No |
| `NEWS_LOOKBACK_DAYS` | Days to look back for news scraping | `14` | No |
| `NEWS_MAX_ITEMS` | Max news items (1–20) | `6` | No |

## Telegram Bot Commands

Commands are sent via Telegram direct message to the bot. Only the user whose chat ID matches `ADMIN_CHAT_ID` can execute commands. The bot polls Telegram's `getUpdates` every 30 seconds.

### /help
Shows the list of all available admin commands.

**Example:**
```
/help
```

**Output:**
> MedicoHelp Bot — Admin Commands
> /status — Bot status & next schedule
> /post — Trigger an immediate revision post
> /post anatomy — Post a specific subject
> ...

### /status
Returns bot health, current schedule, target channel, AI provider, post mode, and library statistics.

**Example:**
```
/status
```

**Output:**
> MedicoHelp Status — ▶ RUNNING
> 🕐 Schedule: 08:00,14:00,20:00,22:00 (Asia/Kolkata)
> 📬 Posting to: @channelname
> 🤖 AI provider: NONE
> 📄 Post mode: text-only
> 📚 Library: 190 topics | Sent: 45 | Fresh: 145 unseen | Weak: 3

### /pause
Pauses all scheduled posting. Manual `/post` commands still work while paused.

**Example:**
```
/pause
```

**Output:**
> ⏸ Posting paused. No scheduled posts will go out.

### /resume
Resumes scheduled posting after a pause.

**Example:**
```
/resume
```

**Output:**
> ▶ Posting resumed.

### /post
Forces an immediate post through the 12-slot rotation strategy. Can optionally specify a subject and format.

**Examples:**
```
/post
/post anatomy
/post anatomy mcq
```

**Output:**
> ⏳ Generating post…
> ✅ Posted! Subject: anatomy | Format: mcq

If the format is invalid:
> ❌ Unknown format <code>invalid</code>.
> Valid: rapid_revision, mcq, concise_notes, pyq_concept, clinical_case, mnemonic, flashcard, true_false, one_liner_recall

### /post_format
Forces a post of a specific content format across subjects. Iterates through subjects until it finds library content for that format.

**Examples:**
```
/post_format mcq
/post_format flashcard
```

**Output:**
> ✅ Posted <b>mcq</b> format!

### /stats
Returns detailed engine statistics: library topics count, topics sent, unseen count, weak topics, per-subject breakdown, and the top 5 weakest topics with accuracy and days since last seen.

**Example:**
```
/stats
```

**Output:**
> 📊 Engine Statistics
> 📚 Library topics: 190
> 📤 Topics sent: 45
> ✨ Unseen: 145
> 📅 Sent last 7d: 12
> ⚠ Weak topics: 3
>
> Top Weak Topics:
>   • Brachial Plexus Injuries — 33% acc (3 tries) | 2d ago
>
> By Subject:
>   Anatomy: 2
>   Physiology: 3
>   ...

### /weak
Forces a weak-topic recall post. Finds the topic with the lowest accuracy score from performance tracking and posts it with a "Weak Topic Recall" header showing accuracy and attempt count.

**Example:**
```
/weak
```

**Output:**
> 🔁 Finding weakest topic…
> ✅ Weak topic posted: Brachial Plexus Injuries

## REST API Endpoints

The FastAPI server runs on `0.0.0.0:8000` by default. All endpoints are unauthenticated — restrict access via firewall or reverse proxy.

| Method | Path | Description | Example |
|---|---|---|---|
| GET | `/health` | Health check — returns status and whether scheduler is running | `curl localhost:8000/health` |
| GET | `/stats` | SmartContentEngine stats (library, send history, weak topics) | `curl localhost:8000/stats` |
| GET | `/subjects` | List all 19 subject slugs | `curl localhost:8000/subjects` |
| GET | `/content-formats` | List all content format slugs | `curl localhost:8000/content-formats` |
| GET | `/pause-status` | Check whether posting is paused | `curl localhost:8000/pause-status` |
| POST | `/pause` | Pause scheduled posting | `curl -X POST localhost:8000/pause` |
| POST | `/resume` | Resume scheduled posting | `curl -X POST localhost:8000/resume` |
| POST | `/planned-post` | Generate the next post from the 12-slot rotation | `curl -X POST localhost:8000/planned-post -H 'Content-Type: application/json' -d '{"publish_to_telegram": true}'` |
| POST | `/generate` | Generate content with optional subject/format override, does not post to Telegram by default | `curl -X POST localhost:8000/generate -H 'Content-Type: application/json' -d '{"subject": "anatomy", "content_format": "mcq"}'` |
| POST | `/post-now` | Same as `/generate` but publishes to Telegram | `curl -X POST localhost:8000/post-now -H 'Content-Type: application/json' -d '{"subject": "anatomy"}'` |
| POST | `/generate-all-subjects` | Generate content for every subject in one format | `curl -X POST localhost:8000/generate-all-subjects -H 'Content-Type: application/json' -d '{"content_format": "rapid_revision", "publish_to_telegram": false}'` |
| GET | `/news/latest?topic=neet_pg` | Fetch latest news items for a topic | `curl 'localhost:8000/news/latest?topic=neet_pg'` |
| POST | `/news/generate` | Generate a news-based post | `curl -X POST localhost:8000/news/generate -H 'Content-Type: application/json' -d '{"topic": "neet_pg", "publish_to_telegram": true}'` |

### Response Examples

**GET /health**
```json
{"status": "ok", "scheduler_running": true}
```

**POST /pause**
```json
{"status": "paused"}
```

**POST /resume**
```json
{"status": "resumed"}
```

**GET /pause-status**
```json
{"paused": false}
```

**GET /stats**
```json
{
  "library_topics": 190,
  "topics_sent": 45,
  "topics_unseen": 145,
  "sent_last_7_days": 12,
  "weak_topics_count": 3,
  "weak_topics": [
    {"title": "Brachial Plexus Injuries", "accuracy": 0.33, "total_attempts": 3, "days_since_last_seen": 2.0, "subject": "anatomy"}
  ],
  "by_subject": {"anatomy": 10, "physiology": 8, ...}
}
```

**POST /planned-post**
```json
{
  "content": { "title": "...", "caption": "...", ... },
  "poster_path": "text-only",
  "telegram_posted": true
}
```

## Scheduler

The bot runs a 4-phase daily schedule using APScheduler with `AsyncIOScheduler`.

### Default Schedule (IST)

| Time | Slot Type | Description |
|---|---|---|
| 08:00 | `morning_revision` | Morning revision post — rapid revision / concise notes |
| 14:00 | `afternoon_mcq` | Afternoon MCQ variant — reworded stem, shuffled options, wrong-option analysis |
| 20:00 | `evening_revision` | Evening revision post |
| 22:00 | `nightly_weak_topic` | Nightly weak-topic recall — resurfaces the topic with lowest accuracy |

### How to Change Schedule

**Via environment variable:** Set `POST_SCHEDULE_TIMES` to a comma-separated list of `HH:MM` values. Each slot type is assigned by index (position 0 = morning, 1 = afternoon, 2 = evening, 3 = nightly). Only the first 4 values are used.

```
POST_SCHEDULE_TIMES=09:00,13:00,19:00,23:00
```

**Via code:** Edit the `_DEFAULT_SCHEDULE` list in `app/services/scheduler.py` (line 15).

If `POST_SCHEDULE_TIMES` is empty, the bot falls back to interval-based posting every `POST_INTERVAL_HOURS` hours (default 6).

### Bot Command Polling

The scheduler also runs a 30-second interval job that polls Telegram for admin bot commands. This is only enabled when both `ADMIN_CHAT_ID` and `TELEGRAM_BOT_TOKEN` are set.

### Timezone

All scheduling uses `Asia/Kolkata` (IST) by default. Change via the `TIMEZONE` env var. Must be a valid IANA timezone string.

## Content Management

### Adding New Topics / Subjects

The content library lives in the `content/` directory. Each file corresponds to one subject (e.g., `anatomy.py`, `pharmacology.py`). The loader in `content/loader.py` aggregates them.

To add a new subject:
1. Create `content/<subject_name>.py`
2. Define a `get_topics()` function that returns a list of `ContentTopic` objects (each with title, content_format, caption, poster_text, etc.)
3. Register it in `content/loader.py` if auto-discovery is not used

To add topics to an existing subject:
1. Open the relevant `content/<subject>.py` file
2. Append a new `ContentTopic` dict or object following the existing structure

### Content Format Requirements

The bot supports these content formats (defined in `ContentFormat` enum):

| Format | Description |
|---|---|
| `rapid_revision` | Concise high-yield revision notes |
| `mcq` | Multiple-choice question with 4 options |
| `concise_notes` | Detailed but concise study notes |
| `pyq_concept` | Previous-year question pattern |
| `clinical_case` | Clinical case scenario |
| `mnemonic` | Memory aid / mnemonic |
| `flashcard` | Question-answer flashcard |
| `true_false` | True/false statement |
| `one_liner_recall` | Fill-in-the-blank one-liner |

### MCQ Vignette Format Rules

The `SmartContentEngine.validate_mcq_vignette` method enforces these rules:

- Stem must be 3–10 sentences (split by ". ")
- Must include at least 2 of these clinical indicators: `year-old`, `presents`, `history`, `examination`, `complaints`
- Must have at least 4 options (A/B/C/D)
- Must have a correct answer

Each topic should also include `high_yield_takeaway`, `explanation`, and optionally `options` (list of `"A. ..."` strings) and `correct_answer` for MCQ content.

## Monitoring

### Logs Directory

All logs are written to `logs/` at the project root:

| File | Description |
|---|---|
| `logs/app.log` | Rotating application log (5 × 2 MB) — all INFO+ messages |
| `logs/generated_posts.jsonl` | JSONL post log — every generated post with metadata |
| `logs/errors.jsonl` | JSONL error log — pipeline failures with context |
| `logs/topic_history.json` | Spaced-repetition send history (title → ISO timestamp) |
| `logs/performance.json` | Weak-topic tracking (per-topic correct/incorrect counts, last seen) |

### Post Logs (JSONL)

Each line in `generated_posts.jsonl` is a JSON object:
```json
{
  "timestamp": "2026-05-26T10:00:00+00:00",
  "content": { "title": "...", "subject": "anatomy", "content_format": "mcq", ... },
  "poster_path": "text-only",
  "telegram_posted": true
}
```

### Performance Data

The `performance.json` file tracks learner performance per topic:
```json
{
  "Brachial Plexus Injuries": {
    "correct": 1,
    "incorrect": 2,
    "last_seen": "2026-05-24T10:00:00+00:00",
    "subject": "anatomy"
  }
}
```

Topics with accuracy below 60% (after at least 3 attempts) are classified as "weak" and resurfaced during the nightly weak-topic slot.

### Error Logs

Pipeline failures are recorded in `errors.jsonl`:
```json
{
  "timestamp": "2026-05-26T10:00:00+00:00",
  "message": "Post generation pipeline failed",
  "context": { "error": "...", "subject": "anatomy", "content_format": "mcq" }
}
```

## Troubleshooting

### Bot Not Posting

1. Check `GET /health` — verify `scheduler_running` is `true`
2. Check `GET /pause-status` — if `paused` is `true`, run `POST /resume`
3. Check `logs/app.log` for scheduler errors
4. Verify `TELEGRAM_CHAT_ID` is correct and the bot is an admin of the target channel
5. Verify `TELEGRAM_BOT_TOKEN` is valid (re-generate from @BotFather if needed)

### Content Not Found Errors

If `/post` or the scheduler returns content-not-found errors:
1. Check the content library with: `python3 -c "from content.loader import get_library; lib = get_library(); print(lib.total())"`
2. Ensure the library has ≥ 190 topics
3. Check `logs/topic_history.json` — if too many topics have been sent, the spaced-repetition cooldown (7 days for normal, 3 for weak) may prevent repeats
4. Run `/stats` to see `topics_unseen` count

### SmartContentEngine Failures

- **MCQ variation fails:** Ensure source MCQs in the library have `options` (list of 4 `"A. ..."` strings) and `correct_answer`
- **Flashcard/True-False generation fails:** Ensure source topics have `high_yield_takeaway` text
- **Performance file corruption:** Delete `logs/performance.json` and `logs/topic_history.json` to reset (topics will be re-queued as unseen)

### Telegram Rate Limits

- The bot uses `max_instances=1` and `coalesce=True` on all scheduler jobs to prevent overlaps
- If posting fails with a 429 error, the Telegram poster will log the rate-limit response
- The Daily Pack command sends 5 messages sequentially — if rate-limited, some items may not post
- Consider increasing `TEXT_ONLY_MODE=true` (the default) to avoid image upload limits

## Deployment Checklist

See [DEPLOYMENT.md](./DEPLOYMENT.md) for the full deployment checklist covering:
- Pre-deployment environment setup
- Telegram bot configuration
- Docker, Render.com, Railway, and Fly.io deployment
- Post-deployment verification steps
