"""High-yield Anesthesiology content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ───────────────────────────────────────────────────────
    {
        "title": "Mallampati Classification and Airway Assessment",
        "subject": Subject.anesthesiology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Airway assessment tools — Mallampati, thyromental distance, 3-3-2 rule for NEET-PG!",
        "caption": (
            "Mallampati Classification and Airway Assessment — Rapid Revision\n\n"
            "MALLAMPATI CLASSIFICATION (mouth open, tongue protruded, seated, no phonation):\n"
            "• Class I: Soft palate, uvula, fauces, pillars visible — easy intubation\n"
            "• Class II: Soft palate, uvula, fauces visible — easy intubation\n"
            "• Class III: Soft palate, base of uvula visible — difficult laryngoscopy\n"
            "• Class IV: Only hard palate visible — very difficult (anticipate failed intubation)\n\n"
            "OTHER PREDICTORS OF DIFFICULT AIRWAY:\n"
            "• Thyromental distance (TMD): < 6 cm (< 3 finger breadths) → difficult intubation\n"
            "• Sternomental distance: < 12.5 cm → difficult\n"
            "• Mouth opening (inter-incisor distance): < 3 cm → difficult\n"
            "• 3-3-2 Rule: < 3 finger mouth opening, < 3 finger hyoid-to-chin, < 2 finger thyroid-to-floor of mouth\n"
            "• Neck mobility: < 35° extension → difficult\n"
            "• BMI > 35, short neck, retrognathia, micrognathia, large tongue, beard\n\n"
            "CORMACK-LEHANE GRADING (laryngoscopic view):\n"
            "• Grade I: Full glottis visible — easy\n"
            "• Grade II: Only posterior commissure/arytenoids visible\n"
            "• Grade III: Only epiglottis visible — difficult\n"
            "• Grade IV: Neither glottis nor epiglottis visible — failed intubation\n\n"
            "DIFFICULT AIRWAY MANAGEMENT (ASA Algorithm):\n"
            "• Anticipated difficult airway: Awake fibreoptic intubation (gold standard)\n"
            "• Unanticipated: Call for help, video laryngoscope, supraglottic airway (LMA)\n"
            "• Cannot intubate, cannot oxygenate (CICO): Emergency cricothyrotomy\n\n"
            "Remember: Pre-oxygenation with 100% O2 for 3–5 minutes extends safe apnoea time to 8–10 min in healthy adults"
        ),
        "high_yield_takeaway": "Mallampati III/IV + TMD < 6 cm + CL Grade III/IV = difficult airway. CICO emergency → cricothyrotomy. Awake FOI for anticipated difficult airway.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Anesthesiology", "#AirwayManagement"],
    },
    {
        "title": "Inhalational Anaesthetic Agents — MAC Values and Properties",
        "subject": Subject.anesthesiology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "MAC values and key properties of inhalational anaesthetics — NEET-PG rapid revision!",
        "caption": (
            "Inhalational Anaesthetic Agents — MAC Values and Properties\n\n"
            "MAC (Minimum Alveolar Concentration): Concentration at which 50% of patients do not move in response to surgical incision — measure of potency.\n"
            "Rule: Lower MAC = higher potency\n\n"
            "MAC VALUES (in O2 at 1 atmosphere):\n"
            "• Halothane: 0.75% — most potent volatile agent\n"
            "• Enflurane: 1.68%\n"
            "• Isoflurane: 1.15% — current gold standard volatile agent\n"
            "• Sevoflurane: 2.05% — most commonly used today (rapid onset/offset)\n"
            "• Desflurane: 6.0% — fastest onset/offset; good for day-case surgery; pungent (airway irritant)\n"
            "• Nitrous oxide (N2O): 104% — cannot produce anaesthesia alone at atmospheric pressure; used as adjunct\n\n"
            "FACTORS MODIFYING MAC:\n"
            "Decrease MAC (reduces anaesthetic requirement):\n"
            "• Opioids, benzodiazepines, alcohol (acute intoxication), hypothermia, hyponatraemia, elderly age, pregnancy\n\n"
            "Increase MAC (increases anaesthetic requirement):\n"
            "• Hyperthermia, chronic alcohol use, hyperthyroidism, young age, cocaine/amphetamines\n\n"
            "KEY AGENT PROPERTIES:\n"
            "• Halothane: Hepatotoxicity (halothane hepatitis — Type II = immune-mediated, rare but serious), sensitises myocardium to catecholamines → arrhythmias; rarely used now\n"
            "• Sevoflurane: Safe in paediatrics; compound A formation (nephrotoxic in rats, not clinically significant); no airway irritation → mask induction\n"
            "• Desflurane: Lowest blood:gas partition coefficient (0.42) after N2O → fastest recovery\n"
            "• Isoflurane: Causes coronary steal (controversial); increases cerebral blood flow; safe for neuro-anaesthesia\n"
            "• N2O: Bone marrow depression with prolonged use; expands air-filled cavities → avoid in pneumothorax, bowel obstruction, middle ear surgery; diffusion hypoxia on discontinuation (give 100% O2)"
        ),
        "high_yield_takeaway": "Lower MAC = more potent. Halothane hepatitis → immune-mediated. N2O expands air cavities. Sevoflurane for paediatric mask induction. Desflurane = fastest recovery.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Anesthesiology", "#InhalationalAgents"],
    },
    # ── MCQ ──────────────────────────────────────────────────────────────────
    {
        "title": "Malignant Hyperthermia — Diagnosis and Management MCQ",
        "subject": Subject.anesthesiology,
        "content_format": ContentFormat.mcq,
        "poster_text": "Masseter spasm and rising CO2 after suxamethonium — is this malignant hyperthermia?",
        "caption": (
            "Malignant Hyperthermia — Key Facts\n\n"
            "Definition: Life-threatening hypermetabolic crisis triggered by volatile anaesthetics or succinylcholine in genetically susceptible individuals\n\n"
            "Genetics: Autosomal dominant; mutation in ryanodine receptor (RYR1) gene — uncontrolled Ca2+ release from sarcoplasmic reticulum → sustained muscle contraction\n\n"
            "TRIGGERS:\n"
            "• Volatile agents: Halothane, sevoflurane, desflurane, isoflurane, enflurane\n"
            "• Succinylcholine (suxamethonium)\n"
            "• SAFE agents: Propofol, opioids, non-depolarising NMBs, nitrous oxide, local anaesthetics\n\n"
            "CLINICAL FEATURES (in order of appearance):\n"
            "1. Masseter muscle rigidity after succinylcholine (early warning)\n"
            "2. Rising end-tidal CO2 (earliest and most sensitive monitor sign)\n"
            "3. Hyperthermia (temperature rises 1–2°C every 5 minutes — LATE sign)\n"
            "4. Tachycardia, arrhythmias\n"
            "5. Mixed metabolic + respiratory acidosis\n"
            "6. Myoglobinuria → acute kidney injury\n"
            "7. Massively elevated creatine kinase (CPK)\n\n"
            "TREATMENT:\n"
            "• STOP triggering agent immediately\n"
            "• Dantrolene sodium: SPECIFIC antidote; 2.5 mg/kg IV bolus, repeat as needed up to 10 mg/kg; inhibits ryanodine receptor → stops Ca2+ release\n"
            "• Cooling measures, correct acidosis, treat hyperkalaemia, maintain urine output\n"
            "• Switch to safe anaesthetic (TIVA with propofol)\n\n"
            "Screening: In vitro caffeine halothane contracture test (IVCT) — gold standard for susceptibility testing"
        ),
        "question": (
            "A 22-year-old man undergoing appendicectomy develops masseter spasm immediately after receiving "
            "succinylcholine, followed by rapidly rising end-tidal CO2 to 72 mmHg, tachycardia of 140 bpm, "
            "and temperature of 39.8°C (rising). Arterial blood gas shows mixed metabolic and respiratory acidosis. "
            "Which of the following is the most appropriate immediate treatment?"
        ),
        "options": [
            "A. Intravenous neostigmine to reverse the succinylcholine-induced rigidity",
            "B. Intravenous dantrolene sodium 2.5 mg/kg; discontinue volatile agents and succinylcholine; institute active cooling",
            "C. Intravenous bicarbonate to correct acidosis as the primary intervention",
            "D. Propofol infusion to deepen anaesthesia and reduce muscle rigidity",
        ],
        "correct_answer": "B. Intravenous dantrolene sodium 2.5 mg/kg; discontinue volatile agents and succinylcholine; institute active cooling",
        "explanation": (
            "The clinical picture — masseter spasm after succinylcholine, rapidly rising end-tidal CO2 (earliest sensitive sign), hyperthermia, tachycardia, and mixed acidosis in a young patient — is classic for malignant hyperthermia (MH). "
            "MH is caused by an uncontrolled release of calcium from the sarcoplasmic reticulum (usually due to RYR1 mutation), triggered by volatile anaesthetics and succinylcholine. "
            "The specific antidote is dantrolene sodium (2.5 mg/kg IV, repeated up to 10 mg/kg), which inhibits the ryanodine receptor and halts calcium release; it must be given immediately alongside stopping all triggering agents. "
            "Active cooling, correction of acidosis and hyperkalaemia, and maintenance of urine output (dantrolene contains mannitol) are essential supportive measures. "
            "Neostigmine has no role in MH; propofol can be used as a safe anaesthetic to continue surgery if needed but does not treat MH itself; bicarbonate treats acidosis as a secondary measure but does not address the underlying pathology."
        ),
        "high_yield_takeaway": "MH: RYR1 mutation, triggered by volatile agents + succinylcholine. Rising ETCO2 = earliest sign. Antidote = dantrolene 2.5 mg/kg IV. Stop trigger immediately.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Anesthesiology", "#MalignantHyperthermia"],
    },
    {
        "title": "Spinal vs Epidural Anaesthesia — Comparison MCQ",
        "subject": Subject.anesthesiology,
        "content_format": ContentFormat.mcq,
        "poster_text": "Spinal vs epidural anaesthesia — differences, complications and clinical scenarios for NEET-PG!",
        "caption": (
            "Spinal vs Epidural Anaesthesia — Comparison\n\n"
            "SPINAL (Subarachnoid Block — SAB):\n"
            "• Site: Subarachnoid space (CSF); below L1-L2 in adults (conus medullaris ends at L1)\n"
            "• Needle: Spinal needle (25–27G; Quincke/Whitacre/Sprotte)\n"
            "• Volume: Small (1.5–3.5 mL heavy bupivacaine)\n"
            "• Onset: Rapid (2–5 min)\n"
            "• Block: Dense (motor + sensory); predictable spread\n"
            "• Duration: Fixed (2–4 hours depending on drug)\n"
            "• Hypotension: Abrupt, significant (sympathetic block)\n"
            "• Post-dural puncture headache (PDPH): More common (especially with larger needles)\n\n"
            "EPIDURAL:\n"
            "• Site: Epidural space (outside dura, does NOT enter CSF)\n"
            "• Needle: Tuohy needle (16–18G); loss of resistance technique\n"
            "• Volume: Large (10–20 mL or via catheter)\n"
            "• Onset: Slower (15–20 min)\n"
            "• Block: Segmental, less dense; catheter allows continuous/prolonged analgesia\n"
            "• Duration: Adjustable via catheter top-ups\n"
            "• Uses: Labour analgesia, post-operative pain, thoracic surgery\n\n"
            "COMPLICATIONS COMMON TO BOTH:\n"
            "• Hypotension (treat: IV fluids, ephedrine/phenylephrine)\n"
            "• Urinary retention, nausea/vomiting, backache\n"
            "• Total spinal (if epidural dose given intrathecally): Apnoea, cardiovascular collapse\n\n"
            "CONTRAINDICATIONS:\n"
            "• Absolute: Patient refusal, coagulopathy, infection at site, raised ICP\n"
            "• Relative: Sepsis, hypovolaemia, fixed cardiac output states"
        ),
        "question": (
            "A 28-year-old primigravida in active labour requests pain relief. She is 5 cm dilated, haemodynamically stable, "
            "and has no contraindications. Her obstetrician plans a vaginal delivery but wants an option for a potential "
            "emergency caesarean section. Which regional anaesthesia technique is most appropriate and what is the key advantage "
            "of this approach over a single-shot spinal?"
        ),
        "options": [
            "A. Single-shot spinal with heavy bupivacaine; advantage is predictable rapid dense motor block ideal for surgery",
            "B. Epidural catheter technique; advantage is the ability to provide continuous labour analgesia and extend block for caesarean section if needed",
            "C. Combined spinal-epidural only if caesarean section is definitively planned; not appropriate for labour analgesia",
            "D. Paravertebral block; advantage is unilateral sensory block without motor weakness",
        ],
        "correct_answer": "B. Epidural catheter technique; advantage is the ability to provide continuous labour analgesia and extend block for caesarean section if needed",
        "explanation": (
            "An epidural catheter is the ideal technique for this scenario because it provides continuous, adjustable analgesia throughout labour via repeated top-ups or infusion, and can be rapidly extended to a surgical block (by injecting a larger volume of higher-concentration local anaesthetic, e.g., 2% lignocaine with adrenaline) if an emergency caesarean section is required — avoiding the risks of urgent general anaesthesia. "
            "Single-shot spinal would provide excellent surgical anaesthesia but offers a fixed duration with no flexibility for prolonged labour; if delivery is delayed or caesarean is needed beyond the block's duration, the patient would require repeat spinal or conversion to general anaesthesia. "
            "A combined spinal-epidural (CSE) technique is also excellent in this setting — it combines the rapid onset of spinal block with the flexibility of an epidural catheter — and is increasingly used for elective caesarean section. "
            "Paravertebral block is not appropriate for labour analgesia or caesarean section as it cannot reliably cover the sacral dermatomes required for delivery."
        ),
        "high_yield_takeaway": "Epidural = continuous via catheter, adjustable, ideal for labour + emergency CS extension. Spinal = rapid dense block, fixed duration. CSE = combines both advantages.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Anesthesiology", "#RegionalAnesthesia"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "Rapid Sequence Induction (RSI) Protocol",
        "subject": Subject.anesthesiology,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "RSI step-by-step — indications, drugs, and Sellick's manoeuvre explained for NEET-PG.",
        "caption": (
            "Rapid Sequence Induction (RSI) — Concise Notes\n\n"
            "DEFINITION: Technique to secure the airway rapidly while minimising pulmonary aspiration risk "
            "in patients with a 'full stomach' or increased aspiration risk.\n\n"
            "INDICATIONS (Full Stomach / Aspiration Risk):\n"
            "• Emergency surgery (not fasted)\n"
            "• Pregnancy ≥16 weeks (raised intra-abdominal pressure + delayed gastric emptying)\n"
            "• Symptomatic GERD/hiatus hernia\n"
            "• Bowel obstruction, ileus\n"
            "• Trauma (delayed gastric emptying)\n"
            "• Morbid obesity\n\n"
            "RSI STEPS (7 P's):\n"
            "1. Preparation: IV access, monitors, emergency drugs, suction, difficult airway equipment ready\n"
            "2. Pre-oxygenation: 100% O2 for 3–5 minutes via tight-fitting face mask (MANDATORY)\n"
            "3. Pre-treatment (optional): Lidocaine (raised ICP), atropine (paediatrics), opioid (blunt pressor response)\n"
            "4. Paralysis + Induction (simultaneous):\n"
            "   — Induction: Propofol (stable), ketamine (compromised), thiopentone (raised ICP), etomidate (shocked)\n"
            "   — NMB: Succinylcholine 1.5–2 mg/kg (gold standard for RSI)\n"
            "     OR rocuronium 1.2 mg/kg (reversed with sugammadex if needed)\n"
            "5. Protection (Sellick's manoeuvre): BURP on cricoid to occlude oesophagus; "
            "controversial — release if it impedes intubation\n"
            "6. Placement of ETT: Confirm with ETCO2 waveform capnography (gold standard)\n"
            "7. Post-intubation: Inflate cuff, bilateral breath sounds, CXR, secure tube\n\n"
            "SUCCINYLCHOLINE CONTRAINDICATIONS:\n"
            "• Hyperkalaemia (burns/crush >24 hrs, denervation injuries, prolonged immobility)\n"
            "  — Risk of lethal hyperkalaemic cardiac arrest\n"
            "• Personal/family history of malignant hyperthermia\n"
            "• Pseudocholinesterase deficiency → prolonged paralysis ('scoline apnoea')\n"
            "• Penetrating eye injury (transient IOP rise)"
        ),
        "high_yield_takeaway": "RSI: Pre-oxygenation → simultaneous induction + succinylcholine → Sellick's → intubation. Confirm with ETCO2 waveform. Succinylcholine CI: hyperkalaemia, MH, pseudocholinesterase deficiency.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Anesthesiology", "#RSI"],
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "Post-Operative Complications — Timeline PYQ Pattern",
        "subject": Subject.anesthesiology,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Post-operative complications by time — fever, DVT, wound dehiscence — NEET-PG PYQ favourite!",
        "caption": (
            "Post-Operative Complications — Timeline PYQ Pattern\n\n"
            "The timing of post-operative complications is one of the most tested PYQ patterns in surgery and anaesthesia.\n\n"
            "IMMEDIATE (Within 24 hours):\n"
            "• Primary haemorrhage: At time of surgery (technical failure)\n"
            "• Reactionary haemorrhage: Within 24 hours — rise in BP dislodges clot\n"
            "• Respiratory: Atelectasis (most common post-op pulmonary complication), laryngospasm, bronchospasm\n"
            "• Cardiovascular: Arrhythmias, hypotension\n"
            "• Oliguria: Pre-renal → inadequate fluid resuscitation\n\n"
            "EARLY (24 hours to 1 week):\n"
            "• Fever mnemonic — 5 W's by day:\n"
            "  — Day 1: Wind — atelectasis/pneumonia (most common cause of early post-op fever)\n"
            "  — Day 3–5: Water — urinary tract infection (UTI; catheter-related)\n"
            "  — Day 5: Wound — surgical site infection (SSI)\n"
            "  — Day 5–7: Walking — deep vein thrombosis (DVT)\n"
            "  — Day 7+: Wonder drugs — drug fever, malignant hyperthermia\n"
            "• Wound haematoma/seroma\n"
            "• Paralytic ileus (most common bowel complication; absent bowel sounds, distension)\n\n"
            "INTERMEDIATE (1–6 weeks):\n"
            "• Secondary haemorrhage: At ~7–10 days → wound infection/erosion of vessel\n"
            "• Pulmonary embolism: Peak at 7–10 days (after DVT organises)\n"
            "• Wound dehiscence: 7–10 days (abdominal wound — 'serous pink fluid' from wound)\n"
            "• Anastomotic leak: Day 5–7 (small bowel > large bowel)\n\n"
            "LATE (> 6 weeks):\n"
            "• Incisional hernia: Months\n"
            "• Adhesive intestinal obstruction: Months to years\n"
            "• Post-cholecystectomy syndrome\n"
            "• Dumping syndrome (post-gastrectomy)\n\n"
            "PYQ ANSWER KEY:\n"
            "Q: Most common cause of post-op fever on day 1? → Atelectasis (Wind)\n"
            "Q: Most common post-op pulmonary complication? → Atelectasis\n"
            "Q: Serosanguinous discharge from abdominal wound on day 7? → Wound dehiscence\n"
            "Q: Secondary haemorrhage occurs at? → 7–10 days post-op\n"
            "Q: Pink frothy serous discharge from abdominal wound? → Wound dehiscence (impending burst abdomen)\n"
            "Q: Best prophylaxis for post-op DVT? → Low-molecular-weight heparin (LMWH) + compression stockings"
        ),
        "high_yield_takeaway": "5 W's: Wind (Day 1), Water (Day 3-5), Wound (Day 5), Walking/DVT (Day 5-7), Wonder drugs. Secondary haemorrhage at 7-10 days. Wound dehiscence: serous pink fluid at Day 7.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Anesthesiology", "#PYQ"],
    },
]
