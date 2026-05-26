"""
High-quality medical education poster generator.

Renders at 2× super-sampling (anti-aliasing via LANCZOS down-scale).
Subject-coded accent colours, format-specific layouts, and hand-crafted
medical schematics for each MBBS subject.
"""
from __future__ import annotations

import logging
import math
import textwrap
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from PIL import Image, ImageDraw, ImageFont

from app.config import Settings
from app.models import ContentFormat, GeneratedContent

logger = logging.getLogger(__name__)

# ── Canvas ─────────────────────────────────────────────────────────────────────
_SS = 2           # super-sampling factor; final output = 1080 × 1500
_FW, _FH = 1080, 1500


def _s(n: int | float) -> int:
    return int(n * _SS)


# ── Colour system ──────────────────────────────────────────────────────────────
_NAVY   = "#0F2D54"
_TEAL   = "#00A88F"
_WHITE  = "#FFFFFF"
_BG     = "#F4F8FF"
_MUTED  = "#5B7083"
_BORDER = "#C8D8EA"
_GOLD   = "#F5A623"
_RED    = "#D32F2F"
_GREEN  = "#2E7D32"

_SUBJECT_ACCENT: dict[str, tuple[str, str]] = {
    "anatomy":               ("#C62828", "#FFEBEE"),
    "physiology":            ("#1565C0", "#E3F2FD"),
    "biochemistry":          ("#2E7D32", "#E8F5E9"),
    "pathology":             ("#6A1B9A", "#F3E5F5"),
    "pharmacology":          ("#E65100", "#FFF3E0"),
    "microbiology":          ("#00695C", "#E0F2F1"),
    "forensic_medicine":     ("#37474F", "#ECEFF1"),
    "community_medicine":    ("#558B2F", "#F1F8E9"),
    "general_medicine":      ("#0D47A1", "#E3F2FD"),
    "general_surgery":       ("#455A64", "#ECEFF1"),
    "obstetrics_gynecology": ("#AD1457", "#FCE4EC"),
    "pediatrics":            ("#E65100", "#FFF8E1"),
    "ophthalmology":         ("#0277BD", "#E1F5FE"),
    "ent":                   ("#00695C", "#E0F2F1"),
    "orthopedics":           ("#5D4037", "#EFEBE9"),
    "dermatology":           ("#BF360C", "#FBE9E7"),
    "psychiatry":            ("#4527A0", "#EDE7F6"),
    "radiology":             ("#263238", "#ECEFF1"),
    "anesthesiology":        ("#283593", "#E8EAF6"),
}

_FORMAT_LABEL: dict[str, str] = {
    "mcq":                    "MCQ CHALLENGE",
    "rapid_revision":         "RAPID REVISION",
    "concise_notes":          "CONCISE NOTES",
    "clinical_case":          "CLINICAL CASE",
    "image_based_question":   "IMAGE MCQ",
    "practical_viva":         "VIVA HIGH-YIELD",
    "pyq_concept":            "PYQ SPECIAL",
    "exam_news_update":       "EXAM NEWS",
    "residency_survival_tip": "RESIDENCY TIP",
    "flashcard":              "FLASHCARD",
    "true_false":             "TRUE OR FALSE",
    "one_liner_recall":       "ONE-LINER RECALL",
    "mnemonic":               "MNEMONIC",
}

# ── Font loader ────────────────────────────────────────────────────────────────
_FONT_BOLD = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
]
_FONT_REG = [
    "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf",
    "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
]


def _font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    paths = _FONT_BOLD if bold else _FONT_REG
    for p in paths:
        try:
            return ImageFont.truetype(p, size=_s(size))
        except OSError:
            continue
    return ImageFont.load_default()


# ── Drawing helpers ────────────────────────────────────────────────────────────

def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)


def _fill_gradient_v(
    img: Image.Image,
    y0: int, y1: int,
    color_top: str,
    color_bot: str,
) -> None:
    """Fill a vertical gradient strip directly into the image pixels."""
    rt, gt, bt = _hex_to_rgb(color_top)
    rb, gb, bb = _hex_to_rgb(color_bot)
    draw = ImageDraw.Draw(img)
    span = max(y1 - y0, 1)
    for y in range(y0, y1):
        t = (y - y0) / span
        r = int(rt + (rb - rt) * t)
        g = int(gt + (gb - gt) * t)
        b = int(bt + (bb - bt) * t)
        draw.line((0, y, img.width, y), fill=(r, g, b))


def _rounded_rect(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    radius: int,
    fill: str | None = None,
    outline: str | None = None,
    width: int = 2,
) -> None:
    draw.rounded_rectangle(box, radius=_s(radius), fill=fill, outline=outline, width=width)


def _wrap(text: str, width: int, max_lines: int) -> list[str]:
    lines = textwrap.wrap(text or "", width=width)
    if len(lines) > max_lines:
        lines = lines[:max_lines]
        lines[-1] = lines[-1].rstrip(".") + "…"
    return lines


def _subject_key(content: GeneratedContent) -> str:
    if content.subject:
        return content.subject.value
    if content.news_topic:
        return content.news_topic.value
    return "general_medicine"


def _accent(content: GeneratedContent) -> tuple[str, str]:
    return _SUBJECT_ACCENT.get(_subject_key(content), (_NAVY, "#E3F2FD"))


def _format_label(content: GeneratedContent) -> str:
    return _FORMAT_LABEL.get(content.content_format.value, content.content_format.value.replace("_", " ").upper())


def _subject_display(content: GeneratedContent) -> str:
    if content.subject:
        return content.subject.value.replace("_", " ").title()
    if content.news_topic:
        return content.news_topic.value.replace("_", " ").upper()
    return "Medical Education"


# ── Medical diagram renderers ──────────────────────────────────────────────────

def _draw_ecg(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: str) -> None:
    """Realistic PQRST ECG waveform on a light grid background."""
    l, t, r, b = box
    # Grid
    grid_col = "#D4EAD4"
    for gx in range(l, r, _s(20)):
        draw.line((gx, t, gx, b), fill=grid_col, width=1)
    for gy in range(t, b, _s(20)):
        draw.line((l, gy, r, gy), fill=grid_col, width=1)
    # Draw a PQRST complex + partial second complex
    mid_y = (t + b) // 2
    amp = _s(60)  # R wave amplitude
    x0 = l + _s(40)
    # baseline → P wave → baseline → Q → R → S → baseline → T → baseline
    pts = [
        (x0,           mid_y),
        (x0 + _s(20),  mid_y),
        (x0 + _s(30),  mid_y - _s(14)),  # P start
        (x0 + _s(40),  mid_y - _s(14)),
        (x0 + _s(50),  mid_y),            # P end
        (x0 + _s(60),  mid_y),
        (x0 + _s(66),  mid_y + _s(10)),   # Q
        (x0 + _s(72),  mid_y - amp),      # R peak
        (x0 + _s(78),  mid_y + _s(16)),   # S
        (x0 + _s(84),  mid_y),
        (x0 + _s(100), mid_y),
        (x0 + _s(118), mid_y - _s(22)),   # T start
        (x0 + _s(134), mid_y - _s(22)),
        (x0 + _s(150), mid_y),            # T end
        (x0 + _s(180), mid_y),
        # second complex (partial)
        (x0 + _s(186), mid_y + _s(10)),
        (x0 + _s(192), mid_y - amp),
        (x0 + _s(198), mid_y + _s(16)),
        (x0 + _s(204), mid_y),
        (r - _s(20),   mid_y),
    ]
    draw.line(pts, fill=color, width=_s(3), joint="curve")
    # Labels
    lf = _font(12)
    draw.text((x0 + _s(30), mid_y - _s(26)), "P", fill=_MUTED, font=lf)
    draw.text((x0 + _s(70), mid_y - amp - _s(20)), "R", fill=_RED, font=lf)
    draw.text((x0 + _s(120), mid_y - _s(34)), "T", fill=_MUTED, font=lf)


