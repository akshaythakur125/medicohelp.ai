"""High-yield Radiology content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ───────────────────────────────────────────────────────
    {
        "title": "Classic X-Ray Signs in Medicine",
        "subject": Subject.radiology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Classic X-ray signs every NEET-PG candidate must know — from tramlines to sunburst!",
        "caption": (
            "Classic X-Ray Signs in Medicine — Rapid Revision\n\n"
            "CHEST X-RAY SIGNS:\n"
            "• Hampton's hump: Wedge-shaped pleural-based opacity in pulmonary embolism (infarction)\n"
            "• Westermark sign: Hyperlucency distal to PE (oligaemia)\n"
            "• Bat-wing/Butterfly opacity: Bilateral perihilar oedema in pulmonary oedema\n"
            "• Tramline shadows: Parallel lines = bronchiectasis (thickened bronchial walls)\n"
            "• Golden S sign: Right upper lobe collapse + central mass (right hilar tumour)\n"
            "• Sail sign: Thymic shadow in normal neonates (not pathological)\n"
            "• Meniscus sign: Pleural effusion — concave upper border\n\n"
            "ABDOMINAL X-RAY SIGNS:\n"
            "• Football sign: Large oval radiolucency (free air outlines both sides of bowel wall)\n"
            "• Rigler's sign (double-wall sign): Free air outlines outer bowel wall\n"
            "• Thumb-printing: Mucosal oedema in ischaemic colitis, bowel ischaemia\n"
            "• String of beads: Small bowel obstruction (air in valvulae conniventes)\n"
            "• Coffee bean sign: Sigmoid volvulus — inverted U-shaped dilated loop\n\n"
            "BONE X-RAY SIGNS:\n"
            "• Sunburst periosteal reaction: Osteosarcoma\n"
            "• Onion-peel periosteal reaction: Ewing's sarcoma\n"
            "• Codman's triangle: Aggressive bone tumour (not specific to one tumour)\n"
            "• Soap-bubble appearance: Giant cell tumour (GCT), aneurysmal bone cyst\n"
            "• Ground-glass appearance: Fibrous dysplasia\n"
            "• Rugger-jersey spine: Renal osteodystrophy (alternating sclerosis/lucency)\n\n"
            "MISCELLANEOUS:\n"
            "• Eggshell calcification: Silicosis (lymph nodes), sarcoidosis\n"
            "• Lead-pipe colon: Chronic ulcerative colitis (loss of haustra)\n"
            "• String sign of Kantor: Crohn's disease (terminal ileum narrowing)"
        ),
        "high_yield_takeaway": "Hampton's hump = PE infarct. Sunburst = osteosarcoma. Onion-peel = Ewing's. Coffee bean = sigmoid volvulus. Bat-wing = pulmonary oedema.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Radiology", "#XRaySigns"],
    },
    {
        "title": "CT vs MRI — When to Use Which Modality",
        "subject": Subject.radiology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "CT vs MRI — choose the right modality every time! NEET-PG rapid revision.",
        "caption": (
            "CT vs MRI — When to Use Which\n\n"
            "COMPUTED TOMOGRAPHY (CT):\n"
            "Strengths:\n"
            "• Fast (minutes) — ideal for emergencies, trauma, unstable patients\n"
            "• Excellent for bone detail, calcifications, acute haemorrhage (bright on non-contrast CT)\n"
            "• Best for: Acute intracranial haemorrhage, chest/abdominal trauma, pulmonary embolism (CTPA),\n"
            "  bony trauma, pneumothorax, pneumoperitoneum\n\n"
            "Limitations: Ionising radiation; poor soft-tissue contrast vs MRI; iodinated contrast nephrotoxicity\n\n"
            "MRI:\n"
            "Strengths:\n"
            "• No ionising radiation — safe in children, pregnancy (after 1st trimester), multiple scans\n"
            "• Superior soft-tissue contrast\n"
            "• Best for: Brain tumours, posterior fossa lesions, spinal cord pathology, multiple sclerosis,\n"
            "  ligament/cartilage injuries (knee, shoulder), liver/biliary disease (MRCP), pelvic pathology,\n"
            "  early osteomyelitis, prostate/uterine tumours\n\n"
            "Limitations: Slower (30–60 min); claustrophobia; metallic implant contraindication;\n"
            "gadolinium contraindicated in severe renal failure (GFR < 30) → nephrogenic systemic fibrosis\n\n"
            "KEY CLINICAL SCENARIOS — EXAM FAVOURITES:\n"
            "• Acute stroke: CT first (to exclude haemorrhage) → then MRI (DWI for ischaemia, detects within minutes)\n"
            "• MS plaques: MRI (periventricular white matter, Dawson's fingers)\n"
            "• ACL tear: MRI knee\n"
            "• Appendicitis in pregnancy: Ultrasound first → MRI if inconclusive (avoid CT radiation)\n"
            "• Renal colic: CECT abdomen\n"
            "• Subarachnoid haemorrhage: CT first → LP if CT negative\n"
            "• Posterior fossa tumour: MRI (CT misses due to bony artefact)\n"
            "• Early avascular necrosis: MRI (CT/X-ray normal in early stages)"
        ),
        "high_yield_takeaway": "CT: fast, acute haemorrhage, bone, trauma. MRI: soft tissue, posterior fossa, spine, MS, no radiation. Acute stroke → CT first, then MRI-DWI.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Radiology", "#CTvsMRI"],
    },
    # ── MCQ ──────────────────────────────────────────────────────────────────
    {
        "title": "Contrast Media Reactions — Classification and Management MCQ",
        "subject": Subject.radiology,
        "content_format": ContentFormat.mcq,
        "poster_text": "Patient develops anaphylaxis after contrast injection — how do you classify and manage it?",
        "caption": (
            "Contrast Media Reactions — Classification and Management\n\n"
            "TYPES OF CONTRAST AGENTS:\n"
            "• Iodinated (CT): High-osmolar (ionic, e.g., diatrizoate) vs Low-osmolar (non-ionic, e.g., iohexol, iopamidol)\n"
            "• Gadolinium-based (MRI): Risk of NSF (nephrogenic systemic fibrosis) in severe renal failure\n"
            "• Barium sulphate (GI): Water-insoluble; never use if perforation suspected → use water-soluble contrast\n\n"
            "ADVERSE REACTIONS TO IODINATED CONTRAST:\n"
            "Chemotoxic (dose-dependent):\n"
            "• Contrast-induced nephropathy (CIN): Creatinine rise > 25% or > 0.5 mg/dL within 48–72 hr\n"
            "• Prevention: IV hydration with normal saline; N-acetylcysteine (controversial); avoid nephrotoxins\n\n"
            "Idiosyncratic (anaphylactoid — not IgE mediated):\n"
            "• Mild: Nausea, vomiting, urticaria, mild flushing — no treatment needed\n"
            "• Moderate: Generalised urticaria, bronchospasm, mild hypotension — IV antihistamines, bronchodilators\n"
            "• Severe (anaphylactoid): Laryngeal oedema, severe bronchospasm, cardiovascular collapse — EPINEPHRINE\n\n"
            "RISK FACTORS for contrast reaction:\n"
            "• Previous reaction to contrast (strongest risk factor)\n"
            "• Asthma, atopy\n"
            "• Renal impairment (for nephropathy)\n"
            "• Metformin: Hold 48 hrs before and after contrast (lactic acidosis risk in CIN)"
        ),
        "question": (
            "A 55-year-old asthmatic woman with a history of mild urticaria to contrast media undergoes CECT abdomen. "
            "Shortly after contrast injection she develops generalised urticaria, stridor, severe dyspnoea, and her blood "
            "pressure drops to 70/40 mmHg. Which of the following is the most appropriate immediate treatment?"
        ),
        "options": [
            "A. Intravenous hydrocortisone 200 mg stat and IV chlorphenamine 10 mg",
            "B. Intramuscular adrenaline (epinephrine) 0.5 mg of 1:1000 solution into the anterolateral thigh",
            "C. Intravenous salbutamol infusion for bronchospasm management",
            "D. Oral cetirizine 10 mg and observation for 2 hours in the radiology department",
        ],
        "correct_answer": "B. Intramuscular adrenaline (epinephrine) 0.5 mg of 1:1000 solution into the anterolateral thigh",
        "explanation": (
            "This patient is experiencing severe anaphylaxis (anaphylactoid reaction to contrast): stridor (laryngeal oedema), severe bronchospasm, generalised urticaria, and cardiovascular collapse (hypotension). "
            "The first-line treatment for anaphylaxis — regardless of the trigger — is intramuscular adrenaline (epinephrine) 0.5 mg of 1:1000 (0.5 mL) into the anterolateral thigh; this is superior to IV route in most settings due to faster onset and greater safety margin. "
            "IM adrenaline acts on alpha-1 receptors (vasoconstriction, reverses hypotension), beta-2 receptors (bronchodilation), and stabilises mast cells. "
            "Corticosteroids and antihistamines are adjuncts — they are too slow to treat the acute life-threatening phase and should NOT be given before adrenaline. "
            "IV salbutamol may be added for persistent bronchospasm after adrenaline but is not first-line. "
            "This patient's prior history of contrast reaction and asthma placed her at high risk — pre-medication with steroids and antihistamines should have been considered before the procedure."
        ),
        "high_yield_takeaway": "Severe contrast anaphylaxis: IM adrenaline 0.5 mg (1:1000) into thigh is FIRST-LINE. Corticosteroids and antihistamines are adjuncts, not first-line.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Radiology", "#ContrastReaction"],
    },
    {
        "title": "Pneumoperitoneum on X-Ray — MCQ",
        "subject": Subject.radiology,
        "content_format": ContentFormat.mcq,
        "poster_text": "Patient with acute abdomen — identify the X-ray sign of free air under the diaphragm!",
        "caption": (
            "Pneumoperitoneum — X-Ray Diagnosis\n\n"
            "Definition: Free air in the peritoneal cavity — a surgical emergency\n\n"
            "COMMON CAUSES:\n"
            "• Perforated peptic ulcer (#1 cause of pneumoperitoneum)\n"
            "• Perforated hollow viscus (typhoid — terminal ileum, diverticulitis, appendicitis)\n"
            "• Iatrogenic: Post-laparoscopy, post-colonoscopy\n"
            "• Trauma: Bowel injury\n\n"
            "X-RAY SIGNS OF PNEUMOPERITONEUM:\n"
            "• Erect CXR: Free air under right hemidiaphragm (most sensitive plain film view)\n"
            "• Rigler's sign (double-wall sign): Free air on both sides of bowel wall (both walls visible)\n"
            "• Football sign: Large oval radiolucency in abdomen (seen on supine AXR)\n"
            "• Falciform ligament sign: Free air outlines falciform ligament\n"
            "• Inverted V sign: Free air outlines medial umbilical ligaments\n"
            "• Cupola sign: Air accumulates under central tendon of diaphragm on supine film\n\n"
            "INVESTIGATION OF CHOICE:\n"
            "• Erect CXR: First-line (as little as 1 mL of air detectable)\n"
            "• CT abdomen: Most sensitive; identifies cause and site of perforation\n"
            "• Left lateral decubitus: Alternative if patient cannot stand — air rises to right side\n\n"
            "Remember: Physiological pneumoperitoneum — post-surgery, persists up to 7–10 days after laparotomy"
        ),
        "question": (
            "A 45-year-old man presents to the emergency department with sudden-onset severe epigastric pain that quickly "
            "became generalised. He is a known peptic ulcer patient on NSAIDs. Examination reveals board-like rigidity, "
            "absent bowel sounds, and guarding. Erect chest X-ray is taken. Which X-ray sign is most likely to be seen, "
            "and what is the most sensitive investigation for confirming the diagnosis?"
        ),
        "options": [
            "A. Rigler's sign on erect CXR; barium swallow is the investigation of choice to locate the perforation site",
            "B. Free air under right hemidiaphragm on erect CXR; CT abdomen is the most sensitive investigation",
            "C. Football sign on erect CXR; ultrasound abdomen is the most sensitive investigation",
            "D. Meniscus sign on erect CXR; MRI abdomen is gold standard for perforation diagnosis",
        ],
        "correct_answer": "B. Free air under right hemidiaphragm on erect CXR; CT abdomen is the most sensitive investigation",
        "explanation": (
            "Perforated peptic ulcer is the most common cause of pneumoperitoneum. The classic X-ray finding on erect chest X-ray is free air (radiolucency) under the right hemidiaphragm — this is the most clinically used and widely available initial imaging. "
            "CT abdomen with IV contrast (or without in an emergency) is the most sensitive investigation, detecting even tiny amounts of free air, locating the perforation site, and identifying associated complications. "
            "Barium swallow is absolutely contraindicated in suspected perforation as barium causes severe chemical peritonitis; water-soluble contrast should be used if a swallow study is necessary. "
            "Rigler's sign is seen on supine AXR (not erect CXR), and the football sign is also a supine AXR finding. "
            "MRI has no role in the acute setting for bowel perforation due to its limited availability and time constraints."
        ),
        "high_yield_takeaway": "Pneumoperitoneum: free air under right diaphragm on erect CXR (most used). CT is most sensitive. NEVER give barium in perforation — use water-soluble contrast.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Radiology", "#Pneumoperitoneum"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "Radiation Safety and Protection — Concise Notes",
        "subject": Subject.radiology,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "Radiation safety principles — ALARA, dose limits, and biological effects for NEET-PG.",
        "caption": (
            "Radiation Safety and Protection — Concise Notes\n\n"
            "UNITS OF RADIATION:\n"
            "• Roentgen (R): Unit of radiation exposure (ionisation in air)\n"
            "• Rad (Radiation Absorbed Dose): Energy absorbed per unit mass; 1 rad = 0.01 Gray\n"
            "• Gray (Gy): SI unit of absorbed dose; 1 Gy = 100 rad\n"
            "• Rem (Roentgen Equivalent Man): Biological effect; 1 rem = 0.01 Sievert\n"
            "• Sievert (Sv): SI unit of effective dose (accounts for tissue sensitivity)\n\n"
            "ALARA PRINCIPLE:\n"
            "As Low As Reasonably Achievable — the guiding principle of radiation protection\n\n"
            "THREE PRINCIPLES OF RADIATION PROTECTION:\n"
            "1. Time: Minimise exposure time — dose is proportional to time\n"
            "2. Distance: Inverse square law — doubling distance reduces dose to 1/4\n"
            "3. Shielding: Lead aprons (0.25–0.5 mm Pb equivalent) for workers; leaded glass, barriers\n\n"
            "ANNUAL DOSE LIMITS (ICRP/AERB):\n"
            "• Radiation workers: 20 mSv/year averaged over 5 years (max 50 mSv in any single year)\n"
            "• General public: 1 mSv/year\n"
            "• Pregnant radiation workers: 1 mSv to foetus during pregnancy\n"
            "• Eye lens: 150 mSv/year (workers); 15 mSv/year (public)\n\n"
            "BIOLOGICAL EFFECTS:\n"
            "Stochastic (probabilistic, no threshold):\n"
            "• Cancer induction, hereditary effects — probability increases with dose\n"
            "• No safe threshold — any dose carries theoretical risk\n\n"
            "Deterministic (threshold exists — severity increases above threshold):\n"
            "• Radiation sickness, cataracts, sterility, hair loss — require minimum dose\n"
            "• Cataracts: Threshold 2 Gy to lens; erythema: 3 Gy to skin\n\n"
            "MOST RADIOSENSITIVE TISSUES (rapidly dividing):\n"
            "• Gonads > Bone marrow > Gut epithelium > Skin > Lens of eye\n"
            "• Most radioresistant: Nervous tissue, muscle, bone\n\n"
            "COMMON DOSES FOR REFERENCE:\n"
            "• Chest X-ray: 0.02 mSv | CT chest: 7 mSv | CT abdomen: 10 mSv\n"
            "• Annual background radiation (India): ~2 mSv"
        ),
        "high_yield_takeaway": "ALARA: Time, Distance (inverse square law), Shielding. Radiation workers: 20 mSv/year. Stochastic = no threshold (cancer). Gonads most radiosensitive.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Radiology", "#RadiationSafety"],
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "Chest X-Ray Findings — PYQ Pattern",
        "subject": Subject.radiology,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Chest X-ray findings and their diagnoses — the most tested PYQ pattern in Radiology!",
        "caption": (
            "Chest X-Ray Findings — PYQ High-Yield Pattern\n\n"
            "MEDIASTINAL WIDENING (> 8 cm on PA CXR):\n"
            "• Aortic dissection / traumatic aortic tear (high-energy trauma)\n"
            "• Anterior mediastinal masses (4 T's): Thymoma, Teratoma, Thyroid, Terrible lymphoma\n"
            "• Superior vena cava syndrome: Bilateral mediastinal widening + superior mediastinal mass\n\n"
            "HILAR ENLARGEMENT:\n"
            "• Bilateral hilar lymphadenopathy (BHL): Sarcoidosis (#1), lymphoma, TB, silicosis\n"
            "• Unilateral: Primary TB, carcinoma bronchus, lymphoma\n"
            "• Egg-shell calcification of hilar nodes: Silicosis, sarcoidosis\n\n"
            "COIN LESION (Solitary Pulmonary Nodule):\n"
            "• Benign features: Smooth margins, calcification (central/popcorn/laminar), size < 3 cm, stable 2 years\n"
            "• Malignant features: Spiculated/irregular margins, > 3 cm, growing, no calcification\n"
            "• Causes: TB (most common worldwide), hamartoma (popcorn calcification), carcinoid, metastasis\n\n"
            "OPACIFICATION PATTERNS:\n"
            "• Bat-wing opacity: Pulmonary oedema\n"
            "• Homogeneous opacity with air-bronchogram: Consolidation (pneumonia, alveolar cell carcinoma)\n"
            "• Miliary pattern: TB, sarcoidosis, metastases (thyroid, renal cell, melanoma)\n"
            "• Reticulonodular pattern: Interstitial lung disease, pulmonary fibrosis\n\n"
            "PLEURAL EFFUSION:\n"
            "• Blunting of costophrenic angle (> 200–300 mL)\n"
            "• Massive effusion: White-out with mediastinal shift AWAY from effusion\n"
            "• Massive effusion with no mediastinal shift: Consider mesothelioma (encasing) or carcinoma (fixing)\n"
            "• Fluid in fissure: Lenticular (lens-shaped) opacity — 'vanishing tumour'\n\n"
            "PYQ ANSWER KEY:\n"
            "Q: Bilateral hilar lymphadenopathy — most common cause? → Sarcoidosis\n"
            "Q: Mediastinal widening after trauma? → Aortic dissection/tear\n"
            "Q: Popcorn calcification in coin lesion? → Hamartoma\n"
            "Q: Miliary pattern on CXR — most common infectious cause? → Tuberculosis\n"
            "Q: Massive effusion without mediastinal shift → → Mesothelioma or central bronchogenic carcinoma\n"
            "Q: Air bronchogram seen in? → Consolidation (not collapse — bronchi collapsed too)"
        ),
        "high_yield_takeaway": "BHL #1 = sarcoidosis. Popcorn calcification = hamartoma. Massive effusion + no shift = mesothelioma. Air bronchogram = consolidation (not collapse).",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Radiology", "#PYQ"],
    },
    # ── Mnemonic ─────────────────────────────────────────────────────────────
    {
        "title": "Mediastinal Masses — 4T / 3B / 3N Mnemonic",
        "subject": Subject.radiology,
        "content_format": ContentFormat.mnemonic,
        "poster_text": "Mediastinal compartments and their masses: 4T (anterior) / 3B (middle) / 3N (posterior)",
        "caption": (
            "Mediastinal Masses — Compartment Mnemonics\n\n"
            "Anterior Mediastinum (prevascular) — 4 T's:\n"
            "T1 — Thymoma (most common anterior mediastinal mass in adults)\n"
            "T2 — Teratoma / Germ cell tumours (seminoma, non-seminoma)\n"
            "T3 — Thyroid mass (retrosternal goitre: most common cause of superior mediastinal mass)\n"
            "T4 — Terrible lymphoma (Hodgkin's > NHL; anterior mediastinal nodes)\n\n"
            "Middle Mediastinum (visceral) — 3 B's:\n"
            "B1 — Bronchogenic cyst (most common mediastinal cyst; near carina)\n"
            "B2 — Bronchogenic carcinoma (central tumours, hilar nodes)\n"
            "B3 — Broncho-oesophageal cysts (rare; near oesophagus)\n\n"
            "Posterior Mediastinum (paravertebral) — 3 N's:\n"
            "N1 — Neurogenic tumours (most common posterior mediastinal mass)\n"
            "  — Schwannoma, neurofibroma, ganglioneuroma, neuroblastoma\n"
            "N2 — Neurenteric cysts (associated with vertebral anomalies)\n"
            "N3 — Notochord remnants (extramedullary hematopoiesis)\n\n"
            "Key radiological clue:\n"
            "• Lateral CXR: Anterior = behind sternum; Middle = around hilum; Posterior = in front of spine\n"
            "• CT is the investigation of choice for assessing mediastinal masses\n"
            "• Calcification: Seen in teratoma (teeth/bone), thymoma, goitre, lymph nodes (TB/silicosis)\n\n"
            "⚠️ Exam Trap: Most common anterior mediastinal mass in adults = Thymoma. "
            "Most common posterior = Neurogenic tumour. Most common overall = Thymoma."
        ),
        "high_yield_takeaway": "Anterior: 4T (Thymoma, Teratoma, Thyroid, Terrible lymphoma). Middle: 3B (Bronchogenic cyst/carcinoma, Broncho-oesophageal). Posterior: 3N (Neurogenic, Neurenteric, Notochord).",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Radiology", "#Mnemonic", "#Mediastinum"],
    },
    # ── Flashcard ─────────────────────────────────────────────────────────────
    {
        "title": "Imaging in Acute Stroke — CT vs MRI-DWI Approach",
        "subject": Subject.radiology,
        "content_format": ContentFormat.flashcard,
        "poster_text": "Acute stroke imaging: CT first (exclude haemorrhage) → MRI-DWI for ischaemic stroke confirmation",
        "caption": (
            "Imaging in Acute Stroke — Flashcard\n\n"
            "GOAL: Differentiate ischaemic vs haemorrhagic stroke; assess for thrombolysis candidacy.\n\n"
            "NON-CONTRAST CT HEAD (First-line, within 20 min of arrival):\n"
            "• Purpose: EXCLUDE intracranial haemorrhage BEFORE thrombolysis\n"
            "• Hyperdense vessel sign: Clot in MCA → hyperdense MCA sign (early ischaemic sign)\n"
            "• Loss of grey-white differentiation: Insular ribbon sign, blurring of basal ganglia\n"
            "• ASPECTS score: 10-point scoring system for MCA territory; score ≤ 7 = poor outcome\n"
            "• Sensitivity for acute ischaemia: Low in first 6 hours (about 50–60%)\n\n"
            "CT ANGIOGRAPHY (CTA):\n"
            "• Identifies vessel occlusion (carotid, MCA, basilar)\n"
            "• Collateral assessment\n"
            "• Performed if thrombectomy is being considered\n\n"
            "CT PERFUSION (CTP):\n"
            "• Ischaemic core (irreversible) vs penumbra (salvageable — target for reperfusion)\n"
            "• Mismatch ratio: core < 70 mL, mismatch > 1.2, penumbra > 15 mL\n\n"
            "MRI BRAIN WITH DWI:\n"
            "• DWI: Positive within MINUTES of ischaemic onset (earliest and most sensitive)\n"
            "• ADC: Restricted diffusion → dark on ADC map\n"
            "• MRI shows ischaemia within 30–60 min vs CT which may be normal for 6–12 hours\n"
            "• T2/FLAIR: Positive at 6–12 hours (DWI-FLAIR mismatch helps time the stroke)\n"
            "• GRE/SWI: Detects haemorrhage (blooming artefact) — alternative if CT not done\n\n"
            "THROMBOLYSIS ELIGIBILITY:\n"
            "• Alteplase (tPA): 0.9 mg/kg IV (max 90 mg): within 4.5 hours of symptom onset\n"
            "• Contraindications: Haemorrhage on CT, recent surgery/stroke, BP > 185/110, INR > 1.7\n"
            "• Mechanical thrombectomy: Up to 24 hours for selected patients (large vessel occlusion)\n\n"
            "⚠️ Exam Trap: CT is always first (rules out bleed). DWI-MRI is most sensitive for acute ischaemia. "
            "Thrombolysis window = 4.5 hours. Thrombectomy window = up to 24 hours."
        ),
        "question": "What is the imaging approach for acute stroke and how does DWI-MRI differ from non-contrast CT?",
        "correct_answer": "CT head first (exclude haemorrhage). MRI-DWI most sensitive for acute ischaemia. Thrombolysis ≤4.5h. Thrombectomy ≤24h for LVO.",
        "high_yield_takeaway": "Acute stroke: CT first (rule out bleed) → MRI-DWI (most sensitive for ischaemia). Alteplase ≤ 4.5 hrs. Thrombectomy ≤ 24 hrs for LVO.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Radiology", "#Flashcard", "#Stroke"],
    },
    # ── True/False ────────────────────────────────────────────────────────────
    {
        "title": "CT for Posterior Fossa Brain Tumour Assessment",
        "subject": Subject.radiology,
        "content_format": ContentFormat.true_false,
        "poster_text": "CT is NOT the best modality for posterior fossa — MRI is superior due to lack of beam-hardening artefact",
        "caption": (
            "True or False: Non-contrast CT of the head is the investigation of choice for evaluating\n"
            "a suspected posterior fossa brain tumour.\n\n"
            "ANSWER: FALSE\n\n"
            "MRI is the investigation of choice for posterior fossa pathology, NOT CT.\n\n"
            "Reasons:\n"
            "1. Beam-hardening artefact on CT: The dense petrous temporal bones and occipital bone\n"
            "   cause severe streak artefact in the posterior fossa, obscuring the brainstem,\n"
            "   cerebellum, and 4th ventricle\n"
            "2. Poor soft-tissue contrast: CT poorly differentiates grey-white matter,\n"
            "   oedema, and tumour margins in the posterior fossa\n"
            "3. MRI superior soft-tissue resolution: Clearly delineates cerebellar hemispheres,\n"
            "   brainstem, 4th ventricle, and CP angle\n\n"
            "Common posterior fossa tumours (more common in children):\n"
            "• Medulloblastoma: 4th ventricle, midline, hyperdense on CT, restricted diffusion\n"
            "• Pilocytic astrocytoma: Cerebellar hemisphere, cystic + enhancing mural nodule\n"
            "• Ependymoma: 4th ventricle → 'extends through foramina' (Luschka, Magendie)\n"
            "• Brainstem glioma: Diffuse expansion of pons\n"
            "• Haemangioblastoma: Cerebellar, cystic with mural nodule; associated with VHL\n"
            "• CP angle masses: Vestibular schwannoma, meningioma, epidermoid\n\n"
            "When is CT useful for posterior fossa?\n"
            "• Acute haemorrhage (CT detects blood well)\n"
            "• Calcification (tumour calcification)\n"
            "• Bony assessment (acoustic neuroma → IAM widening)\n\n"
            "⚠️ Exam Trap: Posterior fossa tumour in child → MRI. "
            "CT 'misses' posterior fossa lesions due to bone artefact."
        ),
        "question": "Non-contrast CT head is the investigation of choice for evaluating a suspected posterior fossa brain tumour.",
        "correct_answer": "FALSE",
        "explanation": "MRI is the investigation of choice for posterior fossa pathology. CT images the posterior fossa poorly due to beam-hardening artefact from the petrous temporal bones. MRI provides superior soft-tissue contrast without bone artefact.",
        "high_yield_takeaway": "Posterior fossa → MRI (not CT — bone artefact). CT is first-line for acute haemorrhage or bony assessment.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Radiology", "#TrueFalse", "#PosteriorFossa"],
    },
    # ── One-liner Recall ──────────────────────────────────────────────────────
    {
        "title": "Gold Standard Investigation for Acute Intracranial Haemorrhage",
        "subject": Subject.radiology,
        "content_format": ContentFormat.one_liner_recall,
        "poster_text": "Non-contrast CT head is the gold standard for diagnosing acute intracranial haemorrhage",
        "caption": (
            "One-liner Recall: Acute Intracranial Haemorrhage\n\n"
            "Fill in the blank:\n\n"
            "\"The gold standard investigation for diagnosing acute intracranial haemorrhage is ___\"\n\n"
            "Answer: Non-contrast CT (NCCT) head\n\n"
            "Why NCCT is gold standard:\n"
            "• 95–100% sensitivity for acute blood (0–72 hours)\n"
            "• Blood appears hyperdense (white, 60–80 HU) on NCCT\n"
            "• Detects: Subarachnoid, intraparenchymal, subdural, epidural, intraventricular haemorrhage\n"
            "• Fast (minutes) — critical in emergency settings\n"
            "• Widely available, no contraindications (vs MRI)\n\n"
            "Types of haemorrhage on CT:\n"
            "• Epidural: Biconvex/lentiform; does NOT cross suture lines; may cross falx\n"
            "• Subdural: Crescentic; crosses suture lines; does NOT cross falx\n"
            "• Subarachnoid: Blood in basal cisterns, sylvian fissures, sulci\n"
            "• Intraparenchymal: Hyperdense mass within brain tissue\n"
            "• Intraventricular: Blood layering in occipital horns (sedimentation)\n\n"
            "Timing of blood on CT:\n"
            "• Acute (0–72 hrs): Hyperdense (white)\n"
            "• Subacute (3–21 days): Isodense → may be missed\n"
            "• Chronic (> 21 days): Hypodense (liquefaction)\n\n"
            "⚠️ Exam Trap: If CT is negative for SAH but clinical suspicion remains → "
            "perform LP (xanthochromia after 12 hours). CT sensitivity for SAH drops from 98% (day 1) to 50% (day 7)."
        ),
        "question": "The gold standard investigation for diagnosing acute intracranial haemorrhage is ___",
        "correct_answer": "Non-contrast CT head (NCCT)",
        "high_yield_takeaway": "Acute haemorrhage → NCCT (hyperdense 60-80 HU). SAH → CT first, then LP if negative. Epidural = biconvex, Subdural = crescentic.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Radiology", "#OneLiner", "#ICH"],
    },
]
