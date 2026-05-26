"""SmartContentEngine: spaced repetition, adaptive weak-topic resurfacing, MCQ variation, vignette generation."""
from __future__ import annotations

import json
import logging
import random
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import TYPE_CHECKING

from app.models import ContentFormat, GeneratedContent, Subject

if TYPE_CHECKING:
    from app.config import Settings

logger = logging.getLogger(__name__)

_SPACED_REPETITION_DAYS = 36500  # never repeat a seen topic (100 years)
_WEAK_TOPIC_COOLDOWN_DAYS = 3
_PERFORMANCE_DECAY_DAYS = 30

_MEMORY_ANCHOR_TEMPLATES = [
    "🧠 *Memory Anchor:* {anchor}",
    "💡 *Remember:* {anchor}",
    "📌 *Key Association:* {anchor}",
    "🔗 *Link it:* {anchor}",
    "🎯 *Exam Pearl:* {anchor}",
]

_CLINICAL_PEARL_TEMPLATES = [
    "⚡ *Revision Pearl:* {pearl}",
    "🏥 *Clinical Pearl:* {pearl}",
    "📋 *High-Yield Pearl:* {pearl}",
    "🩺 *Ward Round Pearl:* {pearl}",
]

_CONCEPT_CROSS_REF_TEMPLATES = [
    "\n\n🔗 *Related:* {topic} ({subject}) — {reason}",
    "\n\n📎 *Cross-Reference:* See also {topic} in {subject} — {reason}",
    "\n\n🔄 *Integrate:* Link to {topic} ({subject}) — {reason}",
]


_VARIATION_FORMATS = {
    ContentFormat.rapid_revision: ContentFormat.pyq_concept,
    ContentFormat.mcq: ContentFormat.rapid_revision,
    ContentFormat.concise_notes: ContentFormat.clinical_case,
    ContentFormat.pyq_concept: ContentFormat.rapid_revision,
}


