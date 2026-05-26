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
    # ── Mnemonic ───────────────────────────────────────────────────────────────
    {
        "title": "Mnemonic: VACTERL Association — Congenital Anomalies",
        "subject": Subject.pediatrics,
        "content_format": ContentFormat.mnemonic,
        "poster_text": "Mnemonic: VACTERL — Vertebral, Anal, Cardiac, Tracheo-Esophageal, Renal, Limb anomalies",
        "caption": (
            "Explain VACTERL association (non-random co-occurrence of congenital anomalies, diagnosis requires ≥3). "
            "V = Vertebral defects (hemivertebrae, scoliosis). "
            "A = Anal atresia/imperforate anus. "
            "C = Cardiac defects (VSD most common). "
            "TE = Tracheo-Esophageal fistula (most commonly type C — proximal esophageal atresia + distal TEF). "
            "R = Renal anomalies (horseshoe kidney, renal agenesis). "
            "L = Limb defects (radial ray defects — preaxial polydactyly/thumbs). "
            "Also remember: rule out CHARGE, 22q11 deletion. "
            "Treatment is multi-specialty surgical correction. Normal intelligence usually."
        ),
        "high_yield_takeaway": "VACTERL: 3+ anomalies = diagnosis. TEF type C = most common (proximal atresia + distal fistula). VSD most common cardiac defect. Radial ray defects.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Pediatrics", "#Mnemonic", "#VACTERL"],
        "question": None,
        "options": [],
        "correct_answer": None,
        "explanation": None,
    },
    # ── Flashcard ──────────────────────────────────────────────────────────────
    {
        "title": "Flashcard: Childhood Leukemia — ALL vs AML Comparison",
        "subject": Subject.pediatrics,
        "content_format": ContentFormat.flashcard,
        "poster_text": "ALL = most common childhood cancer (80% of leukemias). AML = 15-20%. Know the difference.",
        "caption": (
            "Compare ALL vs AML in children. ALL: peak 2-5 years, B-cell precursor (CD19+, CD10+ CALLA), "
            "L1/L2 morphology, Auer rods ABSENT, t(12;21) TEL-AML1 best prognosis, t(9;22) BCR-ABL worst. "
            "Treatment: induction (vincristine + steroid + L-asparaginase) → consolidation → maintenance (2 years). "
            "AML: any age, Auer rods PRESENT (pathognomonic), myeloperoxidase +ve, CD13/33+; t(15;17) PML-RARA = APML "
            "(treat with ATRA + arsenic trioxide). Common presenting features: pallor, fever, bone pain, bruising, "
            "hepatosplenomegaly. CNS prophylaxis (intrathecal methotrexate) in ALL. Cure rate: ALL 85-90%, AML 60-70%."
        ),
        "question": "A 3-year-old presents with pallor, fever, bone pain, and hepatosplenomegaly. PBS shows lymphoblasts. What immunophenotype and prognostic markers would you expect in the MOST common childhood leukemia?",
        "options": [],
        "correct_answer": "B-cell precursor ALL: CD19+, CD10+ (CALLA), TdT+. t(12;21) TEL-AML1 = good prognosis. Hyperdiploidy >50 = good. t(9;22) = poor. L-asparaginase based regimen.",
        "explanation": None,
        "high_yield_takeaway": "ALL = most common childhood cancer, peak 2-5 yrs. CD10+, TdT+. Auer rods = AML. t(12;21) = good prognosis. t(9;22) = poor. ATRA for APML (t(15;17)).",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Pediatrics", "#Flashcard", "#Leukemia"],
    },
    # ── True/False ─────────────────────────────────────────────────────────────
    {
        "title": "True or False: The APGAR score at 5 minutes predicts long-term neurological outcome",
        "subject": Subject.pediatrics,
        "content_format": ContentFormat.true_false,
        "poster_text": "APGAR: assesses transition at birth (1 & 5 min). Does NOT predict long-term neuro outcome alone.",
        "caption": (
            "APGAR score (Appearance, Pulse, Grimace, Activity, Respiration). Each scored 0-2, total 0-10. "
            "Scored at 1 minute and 5 minutes. If <7 at 5 min, repeat q5min up to 20 min. "
            "Components: Appearance (pink all = 2, body pink/blue extremities = 1, blue/pale = 0). "
            "Pulse (>100 = 2, <100 = 1, absent = 0). "
            "Grimace (cough/sneeze = 2, grimace = 1, no response = 0). "
            "Activity (active = 2, some flexion = 1, limp = 0). "
            "Respiration (good cry = 2, slow/irregular = 1, absent = 0). "
            "Interpretation: ≥7 normal, 4-6 moderately depressed, <3 severely depressed. "
            "LIMITATION: APGAR is NOT a predictor of long-term neurological outcome when used alone. "
            "Abnormal APGAR + neonatal encephalopathy + seizures + abnormal EEG = better predictor. "
            "Cord blood pH (umbilical artery) is better for predicting HIE risk."
        ),
        "question": "The APGAR score at 5 minutes is a reliable predictor of long-term neurological outcome in newborns.",
        "options": [],
        "correct_answer": "FALSE",
        "explanation": (
            "APGAR score assesses current physiologic state and response to resuscitation at birth. "
            "It does NOT predict long-term neurological outcome when used alone. A low APGAR score may "
            "result from many factors (prematurity, drugs, infection, trauma). For predicting "
            "neurodevelopmental outcome, combine: APGAR at 10 min + cord blood pH + evidence of neonatal "
            "encephalopathy (Sarnat staging) + EEG/seizures."
        ),
        "high_yield_takeaway": "APGAR: 5 components. ≥7 = normal. Does NOT predict long-term neuro outcome alone. Cord pH + encephalopathy + EEG = better predictors. 10-min APGAR more predictive than 5-min.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Pediatrics", "#TrueFalse", "#APGAR"],
    },
    # ── One-liner Recall ────────────────────────────────────────────────────────
    {
        "title": "One-liner Recall: Normal Body Temperature in Children — Fever Definitions",
        "subject": Subject.pediatrics,
        "content_format": ContentFormat.one_liner_recall,
        "poster_text": "Fever: axillary ≥37.5°C, oral ≥38°C, rectal/tympanic ≥38°C. Hyperpyrexia = >41°C.",
        "caption": (
            'Fill in the blank: "In children, fever is defined as a body temperature of ___°C or higher when measured rectally." '
            'Answer: "38°C (100.4°F)." '
            "Then explain: Temperature measurement methods: Rectal (gold standard, core temp +0.5°C) — most accurate in <5 years. "
            "Axillary — least accurate, +0.5°C lower than core. Tympanic/infra-red — good for >3 months. "
            "Oral — reliable >5 years, wait 30 min after eating/drinking. "
            "Hyperpyrexia >41°C (105.8°F) — concern for CNS infection, heat stroke, malignant hyperthermia. "
            "Fever without focus in 3-36 months: risk of serious bacterial infection (UTI, bacteremia, pneumonia, meningitis). "
            "WBC, CRP, urinalysis, blood culture, CXR as indicated. Vaccination status important."
        ),
        "question": "In children, fever is defined as a body temperature of ___°C or higher when measured rectally.",
        "options": [],
        "correct_answer": "38°C (100.4°F)",
        "explanation": None,
        "high_yield_takeaway": "Fever: rectal ≥38°C. Axillary = core -0.5°C (least accurate). Hyperpyrexia >41°C = emergency. Fever without focus: risk SBI in <36 months.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Pediatrics", "#OneLiner", "#Fever"],
    },
]
