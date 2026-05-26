# MedicoHelp.ai — Deployment Ready Checklist

## Production Readiness
- [ ] All env vars configured in production environment
- [ ] `AI_PROVIDER=none` for library-only mode (no API costs)
- [ ] `TEXT_ONLY_MODE=true` for text-only delivery (no image generation overhead)
- [ ] `LOG_LEVEL=WARNING` in production (reduce log noise)
- [ ] Content library verified: 190 topics across 19 subjects
- [ ] 21/21 tests passing
- [ ] Docker image built and tested

## Quick Deploy

### Docker (Recommended)
```bash
# Build
docker build -t medicohelp-ai .

# Run with .env file
docker run -d \
  --name medicohelp-bot \
  --restart unless-stopped \
  --env-file .env \
  -p 8000:8000 \
  -v $(pwd)/logs:/app/logs \
  -v $(pwd)/generated:/app/generated \
  medicohelp-ai

# Check logs
docker logs -f medicohelp-bot
```

### Render.com
1. Create new Web Service
2. Connect GitHub repo
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
5. Add env vars from .env.example
6. Health check: `/health`

### Railway
1. Deploy from GitHub
2. Start command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
3. Add env vars
4. Health check: `/health`

### Codespaces
```bash
# Already set up with devcontainer — just run:
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## First-Run Verification
1. Hit `GET /health` — expect `{"status":"ok","scheduler_running":true,...}`
2. Hit `GET /subjects` — expect 19 subjects
3. Hit `GET /stats` — expect `library_topics: 190`
4. Hit `POST /generate` with `{"publish_to_telegram": false}` — expect a GeneratedContent response
5. Hit `POST /pause` — expect `{"status":"paused"}`
6. Hit `POST /resume` — expect `{"status":"resumed"}`

## Monitoring
- Logs: `logs/` directory in container volume
- Post log: `logs/generated_posts.jsonl`
- Errors: `logs/errors.jsonl`
- Analytics: `logs/analytics.json`
- Retry queue: `logs/retry_queue.json`
- Health endpoint: `GET /health` (use for uptime monitoring)

## Scaling
- **Horizontal**: Add load balancer, run multiple containers behind it
- **Vertical**: Increase container resources (2GB RAM recommended for APScheduler + FastAPI)
- **Database**: Migrate from file-based to PostgreSQL for concurrent access
- **Content**: Add more subject files to `content/` directory — zero code changes needed

## Backup & Recovery
- `logs/` directory contains all state — back it up regularly
- To reset: delete `logs/*.json` and `logs/*.jsonl` files
- Restart-safe: scheduler saves/recovers pause state automatically
- Content library is read-only code — no backup needed

## Emergency Procedures
1. **Bot not posting**: Check `GET /health` → `scheduler_running` and `posting_paused`
2. **Content errors**: Check `logs/errors.jsonl`
3. **Retry queue**: Failed posts auto-retry up to 3 times (1min, 5min, 15min delays)
4. **Corrupted content**: `_library_fallback()` serves raw library items
5. **Restart**: Container auto-restarts with `--restart unless-stopped`