def _draw_sigmoid(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: str) -> None:
    """Sigmoid dose–response curve (full agonist + partial agonist comparison)."""
    l, t, r, b = box
    w, h = r - l, b - t
    pad = _s(30)
    ax_l, ax_b = l + pad, b - pad
    ax_r, ax_t = r - pad, t + pad
    # Axes
    draw.line((ax_l, ax_b, ax_r, ax_b), fill=_MUTED, width=_s(2))
    draw.line((ax_l, ax_b, ax_l, ax_t), fill=_MUTED, width=_s(2))
    lf = _font(11)
    draw.text((ax_l + _s(4), ax_b + _s(4)), "Dose →", fill=_MUTED, font=lf)
    draw.text((l + _s(2), ax_t + _s(4)), "Effect", fill=_MUTED, font=lf)
    # Full agonist sigmoid (tanh approximation)
    full_pts = []
    part_pts = []
    steps = 80
    for i in range(steps + 1):
        frac = i / steps
        x = ax_l + int((ax_r - ax_l) * frac)
        # full agonist: Emax = 1.0, EC50 = 0.5
        val = 1 / (1 + math.exp(-10 * (frac - 0.5)))
        y_full = ax_b - int((ax_b - ax_t) * val)
        full_pts.append((x, y_full))
        # partial agonist: Emax = 0.55, same EC50
        y_part = ax_b - int((ax_b - ax_t) * 0.55 * val)
        part_pts.append((x, y_part))
    draw.line(full_pts, fill=color, width=_s(3))
    draw.line(part_pts, fill="#FF8C00", width=_s(2))
    # EC50 dashed vertical
    ec50_x = ax_l + (ax_r - ax_l) // 2
    for dy in range(0, ax_b - ax_t, _s(8)):
        draw.line((ec50_x, ax_t + dy, ec50_x, min(ax_t + dy + _s(4), ax_b)), fill=_MUTED, width=1)
    draw.text((ec50_x - _s(14), ax_b + _s(4)), "EC50", fill=_MUTED, font=lf)
    draw.text((ax_r - _s(60), ax_t + _s(4)), "Full agonist", fill=color, font=lf)
    draw.text((ax_r - _s(56), ax_t + _s(20)), "Partial agonist", fill="#FF8C00", font=lf)


def _draw_microscopy(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], subject: str) -> None:
    """Circular microscopy field with subject-appropriate cell types."""
    l, t, r, b = box
    cx, cy = (l + r) // 2, (t + b) // 2
    rad = min(r - l, b - t) // 2 - _s(8)
    # Background: pale yellow (tissue)
    draw.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill="#FFFDE7", outline="#455A64", width=_s(5))
    if subject == "pathology":
        # Granuloma: caseous center + surrounding epithelioid cells
        # Caseous necrotic center
        draw.ellipse((cx - _s(40), cy - _s(30), cx + _s(40), cy + _s(30)),
                     fill="#D4A76A", outline="#A0522D", width=_s(2))
        # Epithelioid cells ring
        for i in range(10):
            angle = math.radians(i * 36)
            ex = int(cx + _s(68) * math.cos(angle))
            ey = int(cy + _s(50) * math.sin(angle))
            draw.ellipse((ex - _s(14), ey - _s(10), ex + _s(14), ey + _s(10)),
                         fill="#FFCCBC", outline="#6A1B9A", width=_s(2))
        # Langhans giant cell (large, multi-nuclei)
        draw.ellipse((cx - _s(110), cy - _s(30), cx - _s(70), cy + _s(30)),
                     fill="#F8BBD9", outline="#6A1B9A", width=_s(2))
        for nx in range(-108, -72, 12):
            draw.ellipse((cx + _s(nx), cy - _s(8), cx + _s(nx) + _s(8), cy + _s(8)),
                         fill="#6A1B9A")
        # Lymphocytes outer ring
        for i in range(16):
            angle = math.radians(i * 22.5 + 11)
            lx = int(cx + _s(100) * math.cos(angle))
            ly = int(cy + _s(78) * math.sin(angle))
            draw.ellipse((lx - _s(6), ly - _s(6), lx + _s(6), ly + _s(6)),
                         fill="#B39DDB")
    elif subject == "microbiology":
        # Acid-fast bacilli (rods) — red on blue
        draw.ellipse((cx - rad, cy - rad, cx + rad, cy + rad), fill="#E3F2FD")
        for i in range(20):
            angle = math.radians(i * 17 + i * 3.7)
            bx = int(cx + _s(60) * math.cos(angle * 2.1))
            by = int(cy + _s(50) * math.sin(angle * 1.7))
            rot = angle * 57.3
            bx2 = int(bx + _s(18) * math.cos(math.radians(rot)))
            by2 = int(by + _s(18) * math.sin(math.radians(rot)))
            draw.line((bx, by, bx2, by2), fill="#C62828", width=_s(4))
    else:
        # Generic: scattered pink cells (skin/misc)
        for i in range(18):
            angle = math.radians(i * 20)
            ex = int(cx + _s(55) * math.cos(angle))
            ey = int(cy + _s(45) * math.sin(angle))
            draw.ellipse((ex - _s(12), ey - _s(10), ex + _s(12), ey + _s(10)),
                         fill="#FFCCBC", outline="#BF360C", width=_s(2))
    # Objective ring
    draw.ellipse((cx - rad, cy - rad, cx + rad, cy + rad),
                 outline="#37474F", width=_s(6), fill=None)


def _draw_pathway(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], color: str) -> None:
    """Metabolic pathway: substrate → enzyme → product with enzyme block."""
    l, t, r, b = box
    w = r - l
    pad_t = t + _s(20)
    row_h = _s(44)
    cx = (l + r) // 2

    labels = [
        ("GLUCOSE-6-P", "#E3F2FD", "#1565C0"),
        ("RIBOSE-5-P", "#E8F5E9", "#2E7D32"),
        ("NADPH ×2",   "#FFF8E1", "#F57C00"),
    ]
    enzymes = ["G6PD ✓", "Transketolase ✓"]
    box_w = _s(160)

    for i, (lbl, bg, fg) in enumerate(labels):
        bx = cx - box_w // 2
        by = pad_t + i * _s(90)
        _rounded_rect(draw, (bx, by, bx + box_w, by + row_h), 8, fill=bg, outline=fg, width=_s(2))
        draw.text((bx + _s(12), by + _s(10)), lbl, fill=fg, font=_font(11, bold=True))
        if i < len(enzymes):
            arrow_y = by + row_h + _s(6)
            draw.line((cx, arrow_y, cx, arrow_y + _s(36)), fill=color, width=_s(2))
            draw.polygon([(cx, arrow_y + _s(42)), (cx - _s(8), arrow_y + _s(30)), (cx + _s(8), arrow_y + _s(30))],
                         fill=color)
            draw.text((cx + _s(8), arrow_y + _s(8)), enzymes[i], fill=color, font=_font(11))

    # Block indicator
    block_y = pad_t + _s(3)
    _rounded_rect(draw, (l + _s(10), block_y, l + _s(72), block_y + _s(30)), 6,
                  fill="#FFEBEE", outline=_RED, width=_s(2))
    draw.text((l + _s(16), block_y + _s(6)), "X-linked\ndeficiency", fill=_RED, font=_font(9))


