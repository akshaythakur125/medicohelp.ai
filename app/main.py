import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException

from app.config import get_settings
from app.logging_config import configure_logging
from app.models import (
    ContentFormat,
    GenerateAllSubjectsRequest,
    GenerateRequest,
    GenerateResponse,
    HealthResponse,
    NewsRequest,
    NewsResponse,
    NewsTopic,
    Subject,
)
from app.services.orchestrator import PostOrchestrator
from app.services.scheduler import PostingScheduler

settings = get_settings()
configure_logging(settings)
logger = logging.getLogger(__name__)

orchestrator = PostOrchestrator(settings)
posting_scheduler = PostingScheduler(settings, orchestrator)


@asynccontextmanager
async def lifespan(_: FastAPI):
    if settings.run_scheduler:
        posting_scheduler.start()
    yield
    posting_scheduler.stop()


app = FastAPI(
    title=settings.project_name,
    version="1.0.0",
    description="AI-powered medical education poster generator and Telegram auto-poster.",
    lifespan=lifespan,
)


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    return HealthResponse(status="ok", scheduler_running=posting_scheduler.scheduler.running)


@app.post("/generate", response_model=GenerateResponse)
async def generate(request: GenerateRequest) -> GenerateResponse:
    try:
        return await orchestrator.generate_post(
            subject=request.subject,
            content_format=request.content_format,
            category=request.category,
            publish_to_telegram=request.publish_to_telegram,
        )
    except Exception as exc:
        logger.exception("Manual generation failed.")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/post-now", response_model=GenerateResponse)
async def post_now(request: GenerateRequest) -> GenerateResponse:
    try:
        return await orchestrator.generate_post(
            subject=request.subject,
            content_format=request.content_format,
            category=request.category,
            publish_to_telegram=True,
        )
    except Exception as exc:
        logger.exception("Manual Telegram posting failed.")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/generate-all-subjects", response_model=list[GenerateResponse])
async def generate_all_subjects(request: GenerateAllSubjectsRequest) -> list[GenerateResponse]:
    results: list[GenerateResponse] = []
    for subject in Subject:
        try:
            results.append(
                await orchestrator.generate_post(
                    subject=subject,
                    content_format=request.content_format,
                    publish_to_telegram=request.publish_to_telegram,
                )
            )
        except Exception as exc:
            logger.exception("Generation failed for subject %s.", subject.value)
            raise HTTPException(status_code=500, detail=f"{subject.value}: {exc}") from exc
    return results


@app.post("/planned-post", response_model=GenerateResponse)
async def planned_post(request: GenerateRequest) -> GenerateResponse:
    """Generate the next post from the 12-slot rotation."""
    try:
        return await orchestrator.generate_planned_post(
            publish_to_telegram=request.publish_to_telegram,
            subject_override=request.subject,
        )
    except Exception as exc:
        logger.exception("Planned post failed.")
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.post("/pause")
async def pause_posting() -> dict:
    orchestrator.pause()
    return {"status": "paused"}


@app.post("/resume")
async def resume_posting() -> dict:
    orchestrator.resume()
    return {"status": "resumed"}


@app.get("/pause-status")
async def pause_status() -> dict:
    return {"paused": orchestrator.paused}


@app.get("/stats")
async def engine_stats() -> dict:
    """SmartContentEngine: spaced-repetition send history and library coverage."""
    try:
        return orchestrator.get_engine_stats()
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc


@app.get("/subjects")
async def subjects() -> list[str]:
    return [subject.value for subject in Subject]


@app.get("/content-formats")
async def content_formats() -> list[str]:
    return [content_format.value for content_format in ContentFormat]


@app.get("/news/latest", response_model=NewsResponse)
async def latest_news(topic: NewsTopic = NewsTopic.neet_pg) -> NewsResponse:
    items = await orchestrator.fetch_latest_news(topic)
    return NewsResponse(items=items)


@app.post("/news/generate", response_model=NewsResponse)
async def generate_news(request: NewsRequest) -> NewsResponse:
    items = await orchestrator.fetch_latest_news(request.topic)
    generated_post = await orchestrator.generate_news_post(
        topic=request.topic,
        publish_to_telegram=request.publish_to_telegram,
    )
    return NewsResponse(items=items, generated_post=generated_post)
