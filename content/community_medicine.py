"""High-yield Community Medicine content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── 1. Rapid Revision ───────────────────────────────────────────────────
    {
        "title": "Sensitivity, Specificity, PPV & NPV",
        "subject": Subject.community_medicine,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "2x2 table mastery = 5 guaranteed marks in Community Medicine",
        "caption": (
            "SENSITIVITY, SPECIFICITY, PPV & NPV — RAPID REVISION\n\n"
            "THE 2×2 TABLE:\n"
            "              Disease +    Disease −\n"
            "Test +           a (TP)       b (FP)\n"
            "Test −           c (FN)       d (TN)\n\n"
            "FORMULAS:\n"
            "• Sensitivity (Sn) = a / (a+c) — True Positive Rate\n"
            "  'Se-N-sitive — rules out Negative (SnNout)'\n"
            "• Specificity (Sp) = d / (b+d) — True Negative Rate\n"
            "  'SP-ecific — rules in Positive (SpPin)'\n"
            "• PPV = a / (a+b) — probability disease present if test positive\n"
            "• NPV = d / (c+d) — probability disease absent if test negative\n\n"
            "KEY RELATIONSHIPS:\n"
            "• Sensitivity ↑ → FN ↓ (miss fewer diseased)\n"
            "• Specificity ↑ → FP ↓ (fewer false alarms)\n"
            "• PPV depends on PREVALENCE — increases as prevalence rises\n"
            "• NPV decreases as prevalence rises\n"
            "• Sensitivity and specificity are FIXED properties of the test\n"
            "  (independent of prevalence)\n\n"
            "SCREENING TESTS: High sensitivity preferred (don't miss disease)\n"
            "CONFIRMATORY TESTS: High specificity preferred (rule in disease)\n\n"
            "LIKELIHOOD RATIOS (advanced):\n"
            "• LR+ = Sensitivity / (1−Specificity)\n"
            "• LR− = (1−Sensitivity) / Specificity\n"
            "• LR+ >10 or LR− <0.1 = strongly changes post-test probability"
        ),
        "high_yield_takeaway": (
            "SnNout: High sensitivity rules out (negative = disease absent). "
            "SpPin: High specificity rules in (positive = disease present). PPV varies with prevalence."
        ),
        "hashtags": ["#MedicoHelp", "#CommunityMedicine", "#MBBS", "#NEETPG", "#Biostatistics"],
    },

    # ── 2. Rapid Revision ───────────────────────────────────────────────────
    {
        "title": "Epidemiological Study Designs",
        "subject": Subject.community_medicine,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Know your study design — it's asked in every NEET-PG paper",
        "caption": (
            "EPIDEMIOLOGICAL STUDY DESIGNS — RAPID REVISION\n\n"
            "OBSERVATIONAL STUDIES:\n\n"
            "1. CROSS-SECTIONAL (Prevalence) Study\n"
            "• Snapshot in time; measures prevalence\n"
            "• Best for: chronic diseases, planning health services\n"
            "• Cannot establish causality (chicken-or-egg problem)\n\n"
            "2. CASE-CONTROL Study\n"
            "• Starts with OUTCOME → looks backward for exposure\n"
            "• Retrospective; measures ODDS RATIO (OR)\n"
            "• Best for: rare diseases, quick, cheap\n"
            "• Bias: recall bias, selection bias\n\n"
            "3. COHORT Study\n"
            "• Starts with EXPOSURE → follows forward for outcome\n"
            "• Prospective (Framingham) or retrospective\n"
            "• Measures RELATIVE RISK (RR) / Incidence Rate Ratio\n"
            "• Best for: common diseases, establishing temporality\n"
            "• Bias: loss to follow-up, Neyman bias (retrospective cohort)\n\n"
            "EXPERIMENTAL STUDIES:\n"
            "4. RCT — gold standard; random allocation; measures RR, NNT\n"
            "5. Community Trial — randomisation at community level\n\n"
            "HIERARCHY OF EVIDENCE (highest → lowest):\n"
            "Meta-analysis → Systematic Review → RCT → Cohort → Case-Control → Cross-Sectional → Case Report\n\n"
            "EXAM TRAP: OR ≈ RR only when disease prevalence is LOW (<10%)"
        ),
        "high_yield_takeaway": (
            "Case-control = OR; Cohort = RR. OR approximates RR only when prevalence <10%. "
            "RCT is the gold standard experimental design."
        ),
        "hashtags": ["#MedicoHelp", "#CommunityMedicine", "#MBBS", "#NEETPG", "#Epidemiology"],
    },

    # ── 3. MCQ ──────────────────────────────────────────────────────────────
    {
        "title": "National Immunization Schedule India — MCQ",
        "subject": Subject.community_medicine,
        "content_format": ContentFormat.mcq,
        "poster_text": "India's immunization schedule saves millions — know every vaccine age",
        "caption": (
            "NATIONAL IMMUNIZATION SCHEDULE — QUICK REFERENCE\n\n"
            "Birth: BCG, OPV-0, Hepatitis B-1\n"
            "6 weeks: OPV-1, DPT-1, HepB-2, IPV-1, PCV-1, Rotavirus-1\n"
            "10 weeks: OPV-2, DPT-2, IPV-2, PCV-2, Rotavirus-2\n"
            "14 weeks: OPV-3, DPT-3, IPV-3, PCV-3, Rotavirus-3\n"
            "9 months: MR-1, JE-1 (in endemic districts), Vitamin A (1st dose)\n"
            "12 months: Hepatitis A-1 (private sector)\n"
            "16–24 months: DPT booster-1, OPV booster, MR-2, JE-2, Vitamin A\n"
            "5–6 years: DPT booster-2\n"
            "10 years: Td\n"
            "16 years: Td\n\n"
            "COLD CHAIN: -15°C to -25°C (OPV); 2°C–8°C (most vaccines)\n"
            "Most heat-sensitive: OPV → stored at -20°C\n"
            "Most freeze-sensitive: DPT, HepB, Td (must not freeze)"
        ),
        "question": (
            "A mother brings her 9-month-old child for vaccination. The child was born at term, received "
            "BCG and OPV-0 at birth, and has received all scheduled vaccines since. The child has no "
            "fever today and is thriving. According to the National Immunization Schedule of India, "
            "which vaccine(s) should be given at this visit?"
        ),
        "options": [
            "A. DPT booster and OPV booster",
            "B. Measles-Rubella (MR-1) and Vitamin A first dose",
            "C. IPV-3 and PCV-3",
            "D. Japanese Encephalitis vaccine only",
        ],
        "correct_answer": "B. Measles-Rubella (MR-1) and Vitamin A first dose",
        "explanation": (
            "At 9 months of age, the National Immunization Schedule of India recommends MR-1 (Measles-Rubella "
            "first dose) and the first dose of Vitamin A (100,000 IU). Japanese Encephalitis vaccine is also "
            "given at 9 months but only in JE-endemic districts, not universally. DPT and OPV boosters are "
            "scheduled at 16–24 months (DPT booster-1). IPV-3 and PCV-3 are given at 14 weeks. "
            "Vitamin A continues every 6 months until 5 years of age."
        ),
        "high_yield_takeaway": (
            "9 months = MR-1 + Vitamin A dose-1 (100,000 IU). DPT booster at 16–24 months. "
            "OPV is most heat-sensitive; DPT/HepB must not freeze."
        ),
        "hashtags": ["#MedicoHelp", "#CommunityMedicine", "#MBBS", "#NEETPG", "#Immunization"],
    },

    # ── 4. MCQ ──────────────────────────────────────────────────────────────
    {
        "title": "Kwashiorkor vs Marasmus — MCQ",
        "subject": Subject.community_medicine,
        "content_format": ContentFormat.mcq,
        "poster_text": "Protein vs calories — can you tell kwashiorkor from marasmus?",
        "caption": (
            "PROTEIN-ENERGY MALNUTRITION — KWASHIORKOR vs MARASMUS\n\n"
            "KWASHIORKOR (Protein deficiency with adequate calories):\n"
            "• Oedema (hallmark) — pitting; starts at feet\n"
            "• Moon face, pot belly\n"
            "• Skin: flaky paint dermatosis, hypopigmentation\n"
            "• Hair: flag sign (alternating light-dark bands), easily pluckable\n"
            "• Fatty liver (↓ apolipoprotein synthesis → fat accumulation)\n"
            "• Serum albumin: markedly LOW\n"
            "• Weight: may appear near-normal due to oedema\n\n"
            "MARASMUS (Total calorie + protein deficiency):\n"
            "• Severe wasting — 'old man facies', 'baggy pants' appearance\n"
            "• No oedema\n"
            "• Skin: loose folds (skin hangs off bones)\n"
            "• Hair: sparse but not flag sign\n"
            "• Serum albumin: near normal\n"
            "• Weight: severely reduced (<60% expected)\n\n"
            "MARASMIC KWASHIORKOR: Features of both — worst prognosis\n\n"
            "DIAGNOSIS: Mid-upper arm circumference (MUAC) <11.5 cm = severe acute malnutrition\n"
            "TREATMENT: F-75 stabilisation → F-100 rehabilitation (WHO protocol)"
        ),
        "question": (
            "A 2-year-old child is brought with complaints of swelling of both legs for 3 weeks. "
            "He was recently weaned off breastfeeding and is being fed predominantly rice gruel. "
            "On examination: pitting oedema up to knees, moon face, flaky skin changes, and "
            "easily pluckable discoloured hair. Serum albumin is 1.8 g/dL. "
            "What is the MOST likely diagnosis?"
        ),
        "options": [
            "A. Marasmus",
            "B. Kwashiorkor",
            "C. Nephrotic syndrome",
            "D. Marasmic kwashiorkor",
        ],
        "correct_answer": "B. Kwashiorkor",
        "explanation": (
            "The clinical picture — pitting oedema, moon face, flaky paint dermatosis, flag sign hair, "
            "low serum albumin, and a diet rich in carbohydrates but deficient in protein after weaning — "
            "is classic kwashiorkor. The oedema in kwashiorkor results from hypoalbuminaemia causing "
            "reduced plasma oncotic pressure, worsened by sodium retention. Marasmus presents with severe "
            "wasting and no oedema; serum albumin is near normal. Nephrotic syndrome is excluded by the "
            "nutritional history and absence of heavy proteinuria context in this case."
        ),
        "high_yield_takeaway": (
            "Kwashiorkor: oedema + low albumin + flaky skin + flag sign = protein deficiency. "
            "Marasmus: severe wasting, no oedema, normal albumin = total calorie deficiency."
        ),
        "hashtags": ["#MedicoHelp", "#CommunityMedicine", "#MBBS", "#NEETPG", "#Nutrition"],
    },

    # ── 5. Concise Notes ────────────────────────────────────────────────────
    {
        "title": "Epidemiological Measurements: Incidence & Prevalence",
        "subject": Subject.community_medicine,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "Incidence vs Prevalence — the confusion ends today",
        "caption": (
            "INCIDENCE & PREVALENCE — CONCISE NOTES\n\n"
            "SECTION 1 — INCIDENCE\n"
            "Definition: Number of NEW cases of disease occurring in a population at risk "
            "over a specified time period.\n\n"
            "Formula: Incidence Rate = (New cases / Population at risk) × 10^n\n\n"
            "Types:\n"
            "• Cumulative Incidence (Attack Rate): proportion of population developing disease\n"
            "  in a defined period (used in outbreaks)\n"
            "• Incidence Density Rate (IDR): new cases per person-time at risk; used when "
            "  follow-up periods differ between individuals\n\n"
            "Secondary Attack Rate (SAR): cases among susceptible contacts / total susceptible contacts × 100\n"
            "Used to measure infectivity in household/community outbreaks.\n\n"
            "SECTION 2 — PREVALENCE\n"
            "Definition: All existing cases (new + old) in a population at a point or period.\n\n"
            "• Point prevalence: at a single point in time\n"
            "• Period prevalence: over a defined time period\n\n"
            "Formula: Prevalence = (All cases / Total population) × 10^n\n\n"
            "SECTION 3 — KEY RELATIONSHIP\n"
            "Prevalence ≈ Incidence × Duration of disease\n"
            "(Valid when prevalence is low and disease is in steady state)\n\n"
            "SECTION 4 — FACTORS AFFECTING EACH\n"
            "Prevalence INCREASES with: long disease duration, in-migration of cases, improved survival\n"
            "Prevalence DECREASES with: high mortality, short duration, cure, out-migration\n"
            "Incidence CHANGES with: true change in new case generation\n\n"
            "EXAM TIP: Prevalence is preferred for planning health services (burden); "
            "Incidence is preferred for causation studies (aetiology)."
        ),
        "high_yield_takeaway": (
            "Prevalence = Incidence × Duration. SAR measures household infectivity. "
            "IDR used when follow-up times differ. Prevalence for planning; Incidence for causation."
        ),
        "hashtags": ["#MedicoHelp", "#CommunityMedicine", "#MBBS", "#NEETPG", "#Epidemiology"],
    },

    # ── 6. PYQ Concept ──────────────────────────────────────────────────────
    {
        "title": "Nutritional Indices — PYQ Pattern",
        "subject": Subject.community_medicine,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Nutritional indices appear every year — own this table",
        "caption": (
            "NUTRITIONAL INDICES — HIGH-YIELD PYQ TABLE\n\n"
            "INDEX            FORMULA                    ASSESSES\n"
            "─────────────────────────────────────────────────────────\n"
            "BMI              Wt(kg)/Ht²(m)              Overweight/obesity\n"
            "Weight-for-Age   Wt / Reference Wt × 100    Overall malnutrition\n"
            "Height-for-Age   Ht / Reference Ht × 100    Stunting (chronic)\n"
            "Weight-for-Ht    Wt / Ref Wt-for-Ht × 100  Wasting (acute)\n"
            "MUAC             Arm circumference           SAM screening\n\n"
            "GOMEZ CLASSIFICATION (Weight-for-Age):\n"
            "• Grade I: 75–90% expected weight (mild)\n"
            "• Grade II: 61–75% (moderate)\n"
            "• Grade III: <60% (severe)\n\n"
            "WATERLOW CLASSIFICATION:\n"
            "• Stunting: Height-for-Age <95% (chronic undernutrition)\n"
            "• Wasting: Weight-for-Height <90% (acute undernutrition)\n\n"
            "IAP CLASSIFICATION (Indian Academy of Pediatrics):\n"
            "• Normal: >80% weight-for-age\n"
            "• Grade I: 71–80%  |  Grade II: 61–70%\n"
            "• Grade III: 51–60%  |  Grade IV: <50%\n\n"
            "MUAC CUTOFFS (6–59 months):\n"
            "• ≥12.5 cm: Normal\n"
            "• 11.5–12.4 cm: Moderate acute malnutrition (MAM)\n"
            "• <11.5 cm: Severe acute malnutrition (SAM)\n\n"
            "PYQ TRAP: Gomez uses Weight-for-Age; Waterlow uses Height-for-Age AND Weight-for-Height.\n"
            "Stunting = past/chronic malnutrition. Wasting = current/acute malnutrition."
        ),
        "high_yield_takeaway": (
            "Gomez Grade III = <60% weight-for-age. MUAC <11.5 cm = SAM. "
            "Stunting (height-for-age) = chronic; Wasting (weight-for-height) = acute."
        ),
        "hashtags": ["#MedicoHelp", "#CommunityMedicine", "#MBBS", "#NEETPG", "#NutritionalIndices"],
    },
]
