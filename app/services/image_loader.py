"""Curated medical image asset loader with metadata indexing and hash-based dedup."""
from __future__ import annotations

import hashlib
import json
import logging
import random
from pathlib import Path
from typing import Optional

from app.config import get_settings
from app.models import ImageAsset, Subject

logger = logging.getLogger(__name__)

_SUBJECT_DIR_MAP: dict[str, str] = {s.value: s.value for s in Subject}
_SUBJECT_DIR_MAP["general"] = "general"


class ImageLoader:
    def __init__(self, images_dir: Optional[Path] = None, index_path: Optional[Path] = None) -> None:
        settings = get_settings()
        self._images_dir = images_dir or settings.assets_images_dir
        self._index_path = index_path or settings.image_index_path
        self._index: dict[str, dict] = {}
        self._assets: list[ImageAsset] = []
        self._loaded = False

    def load_index(self, force: bool = False) -> list[ImageAsset]:
        if self._loaded and not force:
            return self._assets
        if self._index_path.exists():
            try:
                data = json.loads(self._index_path.read_text(encoding="utf-8"))
                self._assets = [ImageAsset(**a) for a in data.get("assets", [])]
                self._index = data.get("index", {})
                self._loaded = True
                logger.info("Loaded %d image assets from index", len(self._assets))
                return self._assets
            except Exception as exc:
                logger.warning("Failed to load image index, rescanning: %s", exc)
        return self.scan(force=True)

    def scan(self, force: bool = False) -> list[ImageAsset]:
        if self._loaded and not force:
            return self._assets
        self._assets = []
        self._index = {}
        known_hashes: set[str] = set()

        for subj_dir in sorted(self._images_dir.iterdir()):
            if not subj_dir.is_dir() or subj_dir.name in ("templates", "overlays", "general"):
                continue
            subj_name = subj_dir.name
            for img_path in sorted(subj_dir.rglob("*")):
                if img_path.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
                    continue
                if img_path.name.startswith("."):
                    continue
                try:
                    data = img_path.read_bytes()
                    md5 = hashlib.md5(data).hexdigest()
                    if md5 in known_hashes:
                        logger.debug("Duplicate skipped: %s (hash %s)", img_path, md5)
                        continue
                    known_hashes.add(md5)
                    asset = ImageAsset(
                        asset_id=f"{subj_name}_{img_path.stem}_{md5[:8]}",
                        file_path=str(img_path.relative_to(self._images_dir)),
                        md5_hash=md5,
                        subject=subj_name,
                        topic=_infer_topics(img_path),
                        format=_infer_formats(img_path),
                        tags=_infer_tags(img_path),
                        caption="",
                        width=0,
                        height=0,
                        file_size_bytes=len(data),
                    )
                    self._assets.append(asset)
                    self._index.setdefault(subj_name, []).append(asset.asset_id)
                    for t in asset.topic:
                        self._index.setdefault(f"topic:{t}", []).append(asset.asset_id)
                    for f in asset.format:
                        self._index.setdefault(f"format:{f}", []).append(asset.asset_id)
                except Exception as exc:
                    logger.debug("Skipping %s: %s", img_path, exc)

        self._loaded = True
        self._save_index()
        logger.info("Scanned %d image assets from %s", len(self._assets), self._images_dir)
        return self._assets

    def _save_index(self) -> None:
        try:
            self._index_path.parent.mkdir(parents=True, exist_ok=True)
            self._index_path.write_text(
                json.dumps({
                    "version": 1,
                    "asset_count": len(self._assets),
                    "index": self._index,
                    "assets": [a.model_dump() for a in self._assets],
                }, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as exc:
            logger.warning("Failed to save image index: %s", exc)

    def by_subject(self, subject: Subject | str) -> list[ImageAsset]:
        subj_key = subject.value if isinstance(subject, Subject) else subject
        asset_ids = self._index.get(subj_key, [])
        return [a for a in self._assets if a.asset_id in asset_ids]

    def by_topic(self, topic: str) -> list[ImageAsset]:
        asset_ids = self._index.get(f"topic:{topic.lower().replace(' ', '_')}", [])
        return [a for a in self._assets if a.asset_id in asset_ids]

    def by_format(self, fmt: str) -> list[ImageAsset]:
        asset_ids = self._index.get(f"format:{fmt}", [])
        return [a for a in self._assets if a.asset_id in asset_ids]

    def by_subject_and_format(self, subject: Subject | str, fmt: str) -> list[ImageAsset]:
        subj_assets = self.by_subject(subject)
        return [a for a in subj_assets if fmt in a.format]

    def random(self, subject: Optional[Subject | str] = None, fmt: Optional[str] = None) -> Optional[ImageAsset]:
        pool = self._assets
        if subject:
            pool = self.by_subject(subject)
        if fmt:
            pool = [a for a in pool if fmt in a.format]
        return random.choice(pool) if pool else None

    def total(self) -> int:
        return len(self._assets)

    def subject_summary(self) -> dict[str, int]:
        summary: dict[str, int] = {}
        for a in self._assets:
            summary[a.subject] = summary.get(a.subject, 0) + 1
        return summary

    def absolute_path(self, asset: ImageAsset) -> Path:
        return self._images_dir / asset.file_path

    def clear_index(self) -> None:
        self._assets = []
        self._index = {}
        self._loaded = False
        if self._index_path.exists():
            self._index_path.unlink()


def _infer_topics(img_path: Path) -> list[str]:
    stem = img_path.stem.lower().replace("-", "_").replace(" ", "_")
    parts = stem.split("_")
    return [p for p in parts if len(p) > 2]


def _infer_formats(img_path: Path) -> list[str]:
    stem = img_path.stem.lower()
    known = {
        "mcq": "mcq", "ibq": "image_based_question", "notes": "concise_notes",
        "case": "clinical_case", "rapid": "rapid_revision", "viva": "practical_viva",
        "pyq": "pyq_concept", "flash": "flashcard", "tf": "true_false",
        "oneliner": "one_liner_recall", "memo": "mnemonic",
    }
    results = []
    for key, val in known.items():
        if key in stem:
            results.append(val)
    return results if results else ["rapid_revision"]


def _infer_tags(img_path: Path) -> list[str]:
    stem = img_path.stem.lower().replace("-", "_").replace(" ", "_")
    return [p for p in stem.split("_") if len(p) > 2 and not p.startswith("img")]
