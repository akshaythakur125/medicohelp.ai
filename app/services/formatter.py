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
    # Tier 1
    "clinical_correlation": "CLINICAL CORRELATION",
    "comparison_table": "COMPARE & CONTRAST",
    "management_algorithm": "MANAGEMENT ALGORITHM",
    "drug_of_day": "DRUG OF THE DAY",
    # Tier 2
    "pimp_question": "WARD ROUND PIMP",
    "spot_diagnosis": "SPOT THE DIAGNOSIS",
    "ward_tip": "WARD SURVIVAL TIP",
    "case_unfolding": "UNFOLDING CASE",
    # Tier 3
    "osce_station": "OSCE STATION",
    "weekly_theme_intro": "WEEKLY THEME",
    "common_mistake": "COMMON MISTAKE",
    "study_schedule": "STUDY PLAN",
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
    elif fmt == ContentFormat.clinical_correlation:
        body = _body_clinical_correlation(content)
    elif fmt == ContentFormat.comparison_table:
        body = _body_comparison_table(content)
    elif fmt == ContentFormat.management_algorithm:
        body = _body_management_algorithm(content)
    elif fmt == ContentFormat.drug_of_day:
        body = _body_drug_of_day(content)
    elif fmt == ContentFormat.pimp_question:
        body = _body_pimp_question(content)
    elif fmt == ContentFormat.spot_diagnosis:
        body = _body_spot_diagnosis(content)
    elif fmt == ContentFormat.ward_tip:
        body = _body_ward_tip(content)
    elif fmt == ContentFormat.case_unfolding:
        body = _body_case_unfolding(content)
    elif fmt == ContentFormat.osce_station:
        body = _body_osce_station(content)
    elif fmt == ContentFormat.weekly_theme_intro:
        body = _body_weekly_theme_intro(content)
    elif fmt == ContentFormat.common_mistake:
        body = _body_common_mistake(content)
    elif fmt == ContentFormat.study_schedule:
        body = _body_study_schedule(content)
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


def _body_clinical_correlation(content: GeneratedContent) -> str:
    """Basic science → clinical bridge format."""
    parts: list[str] = []
    if content.poster_text:
        parts.append(f"<b>🔗 {_esc(content.poster_text)}</b>\n")
    parts.append(_esc(content.caption))
    if content.question:
        parts.append(f"\n<b>Apply it:</b> <i>{_esc(content.question)}</i>")
    if content.correct_answer:
        inner = f"<b>{_esc(content.correct_answer)}</b>"
        if content.explanation:
            inner += f"\n\n{_esc(content.explanation)}"
        parts.append(f"<tg-spoiler>{inner}</tg-spoiler>")
        parts.append("<i>👆 Tap to reveal</i>")
    return "\n".join(parts)


def _body_comparison_table(content: GeneratedContent) -> str:
    """Differential comparison table format."""
    parts: list[str] = []
    if content.poster_text:
        parts.append(f"<b>⚖️ {_esc(content.poster_text)}</b>\n")
    parts.append(f"<pre>{_esc(content.caption)}</pre>")
    if content.question:
        parts.append(f"\n<b>Key Distinguisher:</b> <i>{_esc(content.question)}</i>")
    if content.correct_answer:
        inner = f"✅ <b>{_esc(content.correct_answer)}</b>"
        if content.explanation:
            inner += f"\n\n{_esc(content.explanation)}"
        parts.append(f"<tg-spoiler>{inner}</tg-spoiler>")
        parts.append("<i>👆 Tap to reveal</i>")
    return "\n".join(parts)


def _body_management_algorithm(content: GeneratedContent) -> str:
    """Step-by-step management algorithm format."""
    parts: list[str] = []
    if content.poster_text:
        parts.append(f"<b>📋 {_esc(content.poster_text)}</b>\n")
    parts.append(_esc(content.caption))
    if content.question:
        parts.append(f"\n<b>Critical Step:</b> <i>{_esc(content.question)}</i>")
    if content.correct_answer:
        inner = f"✅ <b>{_esc(content.correct_answer)}</b>"
        if content.explanation:
            inner += f"\n\n{_esc(content.explanation)}"
        parts.append(f"<tg-spoiler>{inner}</tg-spoiler>")
        parts.append("<i>👆 Tap to reveal</i>")
    return "\n".join(parts)


