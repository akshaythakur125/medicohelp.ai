"""Emergency recovery: restart-safe retry queue for failed posts."""
import asyncio
import json
import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

_MAX_RETRIES = 3
_RETRY_DELAYS = [60, 300, 900]  # 1 min, 5 min, 15 min


class RetryQueue:
    def __init__(self, logs_dir: Path) -> None:
        self._path = logs_dir / "retry_queue.json"
        self._entries: list[dict[str, Any]] = self._load()
        self._processing = False

    def enqueue(self, task: dict[str, Any]) -> None:
        task["retry_count"] = task.get("retry_count", 0) + 1
        task["last_attempt"] = datetime.now(tz=timezone.utc).isoformat()
        task["id"] = task.get("id", f"post_{datetime.now(tz=timezone.utc).timestamp()}")
        self._entries.append(task)
        self._trim()
        self._save()
        logger.info("Enqueued retry task %s (attempt %d)", task["id"], task["retry_count"])

    def pending(self) -> list[dict[str, Any]]:
        return [e for e in self._entries if not self._is_expired(e)]

    def _is_expired(self, entry: dict) -> bool:
        return entry.get("retry_count", 0) >= _MAX_RETRIES

    async def process(self, execute_fn):
        if self._processing:
            return
        self._processing = True
        try:
            pending = self.pending()
            for entry in pending:
                delay = _RETRY_DELAYS[min(entry["retry_count"] - 1, len(_RETRY_DELAYS) - 1)]
                logger.info("Retrying task %s in %ds (attempt %d/%d)", entry["id"], delay, entry["retry_count"], _MAX_RETRIES)
                await asyncio.sleep(delay)
                try:
                    await execute_fn(entry)
                    self._entries.remove(entry)
                    logger.info("Retry succeeded for task %s", entry["id"])
                except Exception as exc:
                    entry["retry_count"] += 1
                    entry["last_error"] = str(exc)
                    entry["last_attempt"] = datetime.now(tz=timezone.utc).isoformat()
                    logger.warning("Retry failed for task %s: %s", entry["id"], exc)
                    if self._is_expired(entry):
                        logger.error("Task %s exhausted retries, removing", entry["id"])
                        self._entries.remove(entry)
                self._save()
        finally:
            self._processing = False

    def _trim(self) -> None:
        self._entries = self._entries[-100:]

    def _load(self) -> list[dict[str, Any]]:
        if self._path.exists():
            try:
                return json.loads(self._path.read_text(encoding="utf-8"))
            except Exception as exc:
                logger.warning("Could not read retry queue: %s", exc)
        return []

    def _save(self) -> None:
        try:
            self._path.parent.mkdir(parents=True, exist_ok=True)
            self._path.write_text(
                json.dumps(self._entries, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as exc:
            logger.warning("Could not save retry queue: %s", exc)
