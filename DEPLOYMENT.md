# MedicoHelp.ai — Deployment Checklist

## Pre-Deployment
- [ ] Environment variables set in `.env` or platform dashboard:
  - `TELEGRAM_BOT_TOKEN` — Telegram bot token from @BotFather (required for posting)
  - `TELEGRAM_CHAT_ID` — Target channel/group ID for posting
  - `ADMIN_CHAT_ID` — Admin Telegram user ID for bot commands
  - `POST_SCHEDULE_TIMES` — Comma-separated HH:MM slots (default: `08:00,14:00,20:00,22:00`)
  - `TEXT_ONLY_MODE=true` — Send formatted text instead of image posters
  - `AI_PROVIDER=none` — No external AI dependency; library-first generation
- [ ] Content library verified: `python3 -c "from content.loader import get_library; lib = get_library(); print(f'{lib.total()} topics across {len(lib.summary())} subjects')"`
- [ ] All tests pass: `python3 -m pytest tests/ -v`

## Telegram Bot Setup
- [ ] Bot created via @BotFather, token copied to `TELEGRAM_BOT_TOKEN`
- [ ] Bot added as admin to target channel
- [ ] Channel ID configured in `TELEGRAM_CHAT_ID` (format: `@channelname` or numeric ID)
- [ ] Admin chat ID (`ADMIN_CHAT_ID`) set for `/post`, `/pause`, `/resume` commands

## Deployment Platforms

### Docker
```bash
docker build -t medicohelp-ai .
docker run -d --env-file .env -p 8000:8000 medicohelp-ai
```

### Render.com
- Service type: Web Service
- Build command: `pip install -r requirements.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
- Health check: `/health`

### Railway / Fly.io
- Use `Dockerfile` in repo root
- Port: `8000`
- Health endpoint: `/health`

## Verify Deployment
- [ ] `GET /health` returns `{"status":"ok","scheduler_running":true}`
- [ ] `GET /stats` returns library topics count ≥ 190
- [ ] `POST /pause` returns `{"status":"paused"}`
- [ ] `POST /resume` returns `{"status":"resumed"}`
- [ ] Bot posts to Telegram channel at configured times
- [ ] `/status` command from admin chat shows bot running

## Admin Commands (Telegram)
| Command | Description |
|---------|-------------|
| `/status` | Bot health + schedule + library stats |
| `/post` | Force an immediate rotation post |
| `/post anatomy` | Post a specific subject |
| `/pause` | Pause all scheduled posting |
| `/resume` | Resume scheduled posting |
| `/stats` | Detailed engine statistics + weak topics |
| `/weak` | Force a weak-topic recall post |
| `/post_format mcq` | Post a specific format |
| `/help` | Show all commands |

## Architecture Summary
- **Content-first**: Static library (`content/*.py`) supplies all 19 subjects × 10 topics × 8 formats
- **SmartContentEngine**: SM-2 weak-topic tracking, MCQ variation, spaced repetition (7-day cooldown)
- **Posting pipeline**: Scheduler → ContentStrategy (12-slot rotation) → Orchestrator → Telegram API
- **4-phase day**: Morning revision (08:00), Afternoon MCQ variant (14:00), Evening revision (20:00), Nightly weak-topic recall (22:00)
- **Admin controls**: Pause/resume, subject override, format override, force-post, stats
- **Persistence**: File-based JSONL for post log + JSON for performance tracking (PostgreSQL deferred)
- **Zero AI dependency**: All core content from static library; optional AI provider for fallback generation
