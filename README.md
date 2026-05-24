# MedicoHelp AI Auto Poster

Production-ready Python system that generates educational content for all 19 undergraduate MBBS subjects with AI, creates branded PNG posters with Pillow, and auto-posts them to a Telegram channel.

## Features

- AI generation for all 19 MBBS subjects: Anatomy, Physiology, Biochemistry, Pathology, Pharmacology, Microbiology, Forensic Medicine, Community Medicine, General Medicine, General Surgery, Obstetrics & Gynecology, Pediatrics, Ophthalmology, ENT, Orthopedics, Dermatology, Psychiatry, Radiology, and Anesthesiology
- Supports MCQs, image-based questions, concise notes, clinical cases, rapid revision posts, and practical/viva content
- Image-based learning cards include a schematic visual panel, labels, question stem, options, answer/explanation data, and a reusable image prompt
- Content is original. It can follow the broad polish of medical exam-prep apps, but it must not copy proprietary questions, screenshots, tables, or explanations.
- Premium scheduler mix: image-based questions, PYQ-style concepts, quick revision facts, resident survival tips, and exam-news alerts
- Branded poster generation using Pillow
- Telegram channel posting with retry handling
- FastAPI endpoints for health checks, manual generation, and manual posting
- APScheduler interval-based auto-posting
- JSONL logs for generated posts and failures
- Docker, Docker Compose, systemd, and Google Cloud VM deployment support

## Folder Structure

```text
app/
  main.py
  config.py
  models.py
  logging_config.py
  services/
prompts/
assets/
generated/
logs/
Dockerfile
docker-compose.yml
medicohelp-ai-auto-poster.service
requirements.txt
.env.example
```

## Local Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

On Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

Open:

- API docs: `http://localhost:8000/docs`
- Health check: `http://localhost:8000/health`

## Environment Variables

```env
OPENAI_API_KEY=
GEMINI_API_KEY=
AI_PROVIDER=openai
AI_MODEL=gpt-4o-mini
GENERATE_REALISTIC_IMAGES=false
OPENAI_IMAGE_MODEL=gpt-image-1
OPENAI_IMAGE_SIZE=1024x1024
OPENAI_IMAGE_QUALITY=medium
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
POST_INTERVAL_HOURS=6
TIMEZONE=Asia/Kolkata
RUN_SCHEDULER=true
ALLOW_MOCK_AI=true
NEWS_LOOKBACK_DAYS=14
NEWS_MAX_ITEMS=6
```

Use `AI_PROVIDER=openai` with `OPENAI_API_KEY`, or `AI_PROVIDER=gemini` with `GEMINI_API_KEY`.

Set `GENERATE_REALISTIC_IMAGES=true` to generate an original realistic medical visual before composing the final teaching card. This requires `OPENAI_API_KEY`; if image generation fails or is disabled, the app falls back to a locally generated schematic visual.

## API Usage

Generate a poster without Telegram posting:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"subject":"pathology","content_format":"image_based_question","publish_to_telegram":false}'
```

For image-based teaching content, prefer:

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"subject":"radiology","content_format":"image_based_question","publish_to_telegram":false}'
```

Image-based cards are designed to include:

- A realistic or schematic visual area
- 4 labelled visual clues
- A 6-8 line exam-style question stem
- 4 options
- Correct answer
- One proper explanation paragraph
- High-yield takeaway data in the generated JSON

The app also validates image-based content before rendering. It rejects weak outputs when the visual description is vague, labels are missing, the stem is too short, options are incomplete, the explanation is thin, or the image findings do not directly support the answer.

## Premium Content Mix

The scheduler rotates through a deliberate exam-prep mix:

- Image-based question
- Image-based question
- PYQ-style concept
- Quick revision fact
- Resident survival tip
- NEET PG or INI-CET news alert

PYQ-style posts teach recurring previous-year patterns without copying proprietary question-bank wording or inventing a specific year.

## NEET PG, INI-CET, and Residency Updates

The app can sweep recent web/news feed results for exam updates and turn them into sourced Telegram cards. Exam-news content is treated as an alert, not as an official instruction; always verify actionable details on official portals such as NBEMS/NBE, AIIMS Exams, MCC, or the relevant counselling authority.

Fetch latest items:

```bash
curl "http://localhost:8000/news/latest?topic=neet_pg"
curl "http://localhost:8000/news/latest?topic=inicet"
```

Generate a sourced news card:

```bash
curl -X POST http://localhost:8000/news/generate \
  -H "Content-Type: application/json" \
  -d '{"topic":"neet_pg","publish_to_telegram":false}'
```