def _draw_xray(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    """Schematic chest X-ray (PA view) on a dark background."""
    l, t, r, b = box
    cx, cy = (l + r) // 2, (t + b) // 2
    w, h = r - l, b - t

    # Dark background
    draw.rectangle(box, fill="#1A1A2E")
    # Ribs (curved arcs)
    rib_col = "#6C8EAD"
    for i in range(5):
        y_off = t + _s(30) + i * _s(30)
        draw.arc((l + _s(20), y_off, cx - _s(10), y_off + _s(60)), 200, 360, fill=rib_col, width=_s(2))
        draw.arc((cx + _s(10), y_off, r - _s(20), y_off + _s(60)), 180, 340, fill=rib_col, width=_s(2))
    # Lung fields
    lung_col = "#B0C4D8"
    draw.ellipse((l + _s(24), t + _s(18), cx - _s(16), b - _s(24)), fill=lung_col)
    draw.ellipse((cx + _s(16), t + _s(18), r - _s(24), b - _s(24)), fill=lung_col)
    # Heart shadow (left of midline)
    draw.ellipse((cx - _s(60), cy - _s(56), cx + _s(30), b - _s(30)), fill="#3D5A80")
    # Hilum markings
    draw.ellipse((cx - _s(22), cy - _s(14), cx - _s(6), cy + _s(14)), fill="#2B4162")
    draw.ellipse((cx + _s(6),  cy - _s(14), cx + _s(22), cy + _s(14)), fill="#2B4162")
    # Trachea
    draw.line((cx - _s(4), t + _s(10), cx - _s(4), cy - _s(40)), fill="#90A4AE", width=_s(3))
    draw.line((cx + _s(4), t + _s(10), cx + _s(4), cy - _s(40)), fill="#90A4AE", width=_s(3))
    # Label
    lf = _font(11)
    draw.text((l + _s(6), b - _s(20)), "PA Chest X-Ray", fill="#90A4AE", font=lf)


def _draw_eye(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    """Simplified eye cross-section (sagittal view)."""
    l, t, r, b = box
    cx, cy = (l + r) // 2, (t + b) // 2
    rad_x, rad_y = (r - l) // 2 - _s(12), (b - t) // 2 - _s(12)
    # Sclera
    draw.ellipse((cx - rad_x, cy - rad_y, cx + rad_x, cy + rad_y),
                 fill="#F5F5DC", outline="#A0A0A0", width=_s(3))
    # Cornea (front curve)
    draw.arc((cx - rad_x - _s(16), cy - _s(40), cx - rad_x + _s(40), cy + _s(40)),
             260, 100, fill="#AED6F1", width=_s(6))
    # Iris + pupil
    iris_cx = cx - rad_x + _s(52)
    draw.ellipse((iris_cx - _s(28), cy - _s(28), iris_cx + _s(28), cy + _s(28)),
                 fill="#5B8DB8", outline="#1A3A5C", width=_s(3))
    draw.ellipse((iris_cx - _s(12), cy - _s(12), iris_cx + _s(12), cy + _s(12)), fill="#111111")
    # Lens
    draw.ellipse((cx - _s(28), cy - _s(26), cx + _s(28), cy + _s(26)),
                 fill="#E8F4F8", outline="#7DBBE8", width=_s(3))
    # Retina (posterior)
    draw.arc((cx - rad_x + _s(20), cy - rad_y + _s(10), cx + rad_x - _s(10), cy + rad_y - _s(10)),
             50, 310, fill="#FFCDD2", width=_s(8))
    # Optic nerve
    draw.rectangle((cx + rad_x - _s(20), cy - _s(10), cx + rad_x + _s(10), cy + _s(10)),
                   fill="#BCAAA4")
    # Fovea dot
    fov_x = cx + _s(40)
    draw.ellipse((fov_x - _s(6), cy - _s(6), fov_x + _s(6), cy + _s(6)), fill="#EF9A9A")
    # Labels
    lf = _font(10)
    draw.text((l + _s(2), t + _s(4)), "Cornea", fill=_MUTED, font=lf)
    draw.text((cx - _s(14), t + _s(4)), "Lens", fill=_MUTED, font=lf)
    draw.text((cx + _s(20), b - _s(18)), "Retina", fill=_MUTED, font=lf)
    draw.text((cx + rad_x - _s(14), t + _s(4)), "Optic disc", fill=_MUTED, font=lf)


def _draw_ear(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    """Tympanic membrane and ossicular chain diagram."""
    l, t, r, b = box
    cx, cy = (l + r) // 2, (t + b) // 2
    w = r - l

    # External canal (tube)
    canal_top = cy - _s(22)
    canal_bot = cy + _s(22)
    draw.rectangle((l + _s(20), canal_top, cx - _s(20), canal_bot), fill="#FDEBD0", outline=_MUTED, width=_s(2))
    draw.text((l + _s(26), canal_bot + _s(4)), "Canal", fill=_MUTED, font=_font(10))

    # Tympanic membrane (oval)
    draw.ellipse((cx - _s(28), cy - _s(42), cx + _s(28), cy + _s(42)),
                 fill="#FDEBD0", outline="#5D4037", width=_s(4))

    # Cone of light (triangle from umbo down-anterior)
    draw.polygon([(cx, cy + _s(6)), (cx - _s(18), cy + _s(32)), (cx + _s(4), cy + _s(32))],
                 fill="#FFFDE7", outline="#F9A825", width=_s(2))

    # Malleus handle (line from umbo upward)
    draw.line((cx, cy - _s(42), cx, cy + _s(6)), fill="#795548", width=_s(4))

    # Incus + stapes (simplified)
    draw.ellipse((cx + _s(26), cy - _s(20), cx + _s(50), cy + _s(4)),
                 fill="#BCAAA4", outline="#795548", width=_s(2))
    draw.line((cx + _s(50), cy - _s(8), cx + _s(68), cy - _s(8)), fill="#795548", width=_s(3))
    draw.line((cx + _s(68), cy - _s(18), cx + _s(68), cy + _s(2)), fill="#795548", width=_s(3))

    # Labels
    lf = _font(10)
    draw.text((cx - _s(18), t + _s(4)), "Tympanic membrane", fill=_MUTED, font=lf)
    draw.text((cx + _s(30), b - _s(18)), "Ossicles", fill=_MUTED, font=lf)
    draw.text((cx - _s(22), cy + _s(14)), "Cone of\nlight", fill="#F9A825", font=_font(9))


def _draw_body_outline(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int], accent: str) -> None:
    """Simplified anterior body silhouette with labeled regions."""
    l, t, r, b = box
    cx = (l + r) // 2
    h = b - t

    # Head
    draw.ellipse((cx - _s(32), t + _s(8), cx + _s(32), t + _s(72)),
                 fill="#FFDDC1", outline=accent, width=_s(3))
    # Neck
    draw.rectangle((cx - _s(14), t + _s(70), cx + _s(14), t + _s(95)),
                   fill="#FFDDC1", outline=accent, width=_s(2))
    # Torso
    draw.rounded_rectangle((cx - _s(56), t + _s(94), cx + _s(56), t + _s(230)),
                            radius=_s(12), fill="#FFDDC1", outline=accent, width=_s(3))
    # Left arm
    draw.rounded_rectangle((cx - _s(88), t + _s(98), cx - _s(60), t + _s(210)),
                            radius=_s(10), fill="#FFDDC1", outline=accent, width=_s(2))
    # Right arm
    draw.rounded_rectangle((cx + _s(60), t + _s(98), cx + _s(88), t + _s(210)),
                            radius=_s(10), fill="#FFDDC1", outline=accent, width=_s(2))
    # Legs
    draw.rounded_rectangle((cx - _s(50), t + _s(228), cx - _s(12), b - _s(10)),
                            radius=_s(10), fill="#FFDDC1", outline=accent, width=_s(2))
    draw.rounded_rectangle((cx + _s(12), t + _s(228), cx + _s(50), b - _s(10)),
                            radius=_s(10), fill="#FFDDC1", outline=accent, width=_s(2))
    # Highlight brachial plexus zone (shoulder)
    draw.ellipse((cx - _s(78), t + _s(90), cx - _s(36), t + _s(130)),
                 outline="#FF5722", width=_s(4))
    draw.text((l + _s(2), t + _s(86)), "C5-T1\nPlexus", fill="#FF5722", font=_font(10))


def _draw_partograph(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    """Partograph grid with alert and action lines."""
    l, t, r, b = box
    w, h = r - l, b - t
    ax_l, ax_b = l + _s(36), b - _s(24)
    ax_r, ax_t = r - _s(12), t + _s(12)

    # Grid
    for i in range(11):  # 0-10 cm dilatation
        gy = ax_b - int((ax_b - ax_t) * i / 10)
        draw.line((ax_l, gy, ax_r, gy), fill="#E0E0E0", width=1)
    for i in range(13):  # 0-12 hours
        gx = ax_l + int((ax_r - ax_l) * i / 12)
        draw.line((gx, ax_t, gx, ax_b), fill="#E0E0E0", width=1)

    # Axes
    draw.line((ax_l, ax_b, ax_r, ax_b), fill=_MUTED, width=_s(2))
    draw.line((ax_l, ax_b, ax_l, ax_t), fill=_MUTED, width=_s(2))
    lf = _font(10)
    draw.text((ax_l - _s(30), ax_t), "10", fill=_MUTED, font=lf)
    draw.text((ax_l - _s(20), ax_b - _s(10)), "0", fill=_MUTED, font=lf)
    draw.text((ax_r - _s(20), ax_b + _s(4)), "12h", fill=_MUTED, font=lf)

    # Alert line: 3cm at 0h → 10cm at 7h
    def _pos(hours: float, cm: float) -> tuple[int, int]:
        x = ax_l + int((ax_r - ax_l) * hours / 12)
        y = ax_b - int((ax_b - ax_t) * cm / 10)
        return (x, y)

    draw.line([_pos(0, 3), _pos(7, 10)], fill="#FFA000", width=_s(3))
    # Action line: 4h to the right
    draw.line([_pos(4, 3), _pos(11, 10)], fill=_RED, width=_s(3))
    # Cervical dilatation plot (normal progress)
    plot = [_pos(0, 3), _pos(1, 4), _pos(2, 5), _pos(3, 6), _pos(4, 7), _pos(5, 9), _pos(6, 10)]
    draw.line(plot, fill="#1565C0", width=_s(3))
    for p in plot:
        draw.ellipse((p[0] - _s(5), p[1] - _s(5), p[0] + _s(5), p[1] + _s(5)), fill="#1565C0")

    draw.text((ax_r - _s(60), ax_t + _s(4)), "Alert", fill="#FFA000", font=lf)
    draw.text((ax_r - _s(56), ax_t + _s(18)), "Action", fill=_RED, font=lf)


def _draw_contingency_table(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    """2×2 contingency table for community medicine / biostatistics."""
    l, t, r, b = box
    cx, cy = (l + r) // 2, (t + b) // 2
    pad = _s(20)

    # Header row
    draw.rectangle((l + pad, t + pad, r - pad, t + pad + _s(30)), fill=_NAVY)
    draw.text((cx - _s(50), t + pad + _s(6)), "Disease +    Disease −", fill=_WHITE, font=_font(11, bold=True))

    # Header col
    draw.rectangle((l + pad, t + pad, l + pad + _s(60), b - pad), fill=_NAVY)
    draw.text((l + pad + _s(4), cy - _s(24)), "Test +", fill=_WHITE, font=_font(11, bold=True))
    draw.text((l + pad + _s(4), cy + _s(6)), "Test −", fill=_WHITE, font=_font(11, bold=True))

    cells = [("TP", "#E8F5E9", _GREEN), ("FP", "#FBE9E7", _RED),
             ("FN", "#FBE9E7", _RED),  ("TN", "#E8F5E9", _GREEN)]
    cw = (r - l - pad * 2 - _s(60)) // 2
    ch = (b - t - pad * 2 - _s(30)) // 2
    for i, (lbl, bg, fg) in enumerate(cells):
        col = i % 2
        row = i // 2
        bx = l + pad + _s(60) + col * cw
        by = t + pad + _s(30) + row * ch
        draw.rectangle((bx, by, bx + cw, by + ch), fill=bg, outline=_BORDER, width=_s(2))
        draw.text((bx + cw // 2 - _s(10), by + ch // 2 - _s(12)), lbl, fill=fg, font=_font(18, bold=True))

    lf = _font(10)
    draw.text((l + pad + _s(4), b - pad - _s(20)),
              "Sens = TP/(TP+FN)   Spec = TN/(TN+FP)", fill=_MUTED, font=lf)


def _draw_growth_chart(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    """WHO weight-for-age growth chart (0-24 months, boys)."""
    l, t, r, b = box
    ax_l, ax_b = l + _s(30), b - _s(20)
    ax_r, ax_t = r - _s(14), t + _s(14)

    draw.rectangle((ax_l, ax_t, ax_r, ax_b), fill="#F9FBE7")
    for i in range(5):
        gy = ax_b - int((ax_b - ax_t) * i / 4)
        draw.line((ax_l, gy, ax_r, gy), fill="#E0E0E0", width=1)
    for i in range(5):
        gx = ax_l + int((ax_r - ax_l) * i / 4)
        draw.line((gx, ax_t, gx, ax_b), fill="#E0E0E0", width=1)

    draw.line((ax_l, ax_b, ax_r, ax_b), fill=_MUTED, width=_s(2))
    draw.line((ax_l, ax_b, ax_l, ax_t), fill=_MUTED, width=_s(2))
    lf = _font(10)
    draw.text((ax_l - _s(28), ax_t), "15kg", fill=_MUTED, font=lf)
    draw.text((ax_l - _s(18), ax_b - _s(10)), "3kg", fill=_MUTED, font=lf)
    draw.text((ax_r - _s(18), ax_b + _s(4)), "24m", fill=_MUTED, font=lf)

    # P97, P50, P3 sigmoid-like curves
    for frac, col in [(0.97, "#FFCDD2"), (0.50, "#1565C0"), (0.03, "#FFCDD2")]:
        pts = []
        for i in range(25):
            x = ax_l + int((ax_r - ax_l) * i / 24)
            val = frac * (1 - math.exp(-0.18 * i))
            y = ax_b - int((ax_b - ax_t) * val)
            pts.append((x, y))
        draw.line(pts, fill=col, width=_s(2 if frac == 0.50 else 1))

    draw.text((ax_r - _s(40), ax_t + _s(4)), "P97", fill="#FFCDD2", font=lf)
    draw.text((ax_r - _s(40), ax_t + _s(20)), "P50", fill="#1565C0", font=lf)


def _draw_skin_layers(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    """Skin cross-section showing epidermis, dermis, subcutaneous fat."""
    l, t, r, b = box
    w = r - l

    # Layers (top to bottom)
    layers = [
        (_s(30), "#FFDDC1", "#BF360C", "Epidermis"),
        (_s(90), "#FFCCBC", "#E64A19", "Dermis"),
        (_s(80), "#FFF9C4", "#F57F17", "Subcutaneous fat"),
    ]
    y = t + _s(8)
    for thick, fill, outline, lbl in layers:
        draw.rectangle((l + _s(8), y, r - _s(8), y + thick), fill=fill, outline=outline, width=_s(2))
        draw.text((l + _s(16), y + thick // 2 - _s(8)), lbl, fill=outline, font=_font(12, bold=True))
        y += thick

    # Hair follicle
    fhx = l + _s(80)
    draw.line((fhx, t + _s(8), fhx + _s(16), t + _s(120)), fill="#795548", width=_s(3))
    draw.ellipse((fhx, t + _s(112), fhx + _s(24), t + _s(136)),
                 fill="#BCAAA4", outline="#795548", width=_s(2))

    # Lesion mark (target lesion for dermatology)
    lx, ly = (l + r) // 2 + _s(30), t + _s(28)
    draw.ellipse((lx - _s(22), ly - _s(22), lx + _s(22), ly + _s(22)),
                 fill="#B71C1C", outline="#FF5722", width=_s(3))
    draw.ellipse((lx - _s(12), ly - _s(12), lx + _s(12), ly + _s(12)), fill="#FFCCBC")
    draw.ellipse((lx - _s(5), ly - _s(5), lx + _s(5), ly + _s(5)), fill="#B71C1C")
    draw.text((lx + _s(24), ly - _s(10)), "Target\nlesion", fill="#B71C1C", font=_font(10))


def _draw_brain(draw: ImageDraw.ImageDraw, box: tuple[int, int, int, int]) -> None:
    """Lateral brain diagram with labeled lobes."""
    l, t, r, b = box
    cx, cy = (l + r) // 2, (t + b) // 2
    rx, ry = (r - l) // 2 - _s(10), (b - t) // 2 - _s(10)
    # Main brain ellipse
    draw.ellipse((cx - rx, cy - ry, cx + rx, cy + ry),
                 fill="#FFDDC1", outline="#5D4037", width=_s(4))
    # Cerebellum (rear lower)
    draw.ellipse((cx + _s(30), cy + _s(20), cx + rx + _s(10), cy + ry + _s(10)),
                 fill="#FFCCBC", outline="#5D4037", width=_s(3))
    # Frontal folds (simplified sulci)
    for i in range(3):
        sx = cx - rx + _s(20) + i * _s(32)
        draw.arc((sx, cy - ry + _s(10), sx + _s(30), cy + _s(20)), 200, 20, fill="#A1887F", width=_s(2))
    for i in range(2):
        sx = cx - _s(20) + i * _s(36)
        draw.arc((sx, cy - _s(18), sx + _s(30), cy + _s(30)), 210, 30, fill="#A1887F", width=_s(2))
    # Lobe labels
    lf = _font(11, bold=True)
    draw.text((cx - rx + _s(20), cy - ry + _s(18)), "Frontal", fill="#1565C0", font=lf)
    draw.text((cx + _s(30), cy - ry + _s(18)), "Parietal", fill="#2E7D32", font=lf)
    draw.text((cx + _s(36), cy + _s(14)), "Occipital", fill="#6A1B9A", font=lf)
    draw.text((cx - _s(30), cy + _s(28)), "Temporal", fill="#E65100", font=lf)


def _draw_subject_diagram(
    draw: ImageDraw.ImageDraw,
    box: tuple[int, int, int, int],
    content: GeneratedContent,
) -> None:
    """Route to the correct subject-specific medical diagram."""
    acc_dark, acc_light = _accent(content)
    subj = _subject_key(content)

    draw.rectangle(box, fill=acc_light)

    if subj in ("physiology", "general_medicine", "anesthesiology"):
        _draw_ecg(draw, box, acc_dark)
    elif subj == "pharmacology":
        _draw_sigmoid(draw, box, acc_dark)
    elif subj in ("pathology",):
        _draw_microscopy(draw, box, "pathology")
    elif subj in ("microbiology",):
        _draw_microscopy(draw, box, "microbiology")
    elif subj in ("dermatology",):
        _draw_skin_layers(draw, box)
    elif subj in ("radiology", "general_surgery"):
        _draw_xray(draw, box)
    elif subj == "ophthalmology":
        _draw_eye(draw, box)
    elif subj == "ent":
        _draw_ear(draw, box)
    elif subj in ("anatomy", "forensic_medicine", "orthopedics"):
        _draw_body_outline(draw, box, acc_dark)
    elif subj == "obstetrics_gynecology":
        _draw_partograph(draw, box)
    elif subj == "community_medicine":
        _draw_contingency_table(draw, box)
    elif subj == "pediatrics":
        _draw_growth_chart(draw, box)
    elif subj == "psychiatry":
        _draw_brain(draw, box)
    elif subj == "biochemistry":
        _draw_pathway(draw, box, acc_dark)
    else:
        # Fallback: sigmoid curve
        _draw_sigmoid(draw, box, acc_dark)


# ── Format-specific content renderers ─────────────────────────────────────────

def _render_notes_content(draw: ImageDraw.ImageDraw, content: GeneratedContent, y0: int) -> int:
    """Rapid revision / concise notes / pyq / viva: diagram + numbered breakdown."""
    diagram_h = _s(290)
    diagram_box = (_s(54), y0, _s(1026), y0 + diagram_h)
    _rounded_rect(draw, diagram_box, 16, fill="#F0F7FF", outline=_accent(content)[0], width=_s(2))
    _draw_subject_diagram(draw, diagram_box, content)
    y = y0 + diagram_h + _s(22)

    # Breakdown header
    acc_dark, _ = _accent(content)
    draw.text((_s(60), y), "THE BREAKDOWN", fill=acc_dark, font=_font(17, bold=True))
    y += _s(38)

    # Extract bullet points or fall back to poster_text
    lines: list[str] = []
    for ln in (content.caption or "").split("\n"):
        stripped = ln.strip()
        if stripped.startswith("• "):
            lines.append(stripped[2:].rstrip())
        if len(lines) >= 6:
            break
    if not lines and content.poster_text:
        lines = _wrap(content.poster_text, 70, 5)

    for i, pt in enumerate(lines):
        num_box = (_s(60), y, _s(90), y + _s(26))
        _rounded_rect(draw, num_box, 4, fill=acc_dark)
        draw.text((_s(68), y + _s(2)), str(i + 1), fill=_WHITE, font=_font(13, bold=True))
        for segment in _wrap(pt, 66, 2):
            draw.text((_s(100), y), segment, fill="#1A2B3C", font=_font(14))
            y += _s(24)
        y += _s(6)
    return y


def _render_mcq_content(draw: ImageDraw.ImageDraw, content: GeneratedContent, y0: int) -> int:
    """MCQ: question box + 4 option boxes + answer reveal."""
    acc_dark, acc_light = _accent(content)
    question = content.question or content.poster_text or content.title
    y = y0

    # Question block
    q_lines = _wrap(question.replace("\n", " "), 60, 6)
    q_h = _s(28) + len(q_lines) * _s(28) + _s(16)
    _rounded_rect(draw, (_s(54), y, _s(1026), y + q_h), 14, fill=acc_light, outline=acc_dark, width=_s(3))
    draw.text((_s(70), y + _s(14)), "Q.", fill=acc_dark, font=_font(18, bold=True))
    qy = y + _s(14)
    for ln in q_lines:
        draw.text((_s(100), qy), ln, fill="#1A2B3C", font=_font(14))
        qy += _s(28)
    y += q_h + _s(18)

    # Options 2×2 grid
    options = content.options[:4] if content.options else ["A. Option 1", "B. Option 2", "C. Option 3", "D. Option 4"]
    opt_labels = ["A", "B", "C", "D"]
    opt_w = _s(472)
    opt_h = _s(64)
    opt_gap = _s(16)
    for i, (opt, lbl) in enumerate(zip(options, opt_labels)):
        col = i % 2
        row = i // 2
        ox = _s(54) + col * (opt_w + opt_gap)
        oy = y + row * (opt_h + opt_gap)
        _rounded_rect(draw, (ox, oy, ox + opt_w, oy + opt_h), 12, fill="#FFFFFF", outline=_BORDER, width=_s(2))
        # Letter badge
        _rounded_rect(draw, (ox + _s(10), oy + _s(12), ox + _s(38), oy + _s(40)), 6, fill=acc_dark)
        draw.text((ox + _s(18), oy + _s(14)), lbl, fill=_WHITE, font=_font(13, bold=True))
        for segment in _wrap(opt[2:].strip() if len(opt) > 2 else opt, 34, 2):
            draw.text((ox + _s(48), oy + _s(18)), segment, fill="#1A2B3C", font=_font(12))
            oy += _s(0)  # single line per option for now
    y += 2 * (opt_h + opt_gap) + _s(10)

    # Answer bar
    answer = content.correct_answer or "—"
    _rounded_rect(draw, (_s(54), y, _s(1026), y + _s(50)), 12, fill=acc_dark)
    draw.text((_s(70), y + _s(12)), f"✓  {answer[:72]}", fill=_WHITE, font=_font(14, bold=True))
    y += _s(60)
    return y


def _render_flashcard_content(draw: ImageDraw.ImageDraw, content: GeneratedContent, y0: int) -> int:
    """Flashcard: large question front + answer back with visual indicator."""
    acc_dark, acc_light = _accent(content)
    y = y0

    # Front card
    _rounded_rect(draw, (_s(54), y, _s(1026), y + _s(240)), 20,
                  fill=_WHITE, outline=acc_dark, width=_s(4))
    draw.text((_s(80), y + _s(16)), "QUESTION", fill=acc_dark, font=_font(13, bold=True))
    question = content.question or content.poster_text or content.title
    for ln in _wrap(question, 56, 5):
        draw.text((_s(80), y + _s(50)), ln, fill="#1A2B3C", font=_font(16))
        y += _s(0)
    # Re-draw properly
    y_front = y0 + _s(240) + _s(20)

    # Re-draw question text centred within the front card
    draw.rectangle((_s(54), y0, _s(1026), y0 + _s(240)), fill=None)
    _rounded_rect(draw, (_s(54), y0, _s(1026), y0 + _s(240)), 20,
                  fill=_WHITE, outline=acc_dark, width=_s(4))
    draw.text((_s(80), y0 + _s(16)), "QUESTION", fill=acc_dark, font=_font(13, bold=True))
    qlines = _wrap(question, 54, 5)
    text_h = len(qlines) * _s(32)
    text_start = y0 + (_s(240) - text_h) // 2
    for ln in qlines:
        draw.text((_s(80), text_start), ln, fill="#1A2B3C", font=_font(16))
        text_start += _s(32)

    # Flip divider
    draw.text((_s(440), y_front - _s(10)), "▼  REVEAL ANSWER  ▼", fill=acc_dark, font=_font(12, bold=True))
    y = y_front + _s(20)

    # Back card (answer)
    _rounded_rect(draw, (_s(54), y, _s(1026), y + _s(200)), 20, fill=acc_light, outline=acc_dark, width=_s(3))
    draw.text((_s(80), y + _s(14)), "ANSWER", fill=acc_dark, font=_font(13, bold=True))
    answer = content.correct_answer or content.high_yield_takeaway or ""
    ay = y + _s(50)
    for ln in _wrap(answer, 54, 4):
        draw.text((_s(80), ay), ln, fill="#1A2B3C", font=_font(15))
        ay += _s(30)
    y += _s(210)
    return y


def _render_true_false_content(draw: ImageDraw.ImageDraw, content: GeneratedContent, y0: int) -> int:
    """True/False: large statement + coloured verdict badge."""
    acc_dark, acc_light = _accent(content)
    y = y0

    # Statement box
    statement = content.question or content.poster_text or content.title
    s_lines = _wrap(statement, 58, 6)
    s_h = _s(40) + len(s_lines) * _s(34) + _s(20)
    _rounded_rect(draw, (_s(54), y, _s(1026), y + s_h), 18,
                  fill="#FAFAFA", outline=_BORDER, width=_s(3))
    draw.text((_s(78), y + _s(16)), "STATEMENT:", fill=_MUTED, font=_font(13, bold=True))
    sy = y + _s(52)
    for ln in s_lines:
        draw.text((_s(78), sy), ln, fill="#1A2B3C", font=_font(17))
        sy += _s(34)
    y += s_h + _s(24)

    # Verdict badge (large)
    verdict = (content.correct_answer or "TRUE").strip().upper()
    is_true = verdict.startswith("TRUE")
    badge_col = "#1B5E20" if is_true else "#B71C1C"
    badge_bg  = "#E8F5E9" if is_true else "#FFEBEE"
    badge_txt = "✓  TRUE" if is_true else "✗  FALSE"
    _rounded_rect(draw, (_s(260), y, _s(820), y + _s(80)), 20,
                  fill=badge_bg, outline=badge_col, width=_s(4))
    draw.text((_s(330), y + _s(18)), badge_txt, fill=badge_col, font=_font(24, bold=True))
    y += _s(100)

    # Explanation
    explanation = content.explanation or ""
    for ln in _wrap(explanation, 64, 5):
        draw.text((_s(66), y), ln, fill="#333333", font=_font(13))
        y += _s(26)
    return y


def _render_one_liner_content(draw: ImageDraw.ImageDraw, content: GeneratedContent, y0: int) -> int:
    """One-liner recall: fill-in-blank + answer reveal."""
    acc_dark, acc_light = _accent(content)
    y = y0

    # Stem with blank
    stem = content.question or content.poster_text or content.title
    # Visually emphasise the blank
    stem_display = stem.replace("___", "  _________  ")
    _rounded_rect(draw, (_s(54), y, _s(1026), y + _s(160)), 16,
                  fill=acc_light, outline=acc_dark, width=_s(3))
    draw.text((_s(78), y + _s(14)), "COMPLETE THE STATEMENT:", fill=acc_dark, font=_font(13, bold=True))
    sy = y + _s(52)
    for ln in _wrap(stem_display, 54, 3):
        draw.text((_s(78), sy), ln, fill="#1A2B3C", font=_font(17))
        sy += _s(34)
    y += _s(170)

    # Answer box
    answer = content.correct_answer or "—"
    _rounded_rect(draw, (_s(54), y, _s(1026), y + _s(64)), 14, fill=acc_dark)
    draw.text((_s(76), y + _s(16)), f"Answer:  {answer[:70]}", fill=_WHITE, font=_font(15, bold=True))
    y += _s(80)

    # Explanation
    expl = content.explanation or content.high_yield_takeaway or ""
    for ln in _wrap(expl, 66, 5):
        draw.text((_s(66), y), ln, fill="#333333", font=_font(13))
        y += _s(26)
    return y


def _render_mnemonic_content(draw: ImageDraw.ImageDraw, content: GeneratedContent, y0: int) -> int:
    """Mnemonic: large acronym header + colour-coded letter breakdown."""
    acc_dark, acc_light = _accent(content)
    y = y0

    # Mnemonic word from poster_text (e.g. "MIST = ...")
    mnemonic_word = (content.poster_text or content.title or "").split("=")[0].split("—")[0].strip()
    if len(mnemonic_word) > 12:
        mnemonic_word = mnemonic_word[:12]

    # Large acronym display
    _rounded_rect(draw, (_s(54), y, _s(1026), y + _s(96)), 18, fill=acc_dark)
    draw.text((_s(80), y + _s(18)), mnemonic_word, fill=_WHITE, font=_font(32, bold=True))
    y += _s(110)

    # Letter breakdown from caption
    letter_rows: list[tuple[str, str]] = []
    for ln in (content.caption or "").split("\n"):
        stripped = ln.strip()
        if len(stripped) >= 3 and stripped[1] in " —-" and stripped[0].isalpha():
            letter = stripped[0].upper()
            meaning = stripped[2:].strip().lstrip("—- ").strip()
            if meaning:
                letter_rows.append((letter, meaning))
        if len(letter_rows) >= 8:
            break

    row_colors = ["#E3F2FD", "#E8F5E9", "#FFF3E0", "#F3E5F5",
                  "#FCE4EC", "#E0F2F1", "#FFF8E1", "#E8EAF6"]
    row_txt_colors = ["#0D47A1", "#1B5E20", "#E65100", "#4A148C",
                      "#880E4F", "#004D40", "#F57F17", "#1A237E"]

    for i, (letter, meaning) in enumerate(letter_rows):
        row_bg = row_colors[i % len(row_colors)]
        row_fg = row_txt_colors[i % len(row_txt_colors)]
        row_h = _s(50)
        _rounded_rect(draw, (_s(54), y, _s(1026), y + row_h), 10, fill=row_bg)
        # Letter badge
        _rounded_rect(draw, (_s(64), y + _s(5), _s(104), y + row_h - _s(5)), 8, fill=row_fg)
        draw.text((_s(72), y + _s(10)), letter, fill=_WHITE, font=_font(18, bold=True))
        for seg in _wrap(meaning, 70, 2):
            draw.text((_s(116), y + _s(12)), seg, fill="#1A1A2E", font=_font(14))
            break
        y += row_h + _s(6)
    return y


def _render_clinical_case_content(draw: ImageDraw.ImageDraw, content: GeneratedContent, y0: int) -> int:
    """Clinical case: scenario + options + answer."""
    acc_dark, acc_light = _accent(content)
    y = y0

    case_text = content.question or content.poster_text or ""
    c_lines = _wrap(case_text.replace("\n", " "), 60, 7)
    c_h = _s(36) + len(c_lines) * _s(28) + _s(16)
    _rounded_rect(draw, (_s(54), y, _s(1026), y + c_h), 16,
                  fill=acc_light, outline=acc_dark, width=_s(3))
    draw.text((_s(78), y + _s(14)), "CASE SCENARIO", fill=acc_dark, font=_font(13, bold=True))
    cy2 = y + _s(46)
    for ln in c_lines:
        draw.text((_s(78), cy2), ln, fill="#1A2B3C", font=_font(14))
        cy2 += _s(28)
    y += c_h + _s(16)

    # Options
    options = content.options[:4] if content.options else []
    opt_labels = ["A", "B", "C", "D"]
    for i, (opt, lbl) in enumerate(zip(options, opt_labels)):
        opt_h = _s(52)
        _rounded_rect(draw, (_s(54), y, _s(1026), y + opt_h), 10, fill="#FFFFFF", outline=_BORDER, width=_s(2))
        _rounded_rect(draw, (_s(64), y + _s(10), _s(94), y + _s(42)), 6, fill=acc_dark)
        draw.text((_s(72), y + _s(14)), lbl, fill=_WHITE, font=_font(13, bold=True))
        draw.text((_s(108), y + _s(15)), (opt[2:].strip() if len(opt) > 2 else opt)[:70], fill="#1A2B3C", font=_font(13))
        y += opt_h + _s(8)

    # Answer
    answer = content.correct_answer or "—"
    _rounded_rect(draw, (_s(54), y + _s(8), _s(1026), y + _s(60)), 12, fill=acc_dark)
    draw.text((_s(74), y + _s(20)), f"Next Step:  {answer[:64]}", fill=_WHITE, font=_font(14, bold=True))
    y += _s(72)
    return y


def _render_news_content(draw: ImageDraw.ImageDraw, content: GeneratedContent, y0: int) -> int:
    """Exam news / residency tip: plain text with icon."""
    y = y0
    acc_dark, acc_light = _accent(content)
    _rounded_rect(draw, (_s(54), y, _s(1026), y + _s(520)), 16, fill=acc_light, outline=acc_dark, width=_s(2))
    cy2 = y + _s(24)
    for ln in _wrap(content.caption or "", 62, 12):
        draw.text((_s(78), cy2), ln, fill="#1A2B3C", font=_font(14))
        cy2 += _s(30)
    return cy2 + _s(10)


def _render_ibq_content(
    draw: ImageDraw.ImageDraw,
    canvas: Image.Image,
    content: GeneratedContent,
    visual_path: Path | None,
    y0: int,
) -> int:
    """Image-based question: visual region + question + options."""
    acc_dark, acc_light = _accent(content)
    y = y0
    vis_h = _s(310)
    vis_box = (_s(54), y, _s(1026), y + vis_h)

    if visual_path and visual_path.exists():
        _rounded_rect(draw, vis_box, 14, fill="#FFFFFF", outline=acc_dark, width=_s(3))
        img = Image.open(visual_path).convert("RGB")
        avail_w = _s(1026) - _s(54) - _s(20)
        avail_h = vis_h - _s(20)
        img.thumbnail((_s(960), avail_h))
        px = _s(54) + (_s(1026) - _s(54) - img.width) // 2
        py = y + (vis_h - img.height) // 2
        canvas.paste(img, (px, py))
    else:
        _draw_subject_diagram(draw, vis_box, content)

    # Label bar
    labels = content.visual_labels or content.image_based_data or []
    lx = _s(54)
    label_w = (_s(1026) - _s(54)) // max(len(labels[:4]), 1)
    for lbl in labels[:4]:
        _rounded_rect(draw, (lx + _s(4), y + vis_h - _s(36), lx + label_w - _s(4), y + vis_h - _s(4)),
                      8, fill=acc_dark)
        draw.text((lx + _s(10), y + vis_h - _s(28)), lbl[:18], fill=_WHITE, font=_font(11, bold=True))
        lx += label_w
    y += vis_h + _s(14)

    return _render_mcq_content(draw, content, y)


# ── Main poster class ──────────────────────────────────────────────────────────

class PosterGenerator:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings

    def create(self, content: GeneratedContent, visual_image_path: Path | None = None) -> Path:
        # Render at 2× resolution
        canvas = Image.new("RGB", (_FW * _SS, _FH * _SS), _BG)
        draw = ImageDraw.Draw(canvas)

        self._draw_header(canvas, draw, content)
        self._draw_title_zone(draw, content)

        fmt = content.content_format
        content_y0 = _s(305)

        if fmt == ContentFormat.image_based_question:
            _render_ibq_content(draw, canvas, content, visual_image_path, content_y0)
        elif fmt == ContentFormat.mcq:
            _render_mcq_content(draw, content, content_y0)
        elif fmt == ContentFormat.flashcard:
            _render_flashcard_content(draw, content, content_y0)
        elif fmt == ContentFormat.true_false:
            _render_true_false_content(draw, content, content_y0)
        elif fmt == ContentFormat.one_liner_recall:
            _render_one_liner_content(draw, content, content_y0)
        elif fmt == ContentFormat.mnemonic:
            _render_mnemonic_content(draw, content, content_y0)
        elif fmt == ContentFormat.clinical_case:
            _render_clinical_case_content(draw, content, content_y0)
        elif fmt in (ContentFormat.exam_news_update, ContentFormat.residency_survival_tip):
            _render_news_content(draw, content, content_y0)
        else:
            # rapid_revision, concise_notes, pyq_concept, practical_viva
            _render_notes_content(draw, content, content_y0)

        self._draw_key_point_bar(draw, content)
        self._draw_footer(draw, content)

        # Down-sample for anti-aliasing
        final = canvas.resize((_FW, _FH), Image.LANCZOS)

        filename = (
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}_"
            f"{_subject_key(content)}_{content.content_format.value}_{uuid4().hex[:8]}.png"
        )
        path = self.settings.generated_dir / filename
        final.save(path, "PNG", optimize=True, quality=95)
        logger.info("Poster generated: %s", path)
        return path

    # ── Structural sections ────────────────────────────────────────────────────

    def _draw_header(self, canvas: Image.Image, draw: ImageDraw.ImageDraw, content: GeneratedContent) -> None:
        acc_dark, _ = _accent(content)
        # Accent strip at top
        draw.rectangle((0, 0, _FW * _SS, _s(10)), fill=acc_dark)
        # Navy header band
        _fill_gradient_v(canvas, _s(10), _s(150), _NAVY, "#1A3A5C")
        draw.rectangle((0, _s(10), _FW * _SS, _s(150)), fill=None)  # no-op, gradient already drawn

        # Brand name
        draw.text((_s(52), _s(22)), "MedicoHelp", fill=_WHITE, font=_font(28, bold=True))
        # Sub-brand
        draw.text((_s(52), _s(76)), "MBBS · NEET PG · Medical Education", fill="#90CAF9", font=_font(13))

        # Subject + format badge (right side)
        subj_display = _subject_display(content)
        fmt_lbl = _format_label(content)
        # Format badge
        badge_text = fmt_lbl
        badge_w = len(badge_text) * _s(9) + _s(24)
        _rounded_rect(draw, (_FW * _SS - _s(52) - badge_w, _s(22), _FW * _SS - _s(52), _s(62)),
                      10, fill=acc_dark)
        draw.text((_FW * _SS - _s(44) - badge_w, _s(32)), badge_text, fill=_WHITE, font=_font(12, bold=True))
        # Subject label
        draw.text((_FW * _SS - _s(44) - badge_w, _s(72)), subj_display, fill="#B3D9FF", font=_font(13))

        # Separator with teal accent
        draw.rectangle((0, _s(150), _FW * _SS, _s(154)), fill=_TEAL)

    def _draw_title_zone(self, draw: ImageDraw.ImageDraw, content: GeneratedContent) -> None:
        acc_dark, _ = _accent(content)
        draw.rectangle((0, _s(154), _FW * _SS, _s(305)), fill=_WHITE)
        title = content.title or ""
        if len(title) > 52:
            title = title[:49].rstrip() + "…"
        draw.text((_s(52), _s(172)), title, fill=_NAVY, font=_font(24, bold=True))
        breadcrumb = f"{_subject_display(content)}  ·  {_format_label(content)}"
        draw.text((_s(52), _s(232)), breadcrumb, fill=acc_dark, font=_font(14))
        # Thin separator before content
        draw.rectangle((0, _s(298), _FW * _SS, _s(302)), fill=_BORDER)

    def _draw_key_point_bar(self, draw: ImageDraw.ImageDraw, content: GeneratedContent) -> None:
        if not content.high_yield_takeaway:
            return
        kp_y0 = _s(1080)
        draw.rectangle((0, kp_y0, _FW * _SS, _s(1220)), fill=_TEAL)
        draw.text((_s(52), kp_y0 + _s(14)), "⚡  KEY POINT", fill=_WHITE, font=_font(16, bold=True))
        kp_y = kp_y0 + _s(52)
        for ln in _wrap(content.high_yield_takeaway, 72, 3):
            draw.text((_s(52), kp_y), ln, fill=_WHITE, font=_font(14))
            kp_y += _s(30)

    def _draw_footer(self, draw: ImageDraw.ImageDraw, content: GeneratedContent) -> None:
        draw.rectangle((0, _s(1220), _FW * _SS, _FH * _SS), fill="#EBF3FA")
        # Hashtags
        tags = content.hashtags or ["#MedicoHelp", "#NEETPG", "#MBBS"]
        tag_line = "  ".join(t if t.startswith("#") else f"#{t}" for t in tags[:6])
        draw.text((_s(52), _s(1236)), tag_line, fill=_TEAL, font=_font(14, bold=True))
        # Watermark
        draw.text((_s(52), _s(1300)), "medicohelp.ai  ·  AI-powered NEET PG Revision",
                  fill=_MUTED, font=_font(13))
        # Bottom accent strip
        acc_dark, _ = _accent(content)
        draw.rectangle((0, _FH * _SS - _s(10), _FW * _SS, _FH * _SS), fill=acc_dark)