def _body_drug_of_day(content: GeneratedContent) -> str:
    """Drug of the Day spotlight format."""
    parts: list[str] = []
    if content.poster_text:
        parts.append(f"<b>💊 {_esc(content.poster_text)}</b>\n")
    parts.append(_esc(content.caption))
    if content.question:
        parts.append(f"\n<b>Quick Test:</b> <i>{_esc(content.question)}</i>")
    if content.correct_answer:
        inner = f"✅ <b>{_esc(content.correct_answer)}</b>"
        if content.explanation:
            inner += f"\n{_esc(content.explanation)}"
        parts.append(f"<tg-spoiler>{inner}</tg-spoiler>")
        parts.append("<i>👆 Tap to reveal</i>")
    return "\n".join(parts)


def _body_pimp_question(content: GeneratedContent) -> str:
    """Ward round pimp question format."""
    parts: list[str] = []
    parts.append("<b>🩺 The attending turns to you...</b>\n")
    if content.question:
        parts.append(f"<b>❓ {_esc(content.question)}</b>\n")
    if content.caption:
        parts.append(_esc(content.caption))
    if content.correct_answer:
        inner = f"✅ <b>Model Answer:</b>\n{_esc(content.correct_answer)}"
        if content.explanation:
            inner += f"\n\n<b>Teaching Point:</b>\n{_esc(content.explanation)}"
        parts.append(f"\n<tg-spoiler>{inner}</tg-spoiler>")
        parts.append("<i>👆 Tap to reveal — say it out loud first!</i>")
    return "\n".join(parts)


def _body_spot_diagnosis(content: GeneratedContent) -> str:
    """Spot the diagnosis challenge format."""
    parts: list[str] = []
    parts.append("<b>👀 Look carefully — what's the diagnosis?</b>\n")
    if content.visual_description:
        parts.append(f"<i>🖼 {_esc(content.visual_description)}</i>\n")
    if content.question:
        parts.append(f"<b>Clue:</b> <i>{_esc(content.question)}</i>\n")
    for opt in content.options:
        parts.append(f"  {_esc(opt)}")
    if content.correct_answer or content.explanation:
        inner = ""
        if content.correct_answer:
            inner += f"✅ <b>{_esc(content.correct_answer)}</b>"
        if content.explanation:
            inner += f"\n\n{_esc(content.explanation)}"
        parts.append(f"\n<tg-spoiler>{inner}</tg-spoiler>")
        parts.append("<i>👆 Tap to reveal</i>")
    return "\n".join(parts)


def _body_ward_tip(content: GeneratedContent) -> str:
    """Ward survival tip format."""
    parts: list[str] = []
    if content.poster_text:
        parts.append(f"<b>🏥 {_esc(content.poster_text)}</b>\n")
    parts.append(_esc(content.caption))
    return "\n".join(parts)


def _body_case_unfolding(content: GeneratedContent) -> str:
    """Multi-part unfolding clinical case format."""
    parts: list[str] = []
    parts.append("<b>🩺 Unfolding Case — Part 1: The Presentation</b>\n")
    if content.question:
        parts.append(f"<b>Case:</b>\n<i>{_esc(content.question)}</i>\n")
    for opt in content.options:
        parts.append(f"  {_esc(opt)}")
    if content.caption:
        parts.append(f"\n{_esc(content.caption)}")
    if content.correct_answer or content.explanation:
        inner = ""
        if content.correct_answer:
            inner += f"✅ <b>Initial Approach:</b> {_esc(content.correct_answer)}"
        if content.explanation:
            inner += f"\n\n{_esc(content.explanation)}"
        parts.append(f"\n<tg-spoiler>{inner}</tg-spoiler>")
        parts.append("<i>👆 Tap to reveal Part 1 answer — Part 2 follows soon!</i>")
    return "\n".join(parts)


