"""Reusable educational card templates: flashcard, MCQ infographic, rapid revision."""
from __future__ import annotations

import logging
import random
from pathlib import Path
from typing import Optional

from PIL import Image, ImageDraw, ImageFont

from app.config import get_settings
from app.models import ContentFormat, GeneratedContent, ImageAsset, ImageCardRequest, OverlayElement
from app.services.image_loader import ImageLoader
from app.services.image_overlay import ImageOverlayEngine

logger = logging.getLogger(__name__)

_CARD_W = 1080
_CARD_H = 1500
_MARGIN = 60
_CONTENT_W = _CARD_W - 2 * _MARGIN
_TEXT_COLOR = "#1A1A2E"
_ACCENT = "#0F3460"
_BG = "#F8F9FA"
_WHITE = "#FFFFFF"

_SUBJECT_ACCENTS: dict[str, str] = {
    "anatomy": "#E74C3C", "physiology": "#2ECC71", "biochemistry": "#3498DB",
    "pathology": "#9B59B6", "pharmacology": "#1ABC9C", "microbiology": "#F39C12",
    "forensic_medicine": "#95A5A6", "community_medicine": "#27AE60",
    "general_medicine": "#2980B9", "general_surgery": "#E67E22",
    "obstetrics_gynecology": "#E91E63", "pediatrics": "#00BCD4",
    "ophthalmology": "#3F51B5", "ent": "#FF5722", "orthopedics": "#795548",
    "dermatology": "#FF9800", "psychiatry": "#607D8B", "radiology": "#455A64",
    "anesthesiology": "#8BC34A",
}