Generate a resident survival tip card:

```bash
curl -X POST http://localhost:8000/news/generate \
  -H "Content-Type: application/json" \
  -d '{"topic":"residency","publish_to_telegram":false}'
```

CLI:

```bash
python -m app.cli --news-topic neet_pg
python -m app.cli --news-topic inicet --post
python -m app.cli --news-topic residency
```

Generate and post immediately:

```bash
curl -X POST http://localhost:8000/post-now \
  -H "Content-Type: application/json" \
  -d '{"subject":"general_medicine","content_format":"mcq"}'
```

List supported subjects and formats:

```bash
curl http://localhost:8000/subjects
curl http://localhost:8000/content-formats
```

Available subjects:

- `anatomy`
- `physiology`
- `biochemistry`
- `pathology`
- `pharmacology`
- `microbiology`
- `forensic_medicine`
- `community_medicine`
- `general_medicine`
- `general_surgery`
- `obstetrics_gynecology`
- `pediatrics`
- `ophthalmology`
- `ent`
- `orthopedics`
- `dermatology`
- `psychiatry`
- `radiology`
- `anesthesiology`

Available content formats:

- `mcq`
- `image_based_question`
- `concise_notes`
- `clinical_case`
- `rapid_revision`
- `practical_viva`
- `exam_news_update`
- `residency_survival_tip`
- `pyq_concept`

You can also generate from the command line:

```bash
python -m app.cli --subject pathology --format image_based_question
python -m app.cli --subject pediatrics --format mcq --post
python -m app.cli --all-subjects --format concise_notes
python -m app.cli --all-subjects --format image_based_question
```

Generate one item for all 19 subjects:

```bash
curl -X POST http://localhost:8000/generate-all-subjects \
  -H "Content-Type: application/json" \
  -d '{"content_format":"rapid_revision","publish_to_telegram":false}'
```

Run the smoke test:

```bash
pytest
```

## Telegram Bot Setup

1. Open Telegram and message `@BotFather`.
2. Run `/newbot`, choose a bot name and username, and copy the bot token.
3. Add the bot as an admin to your Telegram channel.
4. Set `TELEGRAM_BOT_TOKEN` in `.env`.
5. Set `TELEGRAM_CHAT_ID`.
   - For public channels, use `@YourChannelUsername`.
   - For private channels, forward a channel message to a bot/user info tool or call Telegram `getUpdates` after sending a test message.
6. Test with `/post-now` from the API docs.

## Docker Deployment

```bash
cp .env.example .env
docker compose up --build -d
docker compose logs -f
```

## Google Cloud VM Setup

Create an Ubuntu VM, then run:

```bash
sudo apt update
sudo apt install -y git python3.11 python3.11-venv python3-pip
sudo useradd --system --create-home --shell /bin/bash medicohelp
sudo mkdir -p /opt/medicohelp-ai-auto-poster
sudo chown medicohelp:medicohelp /opt/medicohelp-ai-auto-poster
```

Clone and install:

```bash
sudo -u medicohelp git clone https://github.com/YOUR_USERNAME/medicohelp-ai-auto-poster.git /opt/medicohelp-ai-auto-poster
cd /opt/medicohelp-ai-auto-poster
sudo -u medicohelp python3.11 -m venv .venv
sudo -u medicohelp .venv/bin/pip install -r requirements.txt
sudo -u medicohelp cp .env.example .env
sudo -u medicohelp nano .env
```

Install systemd service:

```bash
sudo cp medicohelp-ai-auto-poster.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable medicohelp-ai-auto-poster
sudo systemctl start medicohelp-ai-auto-poster
sudo systemctl status medicohelp-ai-auto-poster
```

Allow traffic if you want public API access:

```bash
gcloud compute firewall-rules create allow-medicohelp-api \
  --allow tcp:8000 \
  --source-ranges 0.0.0.0/0 \
  --target-tags medicohelp-api
```

For production, put Nginx and HTTPS in front of FastAPI, or keep the API private and let only the scheduler run.

## GitHub Push Instructions

```bash
git init
git add .
git commit -m "Initial MedicoHelp AI Auto Poster"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/medicohelp-ai-auto-poster.git
git push -u origin main
```

## Logs

- Generated post history: `logs/generated_posts.jsonl`
- Application logs: `logs/app.log`
- Failure records: `logs/errors.jsonl`
- Generated posters: `generated/*.png`

## Medical Safety Note

This project is for educational content generation. Review AI-generated medical content before relying on it in high-stakes contexts, and avoid patient-specific advice.