def _body_osce_station(content: GeneratedContent) -> str:
    """OSCE station preparation format."""
    parts: list[str] = []
    parts.append("<b>🏥 OSCE Station of the Week</b>\n")
    if content.poster_text:
        parts.append(f"<b>Station:</b> {_esc(content.poster_text)}\n")
    parts.append(_esc(content.caption))
    if content.question:
        parts.append(f"\n<b>Examiner's Key Question:</b>\n<i>{_esc(content.question)}</i>")
    if content.correct_answer:
        inner = f"✅ <b>Expected Answer:</b>\n{_esc(content.correct_answer)}"
        if content.explanation:
            inner += f"\n\n{_esc(content.explanation)}"
        parts.append(f"<tg-spoiler>{inner}</tg-spoiler>")
        parts.append("<i>👆 Tap to reveal</i>")
    return "\n".join(parts)


def _body_weekly_theme_intro(content: GeneratedContent) -> str:
    """Weekly theme launch post format."""
    parts: list[str] = []
    parts.append("<b>📅 Weekly Theme Launch!</b>\n")
    if content.poster_text:
        parts.append(f"<b>🎯 {_esc(content.poster_text)}</b>\n")
    parts.append(_esc(content.caption))
    if content.question:
        parts.append(f"\n<b>Baseline Check:</b> <i>{_esc(content.question)}</i>")
    if content.correct_answer:
        inner = f"🔑 <b>Key Concept:</b> {_esc(content.correct_answer)}"
        parts.append(f"<tg-spoiler>{inner}</tg-spoiler>")
        parts.append("<i>👆 Tap to see the most important concept this week</i>")
    return "\n".join(parts)


# ── Engagement Formatters ────────────────────────────────────────────────────


def format_streak_message(streak: int, longest: int) -> str:
    if streak <= 0:
        return "📅 Start your revision streak today! Open MedicoHelp to begin."
    if streak == 1:
        msg = "🔥 Day 1 streak! You've taken the first step — come back tomorrow!"
    elif streak < 7:
        msg = f"🔥 {streak}-day streak! Building momentum — don't break the chain!"
    elif streak < 30:
        msg = f"⚡ {streak}-day streak! You're in the zone — unstoppable!"
    elif streak < 100:
        msg = f"🏆 {streak}-day streak! Legendary consistency — keep it going!"
    else:
        msg = f"👑 {streak}-day streak! You're a revision legend!"
    return f"📊 <b>Revision Streak</b>\n\n{msg}\n\n<i>Longest streak: {longest} days</i>"


def format_daily_challenge_intro(content: GeneratedContent) -> str:
    """Format a daily challenge intro with the MCQ embedded."""
    emoji = _subject_emoji(content)
    subj = _subject_name(content)
    label = _fmt_label(content)
    header = f"🎯 <b>Daily Challenge — {label}: {subj}</b>"
    return header + "\n\n" + _body_mcq(content)


def format_weekly_battle_intro() -> str:
    return (
        "⚔️ <b>Weekly Revision Battle is LIVE!</b>\n\n"
        "Answer this week's questions to score points!\n"
        "🏆 Top scorer gets bragging rights until next week.\n\n"
        "<i>Questions will be posted throughout the week. "
        "Answer correctly to earn points!</i>"
    )


def format_battle_leaderboard(scores: dict[str, int]) -> str:
    if not scores:
        return "⚔️ <b>Weekly Battle</b>\n\nNo scores yet. Answer questions to earn points!"
    sorted_users = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    lines = ["🏆 <b>Weekly Revision Battle</b>", ""]
    for rank, (uid, pts) in enumerate(sorted_users[:10], 1):
        medals = {1: "🥇", 2: "🥈", 3: "🥉"}
        prefix = medals.get(rank, f"{rank}.")
        lines.append(f"{prefix} <b>User {uid}</b> — {pts} pts")
    lines.append("")
    lines.append("<i>Keep answering to climb the leaderboard!</i>")
    return "\n".join(lines)


def format_battle_winner(scores: dict[str, int]) -> str:
    if not scores:
        return "⚔️ <b>Battle Over</b>\n\nNo participants this week."
    winner = max(scores, key=scores.get)
    return (
        f"🏆 <b>Weekly Battle — Results!</b>\n\n"
        f"🥇 <b>Winner: User {winner}</b> — {scores[winner]} pts\n\n"
        f"{format_battle_leaderboard(scores)}\n\n"
        f"<i>Next battle starts Sunday! Stay sharp!</i>"
    )


