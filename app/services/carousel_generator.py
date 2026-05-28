"""Pillow-based Instagram 1080x1080 carousel slide generator."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

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
# Slide-type accent colours
C_PROBLEM = "#B03A2E"   # warning-red header for 'THE PROBLEM' slide
C_INSIGHT = "#0D7377"   # deep teal header for 'KEY INSIGHT' slide
C_AMBER = "#E67E22"     # amber strip accent

# Font sizes
FS_COVER_TITLE = 76
FS_COVER_SUBTITLE = 36
FS_CONTENT_HEADER = 38
FS_CONTENT_BODY = 31
FS_CTA_TITLE = 58
FS_FOOTER = 26
FS_ICON_EMOJI = 54
FS_BADGE = 22
FS_SWIPE = 28

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
        """Combine caption text with formatted hashtags."""
        tag_str = " ".join(f"#{t.lstrip('#')}" for t in self.hashtags)
        if tag_str:
            return f"{self.caption}\n\n{tag_str}"
        return self.caption

    def to_slides(self) -> list[SlideSpec]:
        """Build the ordered list of SlideSpec objects."""
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

        slides.append(SlideSpec(slide_type="cta", title="Follow for more\nEye Health Tips"))

        return slides


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------


class CarouselGenerator:
    """Generates Instagram carousel slides as 1080x1080 JPEG files."""

    def __init__(self) -> None:
        self._font_cache: dict[tuple[str, int], ImageFont.FreeTypeFont] = {}
        self._output_dir: Path | None = None

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate_slides(self, spec: CarouselSpec) -> list[Path]:
        """Render every slide defined by *spec* to disk. Returns a list of Paths."""
        out_dir = self._ensure_output_dir()
        slide_specs = spec.to_slides()
        paths: list[Path] = []

        for i, ss in enumerate(slide_specs):
            if ss.slide_type == "cover":
                img = self._draw_cover(ss)
            elif ss.slide_type == "content":
                img = self._draw_content(ss)
            else:
                img = self._draw_cta(ss)

            filename = f"slide_{i:02d}_{ss.slide_type}.jpg"
            dest = out_dir / filename
            img.convert("RGB").save(dest, format="JPEG", quality=95)
            logger.debug("Saved slide %d -> %s", i, dest)
            paths.append(dest)

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
    # Slide drawers
    # ------------------------------------------------------------------

    def _draw_cover(self, spec: SlideSpec) -> Image.Image:
        """Dark navy cover — scroll-stopping layout with accent polygons."""
        img = Image.new("RGBA", (SLIDE_SIZE, SLIDE_SIZE), self._hex_to_rgb(C_NAVY) + (255,))
        draw = ImageDraw.Draw(img, "RGBA")

        teal_semi = self._hex_to_rgb(C_TEAL) + (90,)
        teal_faint = self._hex_to_rgb(C_TEAL) + (45,)

        # Large triangle top-right
        draw.polygon(
            [(SLIDE_SIZE - 20, 0), (SLIDE_SIZE, 0), (SLIDE_SIZE, 340), (SLIDE_SIZE - 280, 80)],
            fill=teal_semi,
        )
        draw.polygon(
            [(SLIDE_SIZE - 170, 0), (SLIDE_SIZE - 20, 0), (SLIDE_SIZE - 280, 190)],
            fill=teal_faint,
        )
        # Diamond bottom-left
        draw.polygon(
            [(0, SLIDE_SIZE - 280), (190, SLIDE_SIZE - 80), (80, SLIDE_SIZE), (0, SLIDE_SIZE)],
            fill=teal_semi,
        )
        draw.polygon(
            [(0, SLIDE_SIZE - 130), (110, SLIDE_SIZE - 40), (0, SLIDE_SIZE - 20)],
            fill=teal_faint,
        )

        # --- Teal top accent strip ---
        draw.rectangle([(0, 0), (SLIDE_SIZE, 8)], fill=self._hex_to_rgb(C_TEAL))

        # --- Title with number accent ---
        title_font = self._bold(FS_COVER_TITLE)
        title_text = spec.title.upper()
        title_lines = self._wrap_text(draw, title_text, title_font, SLIDE_SIZE - MARGIN * 2)

        line_h = FS_COVER_TITLE + 14
        block_h = len(title_lines) * line_h
        sub_h = FS_COVER_SUBTITLE + 24 if spec.subtitle else 0
        total_h = block_h + sub_h + 30
        y = (SLIDE_SIZE - total_h) // 2 - 30

        for line in title_lines:
            self._draw_line_with_number_accent(draw, line, title_font, y)
            y += line_h

        # --- Subtitle ---
        if spec.subtitle:
            y += 14
            sub_font = self._font(FS_COVER_SUBTITLE)
            sub_lines = self._wrap_text(draw, spec.subtitle, sub_font, SLIDE_SIZE - MARGIN * 3)
            for line in sub_lines:
                bbox = draw.textbbox((0, 0), line, font=sub_font)
                w = bbox[2] - bbox[0]
                x = (SLIDE_SIZE - w) // 2
                draw.text((x, y), line, font=sub_font, fill=(*self._hex_to_rgb(C_WHITE), 210))
                y += FS_COVER_SUBTITLE + 10

        # --- Teal underline accent ---
        accent_y = min(y + 18, SLIDE_SIZE - 100)
        accent_w = 180
        draw.rectangle(
            [(SLIDE_SIZE // 2 - accent_w // 2, accent_y),
             (SLIDE_SIZE // 2 + accent_w // 2, accent_y + 5)],
            fill=self._hex_to_rgb(C_TEAL),
        )

        # --- Branding bottom-left ---
        brand_font = self._font(FS_FOOTER)
        brand_text = "Dr. Akshay Thakur  |  MS Ophthalmology"
        draw.text(
            (MARGIN, SLIDE_SIZE - 52),
            brand_text,
            font=brand_font,
            fill=(*self._hex_to_rgb(C_WHITE), 180),
        )

        # --- SWIPE indicator bottom-right ---
        swipe_font = self._bold(FS_SWIPE)
        swipe_text = "SWIPE →"
        bbox = draw.textbbox((0, 0), swipe_text, font=swipe_font)
        sw = bbox[2] - bbox[0]
        draw.text(
            (SLIDE_SIZE - sw - MARGIN, SLIDE_SIZE - 52),
            swipe_text,
            font=swipe_font,
            fill=self._hex_to_rgb(C_TEAL),
        )

        return img

    def _draw_content(self, spec: SlideSpec) -> Image.Image:
        """Content slide — visual treatment varies by slide position."""
        img = Image.new("RGBA", (SLIDE_SIZE, SLIDE_SIZE), self._hex_to_rgb(C_LIGHT_BG) + (255,))
        draw = ImageDraw.Draw(img, "RGBA")

        HEADER_H = 128
        FOOTER_H = 56
        ICON_RADIUS = 58
        STRIP_H = 8  # coloured top strip

        is_problem = spec.slide_num == 1
        is_insight = spec.slide_num == 2

        # --- Coloured top strip ---
        if is_problem:
            strip_color = C_AMBER
        elif is_insight:
            strip_color = C_GOLD
        else:
            strip_color = C_TEAL
        draw.rectangle([(0, 0), (SLIDE_SIZE, STRIP_H)], fill=self._hex_to_rgb(strip_color))

        # --- Header bar ---
        if is_problem:
            header_bg = C_PROBLEM
        elif is_insight:
            header_bg = C_INSIGHT
        else:
            header_bg = C_NAVY
        draw.rectangle(
            [(0, STRIP_H), (SLIDE_SIZE, STRIP_H + HEADER_H)],
            fill=self._hex_to_rgb(header_bg),
        )

        header_font = self._bold(FS_CONTENT_HEADER)
        header_text = spec.title
        header_lines = self._wrap_text(
            draw, header_text, header_font, SLIDE_SIZE - MARGIN * 2
        )
        hy = STRIP_H + (HEADER_H - len(header_lines) * (FS_CONTENT_HEADER + 4)) // 2
        for line in header_lines:
            bbox = draw.textbbox((0, 0), line, font=header_font)
            lw = bbox[2] - bbox[0]
            draw.text(
                ((SLIDE_SIZE - lw) // 2, hy),
                line,
                font=header_font,
                fill=self._hex_to_rgb(C_WHITE),
            )
            hy += FS_CONTENT_HEADER + 4

        # --- "SAVE \U0001f4be" badge on key insight slide ---
        if is_insight:
            badge_text = "SAVE \U0001f4be"
            badge_font = self._bold(FS_BADGE)
            bb = draw.textbbox((0, 0), badge_text, font=badge_font)
            bw, bh = bb[2] - bb[0], bb[3] - bb[1]
            pad_x, pad_y = 16, 8
            badge_x = SLIDE_SIZE - bw - pad_x * 2 - 12
            badge_y = STRIP_H + HEADER_H + 14
            draw.rounded_rectangle(
                [(badge_x - pad_x, badge_y - pad_y),
                 (badge_x + bw + pad_x, badge_y + bh + pad_y)],
                radius=12,
                fill=self._hex_to_rgb(C_GOLD),
            )
            draw.text(
                (badge_x, badge_y),
                badge_text,
                font=badge_font,
                fill=self._hex_to_rgb(C_DARK_TEXT),
                embedded_color=True,
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
            footer_text,
            font=footer_font,
            fill=self._hex_to_rgb(C_WHITE),
        )

        # --- Body layout bounds ---
        body_top = STRIP_H + HEADER_H + MARGIN
        dot_area_top = SLIDE_SIZE - FOOTER_H - 44
        body_bottom = dot_area_top - 10
        body_h = body_bottom - body_top

        # --- Icon circle (colour matches slide type) ---
        if is_problem:
            icon_color = C_PROBLEM
        elif is_insight:
            icon_color = C_GOLD
        else:
            icon_color = C_TEAL
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
                spec.icon_emoji,
                font=emoji_font,
                fill=self._hex_to_rgb(C_WHITE),
                embedded_color=True,
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
        line_h = FS_CONTENT_BODY + 12
        total_text_h = len(body_lines) * line_h
        ty = icon_cy - total_text_h // 2
        for line in body_lines:
            draw.text((text_x, ty), line, font=body_font, fill=self._hex_to_rgb(C_DARK_TEXT))
            ty += line_h

        # --- Progress dots ---
        if spec.total > 0:
            self._draw_progress_dots(draw, spec.slide_num, spec.total)

        return img

    def _draw_cta(self, spec: SlideSpec) -> Image.Image:
        """Dark CTA/outro slide — follow + save prompt."""
        img = Image.new("RGBA", (SLIDE_SIZE, SLIDE_SIZE), self._hex_to_rgb(C_NAVY) + (255,))
        draw = ImageDraw.Draw(img, "RGBA")

        teal_semi = self._hex_to_rgb(C_TEAL) + (60,)
        draw.polygon([(SLIDE_SIZE - 200, 0), (SLIDE_SIZE, 0), (SLIDE_SIZE, 200)], fill=teal_semi)
        draw.polygon([(0, SLIDE_SIZE - 200), (200, SLIDE_SIZE), (0, SLIDE_SIZE)], fill=teal_semi)
        # Gold top strip
        draw.rectangle([(0, 0), (SLIDE_SIZE, 8)], fill=self._hex_to_rgb(C_GOLD))

        center_x = SLIDE_SIZE // 2
        eye_font = self._bold(110)
        eye_emoji = "\U0001f441"
        text_start_y = SLIDE_SIZE // 2 - 200
        try:
            ebbox = draw.textbbox((0, 0), eye_emoji, font=eye_font)
            ew, eh = ebbox[2] - ebbox[0], ebbox[3] - ebbox[1]
            eye_y = SLIDE_SIZE // 2 - 270
            draw.text(
                (center_x - ew // 2, eye_y),
                eye_emoji,
                font=eye_font,
                fill=self._hex_to_rgb(C_WHITE),
                embedded_color=True,
            )
            text_start_y = eye_y + eh + 28
        except Exception:
            pass

        # CTA text
        cta_font = self._bold(FS_CTA_TITLE)
        cta_lines = spec.title.split("\n") if "\n" in spec.title else [spec.title]
        ty = text_start_y
        for line in cta_lines:
            bbox = draw.textbbox((0, 0), line, font=cta_font)
            lw = bbox[2] - bbox[0]
            draw.text((center_x - lw // 2, ty), line, font=cta_font,
                      fill=self._hex_to_rgb(C_WHITE))
            ty += FS_CTA_TITLE + 14

        # Teal divider
        ty += 18
        div_w = 200
        draw.rectangle(
            [(center_x - div_w // 2, ty), (center_x + div_w // 2, ty + 4)],
            fill=self._hex_to_rgb(C_TEAL),
        )
        ty += 30

        # Doctor name in gold
        doc_font = self._font(FS_CONTENT_HEADER)
        doc_text = "Dr. Akshay Thakur"
        bbox = draw.textbbox((0, 0), doc_text, font=doc_font)
        draw.text(
            (center_x - (bbox[2] - bbox[0]) // 2, ty),
            doc_text,
            font=doc_font,
            fill=self._hex_to_rgb(C_GOLD),
        )
        ty += FS_CONTENT_HEADER + 10

        # Designation
        desig_font = self._font(FS_FOOTER)
        desig_text = "MS Ophthalmologist"
        bbox = draw.textbbox((0, 0), desig_text, font=desig_font)
        draw.text(
            (center_x - (bbox[2] - bbox[0]) // 2, ty),
            desig_text,
            font=desig_font,
            fill=self._hex_to_rgb(C_WHITE),
        )
        ty += FS_FOOTER + 28

        # Save + follow nudge
        nudge_font = self._font(FS_BADGE + 2)
        nudge_text = "\U0001f4be Save  •  \U0001f501 Share  •  \U0001f4ac Comment"
        bbox = draw.textbbox((0, 0), nudge_text, font=nudge_font)
        draw.text(
            (center_x - (bbox[2] - bbox[0]) // 2, ty),
            nudge_text,
            font=nudge_font,
            fill=(*self._hex_to_rgb(C_WHITE), 160),
            embedded_color=True,
        )

        return img

    # ------------------------------------------------------------------
    # Drawing helpers
    # ------------------------------------------------------------------

    def _draw_line_with_number_accent(self,
                                      draw: ImageDraw.ImageDraw,
                                      line: str,
                                      font: ImageFont.FreeTypeFont,
                                      y: int) -> None:
        """Draw a title line, colouring any leading digit/number in teal."""
        bbox = draw.textbbox((0, 0), line, font=font)
        total_w = bbox[2] - bbox[0]
        x = (SLIDE_SIZE - total_w) // 2

        # Check if line starts with a number
        match = re.match(r"^(\d+)(.*)", line)
        if match:
            num_part = match.group(1)
            rest_part = match.group(2)
            num_bbox = draw.textbbox((0, 0), num_part, font=font)
            num_w = num_bbox[2] - num_bbox[0]
            draw.text((x, y), num_part, font=font, fill=self._hex_to_rgb(C_TEAL))
            draw.text((x + num_w, y), rest_part, font=font, fill=self._hex_to_rgb(C_WHITE))
        else:
            draw.text((x, y), line, font=font, fill=self._hex_to_rgb(C_WHITE))

    def _draw_progress_dots(
        self, draw: ImageDraw.ImageDraw, current: int, total: int
    ) -> None:
        """Small progress indicator dots near the slide bottom."""
        DOT_R = 7
        DOT_GAP = 22
        total_w = total * (DOT_R * 2) + (total - 1) * (DOT_GAP - DOT_R * 2)
        start_x = (SLIDE_SIZE - total_w) // 2
        cy = 1038
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
                    outline=white_rgb,
                    fill=navy_rgb,
                    width=2,
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
        draw: ImageDraw.ImageDraw,
        text: str,
        font: ImageFont.FreeTypeFont,
        max_width: int,
    ) -> list[str]:
        """Break *text* into lines that fit within *max_width* pixels."""
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
        """Convert a CSS hex colour string to an (R, G, B) tuple."""
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
