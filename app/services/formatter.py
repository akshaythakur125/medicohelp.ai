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
    "mcq": "MCQ CHALLENGE",
    "rapid_revision": "RAPID REVISION",
    "concise_notes": "CONCISE NOTES",
    "clinical_case": "CLINICAL CASE",
    "image_based_question": "IMAGE MCQ",
    "practical_viva": "VIVA HIGH-YIELD",
    "pyq_concept": "PYQ SPECIAL",
    "exam_news_update": "EXAM NEWS",
    "residency_survival_tip": "RESIDENCY TIP",
    "flashcard": "FLASHCARD",
    "true_false": "TRUE OR FALSE",
    "one_liner_recall": "ONE-LINER RECALL",
    "mnemonic": "MNEMONIC",
}

_MAX_LEN = 4096


def _esc(text: str) -> str:
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _subject_emoji(content: GeneratedContent) -> str:
    if content.subject:
        return _SUBJECT_EMOJI.get(content.subject.value, "🏥")
    return "📰"


def _subject_name(content: GeneratedContent) -> str:
    if content.subject:
        return content.subject.value.replace("_", " ").title()
    if content.news_topic:
        return content.news_topic.value.replace("_", " ").title()
    return "Medicine"


def _fmt_label(content: GeneratedContent) -> str:
    return _FORMAT_LABEL.get(
        content.content_format.value,
        content.content_format.value.replace("_", " ").upper(),
    )


def _hashtags(content: GeneratedContent) -> str:
    tags = content.hashtags or ["#MedicoHelp", "#MBBS", "#NEETPG"]
    return " ".join(t if t.startswith("#") else f"#{t}" for t in tags)


def _extract_breakdown(caption: str, max_points: int = 6) -> list[str]:
    """Extract first-level bullet points from caption for numbered breakdown list."""
    points = []
    for line in caption.split("\n"):
        stripped = line.strip()
        if stripped.startswith("• "):
            points.append(stripped[2:].rstrip())
            if len(points) >= max_points:
                break
    return points


def format_for_telegram(content: GeneratedContent) -> str:
    fmt = content.content_format
    emoji = _subject_emoji(content)
    label = _fmt_label(content)
    subject = _subject_name(content)

    header = f"{emoji} <b>{label}: {subject}</b>"

    if fmt == ContentFormat.mcq:
        body = _body_mcq(content)
    elif fmt == ContentFormat.image_based_question:
        body = _body_ibq(content)
    elif fmt == ContentFormat.clinical_case:
        body = _body_case(content)
    elif fmt == ContentFormat.practical_viva:
        body = _body_viva(content)
    elif fmt in (ContentFormat.exam_news_update, ContentFormat.residency_survival_tip):
        body = _body_news(content)
    elif fmt == ContentFormat.flashcard:
        body = _body_flashcard(content)
    elif fmt == ContentFormat.true_false:
        body = _body_true_false(content)
    elif fmt == ContentFormat.one_liner_recall:
        body = _body_one_liner(content)
    elif fmt == ContentFormat.mnemonic:
        body = _body_mnemonic(content)
    else:
        body = _body_notes(content)

    parts = [header, "", body]

    if content.high_yield_takeaway and fmt not in (
        ContentFormat.exam_news_update,
        ContentFormat.residency_survival_tip,
    ):
        parts += ["", f"⚡ <b>Key Point:</b> {_esc(content.high_yield_takeaway)}"]

    parts += ["", _hashtags(content)]

    text = "\n".join(parts)
    return text[:_MAX_LEN]


def _body_notes(content: GeneratedContent) -> str:
    """Format rapid_revision, concise_notes, and pyq_concept posts."""
    parts: list[str] = []

    if content.poster_text:
        parts.append(f"<i>Scenario: {_esc(content.poster_text)}</i>")
        parts.append("")

    points = _extract_breakdown(content.caption)
    if points:
        parts.append("<b>The Breakdown:</b>")
        for i, pt in enumerate(points, 1):
            parts.append(f"{i}. {_esc(pt)}")
    else:
        parts.append(_esc(content.caption))

    return "\n".join(parts)


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
    if content.poster_text:
        parts.append(f"<i>Scenario: {_esc(content.poster_text)}</i>\n")
    if content.question:
        parts.append(f"<b>Viva Q:</b> {_esc(content.question)}\n")
    if content.explanation:
        parts.append(f"<b>Answer Framework:</b>\n{_esc(content.explanation)}")
    elif content.caption:
        points = _extract_breakdown(content.caption)
        if points:
            parts.append("<b>The Breakdown:</b>")
            for i, pt in enumerate(points, 1):
                parts.append(f"{i}. {_esc(pt)}")
        else:
            parts.append(_esc(content.caption))
    return "\n".join(parts)


def _body_flashcard(content: GeneratedContent) -> str:
    """Q on front, spoiler answer on back."""
    parts: list[str] = []
    question = content.question or content.poster_text or content.title
    parts.append(f"<b>Front:</b> {_esc(question)}")
    answer = content.correct_answer or content.high_yield_takeaway or content.caption
    if answer:
        parts.append(f"\n<tg-spoiler>✅ <b>Answer:</b> {_esc(answer)}</tg-spoiler>")
        parts.append("<i>👆 Tap to reveal</i>")
    return "\n".join(parts)


def _body_true_false(content: GeneratedContent) -> str:
    """True/False with spoiler reveal."""
    parts: list[str] = []
    statement = content.question or content.poster_text
    if statement:
        parts.append(f"<b>Statement:</b> <i>{_esc(statement)}</i>")
    if content.correct_answer or content.explanation:
        inner = ""
        verdict = content.correct_answer or "?"
        colour = "✅" if verdict.upper().startswith("TRUE") else "❌"
        inner += f"{colour} <b>{_esc(verdict.upper())}</b>"
        if content.explanation:
            inner += f"\n\n{_esc(content.explanation)}"
        parts.append(f"\n<tg-spoiler>{inner}</tg-spoiler>")
        parts.append("<i>👆 Tap to reveal</i>")
    return "\n".join(parts)


def _body_one_liner(content: GeneratedContent) -> str:
    """Fill-in-the-blank one-liner recall."""
    parts: list[str] = []
    stem = content.question or content.poster_text or content.title
    if stem:
        parts.append(f"<b>Complete:</b>\n<i>{_esc(stem)}</i>")
    if content.correct_answer:
        inner = f"<b>{_esc(content.correct_answer)}</b>"
        if content.explanation:
            inner += f"\n\n{_esc(content.explanation)}"
        parts.append(f"\n<tg-spoiler>{inner}</tg-spoiler>")
        parts.append("<i>👆 Tap to reveal</i>")
    return "\n".join(parts)


def _body_mnemonic(content: GeneratedContent) -> str:
    """Mnemonic breakdown with clinical hook."""
    parts: list[str] = []
    if content.poster_text:
        parts.append(f"<b>🔤 {_esc(content.poster_text)}</b>")
        parts.append("")
    parts.append(_esc(content.caption))
    return "\n".join(parts)


def _body_news(content: GeneratedContent) -> str:
    parts = [_esc(content.caption)]
    if content.source_url:
        parts.append(f'\n🔗 <a href="{content.source_url}">Read more</a>')
    return "\n".join(parts)
