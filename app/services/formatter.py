"""Converts GeneratedContent into Telegram HTML-formatted revision messages."""
from __future__ import annotations

from app.models import ContentFormat, GeneratedContent

_SUBJECT_EMOJI: dict[str, str] = {
    "anatomy": "🦴",
    "physiology": "🫀",
    "biochemistry": "🧬",
    "pathology": "🔬",
    "pharmacology": "💊",
    "microbiology": "🦠",
    "forensic_medicine": "⚖️",
    "community_medicine": "🌍",
    "general_medicine": "🩺",
    "general_surgery": "🔪",
    "obstetrics_gynecology": "🤱",
    "pediatrics": "👶",
    "ophthalmology": "👁",
    "ent": "👂",
    "orthopedics": "🦴",
    "dermatology": "🩹",
    "psychiatry": "🧠",
    "radiology": "☢",
    "anesthesiology": "💉",
}

_FORMAT_LABEL: dict[str, str] = {
    "mcq": "MCQ",
    "rapid_revision": "Rapid Revision",
    "concise_notes": "Concise Notes",
    "clinical_case": "Clinical Case",
    "image_based_question": "Image-Based MCQ",
    "practical_viva": "Practical Viva",
    "pyq_concept": "PYQ Concept",
    "exam_news_update": "Exam News",
    "residency_survival_tip": "Residency Tip",
}

_DIVIDER = "━━━━━━━━━━━━━━━━━━━━"
_MAX_LEN = 4096


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _subject_emoji(content: GeneratedContent) -> str:
    if content.subject:
        return _SUBJECT_EMOJI.get(content.subject.value, "🏥")
    return "📰"


def _subject_label(content: GeneratedContent) -> str:
    if content.subject:
        return content.subject.value.replace("_", " ").upper()
    if content.news_topic:
        return content.news_topic.value.replace("_", " ").upper()
    return "MEDICINE"


def _hashtags(content: GeneratedContent) -> str:
    tags = content.hashtags or ["#MedicoHelp", "#MBBS", "#NEETPG"]
    return " ".join(t if t.startswith("#") else f"#{t}" for t in tags)


def format_for_telegram(content: GeneratedContent) -> str:
    emoji = _subject_emoji(content)
    subject = _subject_label(content)
    fmt_label = _FORMAT_LABEL.get(
        content.content_format.value,
        content.content_format.value.replace("_", " ").title(),
    )

    header = f"{emoji} <b>{subject} — {fmt_label}</b>"
    body = _build_body(content)

    parts = [header, _DIVIDER, "", body]

    if content.high_yield_takeaway:
        parts += ["", f"💡 <b>High-Yield:</b> {_esc(content.high_yield_takeaway)}"]

    parts += ["", _hashtags(content)]

    text = "\n".join(parts)
    return text[:_MAX_LEN]


def _build_body(content: GeneratedContent) -> str:
    fmt = content.content_format

    if fmt == ContentFormat.mcq:
        return _body_mcq(content)
    if fmt == ContentFormat.image_based_question:
        return _body_ibq(content)
    if fmt == ContentFormat.clinical_case:
        return _body_case(content)
    if fmt == ContentFormat.practical_viva:
        return _body_viva(content)
    if fmt in (ContentFormat.rapid_revision, ContentFormat.concise_notes, ContentFormat.pyq_concept):
        return _esc(content.caption)
    if fmt in (ContentFormat.exam_news_update, ContentFormat.residency_survival_tip):
        return _body_news(content)
    return _esc(content.caption)


def _body_mcq(content: GeneratedContent) -> str:
    parts: list[str] = []
    if content.question:
        parts.append(f"<b>Q.</b> {_esc(content.question)}\n")
    for opt in content.options:
        parts.append(f"  {_esc(opt)}")
    if content.correct_answer or content.explanation:
        inner = ""
        if content.correct_answer:
            inner += f"✅ <b>Answer:</b> {_esc(content.correct_answer)}"
        if content.explanation:
            inner += f"\n\n<b>Explanation:</b>\n{_esc(content.explanation)}"
        parts.append(f"\n<tg-spoiler>{inner}\n</tg-spoiler>")
    return "\n".join(parts)


def _body_ibq(content: GeneratedContent) -> str:
    parts: list[str] = []
    if content.visual_description:
        parts.append(f"<i>🖼 Visual: {_esc(content.visual_description)}</i>\n")
    if content.question:
        parts.append(f"<b>Q.</b> {_esc(content.question)}\n")
    for opt in content.options:
        parts.append(f"  {_esc(opt)}")
    if content.correct_answer or content.explanation:
        inner = ""
        if content.correct_answer:
            inner += f"✅ <b>Answer:</b> {_esc(content.correct_answer)}"
        if content.explanation:
            inner += f"\n\n<b>Explanation:</b>\n{_esc(content.explanation)}"
        parts.append(f"\n<tg-spoiler>{inner}\n</tg-spoiler>")
    return "\n".join(parts)


def _body_case(content: GeneratedContent) -> str:
    parts: list[str] = []
    if content.question:
        parts.append(f"<b>Case:</b>\n{_esc(content.question)}\n")
    elif content.poster_text:
        parts.append(f"<b>Case:</b>\n{_esc(content.poster_text)}\n")
    if content.correct_answer or content.explanation:
        inner = ""
        if content.correct_answer:
            inner += f"✅ <b>Next Step:</b> {_esc(content.correct_answer)}"
        if content.explanation:
            inner += f"\n\n<b>Discussion:</b>\n{_esc(content.explanation)}"
        parts.append(f"<tg-spoiler>{inner}\n</tg-spoiler>")
    return "\n".join(parts)


def _body_viva(content: GeneratedContent) -> str:
    parts: list[str] = []
    if content.question:
        parts.append(f"<b>Viva Q:</b> {_esc(content.question)}\n")
    if content.explanation:
        parts.append(f"<b>Answer framework:</b>\n{_esc(content.explanation)}")
    elif content.caption:
        parts.append(_esc(content.caption))
    return "\n".join(parts)


def _body_news(content: GeneratedContent) -> str:
    parts = [_esc(content.caption)]
    if content.source_url:
        parts.append(f'\n🔗 <a href="{content.source_url}">Read more</a>')
    return "\n".join(parts)
