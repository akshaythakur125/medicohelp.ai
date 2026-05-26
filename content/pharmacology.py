"""High-yield Pharmacology content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ───────────────────────────────────────────────────────
    {
        "title": "Beta-Blockers — Selective vs Non-Selective",
        "subject": Subject.pharmacology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Cardioselective beta-blockers (β1 > β2): safer in asthma, diabetes",
        "caption": (
            "Beta-Blockers — Selective vs Non-Selective — Rapid Revision\n\n"
            "MECHANISM: Competitive antagonism of catecholamines at beta-adrenergic receptors\n"
            "• β1 receptors: Heart (↓ HR, ↓ contractility, ↓ AV conduction), Kidney (↓ renin release)\n"
            "• β2 receptors: Bronchi (bronchoconstriction), Vasculature, Uterus, Liver (↓ glycogenolysis)\n\n"
            "CARDIOSELECTIVE (β1 > β2) — 'A-B-E-M' mnemonic:\n"
            "• Atenolol — no ISA; long half-life; renal excretion\n"
            "• Bisoprolol — most cardioselective; heart failure drug of choice\n"
            "• Esmolol — ultra-short acting (IV); perioperative tachycardia\n"
            "• Metoprolol — cardioselective; metabolised by CYP2D6\n"
            "• Nebivolol — most cardioselective; also causes NO-mediated vasodilation\n\n"
            "NON-SELECTIVE (β1 + β2):\n"
            "• Propranolol — prototype; also blocks Na⁺ channel (membrane stabilising)\n"
            "• Timolol — glaucoma (↓ aqueous humour production)\n"
            "• Carvedilol — also α1 blocker → vasodilation; used in heart failure\n"
            "• Labetalol — α1 + β1 + β2 blocker; drug of choice for hypertension in pregnancy\n"
            "• Nadolol, Sotalol (also K⁺ channel blocker — Class III antiarrhythmic)\n\n"
            "SPECIAL PROPERTIES:\n"
            "• ISA (intrinsic sympathomimetic activity): Pindolol, Acebutolol — partial agonist; causes less bradycardia\n"
            "• Lipid solubility: Propranolol (high) → crosses BBB → nightmares, depression\n"
            "• Atenolol (low lipid solubility) → fewer CNS side effects\n\n"
            "CONTRAINDICATIONS: Asthma/COPD (non-selective), AV block, Prinzmetal angina, uncontrolled HF\n"
            "⚠️ Exam Trap: β-blockers can mask hypoglycaemia symptoms (except sweating) — caution in diabetes."
        ),
        "high_yield_takeaway": "Cardioselective (β1) = Atenolol, Bisoprolol, Esmolol, Metoprolol, Nebivolol. Labetalol = α1+β blocker = drug of choice in hypertension in pregnancy.",
        "hashtags": ["#MedicoHelp", "#Pharmacology", "#MBBS", "#NEETPG", "#BetaBlockers"],
    },
    {
        "title": "Aminoglycoside Toxicity — Key Facts",
        "subject": Subject.pharmacology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Aminoglycosides: nephrotoxic + ototoxic — once-daily dosing reduces toxicity",
        "caption": (
            "Aminoglycoside Toxicity — Rapid Revision\n\n"
            "CLASS: Gentamicin, Amikacin, Tobramycin, Streptomycin, Neomycin, Kanamycin\n"
            "MECHANISM: Bind 30S ribosomal subunit → misreading of mRNA → bactericidal\n"
            "PHARMACOKINETICS: Concentration-dependent killing; post-antibiotic effect (PAE)\n"
            "  → Once-daily dosing (ODD) preferred — equal efficacy, less toxicity\n\n"
            "TOXICITY PROFILE:\n\n"
            "1. NEPHROTOXICITY\n"
            "• Accumulate in proximal tubular cells → tubular necrosis\n"
            "• Non-oliguric acute kidney injury; usually reversible\n"
            "• Risk factors: Pre-existing renal disease, dehydration, vancomycin co-use, age\n"
            "• Monitor: Creatinine, urine output, serum trough levels\n\n"
            "2. OTOTOXICITY\n"
            "• Vestibular toxicity: Streptomycin > Gentamicin (vertigo, ataxia, nystagmus)\n"
            "• Cochlear toxicity: Amikacin > Neomycin (high-frequency hearing loss — irreversible)\n"
            "• Mechanism: Accumulate in perilymph → free radical damage to hair cells\n"
            "• Risk: Prolonged therapy, renal failure, loop diuretics (additive ototoxicity)\n\n"
            "3. NEUROMUSCULAR BLOCKADE\n"
            "• Rare; inhibits acetylcholine release at NMJ\n"
            "• Risk: Post-operatively with anaesthesia; myasthenia gravis patients\n"
            "• Reversal: IV calcium gluconate\n\n"
            "4. TERATOGENICITY\n"
            "• Streptomycin: Category D — causes fetal hearing loss\n"
            "• Avoid in pregnancy (use azithromycin for susceptible infections)\n\n"
            "CLINICAL USES:\n"
            "• Gentamicin: Gram-negative sepsis, endocarditis (synergy)\n"
            "• Amikacin: MDR TB, hospital-acquired infections\n"
            "• Neomycin: Hepatic encephalopathy (oral)\n"
            "• Streptomycin: TB second-line agent\n\n"
            "⚠️ Exam Trap: Gentamicin therapeutic range: Peak 5–10 μg/mL; Trough <2 μg/mL."
        ),
        "high_yield_takeaway": "Aminoglycosides: nephrotoxic (proximal tubule) + ototoxic (irreversible cochlear). Streptomycin = vestibular. Amikacin = cochlear. Reversal of NMJ block = IV calcium.",
        "hashtags": ["#MedicoHelp", "#Pharmacology", "#MBBS", "#NEETPG", "#Aminoglycosides"],
    },
    # ── MCQ ───────────────────────────────────────────────────────────────────
    {
        "title": "Anticoagulants: Heparin vs Warfarin — MCQ",
        "subject": Subject.pharmacology,
        "content_format": ContentFormat.mcq,
        "poster_text": "Heparin = immediate onset, IV/SC, reversed by protamine; Warfarin = oral, days onset",
        "caption": "MCQ: Choosing the correct anticoagulant and understanding their reversal",
        "question": (
            "A 32-year-old pregnant woman at 28 weeks gestation presents with acute deep vein thrombosis "
            "of the left femoral vein confirmed on Doppler ultrasound. She requires anticoagulation for "
            "treatment. Which of the following statements about her anticoagulant management is CORRECT?"
        ),
        "options": [
            "A. Warfarin is the drug of choice; it does not cross the placenta",
            "B. Low molecular weight heparin (LMWH) is safe in pregnancy; it does not cross the placenta",
            "C. Rivaroxaban is safe in pregnancy and preferred over heparin",
            "D. Unfractionated heparin is preferred over LMWH due to better bioavailability",
        ],
        "correct_answer": "B. Low molecular weight heparin (LMWH) is safe in pregnancy; it does not cross the placenta",
        "explanation": (
            "LMWH (e.g., enoxaparin) does not cross the placenta due to its large molecular weight and "
            "is the drug of choice for DVT treatment in pregnancy. Warfarin DOES cross the placenta and "
            "is teratogenic in the first trimester (warfarin embryopathy: nasal hypoplasia, stippled epiphyses) "
            "and causes fetal haemorrhage in late pregnancy — it is contraindicated. "
            "DOACs (rivaroxaban, apixaban) are also contraindicated in pregnancy (risk of fetal bleeding, "
            "lack of safety data). UFH also does not cross the placenta but has lower bioavailability "
            "and requires IV/SC administration with aPTT monitoring, making LMWH preferred for its "
            "predictable pharmacokinetics and once/twice-daily SC dosing."
        ),
        "high_yield_takeaway": "LMWH = drug of choice for DVT in pregnancy (does NOT cross placenta). Warfarin = contraindicated in pregnancy (teratogenic, fetal haemorrhage). DOACs = also contraindicated.",
        "hashtags": ["#MedicoHelp", "#Pharmacology", "#MBBS", "#NEETPG", "#Anticoagulants"],
    },
    {
        "title": "Teratogenic Drugs — MCQ",
        "subject": Subject.pharmacology,
        "content_format": ContentFormat.mcq,
        "poster_text": "Thalidomide = phocomelia; Valproate = NTD; Warfarin = nasal hypoplasia in fetus",
        "caption": "MCQ: Identifying the correct teratogen from fetal defect description",
        "question": (
            "A 26-year-old woman with epilepsy was maintained on a single anticonvulsant throughout her "
            "pregnancy. At birth, her neonate is found to have a lumbar myelomeningocele (open neural "
            "tube defect). She was also noted to have taken folic acid supplements, but the defect "
            "still occurred. Which drug is MOST LIKELY responsible for this outcome?"
        ),
        "options": [
            "A. Lamotrigine",
            "B. Levetiracetam",
            "C. Sodium valproate",
            "D. Carbamazepine",
        ],
        "correct_answer": "C. Sodium valproate",
        "explanation": (
            "Sodium valproate is the most teratogenic of all commonly used anticonvulsants and causes "
            "neural tube defects (NTDs) in up to 1-2% of exposed fetuses, primarily via inhibition of "
            "folic acid metabolism. It is associated with spina bifida (myelomeningocele) specifically. "
            "The risk is not completely abolished even with periconceptional folic acid supplementation. "
            "Carbamazepine also causes NTDs but at a lower rate (0.5%). "
            "Lamotrigine and levetiracetam have significantly lower teratogenic risk and are preferred "
            "anticonvulsants in women of childbearing age. Valproate should be avoided in women of "
            "reproductive potential unless no safer alternative exists."
        ),
        "high_yield_takeaway": "Sodium valproate = highest teratogenic risk among anticonvulsants → neural tube defects (spina bifida). Avoid in pregnancy; prefer lamotrigine or levetiracetam.",
        "hashtags": ["#MedicoHelp", "#Pharmacology", "#MBBS", "#NEETPG", "#Teratogens"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "ACE Inhibitors vs ARBs — Concise Notes",
        "subject": Subject.pharmacology,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "ACEi = dry cough (bradykinin); ARBs = no cough, same renal protection",
        "caption": (
            "ACE Inhibitors vs ARBs — Concise Notes\n\n"
            "RAAS: Renin → Ang I → [ACE] → Ang II → AT1 receptor (vasoconstriction, aldosterone, Na retention)\n\n"
            "ACE INHIBITORS: Ramipril, Enalapril, Lisinopril, Captopril (prototype), Perindopril\n"
            "Mechanism: Block ACE → ↓ Ang II + ↑ Bradykinin\n\n"
            "ARBs: Losartan, Valsartan, Irbesartan, Candesartan, Telmisartan\n"
            "Mechanism: Block AT1 receptor → ↓ Ang II effects; bradykinin NOT elevated\n\n"
            "COMPARISON:\n"
            "Feature         ACE Inhibitors       ARBs\n"
            "────────────────────────────────────────────────\n"
            "Dry cough       YES (bradykinin ↑)   NO\n"
            "Angioedema      YES (rare)           Less common\n"
            "Renal protect.  YES                  YES (similar)\n"
            "Teratogenicity  YES (Category D)     YES\n"
            "────────────────────────────────────────────────\n\n"
            "INDICATIONS (Both):\n"
            "• Hypertension (first-line with DM/CKD)\n"
            "• Diabetic nephropathy (↓ proteinuria)\n"
            "• HFrEF, post-MI cardioprotection\n\n"
            "CONTRAINDICATIONS (Both):\n"
            "• Pregnancy (renal agenesis, oligohydramnios)\n"
            "• Bilateral renal artery stenosis\n"
            "• Hyperkalaemia; Angioedema (for ACEi)\n\n"
            "⚠️ Exam Trap: ACEi + ARB dual RAAS blockade is NOT recommended — ↑ AKI and hyperkalaemia risk.\n"
            "Captopril (sulfhydryl group) → rash and taste disturbance."
        ),
        "high_yield_takeaway": "ACEi → dry cough (bradykinin accumulation); switch to ARB if intolerable. Both contraindicated in pregnancy, bilateral RAS. Both protect kidneys in DM nephropathy.",
        "hashtags": ["#MedicoHelp", "#Pharmacology", "#MBBS", "#NEETPG", "#ACEInhibitors"],
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "Drug-Receptor Interactions — PYQ Pattern",
        "subject": Subject.pharmacology,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Agonist, antagonist, partial agonist, inverse agonist — the concept NEET-PG tests yearly",
        "caption": (
            "Drug-Receptor Interactions — PYQ Concept\n\n"
            "AFFINITY: Drug's ability to bind a receptor\n"
            "EFFICACY (Intrinsic Activity): Ability to produce a response after binding\n\n"
            "Drug Classes by Receptor Activity:\n"
            "─────────────────────────────────────────────────────\n"
            "Type            Affinity  Efficacy     Effect\n"
            "─────────────────────────────────────────────────────\n"
            "Full agonist    +         High (1.0)   Maximal response\n"
            "Partial agonist +         <1.0         Submaximal response\n"
            "Antagonist      +         Zero         Blocks agonist; no response\n"
            "Inverse agonist +         Negative     Reduces constitutive activity\n"
            "─────────────────────────────────────────────────────\n\n"
            "Partial Agonist:\n"
            "• Alone: weak agonist; with full agonist: functional antagonist\n"
            "• Examples: Buprenorphine (opioid), Pindolol (ISA β-blocker), Buspirone (5-HT1A)\n\n"
            "Competitive vs Non-competitive Antagonism:\n"
            "──────────────────────────────────────────────────────────\n"
            "Feature     Competitive          Non-competitive\n"
            "──────────────────────────────────────────────────────────\n"
            "Mechanism   Reversible; competes  Irreversible/allosteric\n"
            "Vmax        Unchanged             ↓ (cannot overcome)\n"
            "EC50        ↑ Rightward shift     Rightward + depressed\n"
            "Example     Naloxone              Phenoxybenzamine\n"
            "──────────────────────────────────────────────────────────\n\n"
            "Receptor Types:\n"
            "• Ionotropic (GABA-A, NMDA, nAChR): fastest (ms)\n"
            "• G-protein coupled (β-adrenergic, muscarinic): seconds\n"
            "• Tyrosine kinase (Insulin, GH): hours\n"
            "• Nuclear (steroids, thyroid hormone): hours to days\n\n"
            "Therapeutic Index (TI) = LD50 / ED50\n"
            "Narrow TI: Digoxin, Phenytoin, Lithium, Warfarin, Aminoglycosides"
        ),
        "high_yield_takeaway": "Partial agonist = submaximal response alone, competitive antagonist vs full agonist. Competitive antagonist = ↑ EC50, same Vmax. Non-competitive = ↓ Vmax.",
        "hashtags": ["#MedicoHelp", "#Pharmacology", "#MBBS", "#NEETPG", "#PYQ"],
    },
    # ── Mnemonic ──────────────────────────────────────────────────────────────
    {
        "title": "NOT GASES — Beta-Blocker Side Effects",
        "subject": Subject.pharmacology,
        "content_format": ContentFormat.mnemonic,
        "poster_text": "NOT GASES = Bronchoconstriction, Heart block, Glucose masked, lipids↑, Sexual dysfunction, Fatigue, Sleep disturbance",
        "caption": (
            "Mnemonic: NOT GASES — Beta-Blocker Side Effects\n\n"
            "N — No beta2 stimulation → Bronchoconstriction\n"
            "   (Dangerous in asthma/COPD; use cardioselective agents with caution)\n\n"
            "O — (Heart) bLOCk → Bradycardia + AV block\n"
            "   (Contraindicated in 2nd/3rd degree AV block; sick sinus syndrome)\n\n"
            "T — (Hypogly)T(caemia masked) → Masks hypoglycaemic warning signs\n"
            "   (Blocks tachycardia response; sweating still present; use with caution in DM)\n\n"
            "G — Glucose/lipid effects → ↑ TG, ↓ HDL (non-cardioselective worse)\n\n"
            "A — (Sexu)A(l dysfunction) → Impotence/decreased libido\n\n"
            "S — Sudden fatigue + (cold) extremities (↓ cardiac output, vasoconstriction)\n\n"
            "E — (Sl)E(ep disturbance) → Nightmares, insomnia (lipophilic: propranolol, metoprolol)\n\n"
            "S — (Rebound) Syndrome on abrupt withdrawal → Rebound hypertension, angina, MI\n\n"
            "Memory hook: When NOT on GASES, side effects creep in.\n\n"
            "⚠️ Exam Trap: Abrupt withdrawal of beta-blockers can precipitate MI in CAD patients — always taper.\n"
            "Lipophilic (propranolol, metoprolol) → cross BBB → more CNS side effects."
        ),
        "high_yield_takeaway": "Beta-blocker SEs: bronchoconstriction, bradycardia/AV block, hypoglycaemia masking, ↑TG/↓HDL, sexual dysfunction, fatigue, sleep disturbance. Never stop abruptly in CAD.",
        "hashtags": ["#MedicoHelp", "#Pharmacology", "#MBBS", "#NEETPG", "#Mnemonic"],
    },
    # ── Flashcard ─────────────────────────────────────────────────────────────
    {
        "title": "First-Line Antihypertensive in Pregnancy",
        "subject": Subject.pharmacology,
        "content_format": ContentFormat.flashcard,
        "poster_text": "First-line antihypertensive in pregnancy = Methyldopa or Labetalol",
        "caption": (
            "First-Line Drug for Hypertension in Pregnancy — Flashcard\n\n"
            "QUESTION: Which antihypertensive is safe in pregnancy as first-line?\n\n"
            "ANSWER: Methyldopa (first-line, longest safety record) or Labetalol (IV for acute)\n\n"
            "Safe antihypertensives in pregnancy:\n"
            "• Methyldopa: Alpha-2 agonist; longest safety data; first-line for chronic HTN in pregnancy\n"
            "• Labetalol: Alpha + beta blocker; IV form for hypertensive urgency in pregnancy\n"
            "• Nifedipine (CCB): Oral; used in pre-eclampsia; tocolytic at high doses\n"
            "• Hydralazine: IV for acute pre-eclampsia; direct vasodilator\n\n"
            "CONTRAINDICATED in pregnancy:\n"
            "• ACE inhibitors (ramipril, enalapril): Teratogenic (renal agenesis, oligohydramnios)\n"
            "• ARBs (losartan, valsartan): Same mechanism — contraindicated\n"
            "• Atenolol: Associated with IUGR; avoid\n\n"
            "Pre-eclampsia severe: MgSO4 (seizure prophylaxis) + IV labetalol or hydralazine\n\n"
            "⚠️ Exam Trap: ACEi/ARBs are Category D/X in pregnancy — must switch before conception if possible."
        ),
        "question": "Which antihypertensive is safe and used as first-line in pregnancy?",
        "correct_answer": "Methyldopa (first-line, safest long-term record) and Labetalol (IV for acute). Nifedipine and Hydralazine are also safe. ACE inhibitors and ARBs are CONTRAINDICATED in pregnancy.",
        "high_yield_takeaway": "Safe in pregnancy: Methyldopa (1st line), Labetalol, Nifedipine, Hydralazine. CONTRAINDICATED: ACEi and ARBs (renal teratogens). MgSO4 for pre-eclampsia seizure prophylaxis.",
        "hashtags": ["#MedicoHelp", "#Pharmacology", "#MBBS", "#NEETPG", "#Flashcard"],
    },
    # ── True/False ────────────────────────────────────────────────────────────
    {
        "title": "ACE Inhibitors in Pregnancy — Safe or Not?",
        "subject": Subject.pharmacology,
        "content_format": ContentFormat.true_false,
        "poster_text": "ACE inhibitors = CONTRAINDICATED in pregnancy (teratogenic — renal agenesis)",
        "caption": (
            "True or False: ACE inhibitors are safe and recommended in pregnancy for hypertension management.\n\n"
            "ANSWER: FALSE\n\n"
            "ACE inhibitors are CONTRAINDICATED in pregnancy — they are known teratogens.\n\n"
            "Mechanism of teratogenicity:\n"
            "• Angiotensin II is essential for normal fetal renal development\n"
            "• ACEi block Ang II → fetal renal hypoperfusion\n"
            "• Result: Renal tubular dysplasia, renal agenesis\n"
            "• Leads to: Oligohydramnios → pulmonary hypoplasia, limb contractures, IUGR\n"
            "• ACE inhibitor fetopathy / neonatal renal failure\n\n"
            "FDA/pregnancy categories:\n"
            "• 1st trimester: Category C (risk of cardiovascular malformations)\n"
            "• 2nd–3rd trimester: Category D (confirmed fetotoxicity)\n"
            "• ARBs: Same mechanism — equally contraindicated\n\n"
            "What to use instead:\n"
            "• Methyldopa (safest, first-line)\n"
            "• Labetalol (IV for acute), Nifedipine, Hydralazine\n\n"
            "Post-partum: ACEi/ARBs can be restarted (compatible with breastfeeding at low doses)\n\n"
            "⚠️ Exam Trap: Women on ACEi/ARBs planning pregnancy should be switched BEFORE conception."
        ),
        "question": "ACE inhibitors are safe and recommended in pregnancy for hypertension management.",
        "correct_answer": "FALSE",
        "explanation": "ACE inhibitors are CONTRAINDICATED in pregnancy. They block Ang II-dependent fetal renal development, causing renal agenesis, oligohydramnios, pulmonary hypoplasia and IUGR. ARBs are equally contraindicated. Use Methyldopa or Labetalol instead.",
        "high_yield_takeaway": "ACEi/ARBs = contraindicated in pregnancy (teratogen — renal agenesis, oligohydramnios). Switch to Methyldopa or Labetalol. Risk greatest in 2nd-3rd trimester.",
        "hashtags": ["#MedicoHelp", "#Pharmacology", "#MBBS", "#NEETPG", "#TrueFalse"],
    },
    # ── One-liner Recall ──────────────────────────────────────────────────────
    {
        "title": "Morphine Mechanism — One-liner Recall",
        "subject": Subject.pharmacology,
        "content_format": ContentFormat.one_liner_recall,
        "poster_text": "Morphine: mu-opioid agonist; reversed by naloxone",
        "caption": (
            "One-liner Recall: Morphine Mechanism\n\n"
            "Fill in the blank:\n\n"
            "\"Morphine mechanism: acts on ___ receptors; reversed by ___\"\n\n"
            "Answer: Mu (μ) opioid receptors (also kappa and delta); reversed by Naloxone\n\n"
            "Full picture:\n"
            "• Primary receptor: Mu (μ) opioid receptor (GPCR — Gi coupled)\n"
            "  → ↓ cAMP, opens K⁺ channels, closes Ca²⁺ channels → ↓ neuronal excitability\n"
            "• Kappa (κ): dysphoria, sedation, spinal analgesia\n"
            "• Delta (δ): mood, spinal analgesia\n\n"
            "Morphine clinical pharmacology:\n"
            "• Analgesia, euphoria, sedation, respiratory depression, constipation (no tolerance)\n"
            "• Miosis (pinpoint pupils): pathognomonic of opioid toxicity\n"
            "• Histamine release: hypotension, pruritus, bronchospasm\n\n"
            "Reversal agents:\n"
            "• Naloxone: competitive opioid antagonist; short-acting (re-narcotization risk)\n"
            "• Naltrexone: longer-acting; oral; used in addiction\n\n"
            "⚠️ Exam Trap: Constipation from opioids has NO tolerance development. Miosis persists."
        ),
        "question": "Morphine mechanism: acts on ___ receptors; reversed by ___",
        "correct_answer": "Mu (μ) opioid receptors (Gi-coupled GPCR); reversed by Naloxone",
        "high_yield_takeaway": "Morphine = mu-opioid agonist (Gi-coupled). Causes miosis, respiratory depression, constipation (no tolerance). Reversed by Naloxone. Constipation has no tolerance.",
        "hashtags": ["#MedicoHelp", "#Pharmacology", "#MBBS", "#NEETPG", "#OneLiner"],
    },
]
