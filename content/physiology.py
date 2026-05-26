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
]
