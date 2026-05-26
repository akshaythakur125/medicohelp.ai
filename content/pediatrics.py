"""High-yield Pediatrics content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ───────────────────────────────────────────────────────
    {
        "title": "Developmental Milestones — Rapid Revision",
        "subject": Subject.pediatrics,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Developmental milestones: 'Never Ever Lets Mother Down' — the NEET PG mnemonic",
        "caption": (
            "Developmental Milestones — Rapid Revision\n\n"
            "GROSS MOTOR:\n"
            "• 2 m: Holds head prone | 4 m: Head steady; rolls prone→supine\n"
            "• 6 m: Sits with support | 9 m: Stands with furniture; crawls\n"
            "• 12 m: Walks one hand held | 15 m: Walks alone\n"
            "• 18 m: Runs; climbs stairs (both feet per step)\n"
            "• 2 yr: Up/down stairs alone | 3 yr: Alternates feet; tricycle\n\n"
            "FINE MOTOR:\n"
            "• 4 m: Reaches for object | 6 m: Palmar grasp; transfers hands\n"
            "• 9 m: Immature pincer | 12 m: Mature pincer; voluntary release\n"
            "• 15 m: 2-cube tower | 18 m: 3–4 cube tower; scribbles\n"
            "• 2 yr: 6-cube tower | 3 yr: 9-cube tower; copies circle\n\n"
            "LANGUAGE:\n"
            "• 2 m: Coos | 4 m: Laughs aloud | 6 m: Monosyllables\n"
            "• 9 m: Bisyllables (non-specific) | 12 m: 1 meaningful word\n"
            "• 18 m: 7–10 words; points to body parts\n"
            "• 2 yr: 2-word phrases; 50 words; 50% stranger intelligibility\n"
            "• 3 yr: Sentences; 75% stranger intelligibility\n\n"
            "SOCIAL:\n"
            "• 6 weeks/2 m: Social smile (first social milestone)\n"
            "• 6 m: Stranger anxiety | 9 m: Waves bye-bye; peek-a-boo\n"
            "• 12 m: Separation anxiety peaks | 18 m: Parallel play\n"
            "• 3 yr: Cooperative play\n\n"
            "EXAM TRAPS:\n"
            "• Social smile = 6 weeks (not 2 months in strict sense)\n"
            "• Denver II: 75th percentile = expected milestone age\n"
            "• Regression of any milestone = always pathological"
        ),
        "high_yield_takeaway": (
            "Social smile = 6 weeks. Pincer grasp = 9 months (mature at 12 months). 2-word phrases = 2 years. "
            "Regression of milestones is always abnormal."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Pediatrics", "#DevelopmentalMilestones"],
        "question": None,
        "options": [],
        "correct_answer": None,
        "explanation": None,
    },
    {
        "title": "Dehydration Assessment in Children — Rapid Revision",
        "subject": Subject.pediatrics,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Child dehydration: Mild = 3–5%, Moderate = 6–9%, Severe ≥10% — know all signs cold",
        "caption": (
            "Dehydration Assessment in Children — Rapid Revision\n\n"
            "WHO SIGNS COMPARISON:\n"
            "Sign            | None       | Some          | Severe\n"
            "General         | Alert/well | Restless      | Lethargic/floppy\n"
            "Eyes            | Normal     | Sunken        | Very sunken + dry\n"
            "Tears           | Present    | Absent        | Absent\n"
            "Mouth/tongue    | Moist      | Dry           | Very dry\n"
            "Thirst          | Normal     | Drinks eagerly| Drinks poorly\n"
            "Skin pinch      | Immediate  | <2 sec        | ≥2 sec\n\n"
            "MANAGEMENT (WHO PLAN A/B/C):\n"
            "• Plan A (None): ORS at home + zinc + continue feeding\n"
            "• Plan B (Some): ORS 75 mL/kg over 4 hours in facility\n"
            "• Plan C (Severe): IV Ringer's lactate 100 mL/kg\n"
            "  - Infant <12 m: 30 mL/kg/1 h then 70 mL/kg/5 h\n"
            "  - Child ≥12 m: 30 mL/kg/30 min then 70 mL/kg/2.5 h\n\n"
            "ORS COMPOSITION (WHO 2002 — reduced osmolarity):\n"
            "Na 75 | Cl 65 | K 20 | Glucose 75 mmol/L | Osmolarity 245 mOsm/L\n\n"
            "KEY POINTS:\n"
            "• Best indicator of severity = % weight loss\n"
            "• Skin turgor least reliable in obese/marasmic children\n"
            "• Zinc 20 mg/day × 14 days reduces stool output by 25%\n"
            "• Cholera (severe rice-water stools): Plan C immediately"
        ),
        "high_yield_takeaway": (
            "Severe dehydration: lethargic + very sunken eyes + skin pinch ≥2 sec. Plan C: RL 100 mL/kg. "
            "Zinc 20 mg/day × 14 days for all diarrhoea."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Pediatrics", "#Dehydration"],
        "question": None,
        "options": [],
        "correct_answer": None,
        "explanation": None,
    },
    # ── MCQ ──────────────────────────────────────────────────────────────────
    {
        "title": "India Immunization Schedule — MCQ",
        "subject": Subject.pediatrics,
        "content_format": ContentFormat.mcq,
        "poster_text": "Universal Immunization Programme India: Know every vaccine and its schedule",
        "caption": (
            "MCQ: India Immunization Schedule\n\n"
            "A mother brings her 6-week-old infant for immunisation. The child was born at term with a "
            "birth weight of 3.1 kg and received BCG, OPV-0, and Hepatitis B at birth. She asks which "
            "vaccines are due today. According to the National Immunization Schedule of India (UIP 2023), "
            "which of the following is the CORRECT set of vaccines for 6 weeks of age?\n\n"
            "A. OPV-1, DPT-1, Hepatitis B-2, Hib-1, Rotavirus-1, PCV-1\n"
            "B. OPV-1, Pentavalent-1 (DPT+HepB+Hib), Rotavirus-1, IPV-1, PCV-1, fIPV-1\n"
            "C. DPT-1, OPV-1, Hepatitis B-2, IPV-1 only\n"
            "D. Pentavalent-1, fIPV-1, Rotavirus-1, PCV-1, OPV-1"
        ),
        "question": (
            "A mother brings her 6-week-old infant for immunisation. The child was born at term with a "
            "birth weight of 3.1 kg and received BCG, OPV-0, and Hepatitis B at birth. She asks which "
            "vaccines are due today. According to the National Immunization Schedule of India (UIP 2023), "
            "which is the CORRECT set of vaccines for 6 weeks of age?"
        ),
        "options": [
            "A. OPV-1, DPT-1, Hepatitis B-2, Hib-1, Rotavirus-1, PCV-1",
            "B. OPV-1, Pentavalent-1 (DPT+HepB+Hib), Rotavirus-1, IPV-1, PCV-1, fIPV-1",
            "C. DPT-1, OPV-1, Hepatitis B-2, IPV-1 only",
            "D. Pentavalent-1, fIPV-1, Rotavirus-1, PCV-1, OPV-1",
        ],
        "correct_answer": "D. Pentavalent-1, fIPV-1, Rotavirus-1, PCV-1, OPV-1",
        "explanation": (
            "Under India's UIP 2023, the 6-week schedule includes: Pentavalent-1 (combines DPT + Hepatitis B + Hib), "
            "fractional IPV (fIPV-1, intradermal 0.1 mL), Rotavirus-1, PCV-1, and OPV-1. "
            "Option B incorrectly lists IPV-1 instead of fIPV-1 — India switched to fractional IPV (two doses at "
            "6 and 14 weeks) to conserve vaccine supply. Option A is outdated (pre-Pentavalent era). "
            "Option C omits Rotavirus, PCV, and the correct formulation. Pentavalent replaces the older separate "
            "DPT + Hepatitis B + Hib injections. Note: BCG, OPV-0, and HepB birth dose are given at delivery or "
            "within 24 hours. PCV is given at 6 weeks, 14 weeks, and 9 months under the expanded UIP."
        ),
        "high_yield_takeaway": (
            "6-week UIP: Pentavalent-1 + fIPV-1 + Rotavirus-1 + PCV-1 + OPV-1. India uses fIPV (0.1 mL ID) at 6 and 14 weeks."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Pediatrics", "#Immunization"],
    },
    {
        "title": "Neonatal Jaundice — MCQ",
        "subject": Subject.pediatrics,
        "content_format": ContentFormat.mcq,
        "poster_text": "Neonatal jaundice: Physiological vs pathological — know the difference",
        "caption": (
            "MCQ: Neonatal Jaundice\n\n"
            "A 2-day-old term neonate (birth weight 3.2 kg) develops yellow discolouration of the skin. "
            "The infant is exclusively breastfed and feeding well. Serum bilirubin is 9 mg/dL (predominantly "
            "unconjugated). Mother is blood group O positive, infant is A positive; Direct Coombs test is "
            "negative. There is no family history of haemolysis and no hepatosplenomegaly. What is the MOST "
            "likely diagnosis and initial management?"
        ),
        "question": (
            "A 2-day-old term neonate develops jaundice with serum bilirubin 9 mg/dL (unconjugated). "
            "The infant is breastfeeding well. Mother is O+, baby is A+. Direct Coombs test is negative. "
            "No hepatosplenomegaly. What is the MOST likely diagnosis and initial management?"
        ),
        "options": [
            "A. ABO incompatibility — start intensive phototherapy immediately",
            "B. Physiological jaundice — continue breastfeeding, monitor bilirubin",
            "C. Breastfeeding jaundice — stop breastfeeding for 48 hours",
            "D. Crigler-Najjar syndrome type I — plan exchange transfusion",
        ],
        "correct_answer": "B. Physiological jaundice — continue breastfeeding, monitor bilirubin",
        "explanation": (
            "This is physiological jaundice of the newborn. Key features: onset Day 2–3 (not <24 hours), "
            "predominantly unconjugated bilirubin, total bilirubin <12 mg/dL in term neonate at Day 2, "
            "no haemolysis (negative Coombs), feeding well. Physiological jaundice peaks at Day 3–4 in "
            "term infants (<12.9 mg/dL) and Day 5–7 in preterm, and resolves by Day 14 (term) or Day 21 "
            "(preterm). Management: continue breastfeeding (which reduces enterohepatic circulation), "
            "monitor bilirubin, and initiate phototherapy only if bilirubin crosses the Bhutani nomogram "
            "threshold for age in hours. ABO incompatibility (Option A) has a positive Coombs or evidence "
            "of haemolysis. Breastfeeding jaundice (Option C) is caused by suboptimal intake and poor "
            "caloric intake — solution is to improve feeding frequency, NOT stop breastfeeding."
        ),
        "high_yield_takeaway": (
            "Physiological jaundice: Day 2–3 onset, peaks Day 3–4, resolves by Day 14. Jaundice <24 h is ALWAYS pathological."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Pediatrics", "#NeonatalJaundice"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "Malnutrition: Gomez, Waterlow, MUAC Classifications",
        "subject": Subject.pediatrics,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "Malnutrition grading: Gomez = weight-for-age | Waterlow = stunting + wasting",
        "caption": (
            "Malnutrition Classifications — Concise Notes\n\n"
            "1. GOMEZ (Weight-for-Age):\n"
            "• Normal ≥90% | Grade I (Mild) 75–90% | Grade II (Mod) 60–74% | Grade III (Severe) <60%\n"
            "• Limitation: cannot distinguish acute vs chronic malnutrition\n\n"
            "2. WATERLOW:\n"
            "STUNTING (chronic) — Height-for-Age:\n"
            "• Normal ≥95% | Mild 87.5–95% | Mod 80–87.4% | Severe <80%\n"
            "WASTING (acute) — Weight-for-Height:\n"
            "• Normal ≥90% | Mild 80–90% | Mod 70–80% | Severe <70%\n\n"
            "3. MUAC (age 6 months–5 years; midpoint of left arm):\n"
            "• Green ≥12.5 cm = Normal\n"
            "• Yellow 11.5–12.4 cm = MAM (Moderate Acute Malnutrition)\n"
            "• Red <11.5 cm = SAM (Severe Acute Malnutrition)\n\n"
            "4. WHO Z-SCORE:\n"
            "• SAM: WHZ <-3 SD OR MUAC <11.5 cm OR bipedal oedema\n"
            "• MAM: WHZ -2 to -3 SD\n\n"
            "CLINICAL SYNDROMES:\n"
            "• Marasmus: Energy + protein deficiency; 'skin and bones'; no oedema; alert\n"
            "• Kwashiorkor: Protein deficiency; oedema (mandatory), moon face, flaky-paint "
            "dermatosis, flag sign hair, hepatomegaly (fatty liver), irritable child\n"
            "• Marasmic-Kwashiorkor: Features of both\n\n"
            "EXAM TRAPS:\n"
            "• Flag sign = alternating dark/light hair bands (kwashiorkor)\n"
            "• Oedema MANDATORY for kwashiorkor diagnosis\n"
            "• SAM management: F-75 (stabilisation) → F-100/RUTF (rehabilitation)"
        ),
        "high_yield_takeaway": (
            "SAM = WHZ <-3 SD OR MUAC <11.5 cm OR oedema. Kwashiorkor = oedema + moon face + flaky paint rash. Marasmus = no oedema, wasted."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Pediatrics", "#Malnutrition"],
        "question": None,
        "options": [],
        "correct_answer": None,
        "explanation": None,
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "Status Epilepticus in Children — PYQ Pattern",
        "subject": Subject.pediatrics,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Status epilepticus: Seizure >5 min or 2+ seizures without recovery — act fast",
        "caption": (
            "Status Epilepticus — PYQ Concept\n\n"
            "WHY THIS IS REPEATEDLY ASKED:\n"
            "Status epilepticus (SE) management steps, drug doses, and timing are consistently tested in "
            "NEET PG and INI-CET. Expect scenario-based questions on drug choice and sequencing.\n\n"
            "DEFINITION:\n"
            "• Seizure lasting ≥5 minutes OR two or more seizures without recovery between them\n"
            "• (Older definition: >30 minutes — now updated to >5 minutes for clinical action)\n\n"
            "STEPWISE MANAGEMENT (TIMELINE):\n\n"
            "0–5 minutes (Stabilisation):\n"
            "• ABC: Airway, Breathing, Circulation\n"
            "• Oxygen, IV/IO access, glucose check (IV dextrose if hypoglycaemia)\n"
            "• Rectal diazepam 0.5 mg/kg OR midazolam 0.2 mg/kg (buccal/intranasal) if no IV access\n\n"
            "5–20 minutes (First-line Benzodiazepine IV):\n"
            "• Lorazepam 0.1 mg/kg IV (max 4 mg) — DRUG OF CHOICE if IV access available\n"
            "• May repeat once after 5–10 minutes\n"
            "• If no IV: Midazolam IM 0.2 mg/kg or buccal 0.5 mg/kg\n\n"
            "20–40 minutes (Second-line — Established SE):\n"
            "• Phenytoin 20 mg/kg IV at ≤1 mg/kg/min (fosphenytoin preferred — less cardiotoxic)\n"
            "• OR Valproate 20–40 mg/kg IV (avoid in <2 years, liver disease)\n"
            "• OR Levetiracetam 60 mg/kg IV (increasingly preferred)\n\n"
            "40–60 minutes (Refractory SE):\n"
            "• Admit to ICU; RSI + intubation\n"
            "• Midazolam infusion OR thiopental OR propofol (avoid propofol infusion syndrome in children)\n"
            "• EEG monitoring mandatory\n\n"
            "COMMON CAUSES IN CHILDREN:\n"
            "• Most common overall: Febrile convulsions (simple vs complex)\n"
            "• Electrolyte disturbances (hyponatraemia, hypocalcaemia)\n"
            "• CNS infections (meningitis, encephalitis)\n"
            "• Hypoglycaemia\n"
            "• Idiopathic epilepsy\n\n"
            "FEBRILE SEIZURE PEARLS:\n"
            "• Simple: <15 min, generalised, once in 24 h — NO prophylaxis needed\n"
            "• Complex: >15 min OR focal OR recurrent → investigate\n\n"
            "⚠️ PYQ Traps:\n"
            "• Lorazepam > diazepam IV (longer action, less resp. depression)\n"
            "• Phenytoin: give in NS only — precipitates in dextrose\n"
            "• EEG: gold standard to confirm electrographic SE"
        ),
        "high_yield_takeaway": (
            "SE >5 min: Lorazepam IV (1st line) → Phenytoin/Valproate (2nd line) → Midazolam infusion (refractory). "
            "Phenytoin in NS only, not dextrose."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Pediatrics", "#StatusEpilepticus"],
        "question": None,
        "options": [],
        "correct_answer": None,
        "explanation": None,
    },
]