def _body_common_mistake(content: GeneratedContent) -> str:
    """Common Mistakes Corner — the correction students never forget."""
    parts: list[str] = []
    if content.poster_text:
        parts.append(f"<b>{_esc(content.poster_text)}</b>\n")
    parts.append(_esc(content.caption))
    if content.question:
        parts.append(f"\n<b>Test Yourself:</b> <i>{_esc(content.question)}</i>")
    if content.correct_answer:
        inner = f"✅ <b>{_esc(content.correct_answer)}</b>"
        if content.explanation:
            inner += f"\n\n{_esc(content.explanation)}"
        parts.append(f"<tg-spoiler>{inner}</tg-spoiler>")
        parts.append("<i>👆 Tap to reveal</i>")
    return "\n".join(parts)


def _body_study_schedule(content: GeneratedContent) -> str:
    """Daily study plan post."""
    parts: list[str] = []
    if content.poster_text:
        parts.append(f"<b>📅 {_esc(content.poster_text)}</b>\n")
    parts.append(_esc(content.caption))
    return "\n".join(parts)


def format_study_schedule_post(days_remaining: int, subject: str, topics: list[str]) -> str:
    """Format a study schedule post with day counter."""
    topic_lines = "\n".join(f"  {i+1}. {t}" for i, t in enumerate(topics[:3]))
    header = f"📅 <b>Day {days_remaining} to Go — Today: {subject}</b>\n" if days_remaining > 0 else f"📅 <b>Today: {subject}</b>\n"
    return (
        f"{header}\n"
        f"🎯 <b>Must-Cover Today:</b>\n{topic_lines}\n\n"
        f"📖 <b>Strategy:</b>\n"
        f"  • Morning: Read concepts + notes\n"
        f"  • Afternoon: Solve 20-30 MCQs\n"
        f"  • Evening: Flashcard revision\n\n"
        f"<i>Stay consistent — one good day compounds into success.</i>"
    )


def format_exam_countdown(days_remaining: int, subject: str = "") -> str:
    if days_remaining <= 0:
        return "🎯 <b>Exam Day — Best of Luck!</b>\nYou've prepared well. Trust your revision!"
    if days_remaining == 1:
        urgency = "Tomorrow is the day! Final review mode — only the highest-yield points now."
    elif days_remaining <= 7:
        urgency = f"Only <b>{days_remaining} days left!</b> Focus on weak areas and revise mnemonics."
    elif days_remaining <= 14:
        urgency = f"<b>{days_remaining} days to go.</b> Speed up revision — one subject per day!"
    else:
        urgency = f"<b>{days_remaining} days remaining.</b> Stay consistent — every session counts!"
    subject_line = f"\n📚 Today's Focus: <b>{subject}</b>" if subject else ""
    return (
        f"⏳ <b>NEET PG Countdown</b>{subject_line}\n\n"
        f"{urgency}\n\n"
        f"<i>Keep your revision strategy tight. You've got this!</i>"
    )


def format_education_mode_announcement(mode_name: str, description: str) -> str:
    return f"📚 <b>Education Mode: {mode_name}</b>\n\n{description}\n\n<i>Your content will now focus on this track.</i>"


def format_challenge_result(accuracy_pct: float, streak: int) -> str:
    if accuracy_pct >= 80:
        feeling = "mastered"
    elif accuracy_pct >= 50:
        feeling = "building"
    else:
        feeling = "needs_review"
    messages = {
        "mastered": (
            f"🎯 <b>Excellent!</b> {accuracy_pct:.0f}% accuracy!\n"
            f"🔥 {streak}-day streak — you're on fire!"
        ),
        "building": (
            f"📚 <b>Good effort!</b> {accuracy_pct:.0f}% accuracy.\n"
            f"🔥 {streak}-day streak — keep revising!"
        ),
        "needs_review": (
            f"🔄 <b>Keep reviewing!</b> {accuracy_pct:.0f}% accuracy.\n"
            f"Focus on weak topics in tomorrow's challenge!"
        ),
    }
    return messages[feeling]
