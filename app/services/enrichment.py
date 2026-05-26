"""Engagement-oriented content enrichment: hook lines, exam tags, memory tricks, clinical pearls, takeaways."""
from __future__ import annotations

import logging
import random
import re

from app.models import ContentFormat, GeneratedContent, Subject

logger = logging.getLogger(__name__)

_HOOKS: dict[str, list[str]] = {
    "anatomy": [
        "One nerve can decide your entire NEET PG rank. Master it.",
        "If you miss this, you will regret it in the exam hall.",
        "This is a cadaveric classic — appears every single year.",
    ],
    "physiology": [
        "Understand this concept once, and 5 questions become free marks.",
        "The single most repeated physiology concept in NEET PG.",
        "If there is one graph you must memorise, it is this one.",
    ],
    "biochemistry": [
        "Biochemistry made easy — one pathway at a time.",
        "This vitamin deficiency question is a guaranteed giveaway.",
        "Never confuse these two enzymes again.",
    ],
    "pathology": [
        "The hallmark of this disease? Every examiner expects you to know it.",
        "If you see this morphology, the diagnosis writes itself.",
        "This is THE classic pathology vignette topic.",
    ],
    "pharmacology": [
        "One drug interaction costs lives. This one is frequently tested.",
        "If you memorise this one MOA, you unlock 3 related questions.",
        "The single most prescribed drug in this class. Know it cold.",
    ],
    "microbiology": [
        "This organism has a unique feature no other has. Remember it.",
        "Gram stain + this one clue = diagnosis. Always tested.",
        "If you learn this one bug well, you eliminate 4 options instantly.",
    ],
    "forensic_medicine": [
        "Medicolegal autopsy question? This fact decides the answer.",
        "In court, this distinction matters. In NEET PG, it is a sure-shot mark.",
        "One postmortem finding separates this from every other cause.",
    ],
    "community_medicine": [
        "Epidemiology formula you must know — appears every single year.",
        "National health programme question? This is the most asked.",
        "If you understand this one rate, 5 biostatistics questions are done.",
    ],
    "general_medicine": [
        "The single most common cause you must never forget.",
        "This clinical sign is pathognomonic. Remember it for life.",
        "If you see this triad, do not waste time — you know the diagnosis.",
    ],
    "general_surgery": [
        "This surgical emergency has a classic presentation. Spot it fast.",
        "The single most asked complication in surgery NEET PG.",
        "If you remember this one step, the entire management is clear.",
    ],
    "obstetrics_gynecology": [
        "This is THE most common cause of maternal mortality. Do not skip.",
        "One ultrasound finding changes everything. Know it.",
        "This ovarian mass has a classic histological pattern.",
    ],
    "pediatrics": [
        "This paediatric emergency has a golden hour. Know the protocol.",
        "If a child presents with these symptoms, this is the answer.",
        "The single most important vaccination fact for NEET PG.",
    ],
    "ophthalmology": [
        "This retinal finding is pathognomonic. Never miss it.",
        "One slit-lamp finding separates these two conditions.",
        "The most tested cranial nerve in ophthalmology.",
    ],
    "ent": [
        "This ENT emergency — airway first, diagnosis second.",
        "If you see this finding on otoscopy, the answer is clear.",
        "The single most common cause of hoarseness. Exam favourite.",
    ],
    "orthopedics": [
        "This fracture has a classic nerve injury. Always tested.",
        "If you see this deformity, do not reduce — recognise.",
        "The single most important X-ray finding in orthopaedics.",
    ],
    "dermatology": [
        "This rash has a classic distribution. One glance is enough.",
        "If you see this morphology, think of this one condition.",
        "The single most common skin condition in India. Know it.",
    ],
    "psychiatry": [
        "One screening question changes the diagnosis entirely.",
        "This delusion type is pathognomonic for schizophrenia.",
        "If you remember this one criterion, the diagnosis is clear.",
    ],
    "radiology": [
        "This X-ray finding is a NEET PG classic. Memorise it.",
        "If you see this CT pattern, do not waste time on differentials.",
        "One MRI sequence tells you everything about this pathology.",
    ],
    "anesthesiology": [
        "This airway assessment score is a must-know for exams.",
        "If you forget this one drug interaction, the patient pays the price.",
        "The single most common intraoperative complication. Be ready.",
    ],
}

_EXAM_TAGS = [
    "🩺 <b>NEET PG 2026:</b> High-yield | Frequently repeated in previous 5 years.",
    "📋 <b>INI-CET:</b> Frequently tested — appears in almost every cycle.",
    "🏆 <b>NEET PG:</b> Rank-defining topic | Master this for a top 1000 rank.",
    "📌 <b>Exam Spotlight:</b> Every major exam (NEET PG, INI-CET, FMGE) tests this.",
    "🎯 <b>Must-Know:</b> Almost guaranteed to appear in the upcoming exam.",
]

