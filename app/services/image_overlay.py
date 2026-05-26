"""Dynamic overlay generation for medical images: labels, arrows, highlights, callouts."""
from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

from app.config import get_settings
from app.models import ImageAsset, ImageCardRequest, OverlayElement

logger = logging.getLogger(__name__)

_FONT_CACHE: dict[str, ImageFont.FreeTypeFont] = {}

_TELEGRAM_CARD_WIDTH = 1080
_TELEGRAM_CARD_HEIGHT = 1500
_HEADER_H = 80
_FOOTER_H = 60

_SUBJECT_COLORS: dict[str, str] = {
    "anatomy": "#E74C3C", "physiology": "#2ECC71", "biochemistry": "#3498DB",
    "pathology": "#9B59B6", "pharmacology": "#1ABC9C", "microbiology": "#F39C12",
    "forensic_medicine": "#95A5A6", "community_medicine": "#27AE60",
    "general_medicine": "#2980B9", "general_surgery": "#E67E22",
    "obstetrics_gynecology": "#E91E63", "pediatrics": "#00BCD4",
    "ophthalmology": "#3F51B5", "ent": "#FF5722", "orthopedics": "#795548",
    "dermatology": "#FF9800", "psychiatry": "#607D8B", "radiology": "#455A64",
    "anesthesiology": "#8BC34A",
}