class VisualCardBuilder:
    def __init__(self) -> None:
        self._overlay = ImageOverlayEngine()
        self._loader = ImageLoader()

    def build_card(self, content: GeneratedContent) -> Optional[Path]:
        """Build the best card for the given content. Auto-selects template."""
        template_map = {
            ContentFormat.mcq: self._build_mcq_card,
            ContentFormat.image_based_question: self._build_image_mcq_card,
            ContentFormat.flashcard: self._build_flashcard_card,
            ContentFormat.rapid_revision: self._build_rapid_revision_card,
            ContentFormat.true_false: self._build_true_false_card,
            ContentFormat.one_liner_recall: self._build_one_liner_card,
            ContentFormat.mnemonic: self._build_mnemonic_card,
            ContentFormat.clinical_case: self._build_clinical_case_card,
            ContentFormat.concise_notes: self._build_notes_card,
        }
        builder = template_map.get(content.content_format, self._build_rapid_revision_card)
        return builder(content)

    # ── Template: Flashcard ────────────────────────────────────────────

    def _build_flashcard_card(self, content: GeneratedContent) -> Optional[Path]:
        img = self._create_base_card(content, "flashcard")
        draw = ImageDraw.Draw(img)
        font_question = self._overlay._get_bold_font(32)
        font_answer = self._overlay._get_font(24)

        q_y = 200
        self._draw_wrapped(draw, (content.question or content.title)[:200], font_question, q_y, _ACCENT)

        answer = content.correct_answer or content.high_yield_takeaway or ""
        if answer:
            a_y = q_y + 120
            self._draw_wrapped(draw, f"Answer:", self._overlay._get_bold_font(26), a_y, "#27AE60")
            self._draw_wrapped(draw, answer[:300], font_answer, a_y + 40, _TEXT_COLOR)

        expl = (content.explanation or "")[:400]
        if expl:
            e_y = _CARD_H - 350
            self._draw_wrapped(draw, expl, self._overlay._get_font(20), e_y, "#555555")

        return self._save_card(img, content, "flashcard")

    # ── Template: MCQ Infographic ──────────────────────────────────────

    def _build_mcq_card(self, content: GeneratedContent) -> Optional[Path]:
        img = self._create_base_card(content, "mcq")
        draw = ImageDraw.Draw(img)

        fq = self._overlay._get_bold_font(26)
        fo = self._overlay._get_font(22)

        q_y = 180
        self._draw_wrapped(draw, (content.question or content.title)[:300], fq, q_y, _ACCENT)

        opt_y = q_y + len((content.question or "")[:300]) // 55 * 30 + 60
        for opt in (content.options or [])[:4]:
            color = "#27AE60" if content.correct_answer and opt.startswith(content.correct_answer[0]) else _TEXT_COLOR
            self._draw_wrapped(draw, opt[:120], fo, opt_y, color)
            opt_y += 45

        if content.high_yield_takeaway:
            py = _CARD_H - 200
            draw.rectangle([_MARGIN, py - 10, _CARD_W - _MARGIN, py + 60], fill=(15, 52, 96, 30))
            self._draw_wrapped(draw, f"Key Point: {content.high_yield_takeaway[:150]}",
                              self._overlay._get_font(20), py + 5, "#0F3460")

        return self._save_card(img, content, "mcq")

    # ── Template: Image-Based MCQ ──────────────────────────────────────

    def _build_image_mcq_card(self, content: GeneratedContent) -> Optional[Path]:
        asset = self._pick_image(content)
        if not asset:
            return self._build_mcq_card(content)

        request = ImageCardRequest(
            content=content,
            template_id="image_mcq",
            overlays=[
                OverlayElement(element_type="border", color=_ACCENT, font_size=6),
            ],
            show_subject_badge=True,
            show_format_badge=True,
        )
        path = self._overlay.create_educational_card(asset, request)
        if not path:
            return self._build_mcq_card(content)

        img = Image.open(path).convert("RGBA")
        draw = ImageDraw.Draw(img)
        stem = (content.question or "")[:200]
        if stem:
            self._draw_wrapped(draw, stem, self._overlay._get_font(22), _CARD_H - 180, _TEXT_COLOR)
        return self._save_card(img, content, "image_mcq")

    # ── Template: Rapid Revision ───────────────────────────────────────

    def _build_rapid_revision_card(self, content: GeneratedContent) -> Optional[Path]:
        img = self._create_base_card(content, "rapid_revision")
        draw = ImageDraw.Draw(img)

        f_title = self._overlay._get_bold_font(30)
        f_body = self._overlay._get_font(22)

        title_y = 160
        self._draw_wrapped(draw, content.title[:120], f_title, title_y, _ACCENT)

        body_y = title_y + 80
        body_text = content.caption[:600]
        self._draw_wrapped(draw, body_text, f_body, body_y, _TEXT_COLOR)

        if content.high_yield_takeaway:
            hy_y = _CARD_H - 180
            draw.rectangle([_MARGIN, hy_y - 10, _CARD_W - _MARGIN, hy_y + 50],
                          fill=(39, 174, 96, 40))
            self._draw_wrapped(draw, f"★ {content.high_yield_takeaway[:200]}",
                              self._overlay._get_font(20), hy_y, "#27AE60")

        return self._save_card(img, content, "rapid_revision")

    # ── Template: True/False ───────────────────────────────────────────

    def _build_true_false_card(self, content: GeneratedContent) -> Optional[Path]:
        img = self._create_base_card(content, "true_false")
        draw = ImageDraw.Draw(img)

        f_statement = self._overlay._get_bold_font(28)
        f_expl = self._overlay._get_font(22)

        s_y = 180
        self._draw_wrapped(draw, (content.question or content.poster_text or "")[:200], f_statement, s_y, _TEXT_COLOR)

        answer = content.correct_answer or "?"
        is_true = answer.upper().startswith("TRUE")
        verdict = "TRUE" if is_true else "FALSE"
        v_color = "#27AE60" if is_true else "#E74C3C"
        v_y = s_y + 100
        draw.rectangle([_MARGIN, v_y - 10, _CARD_W - _MARGIN, v_y + 50], fill=(v_color, 30))
        self._draw_wrapped(draw, f"Verdict: {verdict}", f_statement, v_y, v_color)

        if content.explanation:
            e_y = v_y + 80
            self._draw_wrapped(draw, content.explanation[:400], f_expl, e_y, _TEXT_COLOR)

        return self._save_card(img, content, "true_false")

    # ── Template: One-Liner ────────────────────────────────────────────

    def _build_one_liner_card(self, content: GeneratedContent) -> Optional[Path]:
        img = self._create_base_card(content, "one_liner")
        draw = ImageDraw.Draw(img)

        f_stem = self._overlay._get_bold_font(28)
        f_answer = self._overlay._get_font(24)

        stem = content.question or content.poster_text or ""
        s_y = 200
        self._draw_wrapped(draw, stem[:200], f_stem, s_y, _TEXT_COLOR)

        if content.correct_answer:
            a_y = s_y + len(stem[:200]) // 50 * 30 + 80
            draw.rectangle([_MARGIN, a_y - 10, _CARD_W - _MARGIN, a_y + 50], fill=(52, 152, 219, 40))
            self._draw_wrapped(draw, f"Answer: {content.correct_answer[:100]}", f_answer, a_y, "#3498DB")

        return self._save_card(img, content, "one_liner")

    # ── Template: Mnemonic ─────────────────────────────────────────────

    def _build_mnemonic_card(self, content: GeneratedContent) -> Optional[Path]:
        img = self._create_base_card(content, "mnemonic")
        draw = ImageDraw.Draw(img)

        f_title = self._overlay._get_bold_font(30)
        f_memo = self._overlay._get_font(24)

        t_y = 160
        self._draw_wrapped(draw, (content.poster_text or content.title)[:120], f_title, t_y, _ACCENT)

        m_y = t_y + 80
        lines = content.caption.split("\n")[:8]
        for line in lines:
            self._draw_wrapped(draw, line.strip()[:80], f_memo, m_y, _TEXT_COLOR)
            m_y += 40

        if content.high_yield_takeaway:
            hy_y = _CARD_H - 150
            self._draw_wrapped(draw, content.high_yield_takeaway[:150],
                              self._overlay._get_font(20), hy_y, "#555555")

        return self._save_card(img, content, "mnemonic")

    # ── Template: Clinical Case ────────────────────────────────────────

    def _build_clinical_case_card(self, content: GeneratedContent) -> Optional[Path]:
        img = self._create_base_card(content, "clinical_case")
        draw = ImageDraw.Draw(img)

        f_title = self._overlay._get_bold_font(28)
        f_body = self._overlay._get_font(22)

        t_y = 160
        self._draw_wrapped(draw, (content.poster_text or content.title)[:120], f_title, t_y, _ACCENT)

        case = (content.question or content.caption or "")[:500]
        b_y = t_y + 80
        self._draw_wrapped(draw, case, f_body, b_y, _TEXT_COLOR)

        if content.correct_answer or content.high_yield_takeaway:
            conclusion = content.correct_answer or content.high_yield_takeaway or ""
            c_y = _CARD_H - 200
            draw.rectangle([_MARGIN, c_y - 10, _CARD_W - _MARGIN, c_y + 50],
                          fill=(231, 76, 60, 30))
            self._draw_wrapped(draw, f"Management: {conclusion[:200]}",
                              self._overlay._get_font(20), c_y, "#E74C3C")

        return self._save_card(img, content, "clinical_case")

    # ── Template: Concise Notes ────────────────────────────────────────

    def _build_notes_card(self, content: GeneratedContent) -> Optional[Path]:
        return self._build_rapid_revision_card(content)

    # ── Helpers ─────────────────────────────────────────────────────────

    def _create_base_card(self, content: GeneratedContent, template_id: str) -> Image.Image:
        img = Image.new("RGBA", (_CARD_W, _CARD_H), _BG)
        draw = ImageDraw.Draw(img)

        accent = _SUBJECT_ACCENTS.get(
            content.subject.value if content.subject else "general", _ACCENT
        )

        draw.rectangle([0, 0, _CARD_W, 6], fill=accent)

        emoji_map = {
            "anatomy": "🦴", "physiology": "🫀", "biochemistry": "🧬", "pathology": "🔬",
            "pharmacology": "💊", "microbiology": "🦠", "forensic_medicine": "⚖️",
            "community_medicine": "🌍", "general_medicine": "🩺", "general_surgery": "🔪",
            "obstetrics_gynecology": "🤱", "pediatrics": "👶", "ophthalmology": "👁",
            "ent": "👂", "orthopedics": "🦴", "dermatology": "🩹", "psychiatry": "🧠",
            "radiology": "☢", "anesthesiology": "💉",
        }
        subj_key = content.subject.value if content.subject else ""
        emoji = emoji_map.get(subj_key, "📚")

        subj_name = subj_key.replace("_", " ").title() if subj_key else "Medicine"
        fmt_name = content.content_format.value.replace("_", " ").upper()

        f_header = self._overlay._get_bold_font(24)
        draw.text((_MARGIN, 20), f"{emoji}  {subj_name}  |  {fmt_name}", fill=_ACCENT, font=f_header)

        draw.rectangle([_MARGIN, 60, _CARD_W - _MARGIN, 62], fill=(15, 52, 96, 80))

        return img

    def _draw_wrapped(self, draw: ImageDraw.Draw, text: str, font, y_start: int, color: str) -> None:
        words = text.split()
        lines: list[str] = []
        current = ""
        max_w = _CONTENT_W - 20
        for word in words:
            test = f"{current} {word}".strip()
            bbox = draw.textbbox((0, 0), test, font=font)
            if (bbox[2] - bbox[0]) <= max_w:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)

        line_h = (draw.textbbox((0, 0), "A", font=font)[3] - draw.textbbox((0, 0), "A", font=font)[1]) + 8
        y = y_start
        for line in lines[:15]:
            draw.text((_MARGIN + 10, y), line, fill=color, font=font)
            y += line_h

    def _pick_image(self, content: GeneratedContent) -> Optional[ImageAsset]:
        subject = content.subject
        if subject:
            candidates = self._loader.by_subject(subject)
            fmt_candidates = [c for c in candidates if content.content_format.value in c.format]
            if fmt_candidates:
                return random.choice(fmt_candidates)
            if candidates:
                return random.choice(candidates)
        return self._loader.random()

    def _save_card(self, img: Image.Image, content: GeneratedContent, template: str) -> Optional[Path]:
        try:
            subj_key = content.subject.value if content.subject else "general"
            out_path = get_settings().generated_dir / f"card_{subj_key}_{template}_{random.randint(10000,99999)}.png"
            out_path.parent.mkdir(parents=True, exist_ok=True)
            img.convert("RGB").save(str(out_path), "PNG", optimize=True)
            return out_path
        except Exception as exc:
            logger.error("Failed to save card: %s", exc)
            return None


def _hex_to_rgba(hex_color: str, alpha: int = 255) -> tuple[int, int, int, int]:
    h = hex_color.lstrip("#")
    return tuple(int(h[i:i+2], 16) for i in (0, 2, 4)) + (alpha,)