_MEMORY_TRICKS = [
    "🧠 <b>Memory Trick:</b> {trick}",
    "🔤 <b>Mnemonic:</b> {trick}",
    "💡 <b>Easy Recall:</b> {trick}",
]

_CLINICAL_PEARLS = [
    "💎 <b>Clinical Pearl:</b> {pearl}",
    "🩺 <b>Bedside Tip:</b> {pearl}",
    "⚡ <b>Clinical Insight:</b> {pearl}",
]

_TAKEAWAY_INTROS = [
    "📝 <b>Quick Takeaway:</b>",
    "✅ <b>Bottom Line:</b>",
    "⚡ <b>One-Liner for Revision:</b>",
]


def enrich_for_engagement(content: GeneratedContent) -> GeneratedContent:
    if content.content_format in (
        ContentFormat.exam_news_update,
        ContentFormat.residency_survival_tip,
    ):
        return content

    sections: list[str] = []

    hook = _pick_hook(content)
    if hook:
        sections.append(f"🔥 {hook}")
        sections.append("")

    tag = random.choice(_EXAM_TAGS)
    sections.append(tag)
    sections.append("")

    trick = _build_memory_trick(content)
    if trick:
        sections.append(trick)
        sections.append("")

    pearl = _build_clinical_pearl(content)
    if pearl:
        sections.append(pearl)
        sections.append("")

    takeaway = _build_takeaway(content)
    if takeaway:
        sections.append(takeaway)

    bloom_tag = apply_bloom_taxonomy(content)
    if bloom_tag:
        sections.append("")
        sections.append(bloom_tag)

    if sections:
        enrichment = "\n".join(sections)
        if content.caption:
            content.caption = content.caption.rstrip() + "\n\n" + enrichment
        else:
            content.caption = enrichment

    return content


def _pick_hook(content: GeneratedContent) -> str | None:
    if not content.subject:
        return None
    hooks = _HOOKS.get(content.subject.value)
    if not hooks:
        return None
    return random.choice(hooks)


def _build_memory_trick(content: GeneratedContent) -> str | None:
    source = content.high_yield_takeaway or content.caption[:300]
    if not source:
        return None

    words = [w for w in source.split() if len(w) > 4][:5]
    if len(words) >= 3:
        acronym = "".join(w[0].upper() for w in words[:5])
        if len(acronym) >= 3:
            template = random.choice(_MEMORY_TRICKS)
            return template.format(trick=f"Recall the acronym <b>{acronym}</b>: {', '.join(words[:5])}")

    first_clause = source.split(".")[0] if "." in source else source[:80]
    if len(first_clause) > 20:
        template = random.choice(_MEMORY_TRICKS)
        return template.format(trick=f"Think of <b>'{first_clause[:60]}'</b> — this is the key association.")

    return None


def _build_clinical_pearl(content: GeneratedContent) -> str | None:
    source = content.explanation or content.high_yield_takeaway or content.caption[:400]
    if not source:
        return None

    sentences = [s.strip() for s in re.split(r'[.!?\n]', source) if len(s.strip()) > 30]
    if sentences:
        pearl = random.choice(sentences)[:150]
        template = random.choice(_CLINICAL_PEARLS)
        return template.format(pearl=pearl)

    return None


def _build_takeaway(content: GeneratedContent) -> str | None:
    takeaway = content.high_yield_takeaway
    if not takeaway:
        return None
    intro = random.choice(_TAKEAWAY_INTROS)
    return f"{intro}\n{takeaway[:300]}"


def apply_bloom_taxonomy(content: GeneratedContent) -> str | None:
    stem = (content.question or content.poster_text or "").lower()
    if not stem:
        return None

    level = _classify_bloom(stem)
    if not level:
        return None
    label, desc = level
    return f"🎯 <b>Cognitive Level:</b> {label} — {desc}"


def _classify_bloom(stem: str) -> tuple[str, str] | None:
    recall = ["define", "list", "identify", "name", "state", "enumerate", "what is"]
    comprehend = ["explain", "describe", "differentiate", "distinguish", "classify", "summarize"]
    apply = ["diagnose", "manage", "treat", "prescribe", "calculate", "interpret"]
    analyze = ["compare", "contrast", "correlate", "analyze", "investigate", "evaluate"]

    if any(w in stem for w in analyze):
        return ("Analyzing", "Correlate findings to reach a diagnosis or conclusion.")
    if any(w in stem for w in apply):
        return ("Applying", "Apply clinical knowledge to decide management.")
    if any(w in stem for w in comprehend):
        return ("Understanding", "Explain or differentiate between concepts.")
    if any(w in stem for w in recall):
        return ("Remembering", "Direct recall of facts or classifications.")
    return None