class SmartContentEngine:
    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._history_path = Path("logs/topic_history.json")
        self._performance_path = Path("logs/performance.json")
        self._history: dict[str, str] = self._load_history()
        self._performance: dict[str, dict] = self._load_performance()

    def record_performance(
        self,
        title: str,
        correct: bool,
        subject: Subject | None = None,
    ) -> None:
        """Record learner performance on a topic for weak-topic tracking."""
        entry = self._performance.get(title, {"correct": 0, "incorrect": 0, "last_seen": None})
        if correct:
            entry["correct"] += 1
        else:
            entry["incorrect"] += 1
        entry["last_seen"] = datetime.now(tz=timezone.utc).isoformat()
        if subject:
            entry["subject"] = subject.value
        self._performance[title] = entry
        self._save_performance()

    def weak_topics(self, threshold: float = 0.6, min_attempts: int = 3) -> list[dict]:
        """Return topics with below-threshold accuracy for resurfacing."""
        now = datetime.now(tz=timezone.utc)
        weak: list[dict] = []
        for title, entry in self._performance.items():
            total = entry.get("correct", 0) + entry.get("incorrect", 0)
            if total < min_attempts:
                continue
            accuracy = entry["correct"] / total if total > 0 else 0
            if accuracy < threshold:
                last = entry.get("last_seen")
                days_since = (
                    (now - datetime.fromisoformat(last)).total_seconds() / 86400
                    if last else _PERFORMANCE_DECAY_DAYS
                )
                weak.append({
                    "title": title,
                    "accuracy": round(accuracy, 2),
                    "total_attempts": total,
                    "days_since_last_seen": round(days_since, 1),
                    "subject": entry.get("subject"),
                })
        return sorted(weak, key=lambda w: w["accuracy"])

    def generate_flashcard(self, subject: Subject) -> GeneratedContent | None:
        source = self._get_with_spaced_repetition(subject, ContentFormat.rapid_revision)
        if not source:
            source = self._get_with_spaced_repetition(subject, ContentFormat.concise_notes)
        if not source:
            return None
        content = GeneratedContent(
            title=f"Flashcard: {source.title}",
            caption=f"Flashcard based on: {source.title}\n\n{source.poster_text}"[:2000],
            hashtags=_swap_tag(source.hashtags, "", "Flashcard"),
            poster_text=f"What do you know about: {source.title}?"[:320],
            question=source.poster_text or source.title,
            correct_answer=(source.high_yield_takeaway or source.caption[:200])[:200],
            explanation=source.caption[:800],
            high_yield_takeaway=source.high_yield_takeaway,
            subject=source.subject,
            content_format=ContentFormat.flashcard,
            difficulty="medium",
            topic_tags=[source.subject.value if source.subject else "general"],
        )
        self._record(content)
        return content

    def generate_true_false(self, subject: Subject) -> GeneratedContent | None:
        pool = []
        try:
            from content.loader import get_library
            pool = get_library().pool(subject, None)
        except Exception:
            return None
        if not pool:
            return None

        source = random.choice(pool)
        takeaway = source.high_yield_takeaway or ""
        if not takeaway:
            return None

        facts = [f.strip() for f in takeaway.replace(";", ".").split(".") if len(f.strip()) > 15]
        if not facts:
            return None

        statement = random.choice(facts)
        explanation = f"This is a TRUE statement. {takeaway}"

        content = GeneratedContent(
            title=f"True/False: {source.title}",
            caption=f"True/False question based on: {source.title}"[:2000],
            hashtags=_swap_tag(source.hashtags, "", "TrueFalse"),
            poster_text=f"True or False: {statement}"[:320],
            question=statement,
            correct_answer="TRUE",
            explanation=explanation[:1600],
            high_yield_takeaway=source.high_yield_takeaway,
            subject=source.subject,
            content_format=ContentFormat.true_false,
            difficulty="easy",
            topic_tags=[source.subject.value if source.subject else "general"],
        )
        self._record(content)
        return content

    def generate_one_liner(self, subject: Subject) -> GeneratedContent | None:
        pool = []
        try:
            from content.loader import get_library
            pool = get_library().pool(subject, None)
        except Exception:
            return None

        candidates = [c for c in pool if c.high_yield_takeaway and len(c.high_yield_takeaway) > 20]
        if not candidates:
            return None

        source = random.choice(candidates)
        takeaway = source.high_yield_takeaway or ""

        words = takeaway.split()
        blank_idx = len(words) // 2
        answer = words[blank_idx] if words else "?"
        blanked = " ".join(w if i != blank_idx else "___" for i, w in enumerate(words))

        content = GeneratedContent(
            title=f"One-Liner: {source.title}",
            caption=f"One-liner recall from: {source.title}"[:2000],
            hashtags=_swap_tag(source.hashtags, "", "OneLiner"),
            poster_text=f"Fill in: {blanked}"[:320],
            question=blanked,
            correct_answer=answer[:200],
            explanation=takeaway[:1600],
            high_yield_takeaway=source.high_yield_takeaway,
            subject=source.subject,
            content_format=ContentFormat.one_liner_recall,
            difficulty="easy",
            topic_tags=[source.subject.value if source.subject else "general"],
        )
        self._record(content)
        return content

    def generate_daily_pack(self, count: int = 5) -> list[GeneratedContent]:
        subjects = list(Subject)
        random.shuffle(subjects)
        selected_subjects = subjects[:count]

        pack: list[GeneratedContent] = []
        formats = [
            ContentFormat.mcq,
            ContentFormat.rapid_revision,
            ContentFormat.true_false,
            ContentFormat.flashcard,
            ContentFormat.one_liner_recall,
        ]

        for i, subj in enumerate(selected_subjects):
            fmt = formats[i % len(formats)]
            if fmt == ContentFormat.flashcard:
                item = self.generate_flashcard(subj)
            elif fmt == ContentFormat.true_false:
                item = self.generate_true_false(subj)
            elif fmt == ContentFormat.one_liner_recall:
                item = self.generate_one_liner(subj)
            else:
                item = self.generate(subj, fmt)
            if item:
                pack.append(item)

        return pack

    def add_memory_anchor(self, content: GeneratedContent) -> GeneratedContent:
        """Append a memory anchor / mnemonic / visual association to the explanation."""
        subject_anchors: dict[str, list[str]] = {
            "anatomy": [
                "Radius is lateral in anatomical position — think 'R' for 'R'ight side.",
                "Facial nerve: 'Two Zeros, Two Toes' — temporal, zygomatic, buccal, mandibular, cervical.",
                "Carpal bones: 'She Looks Too Pretty, Try To Catch Her' — scaphoid, lunate, triquetrum, pisiform, trapezium, trapezoid, capitate, hamate.",
                "Brachial plexus: 'Randy Travis Drinks Cold Beer' — roots, trunks, divisions, cords, branches.",
            ],
            "physiology": [
                "Starling forces: 'Push (capillary hydrostatic) vs Pull (plasma oncotic)' — edema when push > pull.",
                "ECG lead II: 'Look for the P wave' — atrial depolarization, best seen in II.",
                "CO = HR × SV — cardiac output is heart rate times stroke volume.",
            ],
            "biochemistry": [
                "Glycolysis: 'Good Friends Always Help In Making ATP' — G-6-P, F-6-P, F-1,6-BP, GAP, 1,3-BPG, 3-PG, PEP, Pyruvate.",
                "Krebs cycle: 'Citrate Is A Kreb Substrate' — citrate, isocitrate, alpha-KG, succinyl-CoA, succinate, fumarate, malate, oxaloacetate.",
                "Ketone bodies: 'ABC' — Acetoacetate, Beta-hydroxybutyrate, Acetone.",
            ],
            "pathology": [
                "Robbins red flags: nuclear atypia, increased N:C ratio, hyperchromasia, pleomorphism = malignancy.",
                "Granuloma: 'Cheese (caseation) or no cheese' — TB has caseating, sarcoid has non-caseating.",
                "Metaplasia: 'One adult cell type replaces another' — Barrett's = squamous → columnar.",
            ],
            "pharmacology": [
                "Beta blockers: '-olol' suffix — think 'block the heart' (negative chrono/inotrope).",
                "Statins: 'HMG-CoA reductase inhibitors' — think 'Halt Makers of Cholesterol'.",
                "ACE inhibitors: '-pril' suffix — 'Pressure Reduction In Lungs' (also cough side effect).",
            ],
            "microbiology": [
                "Gram positive: 'Purple Positives' — Staph, Strep, Enterococcus, Clostridium.",
                "Gram negative: 'Pink Negatives' — E. coli, Klebsiella, Pseudomonas, Proteus.",
                "Acid-fast: 'Red Rods' — Mycobacterium (TB and leprosy).",
            ],
            "forensic_medicine": [
                "Drowning: 'Wet vs Dry' — wet (water in lungs) vs dry (laryngospasm, no water).",
                "Rigor mortis: 'Starts in 1-2 hours, develops fully by 12 hours, resolves by 24-48'.",
                "Postmortem lividity: 'Fixed vs non-fixed' — test with thumb pressure; fixed = 8+ hours.",
            ],
            "community_medicine": [
                "OPD = Out Patient Department; IPD = In Patient Department.",
                "Incidence = new cases in time period; Prevalence = total existing cases.",
                "Vaccination: 'BCG at birth, OPV/Pentavalent at 6, 10, 14 weeks'.",
            ],
            "general_medicine": [
                "Hypertension: '3 Ps' — Prevention, Pharmacotherapy, Lifestyle modification.",
                "Diabetes: '3 Ps' — Polyuria, Polydipsia, Polyphagia.",
                "Pneumonia: CURB-65 — Confusion, Urea >7, RR >30, BP <90/60, age >65.",
            ],
            "general_surgery": [
                "Acute abdomen: 'Think 6 Fs' — Flatulence, Feces, Foreign body, Fetus, Fat, Fluid (in that order of likelihood).",
                "Boas' sign: hyperesthesia below right scapula = acute cholecystitis.",
                "Cullen's sign: periumbilical ecchymosis = pancreatitis/ectopic pregnancy rupture.",
            ],
            "obstetrics_gynecology": [
                "NA (not applicable)",
                "Fundal height in cm = weeks of gestation after 20 weeks.",
                "APGAR: Appearance, Pulse, Grimace, Activity, Respiration — at 1 and 5 minutes.",
            ],
            "pediatrics": [
                "Birth weight: '3-2.5-1.5' — normal >2.5 kg, LBW <2.5, VLBW <1.5.",
                "Denver chart: 'Smile at 2 months, sit at 6 months, stand at 12 months, speak at 18 months'.",
                "BCG scar = immunity not guaranteed but good indicator of vaccination.",
            ],
            "ophthalmology": [
                "Red eye: 'Painless vs Painful' — conjunctivitis (painless) vs keratitis/glaucoma/iritis (painful).",
                "Cataract: 'Painless progressive vision loss' — lens opacity, treat with surgery.",
                "Glaucoma: 'Silent thief of sight' — open angle is painless, closed angle is painful/red.",
            ],
            "ent": [
                "Hearing loss: 'Conductive vs Sensorineural' — Rinne and Weber tests differentiate.",
                "Tonsillitis: 'McIsaac criteria' — fever, cough absent, exudate, nodes, age 3-14.",
                "Vertigo: 'BPPV vs Meniere's' — positional vs episodic + tinnitus.",
            ],
            "orthopedics": [
                "Fracture: 'Open vs Closed' — open = skin breached, closed = skin intact.",
                "Compartment syndrome: '5 Ps' — Pain (out of proportion), Pallor, Pulselessness, Paresthesia, Paralysis.",
                "Osteoarthritis: 'Weight bearing joints' — hip, knee, spine; Heberden's nodes (DIP).",
            ],
            "dermatology": [
                "ABCDE of melanoma: Asymmetry, Border irregular, Color variegated, Diameter >6mm, Evolution.",
                "Psoriasis: 'Auspitz sign' — pinpoint bleeding on scale removal; Koebner phenomenon.",
                "Eczema: 'Itchy rash' — flexor distribution, atopic triad (asthma, hay fever, eczema).",
            ],
            "psychiatry": [
                "Depression: 'SIGECAPS' — Sleep, Interest, Guilt, Energy, Concentration, Appetite, Psychomotor, Suicidal.",
                "Mania: 'DIGFAST' — Distractibility, Irresponsibility, Grandiosity, Flight of ideas, Activity increased, Sleep deficit, Talkativeness.",
                "Schizophrenia: 'Positive (hallucinations/delusions) vs Negative (flat affect/avolition)'.",
            ],
            "radiology": [
                "Chest X-ray: 'ABCDE' — Airway, Bones, Cardiac, Diaphragm, Effusions/fields.",
                "CT scan: 'White = bone/contrast, Gray = soft tissue, Black = air/fat'.",
                "Ultrasound: 'Anechoic (black) = fluid, Hyperechoic (white) = stone/calcium'.",
            ],
            "anesthesiology": [
                "Airway: 'Mallampati classification' — I-IV, higher = more difficult intubation.",
                "ASA classification: 'A healthy, B mild, C severe, D life-threatening, E moribund'.",
                "LA toxicity: 'CNS first (perioral numbness, seizures) then CVS (arrhythmias, arrest)'.",
            ],
        }

        if not content.explanation:
            return content

        subj_key = content.subject.value if content.subject else "general_medicine"
        anchors = subject_anchors.get(subj_key, [
            "Focus on the key clinical clue and link it to management.",
            "High-yield topics repeat — master the classic presentation.",
        ])
        anchor = random.choice(anchors)
        if anchor in ("NA (not applicable)",):
            return content

        template = random.choice(_MEMORY_ANCHOR_TEMPLATES)
        anchor_text = template.format(anchor=anchor)
        content.explanation = (content.explanation + "\n\n" + anchor_text)[:2000]
        return content

    def add_clinical_pearl(self, content: GeneratedContent) -> GeneratedContent:
        """Append a clinical pearl/high-yield point to the explanation."""
        general_pearls = [
            "Always look for the key clinical clue before jumping to management.",
            "Classic presentation + risk factors = most likely diagnosis.",
            "Know the close mimics — they are the most common distractors.",
            "Treatment follows diagnosis — invest time in differentials.",
            "Vital signs + focused examination narrow 90% of differentials.",
            "Investigations confirm, not replace, clinical suspicion.",
            "Red flags: unilateral symptoms, systemic features, rapid progression.",
            "Always check for drug interactions before prescribing.",
            "Pediatric doses are weight-based — never guess.",
            "In emergencies, ABC (Airway, Breathing, Circulation) comes first.",
        ]
        if content.high_yield_takeaway:
            pearl = content.high_yield_takeaway[:80]
        else:
            pearl = random.choice(general_pearls)
        template = random.choice(_CLINICAL_PEARL_TEMPLATES)
        pearl_text = template.format(pearl=pearl)
        if content.explanation:
            content.explanation = (content.explanation + "\n\n" + pearl_text)[:2000]
        return content

    def add_concept_cross_reference(self, content: GeneratedContent) -> GeneratedContent:
        """Link related concepts across subjects for integrated learning."""
        cross_refs: dict[str, list[tuple[str, str, str]]] = {
            "general_medicine": [("Cardiac Biomarkers", "biochemistry", "Troponin is the gold standard for MI")],
            "pathology": [("Tumor Markers", "biochemistry", "CEA for colon, AFP for liver, PSA for prostate")],
            "pharmacology": [("Drug Metabolism", "biochemistry", "CYP450 enzyme system — phase I and II reactions")],
            "general_surgery": [("Wound Healing", "pathology", "Primary vs secondary intention healing")],
            "obstetrics_gynecology": [("Placental Hormones", "physiology", "hCG, progesterone, estrogen in pregnancy")],
            "pediatrics": [("Congenital Heart Disease", "anatomy", "Embryologic development of septa and valves")],
            "ophthalmology": [("Visual Pathway", "anatomy", "Optic nerve → optic chiasm → optic tract → occipital")],
            "ent": [("Branchial Arches", "anatomy", "First arch = mandible, incus, malleus")],
            "orthopedics": [("Bone Healing", "pathology", "Inflammatory → soft callus → hard callus → remodeling")],
            "psychiatry": [("Neurotransmitters", "pharmacology", "Serotonin (mood), Dopamine (psychosis), GABA (anxiety)")],
            "dermatology": [("Skin Layers", "anatomy", "Epidermis (5 layers), dermis, hypodermis")],
            "radiology": [("Contrast Media", "pharmacology", "Iodinated for CT, gadolinium for MRI")],
            "anesthesiology": [("Neuromuscular Blockers", "pharmacology", "Depolarizing vs non-depolarizing")],
            "community_medicine": [("Epidemiology Measures", "physiology", "Incidence vs prevalence, sensitivity vs specificity")],
            "forensic_medicine": [("Thanatology", "pathology", "Postmortem changes and time since death estimation")],
            "microbiology": [("Antimicrobial Resistance", "pharmacology", "MRSA, ESBL, Carbapenemase — mechanisms and management")],
        }
        subj_key = content.subject.value if content.subject else "general_medicine"
        refs = cross_refs.get(subj_key, [])
        if not refs:
            return content
        ref = random.choice(refs)
        template = random.choice(_CONCEPT_CROSS_REF_TEMPLATES)
        ref_text = template.format(topic=ref[0], subject=ref[1], reason=ref[2])
        if content.explanation:
            content.explanation = (content.explanation + ref_text)[:2000]
        return content

    def enhance_educational_quality(self, content: GeneratedContent) -> GeneratedContent:
        """Apply memory anchors, clinical pearls, and cross-references to a piece of content."""
        content = self.add_memory_anchor(content)
        if random.random() < 0.5:
            content = self.add_clinical_pearl(content)
        if random.random() < 0.3:
            content = self.add_concept_cross_reference(content)
        return content

    def generate(
        self,
        subject: Subject,
        content_format: ContentFormat,
    ) -> GeneratedContent | None:
        """Return content with adaptive spaced repetition. Falls back to variations."""
        content = self._get_with_spaced_repetition(subject, content_format)
        if content:
            content = self.enhance_educational_quality(content)
            self._record(content)
            return content

        variation = self._generate_variation(subject)
        if variation:
            variation = self.enhance_educational_quality(variation)
            self._record(variation)
            return variation

        return None

    _dedup_recent: set[str] = set()

    def generate_variate_mcq(
        self,
        subject: Subject,
        difficulty: str | None = None,
    ) -> GeneratedContent | None:
        """MCQ variation engine: rewrite stem, reorder options, assign difficulty, enrich with analysis."""
        try:
            from content.loader import get_library
            pool = get_library().pool(subject, ContentFormat.mcq)
        except Exception:
            return None
        if not pool:
            return None

        unseen = [c for c in pool if c.title not in self._dedup_recent]
        pool = unseen if unseen else pool
        source = random.choice(pool)
        self._dedup_recent.add(source.title)
        if len(self._dedup_recent) > 100:
            self._dedup_recent = set(list(self._dedup_recent)[-50:])
        stem = source.question or source.poster_text or ""
        if not stem:
            return None

        reworded = self._mcq_variate_stem(stem)
        options, correct_idx = self._mcq_variate_options(source)

        assigned_difficulty = difficulty or self.difficulty_for_topic(source.title)

        content = GeneratedContent(
            title=f"{source.title} (Variant)",
            caption=f"Variation: {source.title}"[:2000],
            hashtags=_swap_tag(source.hashtags, "MCQ", "MCQVariant"),
            poster_text=f"Variant: {source.poster_text}"[:320],
            question=reworded[:1200],
            options=options,
            correct_answer=options[correct_idx][:200] if options else source.correct_answer[:200],
            explanation=source.explanation[:1600] if source.explanation else None,
            high_yield_takeaway=source.high_yield_takeaway,
            subject=source.subject,
            content_format=ContentFormat.mcq,
            difficulty=assigned_difficulty,
            topic_tags=[source.subject.value if source.subject else "general"],
        )
        content = self.enrich_mcq_with_analysis(content)

        # Validate vignette quality
        issue = self.validate_mcq_vignette(content)
        if issue:
            logger.debug("MCQ vignette issue for %s: %s", content.title, issue)

        self._record(content)
        return content

    def difficulty_for_topic(self, title: str) -> str:
        """Assign a difficulty tier based on performance history."""
        perf = self._performance.get(title, {})
        total = perf.get("correct", 0) + perf.get("incorrect", 0)
        if total < 3:
            return "moderate"
        accuracy = perf["correct"] / total
        if accuracy < 0.4:
            return "exam_level"
        if accuracy < 0.7:
            return "moderate"
        return "easy"

    def validate_mcq_vignette(self, content: "GeneratedContent") -> str | None:
        """Check if MCQ stem is a proper 6-7 line clinical vignette."""
        from app.models import ContentFormat
        if content.content_format != ContentFormat.mcq:
            return None
        stem = content.question or ""
        if not stem:
            return "Missing question stem"
        line_count = len(stem.split(". "))
        if line_count < 3:
            return "Vignette too short — expected 3-7 clinical details"
        if line_count > 10:
            return "Vignette too long — expected 3-7 clinical details"
        key_indicators = ["year-old", "presents", "history", "examination", "complaints"]
        found = sum(1 for k in key_indicators if k.lower() in stem.lower())
        if found < 2:
            return f"Vignette lacks clinical details — found {found}/5 expected indicators"
        if not content.options or len(content.options) < 3:
            return "Need 4 options for MCQ"
        if not content.correct_answer:
            return "Missing correct answer"
        return None

    def enrich_mcq_with_analysis(self, content: "GeneratedContent") -> "GeneratedContent":
        """Add realistic wrong-option analysis with clinical reasoning for each distractor."""
        from app.models import GeneratedContent
        if content.content_format.value != "mcq" or not content.options or not content.correct_answer:
            return content

        wrong_options = [o for o in content.options if o != content.correct_answer]
        if not wrong_options:
            return content

        analysis_parts = ["\n\n<b>Why other options are wrong:</b>"]

        _distractor_reasons = [
            "This is a close mimic but lacks the {key} feature seen in the correct answer.",
            "This option describes {alt_condition}, which presents differently — look for {key}.",
            "Common confusion: this is seen in {alt_condition}, not in this clinical scenario.",
            "While this may be considered, the absence of {key} makes it less likely.",
            "This is a known distractor — it is associated with {alt_condition}, not this presentation.",
            "Tempting but incorrect: the timeline and clinical clues point away from this.",
            "This would be correct if {key} were present, but it is not described here.",
            "Classic NEET PG trap: students pick this because it sounds similar, but the key clue is {key}.",
        ]

        for opt in wrong_options:
            label = opt.split(".", 1)[0].strip() if ". " in opt else "?"
            opt_text = opt.split(". ", 1)[1] if ". " in opt else opt
            alt_condition = opt_text.split(",")[0].strip()[:40] if opt_text else "another condition"
            key_clue = content.title.split(" —")[0] if " —" in content.title else content.title[:40]
            reason = random.choice(_distractor_reasons).format(
                key=key_clue,
                alt_condition=alt_condition,
            )
            analysis_parts.append(f"• <b>{label}.</b> {opt_text[:80]} — {reason}")

        new_explanation = (content.explanation or "") + "\n".join(analysis_parts)
        content.explanation = new_explanation[:2000]
        return content

    def stats(self) -> dict:
        try:
            from content.loader import get_library
            lib = get_library()
            summary = lib.summary()
            total_lib = lib.total()
        except Exception:
            summary = {}
            total_lib = 0

        sent = set(self._history.keys())
        unseen = max(0, total_lib - len(sent))

        now = datetime.now(tz=timezone.utc)
        cutoff = now - timedelta(days=_SPACED_REPETITION_DAYS)
        recent = sum(
            1 for ts in self._history.values()
            if datetime.fromisoformat(ts) >= cutoff
        )

        weak_list = self.weak_topics()
        return {
            "library_topics": total_lib,
            "topics_sent": len(sent),
            "topics_unseen": unseen,
            "sent_last_7_days": recent,
            "weak_topics_count": len(weak_list),
            "weak_topics": weak_list[:10],
            "by_subject": summary,
        }

    # ── Internal helpers ───────────────────────────────────────────────────────

    def _get_with_spaced_repetition(
        self,
        subject: Subject,
        content_format: ContentFormat,
    ) -> GeneratedContent | None:
        try:
            from content.loader import get_library
            lib = get_library()
        except Exception as exc:
            logger.debug("Content library unavailable: %s", exc)
            return None

        now = datetime.now(tz=timezone.utc)
        pool = lib.pool(subject, content_format)
        if not pool:
            pool = lib.pool(subject, None)

        if not pool:
            return None

        seen = self._history
        performance = self._performance

        def cooldown_days(title: str) -> int:
            perf = performance.get(title, {})
            total = perf.get("correct", 0) + perf.get("incorrect", 0)
            if total >= 3:
                accuracy = perf["correct"] / total
                if accuracy < 0.6:
                    return _WEAK_TOPIC_COOLDOWN_DAYS
            return _SPACED_REPETITION_DAYS

        def is_available(title: str) -> bool:
            ts = seen.get(title)
            if not ts:
                return True
            try:
                last = datetime.fromisoformat(ts)
                return (now - last).total_seconds() / 3600 >= cooldown_days(title) * 24
            except (ValueError, TypeError):
                return True

        available = [c for c in pool if is_available(c.title) and c.title not in self._dedup_recent]

        if available:
            weak_candidates = []
            for c in available:
                perf = performance.get(c.title, {})
                total = perf.get("correct", 0) + perf.get("incorrect", 0)
                if total >= 3 and perf["correct"] / total < 0.6:
                    weak_candidates.append(c)
            if weak_candidates:
                return random.choice(weak_candidates)
            return random.choice(available)

        if pool:
            def _last_seen(c: GeneratedContent) -> datetime:
                ts = seen.get(c.title)
                if ts:
                    try:
                        return datetime.fromisoformat(ts)
                    except (ValueError, TypeError):
                        pass
                return datetime.min.replace(tzinfo=timezone.utc)

            return min(pool, key=_last_seen)

        return None

    def _generate_variation(self, subject: Subject) -> GeneratedContent | None:
        try:
            from content.loader import get_library
            lib = get_library()
        except Exception:
            return None

        pool = lib.pool(subject, None)
        if not pool:
            return None

        source = random.choice(pool)
        target_format = _VARIATION_FORMATS.get(source.content_format)
        if not target_format:
            return None

        if source.content_format == ContentFormat.rapid_revision:
            return self._rapid_to_pyq(source)
        if source.content_format == ContentFormat.mcq:
            return self._mcq_to_rapid(source)
        if source.content_format in (ContentFormat.concise_notes, ContentFormat.pyq_concept):
            return self._notes_to_case(source)
        return None

    def _rapid_to_pyq(self, source: GeneratedContent) -> GeneratedContent:
        intro = (
            "NEET-PG repeatedly tests this topic. "
            "Know the classic clue, the close mimic, and the one-liner takeaway.\n\n"
        )
        return GeneratedContent(
            title=f"{source.title} — PYQ Pattern",
            caption=(intro + source.caption)[:2000],
            hashtags=_swap_tag(source.hashtags, "RapidRevision", "PYQ"),
            poster_text=f"Previous year pattern: {source.poster_text}"[:320],
            image_prompt=source.image_prompt,
            high_yield_takeaway=source.high_yield_takeaway,
            subject=source.subject,
            content_format=ContentFormat.pyq_concept,
            post_lane=source.post_lane,
        )

    def _mcq_to_rapid(self, source: GeneratedContent) -> GeneratedContent:
        base = source.explanation or source.caption
        intro = f"Key concept from MCQ: {source.title}\n\n"
        caption = (intro + base)[:2000]
        return GeneratedContent(
            title=f"{source.title} — Rapid Notes",
            caption=caption,
            hashtags=_swap_tag(source.hashtags, "MCQ", "RapidRevision"),
            poster_text=f"Concept: {source.poster_text}"[:320],
            high_yield_takeaway=source.high_yield_takeaway,
            subject=source.subject,
            content_format=ContentFormat.rapid_revision,
            post_lane=source.post_lane,
        )

    def _notes_to_case(self, source: GeneratedContent) -> GeneratedContent:
        """Enhanced clinical vignette generation with multi-sentence patient scenario."""
        lines = [
            l.strip()[2:] for l in source.caption.split("\n")
            if l.strip().startswith("• ")
        ]
        clue = lines[0] if lines else source.poster_text

        ages = [28, 35, 42, 55, 60, 65, 22, 48, 70]
        settings = [
            "the emergency department",
            "a busy outpatient clinic",
            "the ward round",
            "a primary health centre",
            "a medical camp in a rural area",
        ]
        age = random.choice(ages)
        setting = random.choice(settings)
        gender = random.choice(["male", "female"])

        duration = random.choice([
            "2 days", "1 week", "3 weeks", "over the past month",
            "gradually over 6 months", "acutely over 6 hours",
        ])

        finding = clue[:60]
        scenario = (
            f"A {age}-year-old {gender} presents to {setting} with a {duration} history "
            f"of symptoms suggestive of {source.title.replace(' —', ',').split(',')[0].lower()}. "
            f"On examination, the key finding is: {finding}. "
            f"Based on the clinical presentation and findings, "
            f"what is the most appropriate next step in management?"
        )
        discussion = (source.high_yield_takeaway or "") + "\n\n" + source.caption
        return GeneratedContent(
            title=f"{source.title} — Case",
            caption=f"Clinical case based on: {source.title}\n\n{source.poster_text}"[:2000],
            hashtags=_swap_tag(source.hashtags, "ConciseNotes", "ClinicalCase"),
            poster_text=f"Case: {source.poster_text}"[:320],
            question=scenario[:1200],
            correct_answer=f"Investigate and manage {source.title}"[:200],
            explanation=discussion[:1600],
            high_yield_takeaway=source.high_yield_takeaway,
            subject=source.subject,
            content_format=ContentFormat.clinical_case,
            post_lane=source.post_lane,
        )

    def _mcq_variate_stem(self, stem: str) -> str:
        """Reword an MCQ stem for variation while preserving clinical meaning."""
        swaps = [
            (r"\bpresents with\b", "comes with complaints of"),
            (r"\bpatient\b", "person"),
            (r"\bmost likely\b", "most probable"),
            (r"\bappropriate\b", "suitable"),
            (r"\bdue to\b", "attributed to"),
            (r"\bhistory of\b", "past history of"),
            (r"\bshows\b", "demonstrates"),
            (r"\bindicates\b", "suggests"),
            (r"\bdiagnosis\b", "underlying condition"),
            (r"\bmanagement\b", "treatment approach"),
        ]
        result = stem
        for pattern, replacement in swaps:
            result = re.sub(pattern, replacement, result, count=1, flags=re.IGNORECASE)
        return result

    def _mcq_variate_options(
        self,
        source: GeneratedContent,
    ) -> tuple[list[str], int]:
        """Reorder MCQ options and return (shuffled_options, correct_index)."""
        options = list(source.options or [])
        if len(options) < 2:
            return options, 0

        correct = source.correct_answer or ""
        correct_idx = 0
        for i, opt in enumerate(options):
            label = opt.split(".", 1)[0].strip().upper() if ". " in opt else ""
            if label and label == correct[0]:
                correct_idx = i
                break
            if opt.strip() == correct.strip():
                correct_idx = i
                break

        correct_val = options[correct_idx]
        others = [o for i, o in enumerate(options) if i != correct_idx]
        random.shuffle(others)
        insert_pos = random.randint(0, len(others))
        new_options = others[:insert_pos] + [correct_val] + others[insert_pos:]

        labels = ["A", "B", "C", "D"]
        new_labeled = []
        for i, opt in enumerate(new_options):
            text = opt.split(". ", 1)[1] if ". " in opt else opt
            label = labels[i] if i < len(labels) else chr(65 + i)
            new_labeled.append(f"{label}. {text}")
            if opt == correct_val:
                correct_idx = i

        new_correct = new_labeled[correct_idx] if new_labeled else correct[:200]
        return [n[:200] for n in new_labeled], correct_idx

    def _record(self, content: GeneratedContent) -> None:
        self._history[content.title] = datetime.now(tz=timezone.utc).isoformat()
        self._save_history()

    def _load_history(self) -> dict[str, str]:
        if self._history_path.exists():
            try:
                return json.loads(self._history_path.read_text(encoding="utf-8"))
            except Exception as exc:
                logger.warning("Could not read topic history: %s", exc)
        return {}

    def _save_history(self) -> None:
        try:
            self._history_path.parent.mkdir(parents=True, exist_ok=True)
            self._history_path.write_text(
                json.dumps(self._history, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as exc:
            logger.warning("Could not save topic history: %s", exc)

    def _load_performance(self) -> dict[str, dict]:
        if self._performance_path.exists():
            try:
                return json.loads(self._performance_path.read_text(encoding="utf-8"))
            except Exception as exc:
                logger.warning("Could not read performance data: %s", exc)
        return {}

    def _save_performance(self) -> None:
        try:
            self._performance_path.parent.mkdir(parents=True, exist_ok=True)
            self._performance_path.write_text(
                json.dumps(self._performance, indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        except Exception as exc:
            logger.warning("Could not save performance data: %s", exc)


def _swap_tag(tags: list[str], old: str, new: str) -> list[str]:
    result = []
    replaced = False
    for t in tags:
        if old.lower() in t.lower() and not replaced:
            result.append(f"#{new}")
            replaced = True
        else:
            result.append(t)
    if not replaced:
        result.append(f"#{new}")
    return result