class ImageOverlayEngine:
    def __init__(self) -> None:
        settings = get_settings()
        self._fonts_dir = Path("/usr/share/fonts/truetype")
        self._overlays_dir = settings.assets_images_dir / "overlays"
        self._overlays_dir.mkdir(parents=True, exist_ok=True)

    def _get_font(self, size: int = 24) -> ImageFont.FreeTypeFont:
        key = f"regular_{size}"
        if key in _FONT_CACHE:
            return _FONT_CACHE[key]
        paths = [
            self._fonts_dir / "dejavu" / "DejaVuSans.ttf",
            self._fonts_dir / "liberation" / "LiberationSans-Regular.ttf",
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
        ]
        font_path = None
        for p in paths:
            if p.exists():
                font_path = p
                break
        if not font_path:
            try:
                _FONT_CACHE[key] = ImageFont.load_default()
                return _FONT_CACHE[key]
            except Exception:
                raise
        try:
            _FONT_CACHE[key] = ImageFont.truetype(str(font_path), size)
        except Exception:
            _FONT_CACHE[key] = ImageFont.load_default()
        return _FONT_CACHE[key]

    def _get_bold_font(self, size: int = 28) -> ImageFont.FreeTypeFont:
        key = f"bold_{size}"
        if key in _FONT_CACHE:
            return _FONT_CACHE[key]
        paths = [
            self._fonts_dir / "dejavu" / "DejaVuSans-Bold.ttf",
            Path("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
        ]
        font_path = None
        for p in paths:
            if p.exists():
                font_path = p
                break
        if not font_path:
            return self._get_font(size)
        try:
            _FONT_CACHE[key] = ImageFont.truetype(str(font_path), size)
        except Exception:
            _FONT_CACHE[key] = self._get_font(size)
        return _FONT_CACHE[key]

    def apply_overlays(self, img: Image.Image, overlays: list[OverlayElement]) -> Image.Image:
        """Apply overlay elements (labels, arrows, highlights) to an image."""
        draw = ImageDraw.Draw(img, "RGBA")
        for element in overlays:
            try:
                self._apply_element(draw, img, element)
            except Exception as exc:
                logger.debug("Overlay element failed: %s", exc)
        return img

    def _apply_element(self, draw: ImageDraw.Draw, img: Image.Image, el: OverlayElement) -> None:
        if el.element_type == "label":
            self._draw_label(draw, el, img)
        elif el.element_type == "arrow":
            self._draw_arrow(draw, el, img)
        elif el.element_type == "highlight":
            self._draw_highlight(draw, el, img)
        elif el.element_type == "border":
            self._draw_border(draw, el, img)
        elif el.element_type == "callout":
            self._draw_callout(draw, el, img)

    def _draw_label(self, draw: ImageDraw.Draw, el: OverlayElement, img: Image.Image) -> None:
        font = self._get_font(el.font_size)
        bbox = draw.textbbox((0, 0), el.text, font=font)
        tw = bbox[2] - bbox[0]
        th = bbox[3] - bbox[1]
        px = int(el.x * img.width) if el.x <= 1 else int(el.x)
        py = int(el.y * img.height) if el.y <= 1 else int(el.y)
        padding = 4
        draw.rectangle(
            [px - padding, py - padding, px + tw + padding, py + th + padding],
            fill=(0, 0, 0, 180),
        )
        draw.text((px, py), el.text, fill=el.color if el.color else "#FFFFFF", font=font)

    def _draw_arrow(self, draw: ImageDraw.Draw, el: OverlayElement, img: Image.Image) -> None:
        cx = int(el.x * img.width) if el.x <= 1 else int(el.x)
        cy = int(el.y * img.height) if el.y <= 1 else int(el.y)
        arrow_len = 40
        direction = el.arrow_direction or "auto"
        if direction == "up":
            start = (cx, cy + arrow_len)
            end = (cx, cy)
        elif direction == "down":
            start = (cx, cy - arrow_len)
            end = (cx, cy)
        elif direction == "left":
            start = (cx + arrow_len, cy)
            end = (cx, cy)
        elif direction == "right":
            start = (cx - arrow_len, cy)
            end = (cx, cy)
        else:
            start = (cx, cy + arrow_len)
            end = (cx, cy)
        draw.line([start, end], fill=el.color if el.color else "#FF0000", width=3)
        draw.polygon([
            (end[0], end[1] - 8),
            (end[0] - 5, end[1] + 2),
            (end[0] + 5, end[1] + 2),
        ], fill=el.color if el.color else "#FF0000")

    def _draw_highlight(self, draw: ImageDraw.Draw, el: OverlayElement, img: Image.Image) -> None:
        cx = int(el.x * img.width) if el.x <= 1 else int(el.x)
        cy = int(el.y * img.height) if el.y <= 1 else int(el.y)
        r = 40
        overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
        overlay_draw = ImageDraw.Draw(overlay)
        overlay_draw.ellipse(
            [cx - r, cy - r, cx + r, cy + r],
            fill=(255, 255, 0, 60),
            outline=(255, 200, 0, 180),
            width=3,
        )
        img.paste(overlay, (0, 0), overlay)

    def _draw_border(self, draw: ImageDraw.Draw, el: OverlayElement, img: Image.Image) -> None:
        color = el.color if el.color else "#0F3460"
        width = int(el.font_size * 0.5) or 4
        for i in range(width):
            draw.rectangle([i, i, img.width - 1 - i, img.height - 1 - i], outline=color)

    def _draw_callout(self, draw: ImageDraw.Draw, el: OverlayElement, img: Image.Image) -> None:
        font = self._get_font(el.font_size)
        lines = el.text.split("\n")
        line_h = el.font_size + 6
        total_h = len(lines) * line_h + 20
        margin = 20
        y_pos = img.height - total_h - margin
        draw.rectangle(
            [margin, y_pos, img.width - margin, y_pos + total_h],
            fill=(0, 0, 0, 200),
        )
        for i, line in enumerate(lines):
            draw.text(
                (margin + 10, y_pos + 10 + i * line_h),
                line,
                fill=el.color if el.color else "#FFFFFF",
                font=font,
            )

    def create_educational_card(
        self,
        asset: ImageAsset,
        request: ImageCardRequest,
    ) -> Optional[Path]:
        """Composite the base image with overlays into a Telegram-ready educational card."""
        try:
            src_path = get_settings().assets_images_dir / asset.file_path
            if not src_path.exists():
                logger.warning("Asset file not found: %s", src_path)
                return None
            img = Image.open(src_path).convert("RGBA")
            img = self._resize_to_card(img)
            img = self.apply_overlays(img, request.overlays)
            img = self._add_header_footer(img, request)
            out_path = get_settings().generated_dir / f"card_{asset.asset_id}_{request.template_id}.png"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            final = img.convert("RGB")
            final.save(str(out_path), "PNG", optimize=True)
            logger.info("Educational card saved: %s", out_path)
            return out_path
        except Exception as exc:
            logger.error("Failed to create educational card: %s", exc)
            return None

    def _resize_to_card(self, img: Image.Image) -> Image.Image:
        target_ratio = _TELEGRAM_CARD_WIDTH / _TELEGRAM_CARD_HEIGHT
        current_ratio = img.width / img.height
        if abs(current_ratio - target_ratio) < 0.05:
            return img.resize((_TELEGRAM_CARD_WIDTH, _TELEGRAM_CARD_HEIGHT), Image.LANCZOS)
        if current_ratio > target_ratio:
            new_w = int(img.height * target_ratio)
            offset = (img.width - new_w) // 2
            img = img.crop((offset, 0, offset + new_w, img.height))
        else:
            new_h = int(img.width / target_ratio)
            offset = (img.height - new_h) // 2
            img = img.crop((0, offset, img.width, offset + new_h))
        return img.resize((_TELEGRAM_CARD_WIDTH, _TELEGRAM_CARD_HEIGHT), Image.LANCZOS)

    def _add_header_footer(self, img: Image.Image, request: ImageCardRequest) -> Image.Image:
        draw = ImageDraw.Draw(img)
        if request.show_subject_badge or request.show_format_badge:
            overlay = Image.new("RGBA", img.size, (0, 0, 0, 0))
            odraw = ImageDraw.Draw(overlay)
            subject_color = _SUBJECT_COLORS.get(
                request.content.subject.value if request.content.subject else "general",
                "#0F3460",
            )
            if request.show_subject_badge and request.content.subject:
                subj_name = request.content.subject.value.replace("_", " ").title()
                odraw.rectangle([0, 0, 300, _HEADER_H], fill=(0, 15, 54, 200))
                font = self._get_bold_font(22)
                odraw.text((20, 25), subj_name, fill="#FFFFFF", font=font)
                odraw.rectangle([0, _HEADER_H - 3, 300, _HEADER_H], fill=subject_color)
            if request.show_format_badge:
                fmt_name = request.content.content_format.value.replace("_", " ").upper()
                fw = 260
                fx = img.width - fw - 10
                odraw.rectangle([fx, 0, fx + fw, _HEADER_H], fill=(0, 15, 54, 200))
                font = self._get_bold_font(18)
                odraw.text((fx + 10, 28), fmt_name, fill="#E0E0E0", font=font)
            img = Image.alpha_composite(img, overlay)
        return img
