"""High-yield Physiology content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ────────────────────────────────────────────────────────
    {
        "title": "Oxygen Dissociation Curve — Left & Right Shifts",
        "subject": Subject.physiology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Right shift = ↓ O2 affinity = ↑ O2 delivery to tissues",
        "caption": (
            "Oxygen Dissociation Curve (ODC) — Rapid Revision\n\n"
            "Sigmoidal shape: Due to cooperative binding of O2 to haemoglobin\n\n"
            "RIGHT SHIFT (↓ O2 affinity → ↑ O2 release to tissues):\n"
            "↑ CO2 | ↑ Temperature | ↓ pH (acidosis) | ↑ 2,3-DPG | ↑ Exercise\n"
            "Mnemonic: CADET face right — CO2, Acid, DPG, Exercise, Temperature\n\n"
            "LEFT SHIFT (↑ O2 affinity → ↓ O2 release):\n"
            "↓ CO2 | ↓ Temperature | ↑ pH (alkalosis) | ↓ 2,3-DPG | CO poisoning\n"
            "Fetal Hb (HbF): Left shift — extracts O2 from maternal blood\n"
            "HbF: γ-chains instead of β-chains; less 2,3-DPG binding\n\n"
            "P50: pO2 at which Hb is 50% saturated\n"
            "Normal P50 = 26 mmHg\n"
            "Right shift → ↑ P50 | Left shift → ↓ P50\n\n"
            "⚠️ CO poisoning: Left shift + pink-red skin + SpO2 falsely normal"
        ),
        "high_yield_takeaway": "CADET face right (CO2, Acid, DPG, Exercise, Temp). Left shift: HbF, CO poisoning, alkalosis.",
        "hashtags": ["#MedicoHelp", "#Physiology", "#MBBS", "#NEETPG", "#ODC"],
    },
    {
        "title": "Respiratory Volumes & Capacities",
        "subject": Subject.physiology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "TV + IRV + ERV + RV = TLC; FRC = ERV + RV; cannot measure RV directly",
        "caption": (
            "Respiratory Volumes & Capacities — Rapid Revision\n\n"
            "Volumes (cannot be added; basic measurements):\n"
            "• Tidal Volume (TV) = 500 mL (normal quiet breathing)\n"
            "• Inspiratory Reserve Volume (IRV) = 3000 mL\n"
            "• Expiratory Reserve Volume (ERV) = 1100 mL\n"
            "• Residual Volume (RV) = 1200 mL (cannot be measured by spirometry)\n\n"
            "Capacities (sum of volumes):\n"
            "• Vital Capacity (VC) = TV + IRV + ERV = 4600 mL\n"
            "• Inspiratory Capacity (IC) = TV + IRV = 3500 mL\n"
            "• Functional Residual Capacity (FRC) = ERV + RV = 2300 mL\n"
            "• Total Lung Capacity (TLC) = VC + RV = 5800 mL\n\n"
            "⚠️ Cannot measure by spirometry: RV, FRC, TLC (contain RV)\n"
            "Method to measure RV: Helium dilution or body plethysmography\n\n"
            "Obstructive disease: ↑ RV, ↑ FRC, ↑ TLC; FEV1/FVC < 0.7\n"
            "Restrictive disease: ↓ TLC, ↓ VC; FEV1/FVC normal or ↑"
        ),
        "high_yield_takeaway": "RV cannot be measured by spirometry. FRC = ERV + RV. Obstruction ↑ RV; Restriction ↓ TLC.",
        "hashtags": ["#MedicoHelp", "#Physiology", "#MBBS", "#NEETPG", "#Respiratory"],
    },
    # ── MCQ ───────────────────────────────────────────────────────────────────
    {
        "title": "Action Potential — Cardiac vs Nerve — MCQ",
        "subject": Subject.physiology,
        "content_format": ContentFormat.mcq,
        "poster_text": "Phase 0 nerve: Na+ | Phase 0 cardiac: Na+ | Phase 2 cardiac unique: Ca2+",
        "caption": "MCQ: Ionic basis of action potential phases",
        "question": (
            "A pharmacologist studies the cardiac action potential. She blocks a specific "
            "channel and abolishes the plateau phase (Phase 2) of the ventricular action "
            "potential without affecting Phase 0 depolarisation. "
            "Which channel did she block?"
        ),
        "options": [
            "A. Fast sodium channels (Nav1.5)",
            "B. L-type calcium channels (Cav1.2)",
            "C. Inward rectifier potassium channels (IKir)",
            "D. Transient outward potassium channels (Ito)",
        ],
        "correct_answer": "B. L-type calcium channels (Cav1.2)",
        "explanation": (
            "The plateau (Phase 2) of the ventricular action potential is uniquely maintained by "
            "L-type (slow) Ca2+ channels. Phase 0 (rapid depolarisation) depends on fast Na+ channels. "
            "Phase 1 involves transient outward K+ (Ito). Phase 3 (repolarisation) involves IKr and IKs. "
            "The plateau is absent in nerve and skeletal muscle — it is unique to cardiac muscle, "
            "preventing tetanic contraction. Blocking L-type Ca2+ channels (CCBs like verapamil, diltiazem) "
            "shortens the action potential and reduces contractility."
        ),
        "high_yield_takeaway": "Phase 2 plateau: L-type Ca2+ channels. Unique to cardiac muscle — prevents tetany. CCBs block Phase 2.",
        "hashtags": ["#MedicoHelp", "#Physiology", "#MBBS", "#NEETPG", "#Cardiac"],
    },
    {
        "title": "Starling's Law — Heart Failure MCQ",
        "subject": Subject.physiology,
        "content_format": ContentFormat.mcq,
        "poster_text": "Starling: ↑ preload → ↑ stroke volume (up to a point)",
        "caption": "MCQ: Starling's law and its failure in cardiac disease",
        "question": (
            "A 65-year-old with dilated cardiomyopathy has a markedly enlarged left ventricle "
            "with an EF of 20%. Despite high filling pressures (PCWP 28 mmHg), cardiac output "
            "is severely reduced. Which of the following best explains why further increasing "
            "preload does NOT improve cardiac output in this patient?"
        ),
        "options": [
            "A. Reduced heart rate due to vagal dominance",
            "B. The ventricle is operating beyond the optimal length on the Starling curve",
            "C. Systemic vascular resistance is pathologically low",
            "D. Coronary artery disease has abolished the Frank-Starling mechanism",
        ],
        "correct_answer": "B. The ventricle is operating beyond the optimal length on the Starling curve",
        "explanation": (
            "Starling's law states that stroke volume increases with preload (end-diastolic volume) "
            "up to an optimal fibre length. Beyond this point, excessive stretch reduces the overlap "
            "of actin-myosin filaments and stroke volume falls (descending limb). In dilated "
            "cardiomyopathy, the grossly dilated, thin-walled ventricle operates on the flat/descending "
            "limb of the Starling curve. Further fluid loading increases wall stress (LaPlace's law: "
            "T = P×r/2h) and worsens function. Treatment aims to reduce preload (diuretics, nitrates)."
        ),
        "high_yield_takeaway": "Dilated CMP → descending limb of Starling curve. More preload = worse. Use diuretics to unload.",
        "hashtags": ["#MedicoHelp", "#Physiology", "#MBBS", "#NEETPG", "#Starling"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "Renin-Angiotensin-Aldosterone System (RAAS)",
        "subject": Subject.physiology,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "RAAS: ↓BP/↓Na+ → Renin → Ang I → ACE → Ang II → Aldosterone",
        "caption": (
            "RAAS — Concise Notes\n\n"
            "Trigger for renin release (JGA):\n"
            "• ↓ Renal perfusion pressure | ↓ Na+ at macula densa | ↑ Sympathetic (β1)\n\n"
            "Steps:\n"
            "1. Renin (kidney) → cleaves Angiotensinogen → Angiotensin I (inactive)\n"
            "2. ACE (lung mainly) → Angiotensin I → Angiotensin II (active)\n"
            "3. Ang II actions:\n"
            "   → Vasoconstriction (AT1 receptor) — ↑ BP\n"
            "   → Aldosterone release (adrenal cortex) — Na+ & water retention\n"
            "   → ADH release — ↑ water reabsorption\n"
            "   → Stimulates thirst\n"
            "   → Efferent arteriole constriction — maintains GFR\n\n"
            "Aldosterone: Na+ reabsorption + K+ & H+ excretion (collecting duct)\n\n"
            "Pharmacology targets:\n"
            "ACE inhibitors (ramipril) → ↓ Ang II, ↑ bradykinin (→ cough, angioedema)\n"
            "ARBs (losartan) → block AT1 receptor; no bradykinin effect\n"
            "Spironolactone → aldosterone antagonist; K+ sparing diuretic"
        ),
        "high_yield_takeaway": "ACE inhibitors cause cough (↑ bradykinin). ARBs don't. Both are contraindicated in pregnancy (teratogenic).",
        "hashtags": ["#MedicoHelp", "#Physiology", "#MBBS", "#NEETPG", "#RAAS"],
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "GFR Determinants — Renal Autoregulation PYQ",
        "subject": Subject.physiology,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "GFR = Kf × Net filtration pressure. Autoregulation: 80-180 mmHg MAP",
        "caption": (
            "GFR & Renal Autoregulation — PYQ Concept\n\n"
            "GFR = Kf × (Pgc − Pbs − πgc + πbs)\n"
            "Pgc: Glomerular capillary pressure (↑GFR)\n"
            "Pbs: Bowman's space pressure (↑ = ↓GFR, e.g. urinary obstruction)\n"
            "πgc: Oncotic pressure in glomerular capillary (↑ = ↓GFR)\n\n"
            "Normal GFR: ~125 mL/min | Normal RBF: ~1200 mL/min\n"
            "Filtration fraction (FF) = GFR/RPF = 125/625 ≈ 0.2 (20%)\n\n"
            "Autoregulation range: MAP 80–180 mmHg\n"
            "Mechanisms:\n"
            "• Myogenic reflex: ↑ pressure → afferent arteriole constricts\n"
            "• Tubuloglomerular feedback (TGF): ↑ NaCl at macula densa → ↓ GFR\n\n"
            "EXAM PATTERN: Which drug reduces GFR in renal artery stenosis?\n"
            "→ ACE inhibitors / ARBs: Block efferent constriction → ↓ GFR\n"
            "→ NSAIDs: Block afferent dilation (PGs) → ↓ GFR\n"
            "→ Contraindicated in bilateral renal artery stenosis!"
        ),
        "high_yield_takeaway": "ACE-I + bilateral RAS → acute renal failure (efferent dilation blocked). NSAIDs also ↓ GFR.",
        "hashtags": ["#MedicoHelp", "#Physiology", "#MBBS", "#NEETPG", "#Renal"],
    },
    # ── Mnemonic ─────────────────────────────────────────────────────────────
    {
        "title": "CADET — Factors Shifting ODC to the Right",
        "subject": Subject.physiology,
        "content_format": ContentFormat.mnemonic,
        "poster_text": "CADET face right: CO2, Acid, DPG, Exercise, Temperature↑",
        "caption": (
            "CADET — Oxygen Dissociation Curve Right Shift Mnemonic\n\n"
            "Right shift = ↓ O2 affinity = ↑ O2 RELEASE to tissues (Bohr effect)\n\n"
            "C — CO2 ↑ (hypercapnia)\n"
            "A — Acid (↓ pH / acidosis)\n"
            "D — 2,3-DPG ↑ (e.g. chronic anaemia, high altitude adaptation)\n"
            "E — Exercise (↑ metabolic demand)\n"
            "T — Temperature ↑ (fever, active muscles)\n\n"
            "Memory hook: 'CADET face RIGHT' — a cadet marching to the right.\n\n"
            "What it means clinically:\n"
            "• Right shift: Hb gives up O2 more readily → beneficial in active/hypoxic tissues\n"
            "• ↑ P50 (pO2 at 50% saturation; normal = 26 mmHg)\n\n"
            "Left shift (opposite — ↑ O2 affinity, ↓ release):\n"
            "• HbF, HbCO, alkalosis, hypothermia, ↓ 2,3-DPG\n"
            "• ↓ P50\n\n"
            "⚠️ Exam Trap: CO shifts curve LEFT (not right) — O2 held tightly by Hb."
        ),
        "high_yield_takeaway": "CADET = CO2, Acid, 2,3-DPG, Exercise, Temp → right shift of ODC → ↑ P50 → ↑ O2 delivery to tissues.",
        "hashtags": ["#MedicoHelp", "#Physiology", "#MBBS", "#NEETPG", "#Mnemonic"],
    },
    # ── Flashcard ─────────────────────────────────────────────────────────────
    {
        "title": "GFR Normal Value",
        "subject": Subject.physiology,
        "content_format": ContentFormat.flashcard,
        "poster_text": "Normal GFR = 125 mL/min; measured by inulin clearance (gold standard)",
        "caption": (
            "GFR Normal Value — Flashcard\n\n"
            "QUESTION: What is the normal GFR and how is it measured?\n\n"
            "ANSWER:\n"
            "Normal GFR = ~125 mL/min (in a 70 kg adult male)\n"
            "• Equivalent to ~180 L/day filtered\n\n"
            "Gold Standard Measurement: Inulin clearance\n"
            "• Inulin: freely filtered, NOT secreted, NOT reabsorbed → clearance = GFR exactly\n"
            "• Formula: GFR = (U_inulin × V) / P_inulin\n\n"
            "Clinical Estimation (eGFR):\n"
            "• Creatinine clearance (CrCl): Overestimates slightly (some tubular secretion)\n"
            "• CKD-EPI or MDRD formula: Used in clinical labs\n"
            "• Serum creatinine rises only when GFR falls by ~50%\n\n"
            "Age-related decline:\n"
            "• GFR decreases ~1 mL/min/year after age 40\n\n"
            "CKD staging by GFR:\n"
            "• G1: ≥90 | G2: 60–89 | G3a: 45–59 | G3b: 30–44 | G4: 15–29 | G5: <15\n\n"
            "⚠️ Exam Trap: Serum creatinine is insensitive — rises late when GFR already halved."
        ),
        "question": "What is the normal GFR and how is it measured (gold standard)?",
        "correct_answer": "Normal GFR = ~125 mL/min. Gold standard = inulin clearance (freely filtered, not secreted/reabsorbed). Clinically estimated by creatinine clearance or CKD-EPI formula.",
        "high_yield_takeaway": "Normal GFR = 125 mL/min. Gold standard = inulin clearance. Creatinine rises only when GFR falls 50%.",
        "hashtags": ["#MedicoHelp", "#Physiology", "#MBBS", "#NEETPG", "#Flashcard"],
    },
    # ── True/False ────────────────────────────────────────────────────────────
    {
        "title": "Loop Diuretics — Site of Action",
        "subject": Subject.physiology,
        "content_format": ContentFormat.true_false,
        "poster_text": "Loop diuretics act on THICK ASCENDING LIMB of Loop of Henle (not PCT)",
        "caption": (
            "True or False: Loop diuretics act on the proximal convoluted tubule.\n\n"
            "ANSWER: FALSE\n\n"
            "Loop diuretics (furosemide, bumetanide, torsemide) act on the THICK ASCENDING LIMB (TAL) of the Loop of Henle.\n\n"
            "Mechanism:\n"
            "• Inhibit Na⁺-K⁺-2Cl⁻ (NKCC2) co-transporter on the luminal membrane\n"
            "• TAL is normally water-impermeable → loops diuretics abolish the medullary concentration gradient\n"
            "• Result: ↑ urinary Na⁺, K⁺, Cl⁻, Ca²⁺, Mg²⁺ excretion\n\n"
            "Sites of action — diuretics overview:\n"
            "• PCT: Acetazolamide (carbonic anhydrase inhibitor)\n"
            "• TAL: Loop diuretics (furosemide) ← THE MOST POWERFUL diuretics\n"
            "• DCT: Thiazides (hydrochlorothiazide) — inhibit Na⁺-Cl⁻ co-transporter\n"
            "• Collecting duct: Spironolactone (aldosterone antagonist), Amiloride (ENaC blocker)\n\n"
            "Clinical uses of loop diuretics:\n"
            "• Acute pulmonary oedema, heart failure, hypercalcaemia, hyperkalaemia\n\n"
            "⚠️ Exam Trap: Loop diuretics WASTE calcium; thiazides RETAIN calcium."
        ),
        "question": "Loop diuretics act on the proximal convoluted tubule.",
        "correct_answer": "FALSE",
        "explanation": "Loop diuretics (furosemide, etc.) act on the THICK ASCENDING LIMB of the Loop of Henle, inhibiting the NKCC2 co-transporter. The PCT is the site of action for acetazolamide. The DCT is targeted by thiazides.",
        "high_yield_takeaway": "Loop diuretics = TAL of Loop of Henle (NKCC2 inhibition). Most powerful diuretics. Waste Ca²⁺ (unlike thiazides which spare Ca²⁺).",
        "hashtags": ["#MedicoHelp", "#Physiology", "#MBBS", "#NEETPG", "#TrueFalse"],
    },
    # ── One-liner Recall ──────────────────────────────────────────────────────
    {
        "title": "Normal GFR — One-liner Recall",
        "subject": Subject.physiology,
        "content_format": ContentFormat.one_liner_recall,
        "poster_text": "Normal GFR = 125 mL/min; decreases ~1 mL/min/year after age 40",
        "caption": (
            "One-liner Recall: Normal GFR\n\n"
            "Fill in the blank:\n\n"
            "\"Normal GFR = ___ mL/min; decreases by ___ mL/min/year after age 40\"\n\n"
            "Answer: 125 mL/min; decreases by ~1 mL/min/year after age 40\n\n"
            "Quick facts:\n"
            "• 125 mL/min = ~180 L/day filtered at glomerulus\n"
            "• Only ~1.5 L/day excreted as urine (99% reabsorbed)\n"
            "• Measured by inulin clearance (gold standard)\n"
            "• Clinically by creatinine clearance (overestimates slightly)\n"
            "• Creatinine rises only when GFR falls to ~60 mL/min or below"
        ),
        "question": "Normal GFR = ___ mL/min; decreases by ___ mL/min/year after age 40",
        "correct_answer": "125 mL/min; decreases by ~1 mL/min/year after age 40",
        "high_yield_takeaway": "Normal GFR = 125 mL/min (180 L/day filtered). Declines ~1 mL/min/year after 40. Creatinine insensitive marker — rises only when GFR drops ~50%.",
        "hashtags": ["#MedicoHelp", "#Physiology", "#MBBS", "#NEETPG", "#OneLiner"],
    },
]
