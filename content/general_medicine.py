"""High-yield General Medicine content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── 1. Rapid Revision ───────────────────────────────────────────────────
    {
        "title": "Diabetic Ketoacidosis (DKA) Management",
        "subject": Subject.general_medicine,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "DKA: Fluids first, insulin second — never forget potassium",
        "caption": (
            "DIABETIC KETOACIDOSIS (DKA) — MANAGEMENT RAPID REVISION\n\n"
            "DIAGNOSTIC TRIAD:\n"
            "• Blood glucose >250 mg/dL (occasionally euglycaemic DKA in SGLT2i users)\n"
            "• Anion gap metabolic acidosis (pH <7.3, bicarbonate <15 mEq/L)\n"
            "• Ketonaemia / ketonuria\n\n"
            "STEP 1 — FLUIDS (first priority):\n"
            "• Normal saline 0.9% — 1 litre in first hour, then 500 mL/hr × 4 hrs\n"
            "• Switch to 0.45% NaCl when glucose <250 mg/dL and add 5% dextrose\n\n"
            "STEP 2 — POTASSIUM (before insulin if K+ <3.5 mEq/L):\n"
            "• If K+ 3.5–5.5: give 20–40 mEq/hr KCl with each litre of fluid\n"
            "• Do NOT give insulin if K+ <3.3 mEq/L (risk of fatal hypokalaemia)\n\n"
            "STEP 3 — INSULIN:\n"
            "• Regular insulin IV: 0.1 units/kg/hr infusion (or 0.1 units/kg bolus then 0.05 units/kg/hr)\n"
            "• Target glucose fall: 50–70 mg/dL/hr\n"
            "• Continue insulin infusion until anion gap normalises (not just glucose!)\n\n"
            "STEP 4 — BICARBONATE:\n"
            "• Only if pH <6.9: 100 mEq NaHCO₃ over 2 hours (controversial)\n\n"
            "MONITORING:\n"
            "• Glucose hourly; electrolytes, BUN, pH every 2–4 hrs\n"
            "• Resolution: pH >7.3, bicarbonate >15, anion gap closed, patient eating\n\n"
            "COMPLICATIONS: Cerebral oedema (most dangerous in children), hypokalaemia, hypoglycaemia"
        ),
        "high_yield_takeaway": (
            "DKA: Fluids first → K+ correction (hold insulin if K+<3.3) → Insulin infusion. "
            "Stop insulin only after anion gap closes, not just when glucose normalises."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralMedicine", "#MBBS", "#NEETPG", "#DKA"],
    },

    # ── 2. Rapid Revision ───────────────────────────────────────────────────
    {
        "title": "ECG Changes — Common High-Yield Patterns",
        "subject": Subject.general_medicine,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Read every ECG like a pro — these patterns repeat in every exam",
        "caption": (
            "HIGH-YIELD ECG PATTERNS — RAPID REVISION\n\n"
            "NORMAL INTERVALS:\n"
            "• PR interval: 0.12–0.20 sec (3–5 small squares)\n"
            "• QRS: <0.12 sec (<3 small squares)\n"
            "• QTc: <0.44 sec men, <0.46 sec women (Bazett formula: QT/√RR)\n\n"
            "MYOCARDIAL INFARCTION:\n"
            "• Hyperacute T waves → ST elevation → Q waves → T inversion\n"
            "• Anteroseptal: V1–V4 (LAD)\n"
            "• Inferior: II, III, aVF (RCA) → check V4R for RV infarct\n"
            "• Lateral: I, aVL, V5–V6 (LCx)\n"
            "• Posterior: tall R + ST depression in V1–V2 (mirror image)\n\n"
            "BLOCKS:\n"
            "• 1° AV block: prolonged PR (>0.20 sec)\n"
            "• 2° Mobitz I (Wenckebach): progressive PR lengthening → dropped beat\n"
            "• 2° Mobitz II: fixed PR, sudden dropped beat → needs pacemaker\n"
            "• 3° (Complete) AV block: no relationship between P and QRS → pacemaker\n"
            "• LBBB: WiLLiaM (W in V1, M in V6)\n"
            "• RBBB: MaRRoW (M in V1, W in V6)\n\n"
            "ELECTROLYTES:\n"
            "• Hyperkalaemia: peaked T → PR prolongation → wide QRS → sine wave → VF\n"
            "• Hypokalaemia: U wave, flat T, prolonged QU\n"
            "• Hypercalcaemia: short QT\n"
            "• Hypocalcaemia: prolonged QT → torsades de pointes\n\n"
            "OTHERS:\n"
            "• Digoxin toxicity: 'reverse tick' (scooped ST depression)\n"
            "• PE: S1Q3T3 pattern (S in I, Q in III, T inversion in III)\n"
            "• WPW: delta wave + short PR + wide QRS"
        ),
        "high_yield_takeaway": (
            "RBBB = MaRRoW (M in V1, W in V6). LBBB = WiLLiaM (W in V1, M in V6). "
            "Mobitz II → needs pacemaker. Hyperkalaemia: peaked T → sine wave → VF."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralMedicine", "#MBBS", "#NEETPG", "#ECG"],
    },

    # ── 3. MCQ ──────────────────────────────────────────────────────────────
    {
        "title": "Hypertension Staging & Treatment — MCQ",
        "subject": Subject.general_medicine,
        "content_format": ContentFormat.mcq,
        "poster_text": "Hypertension: Stage it, target it, treat it — NEET loves this",
        "caption": (
            "JNC-8 / ACC-AHA HYPERTENSION CLASSIFICATION:\n\n"
            "Normal: <120/<80 mmHg\n"
            "Elevated: 120–129/<80 mmHg\n"
            "Stage 1 HT: 130–139 / 80–89 mmHg\n"
            "Stage 2 HT: ≥140 / ≥90 mmHg\n"
            "Hypertensive Urgency: >180/>120 without end-organ damage\n"
            "Hypertensive Emergency: >180/>120 WITH end-organ damage\n\n"
            "FIRST-LINE DRUGS:\n"
            "• General population: ACE inhibitor / ARB / CCB / Thiazide diuretic\n"
            "• CKD (with proteinuria): ACE inhibitor or ARB (preferred — renoprotective)\n"
            "• Heart failure with reduced EF: ACE inhibitor/ARB + Beta blocker + Aldosterone antagonist\n"
            "• Post-MI: Beta blocker + ACE inhibitor\n"
            "• Pregnancy: Methyldopa, Labetalol, Nifedipine (avoid ACEi/ARB — teratogenic)\n"
            "• Isolated systolic HT in elderly: Thiazide or CCB\n\n"
            "HYPERTENSIVE EMERGENCY DRUG OF CHOICE: IV Sodium nitroprusside (or Labetalol, Nicardipine)\n"
            "TARGET: Reduce MAP by no more than 25% in first hour"
        ),
        "question": (
            "A 55-year-old man with type 2 diabetes and chronic kidney disease (eGFR 42 mL/min, "
            "urine albumin-creatinine ratio 350 mg/g) presents with BP 148/92 mmHg on two readings. "
            "He is currently on metformin and lifestyle modifications. "
            "Which antihypertensive is MOST appropriate as first-line therapy for this patient?"
        ),
        "options": [
            "A. Amlodipine",
            "B. Hydrochlorothiazide",
            "C. Ramipril",
            "D. Atenolol",
        ],
        "correct_answer": "C. Ramipril",
        "explanation": (
            "In a diabetic patient with CKD and significant proteinuria (ACR >300 mg/g = macroalbuminuria), "
            "ACE inhibitors (like Ramipril) or ARBs are the preferred first-line antihypertensives. "
            "They reduce intraglomerular pressure by dilating the efferent arteriole, thereby slowing "
            "progression of diabetic nephropathy independent of their BP-lowering effect. "
            "Calcium channel blockers (amlodipine) are acceptable alternatives but are not preferred "
            "when significant proteinuria is present. Thiazides have limited efficacy when eGFR <30. "
            "Beta blockers are not first-line for hypertension in diabetics unless there is a concurrent "
            "cardiac indication."
        ),
        "high_yield_takeaway": (
            "CKD with proteinuria + diabetes → ACE inhibitor/ARB first line (renoprotective). "
            "Avoid ACEi/ARB in pregnancy; prefer Methyldopa or Labetalol."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralMedicine", "#MBBS", "#NEETPG", "#Hypertension"],
    },

    # ── 4. MCQ ──────────────────────────────────────────────────────────────
    {
        "title": "Thyroid Storm — MCQ",
        "subject": Subject.general_medicine,
        "content_format": ContentFormat.mcq,
        "poster_text": "Thyroid storm kills fast — recognise it, treat it immediately",
        "caption": (
            "THYROID STORM (Thyrotoxic Crisis) — KEY FACTS\n\n"
            "PRECIPITANTS: Surgery, infection, trauma, radioiodine therapy, abrupt anti-thyroid drug withdrawal\n\n"
            "CLINICAL FEATURES (Burch-Wartofsky Score >45 = storm):\n"
            "• High fever (>38.5°C, often >40°C)\n"
            "• Tachycardia (HR >140 bpm), atrial fibrillation\n"
            "• CNS: agitation, delirium, coma\n"
            "• GI: vomiting, diarrhoea, jaundice (hepatic failure)\n"
            "• Cardiovascular: high-output heart failure\n\n"
            "MANAGEMENT (Sequential — PPIB mnemonic):\n"
            "• P — Propranolol: IV/oral to control heart rate AND block T4→T3 conversion\n"
            "• P — PTU (Propylthiouracil): preferred over Methimazole in storm (blocks T4→T3)\n"
            "• I — Iodide (Lugol's): given 1 hour AFTER PTU (prevents thyroid hormone release)\n"
            "• B — Block with corticosteroids: Hydrocortisone 100 mg q8h (reduces T4→T3 conversion)\n"
            "• Supportive: cooling blanket, IV fluids, treat precipitant, ICU care\n\n"
            "KEY EXAM POINTS:\n"
            "• Iodide must be given AFTER PTU (to prevent organification of iodide)\n"
            "• PTU preferred over Methimazole in storm, pregnancy (1st trimester), thyrotoxicosis with liver disease\n"
            "• Aspirin is CONTRAINDICATED in thyroid storm (displaces T4 from TBG)"
        ),
        "question": (
            "A 35-year-old woman with known Graves' disease is admitted with fever (39.8°C), "
            "heart rate of 148 bpm, profuse sweating, agitation, and diarrhoea. She had an "
            "elective cholecystectomy 24 hours ago. TSH is undetectable, free T4 is markedly elevated. "
            "Which of the following is the CORRECT sequence of treatment for this patient?"
        ),
        "options": [
            "A. Methimazole → Lugol's iodine → Propranolol → Hydrocortisone",
            "B. Lugol's iodine → PTU → Propranolol → Hydrocortisone",
            "C. Propranolol → PTU → Lugol's iodine (1 hr later) → Hydrocortisone",
            "D. Hydrocortisone → Propranolol → Methimazole → Lugol's iodine",
        ],
        "correct_answer": "C. Propranolol → PTU → Lugol's iodine (1 hr later) → Hydrocortisone",
        "explanation": (
            "In thyroid storm, management follows a specific sequence: Propranolol controls the "
            "adrenergic symptoms and also inhibits peripheral T4-to-T3 conversion. PTU (not methimazole) "
            "is preferred because it additionally blocks T4→T3 conversion. Lugol's iodine (Wolff-Chaikoff "
            "effect) must be administered at least 1 hour after PTU to prevent the iodine from being "
            "organified into new thyroid hormone. Hydrocortisone reduces peripheral conversion and also "
            "covers relative adrenal insufficiency. Giving iodine before PTU is a dangerous error."
        ),
        "high_yield_takeaway": (
            "Thyroid storm sequence: Propranolol → PTU → Iodide (1 hr after PTU) → Hydrocortisone. "
            "Never give iodine before PTU. Aspirin is contraindicated."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralMedicine", "#MBBS", "#NEETPG", "#ThyroidStorm"],
    },

    # ── 5. Concise Notes ────────────────────────────────────────────────────
    {
        "title": "Heart Failure: NYHA Classification & Management",
        "subject": Subject.general_medicine,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "Heart failure management is a 5-mark gift — know every drug class",
        "caption": (
            "HEART FAILURE — NYHA CLASSIFICATION & MANAGEMENT\n\n"
            "SECTION 1 — NYHA FUNCTIONAL CLASSIFICATION:\n"
            "• Class I: No symptoms with ordinary activity\n"
            "• Class II: Slight limitation; comfortable at rest, symptomatic with moderate exertion\n"
            "• Class III: Marked limitation; comfortable at rest, symptomatic with minimal exertion\n"
            "• Class IV: Symptoms at rest; unable to carry on any activity without discomfort\n\n"
            "SECTION 2 — TERMINOLOGY:\n"
            "• HFrEF (Heart Failure with Reduced EF): EF <40%; systolic dysfunction\n"
            "• HFpEF (Preserved EF): EF ≥50%; diastolic dysfunction\n"
            "• HFmrEF (Mildly reduced EF): EF 41–49%\n\n"
            "SECTION 3 — MANAGEMENT OF HFrEF (Evidence-based mortality benefit):\n"
            "The 'Fantastic Four' disease-modifying therapies:\n"
            "1. ACE inhibitor / ARB (or ARNI — Sacubitril/Valsartan): preferred first-line\n"
            "2. Beta blocker: Carvedilol, Metoprolol succinate, Bisoprolol (the three proven)\n"
            "3. Aldosterone antagonist: Spironolactone/Eplerenone (NYHA III–IV or post-MI HF)\n"
            "4. SGLT2 inhibitor: Dapagliflozin/Empagliflozin (proven mortality benefit in HFrEF)\n\n"
            "SECTION 4 — SYMPTOMATIC RELIEF:\n"
            "• Loop diuretics (Furosemide): relieve congestion; no mortality benefit\n"
            "• Digoxin: reduces hospitalisations; no mortality benefit; used in AF + HF\n"
            "• Hydralazine + Nitrates: alternative if ACEi/ARB intolerant (especially in Black patients)\n\n"
            "SECTION 5 — DEVICES:\n"
            "• ICD: EF <35% despite optimal therapy (>40 days post-MI)\n"
            "• CRT (Cardiac Resynchronisation): EF <35% + LBBB + QRS >150 ms + NYHA II–IV\n\n"
            "EXAM TIP: ARNI (Sacubitril/Valsartan) = superior to ACEi in symptomatic HFrEF; "
            "avoid with ACEi concurrently (36-hr washout needed)."
        ),
        "high_yield_takeaway": (
            "HFrEF 'Fantastic Four': ACEi/ARNI + Beta blocker + Aldosterone antagonist + SGLT2i. "
            "Furosemide relieves symptoms but has no mortality benefit. ICD if EF <35%."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralMedicine", "#MBBS", "#NEETPG", "#HeartFailure"],
    },

    # ── 6. PYQ Concept ──────────────────────────────────────────────────────
    {
        "title": "Acid-Base Disorders — PYQ Pattern",
        "subject": Subject.general_medicine,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Acid-base questions: 5 marks every year — crack the algorithm",
        "caption": (
            "ACID-BASE DISORDERS — HIGH-YIELD PYQ TABLE\n\n"
            "DISORDER         pH    PaCO₂   HCO₃⁻   COMPENSATION\n"
            "──────────────────────────────────────────────────────────\n"
            "Metabolic acidosis  ↓    ↓       ↓↓     ↓PaCO₂ (Winter's)\n"
            "Metabolic alkalosis ↑    ↑       ↑↑     ↑PaCO₂ (0.7 per mEq↑HCO₃)\n"
            "Resp. acidosis      ↓    ↑↑      ↑      ↑HCO₃ (acute: 1; chronic: 3.5)\n"
            "Resp. alkalosis     ↑    ↓↓      ↓      ↓HCO₃ (acute: 2; chronic: 5)\n\n"
            "WINTER'S FORMULA (expected PaCO₂ in metabolic acidosis):\n"
            "Expected PaCO₂ = 1.5 × HCO₃ + 8 ± 2\n"
            "If actual PaCO₂ < expected → additional resp alkalosis\n"
            "If actual PaCO₂ > expected → additional resp acidosis\n\n"
            "ANION GAP = Na − (Cl + HCO₃) | Normal: 8–12 mEq/L\n\n"
            "HIGH ANION GAP METABOLIC ACIDOSIS (MUDPILES):\n"
            "M — Methanol  U — Uraemia  D — DKA  P — Propylene glycol\n"
            "I — Isoniazid/Iron  L — Lactic acidosis  E — Ethylene glycol  S — Salicylates\n\n"
            "NORMAL ANION GAP METABOLIC ACIDOSIS (HARDUP):\n"
            "H — Hyperalimentation  A — Acetazolamide  R — RTA (type 1,2,4)\n"
            "D — Diarrhoea  U — Ureteral diversion  P — Post-hypocapnia\n\n"
            "DELTA-DELTA RATIO (in high AG met acidosis):\n"
            "(AG − 12) / (24 − HCO₃)\n"
            "• <0.4: pure NAGMA  • 0.4–0.8: mixed HAGMA + NAGMA\n"
            "• 1–2: pure HAGMA   • >2: HAGMA + metabolic alkalosis"
        ),
        "high_yield_takeaway": (
            "Winter's formula: Expected PaCO₂ = 1.5×HCO₃ + 8 ± 2. MUDPILES = high AG metabolic acidosis. "
            "Delta-Delta >2 suggests coexisting metabolic alkalosis."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralMedicine", "#MBBS", "#NEETPG", "#AcidBase"],
    },
]
