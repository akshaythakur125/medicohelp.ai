import logging
import textwrap
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from PIL import Image, ImageDraw, ImageFont

from app.config import Settings
from app.models import GeneratedContent

logger = logging.getLogger(__name__)


class PosterGenerator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def create(self, content: GeneratedContent, visual_image_path: Path | None = None) -> Path:
        width, height = 1080, 1500
        image = Image.new("RGB", (width, height), "#f7fbff")
        draw = ImageDraw.Draw(image)

        self._draw_background(draw, width, height)
        title_font = self._font(56, bold=True)
        body_font = self._font(46, bold=False)
        brand_font = self._font(42, bold=True)
        small_font = self._font(30, bold=False)
        micro_font = self._font(26, bold=False)

        draw.rounded_rectangle((56, 52, 1024, 168), radius=28, fill="#063b5b")
        draw.text((92, 84), "MedicoHelp", fill="#ffffff", font=brand_font)
        draw.text((742, 94), "MBBS AI", fill="#9ee7d7", font=small_font)

        draw.text((78, 238), self._fit_title(content.title), fill="#063b5b", font=title_font)

        draw.text(
            (92, 335),
            f"{self._content_scope(content)} | {self._label(content.content_format.value)}",
            fill="#07615a",
            font=micro_font,
        )

        if content.content_format.value == "image_based_question" or content.visual_description:
            self._draw_image_based_card(image, draw, content, small_font, micro_font, visual_image_path)
        else:
            y = 410
            for line in self._wrap(content.poster_text, width=30, max_lines=6):
                draw.text((92, y), line, fill="#102a43", font=body_font)
                y += 68

            draw.rounded_rectangle((86, 830, 994, 938), radius=24, fill="#dff7f2", outline="#00a88f", width=3)
            draw.text((122, 858), "Learn. Revise. Remember.", fill="#07615a", font=self._font(38, bold=True))

        footer = "MBBS Curriculum | NEET PG | Medical Education"
        draw.text((92, 1420), footer, fill="#5b7083", font=small_font)

        filename = (
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_"
            f"{self._filename_scope(content)}_{content.content_format.value}_{uuid4().hex[:8]}.png"
        )
        path = self.settings.generated_dir / filename
        image.save(path, "PNG", optimize=True)
        logger.info("Poster generated: %s", path)
        return path

    def _draw_background(self, draw: ImageDraw.ImageDraw, width: int, height: int) -> None:
        draw.rectangle((0, 0, width, height), fill="#f7fbff")
        draw.polygon([(0, 0), (1080, 0), (1080, 260), (0, 410)], fill="#e9f7ff")
        draw.ellipse((750, 1040, 1220, 1510), fill="#c8f1e8")
        draw.ellipse((-180, 1100, 240, 1520), fill="#d7ecff")
        draw.line((80, 210, 1000, 210), fill="#00a88f", width=6)

    def _draw_image_based_card(
        self,
        canvas: Image.Image,
        draw: ImageDraw.ImageDraw,
        content: GeneratedContent,
        small_font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
        micro_font: ImageFont.FreeTypeFont | ImageFont.ImageFont,
        visual_image_path: Path | None,
    ) -> None:
        visual_box = (78, 390, 1002, 705)
        draw.rounded_rectangle(visual_box, radius=26, fill="#ffffff", outline="#90cdf4", width=4)
        draw.text((106, 410), "IMAGE-BASED CLUE", fill="#0b4f6c", font=self._font(30, bold=True))
        if visual_image_path and visual_image_path.exists():
            self._paste_realistic_visual(canvas, visual_image_path, visual_box)
        else:
            self._draw_subject_visual(draw, content, visual_box)

        labels = content.visual_labels or content.image_based_data
        x_positions = [118, 360, 600, 790]
        for index, label in enumerate(labels[:4]):
            x = x_positions[index]
            y = 652 if index % 2 == 0 else 600
            draw.rounded_rectangle((x, y, x + 178, y + 42), radius=14, fill="#e6fffb", outline="#00a88f", width=2)
            draw.text((x + 12, y + 10), self._fit_line(label, 16), fill="#07615a", font=self._font(20, bold=True))

        question = content.question or content.poster_text
        y = 732
        question_font = self._font(26, bold=False)
        for line in self._wrap(question.replace("\n", " "), width=72, max_lines=8):
            draw.text((92, y), line, fill="#102a43", font=question_font)
            y += 32

        option_font = self._font(25, bold=False)
        options = content.options[:4] if content.options else ["A. Correct concept", "B. Distractor", "C. Mimic", "D. Trap"]
        option_boxes = [(92, 1004), (552, 1004), (92, 1062), (552, 1062)]
        for option, (x, y) in zip(options, option_boxes):
            draw.rounded_rectangle((x, y, x + 408, y + 46), radius=14, fill="#f7fbff", outline="#b6d8ef", width=2)
            draw.text((x + 14, y + 11), self._fit_line(option, 34), fill="#102a43", font=option_font)

        answer = content.correct_answer or "Answer: identify the key visual clue."
        draw.rounded_rectangle((86, 1135, 994, 1198), radius=18, fill="#063b5b")
        draw.text((112, 1152), self._fit_line(answer, 62), fill="#ffffff", font=self._font(25, bold=True))

        explanation = content.explanation or content.high_yield_takeaway or "Identify the visual clue before reading options."
        y = 1212
        for line in self._wrap(explanation, width=76, max_lines=6):
            draw.text((92, y), line, fill="#102a43", font=self._font(22, bold=False))
            y += 28

    def _paste_realistic_visual(
        self,
        canvas: Image.Image,
        visual_image_path: Path,
        box: tuple[int, int, int, int],
    ) -> None:
        left, top, right, bottom = box
        image = Image.open(visual_image_path).convert("RGB")
        target_w = right - left - 44
        target_h = bottom - top - 76
        image.thumbnail((target_w, target_h))
        x = left + (right - left - image.width) // 2
        y = top + 56 + (target_h - image.height) // 2
        canvas.paste(image, (x, y))

    def _draw_subject_visual(
        self,
        draw: ImageDraw.ImageDraw,
        content: GeneratedContent,
        box: tuple[int, int, int, int],
    ) -> None:
        left, top, right, bottom = box
        subject = content.subject.value if content.subject else content.news_topic.value if content.news_topic else "medical"
        cx = (left + right) // 2
        cy = (top + bottom) // 2 + 18

        if subject in {"general_medicine", "physiology", "anesthesiology"}:
            points = [(left + 90, cy), (left + 170, cy - 70), (left + 250, cy + 15), (left + 330, cy - 95)]
            points += [(left + 410, cy + 5), (left + 490, cy - 55), (left + 570, cy + 10), (left + 650, cy - 80), (left + 740, cy)]
            draw.line(points, fill="#0b4f6c", width=8, joint="curve")
            draw.line((left + 75, cy + 70, right - 70, cy + 70), fill="#8aa6b7", width=3)
        elif subject in {"pathology", "microbiology", "dermatology"}:
            colors = ["#ef476f", "#ffd166", "#06d6a0", "#118ab2"]
            for index in range(26):
                x = left + 120 + (index * 67) % 720
                y = top + 78 + (index * 41) % 150
                draw.ellipse((x, y, x + 42, y + 42), fill=colors[index % len(colors)], outline="#ffffff", width=3)
            draw.ellipse((cx - 92, cy - 58, cx + 92, cy + 58), outline="#7b2cbf", width=8)
        elif subject in {"radiology", "general_surgery", "orthopedics"}:
            draw.rounded_rectangle((left + 140, top + 58, right - 140, bottom - 42), radius=18, fill="#1d3557")
            draw.arc((left + 260, top + 100, right - 260, bottom + 120), 190, 350, fill="#f1faee", width=10)
            draw.polygon([(cx - 80, cy - 45), (cx + 80, cy - 45), (cx, cy + 70)], outline="#e63946", fill=None)
            draw.line((cx, cy - 92, cx, cy + 92), fill="#a8dadc", width=5)
        elif subject in {"anatomy", "ent", "ophthalmology"}:
            draw.ellipse((cx - 160, cy - 86, cx + 160, cy + 86), outline="#0b4f6c", width=8)
            draw.ellipse((cx - 62, cy - 62, cx + 62, cy + 62), fill="#9ee7d7", outline="#063b5b", width=5)
            draw.ellipse((cx - 20, cy - 20, cx + 20, cy + 20), fill="#ef476f")
            draw.line((cx - 250, cy, cx + 250, cy), fill="#8aa6b7", width=4)
        else:
            draw.rounded_rectangle((left + 170, top + 72, right - 170, bottom - 58), radius=30, fill="#e9f7ff")
            draw.line((cx - 190, cy + 70, cx - 70, cy - 40, cx + 40, cy + 20, cx + 190, cy - 70), fill="#0b4f6c", width=10)
            draw.ellipse((cx - 54, cy - 54, cx + 54, cy + 54), fill="#9ee7d7", outline="#00a88f", width=5)

    def _font(self, size: int, bold: bool) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
        candidates = [
            "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
            "arialbd.ttf" if bold else "arial.ttf",
        ]
        for candidate in candidates:
            try:
                return ImageFont.truetype(candidate, size=size)
            except OSError:
                continue
        return ImageFont.load_default()

    def _wrap(self, text: str, width: int, max_lines: int) -> list[str]:
        lines = textwrap.wrap(text, width=width)
        if len(lines) > max_lines:
            lines = lines[:max_lines]
            lines[-1] = lines[-1].rstrip(".") + "..."
        return lines

    def _fit_title(self, title: str) -> str:
        return title if len(title) <= 36 else title[:33].rstrip() + "..."

    def _fit_line(self, text: str, max_chars: int) -> str:
        return text if len(text) <= max_chars else text[: max_chars - 3].rstrip() + "..."

    def _label(self, value: str) -> str:
        label = value.replace("_", " ").title()
        return label.replace("Pyq", "PYQ").replace("Inicet", "INI-CET").replace("Neet Pg", "NEET PG")

    def _content_scope(self, content: GeneratedContent) -> str:
        if content.subject:
            return self._label(content.subject.value)
        if content.news_topic:
            return self._label(content.news_topic.value)
        return "Medical Education"

    def _filename_scope(self, content: GeneratedContent) -> str:
        if content.subject:
            return content.subject.value
        if content.news_topic:
            return content.news_topic.value
        return "medical"
