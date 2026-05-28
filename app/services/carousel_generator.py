"""Pillow-based Instagram 1080x1080 carousel slide generator.

Viral-optimised visuals: scroll-stopping cover, problem/insight slides,
branded CTA with engagement line.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont, ImageOps

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Layout constants
# ---------------------------------------------------------------------------
SLIDE_SIZE = 1080
MARGIN = 72

# Colour palette
C_NAVY = "#16213E"
C_TEAL = "#1E9AB0"
C_WHITE = "#FFFFFF"
C_LIGHT_BG = "#F4F9FB"
C_DARK_TEXT = "#1A1A2E"
C_MID_TEXT = "#4A5568"
C_GOLD = "#F2C94C"
C_AMBER = "#F39C12"
C_RED = "#B03A2E"
C_TEAL_DEEP = "#0D7377"
C_GOLD_LIGHT = "#FDEBD0"

# Font sizes
FS_COVER_TITLE = 72
FS_COVER_SUBTITLE = 36
FS_CONTENT_HEADER = 40
FS_CONTENT_BODY = 32
FS_CTA_TITLE = 60
FS_FOOTER = 26
FS_ICON_EMOJI = 54
FS_SWIPE = 28
FS_SAVE_BADGE = 22

# DejaVu font paths (present on Debian/Ubuntu)
_DEJAVU_DIR = Path("/usr/share/fonts/truetype/dejavu")
_FONT_REGULAR = _DEJAVU_DIR / "DejaVuSans.ttf"
_FONT_BOLD = _DEJAVU_DIR / "DejaVuSans-Bold.ttf"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------


@dataclass
class SlideSpec:
    slide_type: str  # "cover" | "content" | "cta"
    title: str
    subtitle: str = ""
    body_text: str = ""
    icon_emoji: str = "\U0001f441"
    slide_num: int = 0  # 1-based index of this content slide
    total: int = 0      # total number of content slides (excl. cover & cta)


@dataclass
class CarouselSpec:
    cover_title: str
    cover_subtitle: str
    points: list[dict] = field(default_factory=list)
    caption: str = ""
    hashtags: list[str] = field(default_factory=list)

    def full_caption(self) -> str:
        tag_str = " ".join(f"#{t.lstrip('#')}" for t in self.hashtags)
        if tag_str:
            return f"{self.caption}\n\n{tag_str}"
        return self.caption

    def to_slides(self) -> list[SlideSpec]:
        slides: list[SlideSpec] = []

        slides.append(
            SlideSpec(
                slide_type="cover",
                title=self.cover_title,
                subtitle=self.cover_subtitle,
            )
        )

        total_content = len(self.points)
        for idx, point in enumerate(self.points, start=1):
            slides.append(
                SlideSpec(
                    slide_type="content",
                    title=point.get("label", f"Point {idx}"),
                    body_text=point.get("body", ""),
                    icon_emoji=point.get("icon_emoji", "\U0001f441"),
                    slide_num=idx,
                    total=total_content,
                )
            )

        return slides


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------


class CarouselGenerator:
    """Generates Instagram carousel slides as 1080x1080 JPEG files.

    Viral-optimised slide variants:
      - Cover: scroll-stopping hook, "SWIPE →" indicator, branding
      - Slide 1 (THE PROBLEM): amber strip, dark red header, red icon
      - Slide 2 (THE KEY INSIGHT): gold strip, deep teal header, gold icon, SAVE badge
      - Slides 3+ : normal teal style (no "Sign X:" prefix)
      - Final (photo): doctor's personal photo with branded bottom bar
    """

    def __init__(self, doctor_photo_path: str | None = None) -> None:
        self._font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}
        self._output_dir: Path | None = None
        self._doctor_photo: Path | None = Path(doctor_photo_path) if doctor_photo_path else None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate_slides(self, spec: CarouselSpec) -> list[Path]:
        """Render every slide defined by *spec* to disk. Returns a list of Paths.

        When ``doctor_photo_path`` was provided at construction and the file
        exists, a final photo slide is appended after all content slides.
        """
        out_dir = self._ensure_output_dir()
        slide_specs = spec.to_slides()
        paths: list[Path] = []

        for i, ss in enumerate(slide_specs):
            if ss.slide_type == "cover":
                img = self._draw_cover(ss)
            elif ss.slide_type == "content":
                img = self._draw_content(ss)

            filename = f"slide_{i:02d}_{ss.slide_type}.jpg"
            dest = out_dir / filename
            img.convert("RGB").save(dest, format="JPEG", quality=92)
            logger.debug("Saved slide %d -> %s", i, dest)
            paths.append(dest)

        # --- Doctor photo slide (replaces the old text CTA) ---
        if self._doctor_photo and self._doctor_photo.exists():
            try:
                photo_idx = len(slide_specs)
                photo_img = ImageOps.fit(
                    Image.open(self._doctor_photo).convert("RGBA"),
                    (SLIDE_SIZE, SLIDE_SIZE),
                    method=Image.LANCZOS,
                )

                # Add 70px dark navy bottom bar with branding
                bar_h = 70
                bar_img = Image.new("RGBA", (SLIDE_SIZE, bar_h), self._hex_to_rgb(C_NAVY) + (255,))
                photo_img.paste(bar_img, (0, SLIDE_SIZE - bar_h), bar_img)

                draw = ImageDraw.Draw(photo_img)
                footer_font = self._font(FS_FOOTER)
                footer_text = "Dr. Akshay Thakur  |  MS Ophthalmology"
                bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
                fw, fh = bbox[2] - bbox[0], bbox[3] - bbox[1]
                draw.text(
                    ((SLIDE_SIZE - fw) // 2, SLIDE_SIZE - bar_h + (bar_h - fh) // 2),
                    footer_text, font=footer_font, fill=self._hex_to_rgb(C_WHITE),
                )

                dest = out_dir / f"slide_{photo_idx:02d}_photo.jpg"
                photo_img.convert("RGB").save(dest, format="JPEG", quality=92)
                logger.info("Saved doctor photo slide -> %s", dest)
                paths.append(dest)
            except Exception as exc:
                logger.warning("Failed to render doctor photo slide: %s", exc)

        logger.info("Generated %d slides in %s", len(paths), out_dir)
        return paths

    @staticmethod
    def cleanup_slides(paths: list[Path]) -> None:
        """Delete slide JPEG files after they have been posted to Instagram."""
        for path in paths:
            try:
                path.unlink(missing_ok=True)
                logger.debug("Deleted slide file: %s", path.name)
            except Exception as exc:
                logger.warning("Failed to delete slide %s: %s", path.name, exc)

    # ------------------------------------------------------------------
    # Cover slide
    # ------------------------------------------------------------------

    def _draw_cover(self, spec: SlideSpec) -> Image.Image:
        """Dark navy cover with teal accents, "SWIPE →" indicator, and branding."""
        img = Image.new("RGBA", (SLIDE_SIZE, SLIDE_SIZE), self._hex_to_rgb(C_NAVY) + (255,))
        draw = ImageDraw.Draw(img, "RGBA")

        # --- Thin teal top strip ---
        draw.rectangle([(0, 0), (SLIDE_SIZE, 8)], fill=self._hex_to_rgb(C_TEAL))

        # --- Decorative polygons ---
        teal_semi = self._hex_to_rgb(C_TEAL) + (90,)
        draw.polygon(
            [(SLIDE_SIZE - 20, 0), (SLIDE_SIZE, 0), (SLIDE_SIZE, 320), (SLIDE_SIZE - 260, 80)],
            fill=teal_semi,
        )
        draw.polygon(
            [(SLIDE_SIZE - 160, 0), (SLIDE_SIZE - 20, 0), (SLIDE_SIZE - 260, 180)],
            fill=self._hex_to_rgb(C_TEAL) + (50,),
        )
        draw.polygon(
            [(0, SLIDE_SIZE - 260), (180, SLIDE_SIZE - 80), (80, SLIDE_SIZE), (0, SLIDE_SIZE)],
            fill=teal_semi,
        )
        draw.polygon(
            [(0, SLIDE_SIZE - 120), (100, SLIDE_SIZE - 40), (0, SLIDE_SIZE - 20)],
            fill=self._hex_to_rgb(C_TEAL) + (50,),
        )

        # --- Title (leading number in teal if present) ---
        title_font = self._bold(FS_COVER_TITLE)
        title_text = spec.title.upper()
        title_lines = self._wrap_text(draw, title_text, title_font, SLIDE_SIZE - MARGIN * 2)

        line_h = FS_COVER_TITLE + 12
        block_h = len(title_lines) * line_h
        sub_h = FS_COVER_SUBTITLE + 20 if spec.subtitle else 0
        total_h = block_h + sub_h
        y = (SLIDE_SIZE - total_h) // 2 - 20

        for line in title_lines:
            bbox = draw.textbbox((0, 0), line, font=title_font)
            w = bbox[2] - bbox[0]
            x = (SLIDE_SIZE - w) // 2

            # Check if first word is a number (e.g., "5", "70%") — render in teal
            first_word = line.split()[0] if line.split() else ""
            if any(c.isdigit() for c in first_word):
                first_bbox = draw.textbbox((0, 0), first_word, font=title_font)
                fw = first_bbox[2] - first_bbox[0]
                draw.text((x, y), first_word, font=title_font, fill=self._hex_to_rgb(C_TEAL))
                rest = line[len(first_word):]
                draw.text((x + fw, y), rest, font=title_font, fill=self._hex_to_rgb(C_WHITE))
            else:
                draw.text((x, y), line, font=title_font, fill=self._hex_to_rgb(C_WHITE))
            y += line_h

        # --- Subtitle ---
        if spec.subtitle:
            y += 10
            sub_font = self._font(FS_COVER_SUBTITLE)
            sub_lines = self._wrap_text(draw, spec.subtitle, sub_font, SLIDE_SIZE - MARGIN * 2)
            for line in sub_lines:
                bbox = draw.textbbox((0, 0), line, font=sub_font)
                w = bbox[2] - bbox[0]
                x = (SLIDE_SIZE - w) // 2
                draw.text((x, y), line, font=sub_font, fill=self._hex_to_rgb(C_WHITE))
                y += FS_COVER_SUBTITLE + 8

        # --- Teal underline accent ---
        accent_y = min(y + 20, SLIDE_SIZE - 120)
        accent_w = 160
        draw.rectangle(
            [(SLIDE_SIZE // 2 - accent_w // 2, accent_y),
             (SLIDE_SIZE // 2 + accent_w // 2, accent_y + 5)],
            fill=self._hex_to_rgb(C_TEAL),
        )

        # --- "SWIPE →" bottom-right ---
        swipe_font = self._bold(FS_SWIPE)
        swipe_text = "SWIPE \u2192"
        swipe_bbox = draw.textbbox((0, 0), swipe_text, font=swipe_font)
        sw, sh = swipe_bbox[2] - swipe_bbox[0], swipe_bbox[3] - swipe_bbox[1]
        draw.text(
            (SLIDE_SIZE - MARGIN - sw, SLIDE_SIZE - 40 - sh),
            swipe_text, font=swipe_font, fill=self._hex_to_rgb(C_TEAL),
        )

        # --- Branding bottom-left ---
        brand_font = self._font(FS_FOOTER)
        brand_text = "Dr. Akshay Thakur | MS Ophthalmology"
        draw.text(
            (MARGIN, SLIDE_SIZE - 40 - FS_FOOTER),
            brand_text, font=brand_font, fill=self._hex_to_rgb(C_TEAL),
        )

        return img

    # ------------------------------------------------------------------
    # Content slide
    # ------------------------------------------------------------------

    def _draw_content(self, spec: SlideSpec) -> Image.Image:
        """Content slide — styling varies by slide_num.

        slide_num=1 (THE PROBLEM) : amber top strip, dark red header, red icon
        slide_num=2 (KEY INSIGHT) : gold top strip, deep teal header, gold icon, SAVE badge
        slide_num=3+              : default teal header
        """
        img = Image.new("RGBA", (SLIDE_SIZE, SLIDE_SIZE), self._hex_to_rgb(C_LIGHT_BG) + (255,))
        draw = ImageDraw.Draw(img, "RGBA")

        HEADER_H = 120
        FOOTER_H = 55
        ICON_RADIUS = 60

        # --- Determine slide variant ---
        is_problem = spec.slide_num == 1
        is_insight = spec.slide_num == 2

        header_color = C_NAVY
        icon_color = C_TEAL
        top_strip_color = None
        has_save_badge = False

        if is_problem:
            top_strip_color = C_AMBER
            header_color = C_RED
            icon_color = C_RED
        elif is_insight:
            top_strip_color = C_GOLD
            header_color = C_TEAL_DEEP
            icon_color = C_GOLD
            has_save_badge = True

        # --- Top strip (thin accent line) ---
        if top_strip_color:
            draw.rectangle([(0, 0), (SLIDE_SIZE, 8)], fill=self._hex_to_rgb(top_strip_color))

        # --- Header bar ---
        draw.rectangle([(0, 0), (SLIDE_SIZE, HEADER_H)], fill=self._hex_to_rgb(header_color))
        header_font = self._bold(FS_CONTENT_HEADER)
        header_text = spec.title  # No "Sign X:" prefix
        header_lines = self._wrap_text(draw, header_text, header_font, SLIDE_SIZE - MARGIN * 2)
        hy = (HEADER_H - len(header_lines) * (FS_CONTENT_HEADER + 4)) // 2
        for line in header_lines:
            bbox = draw.textbbox((0, 0), line, font=header_font)
            lw = bbox[2] - bbox[0]
            draw.text(
                ((SLIDE_SIZE - lw) // 2, hy), line,
                font=header_font, fill=self._hex_to_rgb(C_WHITE),
            )
            hy += FS_CONTENT_HEADER + 4

        # --- "SAVE 💾" badge (slide 3 / KEY INSIGHT only) ---
        if has_save_badge:
            badge_font = self._bold(FS_SAVE_BADGE)
            badge_text = "SAVE \U0001f4be"
            badge_pad_x = 14
            badge_pad_y = 6
            badge_bbox = draw.textbbox((0, 0), badge_text, font=badge_font)
            bw = badge_bbox[2] - badge_bbox[0] + badge_pad_x * 2
            bh = badge_bbox[3] - badge_bbox[1] + badge_pad_y * 2
            badge_x = SLIDE_SIZE - MARGIN - bw
            badge_y = 16
            # Rounded rectangle background
            draw.rounded_rectangle(
                [(badge_x, badge_y), (badge_x + bw, badge_y + bh)],
                radius=14, fill=self._hex_to_rgb(C_GOLD),
            )
            draw.text(
                (badge_x + badge_pad_x, badge_y + badge_pad_y),
                badge_text, font=badge_font, fill=self._hex_to_rgb(C_DARK_TEXT),
            )

        # --- Branding footer ---
        draw.rectangle(
            [(0, SLIDE_SIZE - FOOTER_H), (SLIDE_SIZE, SLIDE_SIZE)],
            fill=self._hex_to_rgb(C_DARK_TEXT),
        )
        footer_font = self._font(FS_FOOTER)
        footer_text = "Dr. Akshay Thakur  |  MS Ophthalmology"
        bbox = draw.textbbox((0, 0), footer_text, font=footer_font)
        fw, fh = bbox[2] - bbox[0], bbox[3] - bbox[1]
        draw.text(
            ((SLIDE_SIZE - fw) // 2, SLIDE_SIZE - FOOTER_H + (FOOTER_H - fh) // 2),
            footer_text, font=footer_font, fill=self._hex_to_rgb(C_WHITE),
        )

        # --- Body layout bounds ---
        body_top = HEADER_H + MARGIN
        dot_area_top = SLIDE_SIZE - FOOTER_H - 40
        body_bottom = dot_area_top - 10
        body_h = body_bottom - body_top

        # --- Icon circle ---
        icon_cx = MARGIN + ICON_RADIUS
        icon_cy = body_top + body_h // 2
        draw.ellipse(
            [(icon_cx - ICON_RADIUS, icon_cy - ICON_RADIUS),
             (icon_cx + ICON_RADIUS, icon_cy + ICON_RADIUS)],
            fill=self._hex_to_rgb(icon_color),
        )
        emoji_font = self._bold(FS_ICON_EMOJI)
        try:
            ebbox = draw.textbbox((0, 0), spec.icon_emoji, font=emoji_font)
            ew, eh = ebbox[2] - ebbox[0], ebbox[3] - ebbox[1]
            draw.text(
                (icon_cx - ew // 2, icon_cy - eh // 2),
                spec.icon_emoji, font=emoji_font,
                fill=self._hex_to_rgb(C_WHITE), embedded_color=True,
            )
        except Exception:
            draw.text(
                (icon_cx - 10, icon_cy - 14), "+",
                font=self._bold(36), fill=self._hex_to_rgb(C_WHITE),
            )

        # --- Body text ---
        text_x = icon_cx + ICON_RADIUS + MARGIN
        text_max_w = SLIDE_SIZE - text_x - MARGIN
        body_font = self._font(FS_CONTENT_BODY)
        body_lines = self._wrap_text(draw, spec.body_text, body_font, text_max_w)
        line_h = FS_CONTENT_BODY + 10
        total_text_h = len(body_lines) * line_h
        ty = icon_cy - total_text_h // 2
        for line in body_lines:
            draw.text((text_x, ty), line, font=body_font, fill=self._hex_to_rgb(C_DARK_TEXT))
            ty += line_h

        # --- Progress dots ---
        if spec.total > 0:
            self._draw_progress_dots(draw, spec.slide_num, spec.total)

        return img

    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------

    def _draw_progress_dots(
        self, draw: ImageDraw.ImageDraw, current: int, total: int
    ) -> None:
        DOT_R = 7
        DOT_GAP = 22
        total_w = total * (DOT_R * 2) + (total - 1) * (DOT_GAP - DOT_R * 2)
        start_x = (SLIDE_SIZE - total_w) // 2
        cy = 1040
        teal_rgb = self._hex_to_rgb(C_TEAL)
        navy_rgb = self._hex_to_rgb(C_NAVY)
        white_rgb = self._hex_to_rgb(C_WHITE)

        for i in range(1, total + 1):
            cx = start_x + (i - 1) * DOT_GAP + DOT_R
            if i == current:
                draw.ellipse(
                    [(cx - DOT_R, cy - DOT_R), (cx + DOT_R, cy + DOT_R)],
                    fill=teal_rgb,
                )
            else:
                draw.ellipse(
                    [(cx - DOT_R, cy - DOT_R), (cx + DOT_R, cy + DOT_R)],
                    outline=white_rgb, fill=navy_rgb, width=2,
                )

    # ------------------------------------------------------------------
    # Font helpers
    # ------------------------------------------------------------------

    def _font(self, size: int) -> ImageFont.FreeTypeFont:
        key = ("regular", size)
        if key not in self._font_cache:
            try:
                self._font_cache[key] = ImageFont.truetype(str(_FONT_REGULAR), size)
            except OSError:
                logger.warning("DejaVuSans.ttf not found, falling back to default font")
                self._font_cache[key] = ImageFont.load_default()
        return self._font_cache[key]

    def _bold(self, size: int) -> ImageFont.FreeTypeFont:
        key = ("bold", size)
        if key not in self._font_cache:
            try:
                self._font_cache[key] = ImageFont.truetype(str(_FONT_BOLD), size)
            except OSError:
                logger.warning("DejaVuSans-Bold.ttf not found, falling back to default font")
                self._font_cache[key] = ImageFont.load_default()
        return self._font_cache[key]

    # ------------------------------------------------------------------
    # Text / colour utilities
    # ------------------------------------------------------------------

    @staticmethod
    def _wrap_text(
        draw: ImageDraw.ImageDraw, text: str, font: ImageFont.FreeTypeFont, max_width: int,
    ) -> list[str]:
        words = text.split()
        lines: list[str] = []
        current = ""
        for word in words:
            candidate = f"{current} {word}".strip()
            bbox = draw.textbbox((0, 0), candidate, font=font)
            if bbox[2] - bbox[0] <= max_width:
                current = candidate
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines or [""]

    @staticmethod
    def _hex_to_rgb(h: str) -> tuple[int, int, int]:
        h = h.lstrip("#")
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)

    # ------------------------------------------------------------------
    # Directory management
    # ------------------------------------------------------------------

    def _ensure_output_dir(self) -> Path:
        if self._output_dir is None:
            from app.config import get_settings
            self._output_dir = get_settings().generated_dir / "instagram"
        self._output_dir.mkdir(parents=True, exist_ok=True)
        return self._output_dir
