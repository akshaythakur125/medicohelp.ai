"""High-yield Obstetrics & Gynecology content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ───────────────────────────────────────────────────────
    {
        "title": "Pre-eclampsia vs Eclampsia — Key Differentiators",
        "subject": Subject.obstetrics_gynecology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Pre-eclampsia: HTN + proteinuria after 20 wks. Eclampsia = + seizures.",
        "caption": (
            "Pre-eclampsia vs Eclampsia — Rapid Revision\n\n"
            "Pre-eclampsia:\n"
            "• BP ≥140/90 mmHg on ≥2 occasions, 4 hrs apart, after 20 weeks\n"
            "• Proteinuria ≥300 mg/24 hrs OR PCR ≥0.3 OR dipstick 2+\n"
            "• WITHOUT proteinuria if: thrombocytopenia, renal insufficiency, impaired liver function, pulmonary oedema, new-onset headache or visual symptoms\n"
            "• Severe features: BP ≥160/110, platelets <100,000, Cr >1.1 mg/dL, doubling of LFTs, pulmonary oedema, new-onset headache\n\n"
            "Eclampsia:\n"
            "• Pre-eclampsia + generalised tonic-clonic seizures NOT attributed to other causes\n"
            "• Can occur antepartum (50%), intrapartum (25%), postpartum (25%)\n"
            "• Postpartum eclampsia can occur up to 4 weeks after delivery\n\n"
            "Management of Eclampsia:\n"
            "• MgSO4 (Pritchard/Zuspan regimen) — drug of choice for seizure prophylaxis & treatment\n"
            "• Loading dose: 4 g IV over 20 min + 10 g IM (Pritchard)\n"
            "• Antihypertensive: Labetalol IV, Hydralazine IV, or Nifedipine oral\n"
            "• Definitive treatment: Delivery\n\n"
            "HELLP Syndrome:\n"
            "• Haemolysis, Elevated Liver enzymes, Low Platelets\n"
            "• Platelets <100,000; LDH >600 IU/L; AST >70 IU/L\n"
            "• Delivery is definitive treatment regardless of gestation\n\n"
            "⚠️ Exam Trap: MgSO4 toxicity → absent patellar reflex (first sign); antidote = 10% calcium gluconate IV."
        ),
        "high_yield_takeaway": "Eclampsia = pre-eclampsia + seizures. MgSO4 is DOC. Antidote for MgSO4 toxicity = calcium gluconate.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ObsGyn", "#PreEclampsia"],
    },
    {
        "title": "Placenta Previa vs Abruptio Placentae — Comparison",
        "subject": Subject.obstetrics_gynecology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Previa: painless PV bleed. Abruption: painful, concealed/revealed bleed.",
        "caption": (
            "Placenta Previa vs Abruptio Placentae\n\n"
            "Placenta Previa:\n"
            "• Placenta implanted in lower uterine segment, partially or completely covering internal os\n"
            "• Bleeding: Painless, bright red, revealed, RECURRENT\n"
            "• Uterus: Soft, non-tender\n"
            "• Fetal parts: Malpresentation common (transverse lie, breech)\n"
            "• Fetal heart: Usually normal\n"
            "• Diagnosis: USG (TVS most accurate — 100% sensitivity)\n"
            "• Management: Expectant if <36 wks (no PV exam!); C-section is delivery of choice\n\n"
            "Abruptio Placentae (Accidental Haemorrhage):\n"
            "• Premature separation of normally situated placenta after 20 weeks\n"
            "• Bleeding: Painful (constant pain), may be concealed (80% revealed, 20% concealed)\n"
            "• Uterus: Rigid, board-like tenderness ('Woody hard uterus')\n"
            "• Fetal heart: Often absent (fetal distress/death)\n"
            "• Complications: DIC, Couvelaire uterus (uteroplacental apoplexy), renal cortical necrosis\n"
            "• Risk factors: HTN, trauma, smoking, cocaine, short umbilical cord, previous abruption\n\n"
            "Grades of Abruption (Page's Classification):\n"
            "• Grade 0: Asymptomatic (diagnosed retrospectively)\n"
            "• Grade 1: Mild bleeding, no fetal distress\n"
            "• Grade 2: Moderate, fetal distress present\n"
            "• Grade 3: Severe; fetal death; may have coagulopathy\n\n"
            "⚠️ Exam Trap: Concealed abruption is the most dangerous — no external bleeding but severe internal haemorrhage and DIC risk."
        ),
        "high_yield_takeaway": "Previa = painless, soft uterus. Abruption = painful, woody-hard uterus. DIC is the dreaded complication of abruption.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ObsGyn", "#AntepartumHaemorrhage"],
    },
    # ── MCQ ──────────────────────────────────────────────────────────────────
    {
        "title": "PCOS Diagnostic Criteria — MCQ",
        "subject": Subject.obstetrics_gynecology,
        "content_format": ContentFormat.mcq,
        "poster_text": "Rotterdam criteria: 2 of 3 — oligo-ovulation, hyperandrogenism, PCO morphology.",
        "caption": (
            "MCQ: PCOS Diagnostic Criteria\n\n"
            "A 24-year-old woman presents with irregular periods (cycles of 40–60 days) for 2 years, "
            "increased facial hair, and acne. Pelvic USG shows bilateral enlarged ovaries with 14 follicles "
            "measuring 2–9 mm in each ovary arranged peripherally. Serum testosterone is mildly elevated. "
            "Which set of criteria is used to diagnose her condition?\n\n"
            "A. NIH criteria (1990) — requires both oligo-ovulation AND hyperandrogenism\n"
            "B. Rotterdam criteria (2003) — requires 2 of 3: oligo-ovulation, hyperandrogenism, or polycystic ovaries on USG\n"
            "C. Androgen Excess Society criteria (2006) — hyperandrogenism is mandatory\n"
            "D. WHO criteria — requires only elevated LH:FSH ratio >2:1"
        ),
        "question": (
            "A 24-year-old woman presents with irregular periods (cycles of 40–60 days) for 2 years, "
            "increased facial hair, and acne. Pelvic USG shows bilateral enlarged ovaries with 14 follicles "
            "measuring 2–9 mm in each ovary arranged peripherally. Serum testosterone is mildly elevated. "
            "Which set of criteria is used to diagnose her condition?"
        ),
        "options": [
            "A. NIH criteria (1990) — requires both oligo-ovulation AND hyperandrogenism",
            "B. Rotterdam criteria (2003) — requires 2 of 3: oligo-ovulation, hyperandrogenism, or polycystic ovaries on USG",
            "C. Androgen Excess Society criteria (2006) — hyperandrogenism is mandatory",
            "D. WHO criteria — requires only elevated LH:FSH ratio >2:1",
        ],
        "correct_answer": "B. Rotterdam criteria (2003) — requires 2 of 3: oligo-ovulation, hyperandrogenism, or polycystic ovaries on USG",
        "explanation": (
            "The Rotterdam criteria (2003), endorsed by ESHRE/ASRM, are the most widely used and accepted globally. "
            "Diagnosis requires at least 2 of 3 features: (1) oligo- or anovulation, (2) clinical or biochemical hyperandrogenism, "
            "and (3) polycystic ovarian morphology on USG (≥12 follicles 2–9 mm per ovary or ovarian volume >10 mL). "
            "This patient satisfies all three criteria. The NIH 1990 criteria are stricter (both oligo-ovulation AND hyperandrogenism mandatory). "
            "The Androgen Excess Society criteria mandate hyperandrogenism as an obligatory feature. "
            "PCOS is the most common endocrine disorder in reproductive-age women, affecting 6–12%, and is a frequent NEET-PG topic."
        ),
        "high_yield_takeaway": "Rotterdam 2003 = most used PCOS criteria: 2 of 3 (oligo-anovulation, hyperandrogenism, PCO morphology on USG).",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ObsGyn", "#PCOS"],
    },
    {
        "title": "Partograph Interpretation — MCQ",
        "subject": Subject.obstetrics_gynecology,
        "content_format": ContentFormat.mcq,
        "poster_text": "Alert line = 1 cm/hr. Action line = 4 hrs to right of alert line.",
        "caption": (
            "MCQ: Partograph Interpretation\n\n"
            "A primigravida at 39 weeks is in active labour. At 10:00 AM her cervical dilatation is 4 cm. "
            "On partograph, her cervical dilatation plot crosses the alert line at 2:00 PM but remains "
            "between the alert and action lines. By 6:00 PM the cervix is 8 cm and the plot has now "
            "crossed the action line. What is the most appropriate next step?\n\n"
            "A. Continue expectant management and reassess after 2 hours\n"
            "B. Perform immediate caesarean section for failure to progress\n"
            "C. Evaluate the cause, consider augmentation or operative delivery as indicated\n"
            "D. Administer tocolytics and allow further trial of labour"
        ),
        "question": (
            "A primigravida at 39 weeks is in active labour. At 10:00 AM her cervical dilatation is 4 cm. "
            "On partograph, her cervical dilatation plot crosses the alert line at 2:00 PM but remains "
            "between the alert and action lines. By 6:00 PM the cervix is 8 cm and the plot has now "
            "crossed the action line. What is the most appropriate next step?"
        ),
        "options": [
            "A. Continue expectant management and reassess after 2 hours",
            "B. Perform immediate caesarean section for failure to progress",
            "C. Evaluate the cause, consider augmentation or operative delivery as indicated",
            "D. Administer tocolytics and allow further trial of labour",
        ],
        "correct_answer": "C. Evaluate the cause, consider augmentation or operative delivery as indicated",
        "explanation": (
            "The WHO partograph has an alert line (expected progress of 1 cm/hr in active phase, starting at 4 cm) "
            "and an action line drawn 4 hours to the right of the alert line. Crossing the alert line signals that "
            "labour is progressing slower than expected and increased surveillance is needed. Crossing the action line "
            "mandates intervention — the clinician must evaluate the cause (power, passenger, or passage) and act: "
            "augmentation with oxytocin if no CPD, or caesarean section if indicated. Expectant management alone after "
            "crossing the action line is inappropriate. Tocolytics are contraindicated in active labour dystocia."
        ),
        "high_yield_takeaway": "Action line crossed = mandatory intervention. Alert line = warning; action line = act now (4 hrs gap between them).",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ObsGyn", "#Partograph"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "Menstrual Cycle Phases and Hormones",
        "subject": Subject.obstetrics_gynecology,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "Menstrual cycle: Follicular → Ovulation → Luteal. FSH rises first; LH surge triggers ovulation.",
        "caption": (
            "Menstrual Cycle Phases and Hormones — Concise Notes\n\n"
            "Normal cycle: 21–35 days (mean 28 days); blood loss ≤80 mL\n\n"
            "PHASE 1 — Menstrual (Days 1–5):\n"
            "• Corpus luteum regresses → ↓ Progesterone + ↓ Oestrogen → endometrial shedding\n"
            "• FSH begins to rise\n\n"
            "PHASE 2 — Proliferative/Follicular (Days 5–14):\n"
            "• FSH stimulates follicles; dominant Graafian follicle selected by day 7\n"
            "• Rising oestrogen → endometrial proliferation; Spinnbarkeit cervical mucus (ferning)\n"
            "• High oestrogen → LH surge (36–48 hrs before ovulation)\n\n"
            "OVULATION (Day 14):\n"
            "• Triggered by LH surge; BBT rises 0.2–0.5°C post-ovulation\n"
            "• Mittelschmerz (mid-cycle pain) may occur\n\n"
            "PHASE 3 — Secretory/Luteal (Days 15–28):\n"
            "• Corpus luteum → Progesterone (dominant) + Oestrogen\n"
            "• Endometrium: subnuclear vacuoles (day 17), tortuous secretory glands\n"
            "• Progesterone: ↑ BBT, thick cervical mucus, no ferning\n"
            "• No fertilisation → corpus luteum degenerates (day 24–26) → menstruation\n"
            "• Fertilisation → hCG maintains corpus luteum\n\n"
            "HORMONE PEAKS:\n"
            "• FSH: peaks pre-ovulatory | LH: single surge 36 hrs before ovulation\n"
            "• Oestrogen: pre-ovulatory peak + smaller mid-luteal peak\n"
            "• Progesterone: peaks day 21 (best indicator of ovulation)\n\n"
            "EXAM TRAPS:\n"
            "• Most fertile period = days 10–17; implantation window = days 20–22\n"
            "• Corpus luteum lifespan = fixed 14 days regardless of cycle length\n"
            "• Subnuclear vacuoles = day 17 (earliest sign of secretory change)"
        ),
        "high_yield_takeaway": "LH surge → ovulation in 36 hrs. Corpus luteum lasts 14 days fixed. Progesterone peaks day 21. Subnuclear vacuoles = day 17.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ObsGyn", "#MenstrualCycle"],
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "Cervical Cancer Screening — PYQ Pattern",
        "subject": Subject.obstetrics_gynecology,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Pap smear: start at 21 yrs. HPV co-test at 30. CIN II/III → colposcopy + biopsy.",
        "caption": (
            "Cervical Cancer Screening — PYQ Concept\n\n"
            "WHY REPEATEDLY ASKED: 2nd most common cancer in Indian women; screening protocols, "
            "Bethesda system, and HPV vaccine appear in nearly every NEET-PG and INI-CET paper.\n\n"
            "PAP SMEAR SCHEDULE:\n"
            "• Start: Age 21 (regardless of sexual debut)\n"
            "• Age 21–29: Pap alone every 3 years\n"
            "• Age 30–65: Pap + HPV co-test every 5 years (preferred) OR Pap alone every 3 years\n"
            "• Stop at 65 with adequate prior negative screening\n\n"
            "BETHESDA 2014 CATEGORIES & MANAGEMENT:\n"
            "• NILM: Routine screening\n"
            "• ASC-US: HPV reflex testing → if HPV+, colposcopy\n"
            "• LSIL (>25 yrs): Colposcopy\n"
            "• HSIL / ASC-H: Immediate colposcopy + biopsy\n"
            "• CIN 1: Observation (spontaneous regression common)\n"
            "• CIN 2/3: LEEP or cone biopsy\n"
            "• AGC: Colposcopy + endocervical curettage\n\n"
            "HPV VACCINE (INDIA):\n"
            "• 9–14 years: 2-dose (0, 6 months)\n"
            "• ≥15 years: 3-dose (0, 1–2, 6 months)\n"
            "• HPV 16 & 18 → 70% of cervical cancers\n"
            "• HPV 6 & 11 → genital warts\n"
            "• Vaccination does NOT replace Pap smear screening\n\n"
            "PYQ TRAPS:\n"
            "• Transformation zone (squamocolumnar junction) = most common CIN/cancer site\n"
            "• VIA: acetowhite areas = abnormal (used in low-resource settings)\n"
            "• Most common type = Squamous cell carcinoma (85%)\n"
            "• FIGO staging = CLINICAL (not surgical)"
        ),
        "high_yield_takeaway": "Pap from age 21. HSIL/ASC-H → colposcopy immediately. HPV 16+18 = 70% cervical cancers. CIN 2/3 = LEEP/cone biopsy.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ObsGyn", "#CervicalCancer"],
    },
]
