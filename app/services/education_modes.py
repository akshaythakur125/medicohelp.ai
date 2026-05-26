from __future__ import annotations

import random
from typing import Optional

from app.models import (
    FIRST_YEAR_SUBJECTS,
    FINAL_YEAR_SUBJECTS,
    NEET_PG_CORE_SUBJECTS,
    EMERGENCY_5_MIN_FORMATS,
    ContentFormat,
    EducationMode,
    Subject,
)


def get_mode_subjects(mode: EducationMode) -> set[Subject]:
    mapping: dict[EducationMode, set[Subject]] = {
        EducationMode.comprehensive: set(Subject),
        EducationMode.first_year_mbbs: FIRST_YEAR_SUBJECTS,
        EducationMode.final_year_revision: FINAL_YEAR_SUBJECTS,
        EducationMode.neet_pg_revision: NEET_PG_CORE_SUBJECTS,
        EducationMode.inicet_high_yield: NEET_PG_CORE_SUBJECTS,
        EducationMode.emergency_5_min: set(Subject),
    }
    return mapping.get(mode, set(Subject))


def get_mode_formats(mode: EducationMode) -> set[ContentFormat]:
    if mode == EducationMode.emergency_5_min:
        return EMERGENCY_5_MIN_FORMATS
    if mode in (EducationMode.final_year_revision, EducationMode.neet_pg_revision, EducationMode.inicet_high_yield):
        return {
            ContentFormat.mcq,
            ContentFormat.image_based_question,
            ContentFormat.concise_notes,
            ContentFormat.clinical_case,
            ContentFormat.rapid_revision,
            ContentFormat.flashcard,
            ContentFormat.true_false,
            ContentFormat.one_liner_recall,
        }
    if mode == EducationMode.first_year_mbbs:
        return {
            ContentFormat.concise_notes,
            ContentFormat.flashcard,
            ContentFormat.rapid_revision,
            ContentFormat.mcq,
            ContentFormat.true_false,
            ContentFormat.mnemonic,
            ContentFormat.one_liner_recall,
        }
    return set(ContentFormat)


def get_mode_description(mode: EducationMode) -> str:
    descriptions = {
        EducationMode.comprehensive: (
            "📚 *Comprehensive Mode*\nAll 19 MBBS subjects — full revision curriculum."
        ),
        EducationMode.first_year_mbbs: (
            "📗 *First Year MBBS Mode*\nAnatomy, Physiology, Biochemistry — foundation focus."
        ),
        EducationMode.final_year_revision: (
            "📘 *Final Year Revision Mode*\nMedicine, Surgery, OBG, Pediatrics — clinical prep."
        ),
        EducationMode.neet_pg_revision: (
            "📕 *NEET PG Revision Mode*\nCore clinical subjects — high-yield PG prep."
        ),
        EducationMode.inicet_high_yield: (
            "📙 *INICET High-Yield Mode*\nExam-focused rapid revision for INICET."
        ),
        EducationMode.emergency_5_min: (
            "⏱️ *Emergency 5-Min Revision Mode*\nUltra-rapid flashcards, mnemonics & one-liners."
        ),
    }
    return descriptions.get(mode, "📚 *Comprehensive Mode*")


def select_mode_subject(
    mode: EducationMode,
    weak_subjects: list[Subject],
    recent_subjects: list[Subject],
) -> Optional[Subject]:
    allowed = get_mode_subjects(mode)
    if not allowed:
        return None
    if weak_subjects:
        weak_allowed = [s for s in weak_subjects if s in allowed and s not in recent_subjects]
        if weak_allowed and random.random() < 0.25:
            return random.choice(weak_allowed)
    pool = [s for s in allowed if s not in recent_subjects]
    if not pool:
        pool = list(allowed)
    return random.choice(pool) if pool else None
