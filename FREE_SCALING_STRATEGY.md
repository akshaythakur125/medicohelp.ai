# Free Scaling Strategy

## Zero-Cost Architecture

### Current State
| Component | Cost | Notes |
|-----------|------|-------|
| Static content library | Free | 19 subjects × 10 topics × 8 formats = 1520 items |
| Telegram API | Free | No cost for bot API |
| FastAPI server | Free | Runs on any Python host |
| Spaced repetition engine | Free | SM-2 variant, file-based |
| Analytics | Free | JSONL/JSON file persistence |
| Engagement tracker | Free | File-based, no DB needed |
| AI provider (optional) | Free | Default `AI_PROVIDER=none` |

### Content Growth Strategy
1. **Static library first** — 190+ topics curated manually (already complete)
2. **Format expansion** — Each topic has 8 ready-made formats
3. **AI as enhancer** — AI provider only enhances, never required for core flow
4. **Community contributions** — Accept PRs for new subjects and topics

### Deployment Options
| Platform | Cost | Suitability |
|----------|------|-------------|
| Railway (Hobby) | Free | 500MB RAM, always-on |
| Render (Free) | Free | 512MB RAM, spins down after inactivity |
| Koyeb (Free) | Free | 1GB RAM, always-on |
| Fly.io | Free tier | 256MB always-on, 3GB monthly transfer |
| Oracle Cloud (Always Free) | Free | 24GB RAM, 4 ARM cores |
| Self-hosted (Raspberry Pi) | Free | Low power, always-on |

### PostgreSQL Migration Path (if needed)
- Not required for current scale
- If needed: Railway provides $5/mo PostgreSQL
- SQLite alternative: Zero-cost, file-based, built into Python
- Migration would only affect `storage.py` and `analytics.py`

### Avoiding Rate Limits
- Telegram: 30 messages/sec per chat — far below our 4 posts/day
- APScheduler: max_instances=1, coalesce=True prevents overlap
- Retry queue: 3 attempts max with exponential backoff
- All async I/O — no blocking operations

### Monitoring (Free)
- Application logs to stdout (captured by Railway/Render/Koyeb)
- Error logging to `logs/errors.jsonl`
- Health endpoint at `/health` — usable with free uptime monitors
- Analytics report at `/api/analytics` — plain JSON

## Operational Cost: $0/month
- No paid API calls required for core functionality
- No database hosting fees
- No image generation costs (text-only mode default)
- No domain required (Telegram bot username is the entry point)
