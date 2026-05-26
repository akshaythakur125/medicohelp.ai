from app.models import ContentFormat, Subject

TOPICS = [
    # ── 1. Rapid Revision ───────────────────────────────────────────────────
    {
        "title": "Rigor Mortis & Postmortem Changes Timeline",
        "subject": Subject.forensic_medicine,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Dead but on schedule — every postmortem change has a clock 🕐",
        "caption": (
            "POSTMORTEM CHANGES — SEQUENCE & TIMING\n\n"
            "IMMEDIATE CHANGES (within minutes):\n"
            "• Cessation of circulation & respiration\n"
            "• Loss of consciousness & corneal reflex\n"
            "• Somatic death → cellular death (neurons: 3–5 min)\n\n"
            "EARLY CHANGES (hours):\n"
            "• Algor Mortis: body cools ~1°C/hr (first 6 hrs); affected by environment, obesity, clothing\n"
            "• Livor Mortis (Hypostasis): begins 1–2 hrs, fixed by 6–12 hrs; appears blue-red on dependent parts\n"
            "• Rigor Mortis: ATP depletion → actin-myosin lock\n"
            "  — Onset: 1–2 hrs (face/jaw first — Nysten's law)\n"
            "  — Complete: 12 hrs\n"
            "  — Passes off: 24–48 hrs (secondary flaccidity)\n\n"
            "LATE CHANGES:\n"
            "• Decomposition begins ~24–48 hrs in hot/humid climate\n"
            "  — Greenish discoloration first in RIF (cecum → most bacteria)\n"
            "  — Bloating, skin slippage, putrefaction odour\n"
            "• Adipocere: saponification of fat; takes 3 weeks–months; alkaline, moist conditions\n"
            "• Mummification: desiccation; dry, hot conditions; months\n\n"
            "KEY EXAM POINTS:\n"
            "• Cadaveric spasm (instantaneous rigor) — extreme emotion/exhaustion at death; no relaxation phase\n"
            "• Heat stiffening ≠ rigor — caused by muscle protein coagulation; irreversible\n"
            "• Rigor mortis absent in: newborns, extreme wasting (marasmus), sudden violent death\n"
            "• Highest internal temperature at death (putrefaction heat) can be 38–40°C"
        ),
        "high_yield_takeaway": (
            "Rigor starts face → trunk → limbs (Nysten's law); complete at 12 hrs, passes off 24–48 hrs. "
            "Greenish discoloration in RIF = first sign of decomposition."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ForensicMedicine", "#PostmortemChanges"],
    },

    # ── 2. Rapid Revision ───────────────────────────────────────────────────
    {
        "title": "Types of Asphyxia",
        "subject": Subject.forensic_medicine,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Asphyxia kills in minutes — know every type cold.",
        "caption": (
            "ASPHYXIA — CLASSIFICATION & HIGH-YIELD FACTS\n\n"
            "DEFINITION: Deficient O₂ + excess CO₂ in blood due to impaired respiration.\n\n"
            "TYPES:\n\n"
            "1. HANGING\n"
            "• Typical: knot at back of neck; suicidal\n"
            "• Atypical: knot elsewhere; may be homicidal\n"
            "• Judicial hanging: C2–C3 fracture-dislocation (Hangman's fracture)\n"
            "• Vagal inhibition can cause sudden death even before asphyxia\n\n"
            "2. STRANGULATION\n"
            "• Ligature strangulation: horizontal mark, homicidal\n"
            "• Manual strangulation (throttling): fingernail abrasions, always homicidal\n"
            "• Mugging (forearm compression): homicidal\n\n"
            "3. SMOTHERING — obstruction of nose/mouth; homicidal; no external marks\n\n"
            "4. GAGGING — material in mouth/pharynx\n\n"
            "5. CHOKING — obstruction within larynx/trachea (café coronary = food bolus)\n\n"
            "6. TRAUMATIC ASPHYXIA — compression of chest (crowd crush); Masque ecchymotique\n\n"
            "7. DROWNING\n"
            "• Wet: lung filled with water; froth from nostrils (salmon-pink)\n"
            "• Dry: laryngeal spasm; no water in lungs (~10–15%)\n"
            "• Fresh water: hypotonic → haemolysis → hyponatraemia\n"
            "• Salt water: hypertonic → pulmonary oedema → hypernatraemia\n"
            "• Diatoms: found in bone marrow = confirmatory test for drowning\n\n"
            "GENERAL SIGNS OF ASPHYXIA:\n"
            "• Petechiae (Tardieu spots) — subconjunctival, pleural, epicardial\n"
            "• Cyanosis, congestion, fluidity of blood\n"
            "• Right heart dilation\n"
            "• Subendocardial haemorrhage"
        ),
        "high_yield_takeaway": (
            "Manual strangulation is ALWAYS homicidal. Diatoms in bone marrow = confirmatory drowning test. "
            "Tardieu spots = petechiae in subconjunctiva, pleura, epicardium."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ForensicMedicine", "#Asphyxia"],
    },

    # ── 3. MCQ ──────────────────────────────────────────────────────────────
    {
        "title": "Postmortem Lividity — MCQ",
        "subject": Subject.forensic_medicine,
        "content_format": ContentFormat.mcq,
        "poster_text": "Can you tell time of death from the colour of the skin?",
        "caption": (
            "CLINICAL VIGNETTE — POSTMORTEM LIVIDITY\n\n"
            "A body is discovered at 10 AM. The police note blue-red discolouration on the back and "
            "posterior thighs. When pressed, the discolouration completely disappears and reappears on "
            "release. The examining forensic officer estimates the time of death.\n\n"
            "QUICK THEORY:\n"
            "Livor mortis (hypostasis) develops due to gravitational settling of blood in dependent vessels "
            "after circulation stops. It begins within 1–2 hours and is initially non-fixed (blanches on "
            "pressure). Fixation (no blanching) occurs at 6–12 hours.\n\n"
            "Key colour variations:\n"
            "• Cherry red — CO poisoning or cold environments\n"
            "• Chocolate brown — methaemoglobinaemia (CN, NO₂ poisoning)\n"
            "• Bright pink in cold — refrigeration artefact\n\n"
            "Paradoxical lividity: if the body is moved after fixation, lividity remains at original site "
            "and new lividity forms at new dependent areas — indicates body was moved post-fixation (>12 hrs)."
        ),
        "question": (
            "A 45-year-old man is found dead at home at 10 AM. Postmortem examination reveals cherry-red "
            "discolouration of the lividity on the dependent parts of the body. Toxicology is pending. "
            "Which of the following is the MOST likely cause of death?"
        ),
        "options": [
            "A. Drowning",
            "B. Carbon monoxide poisoning",
            "C. Cyanide poisoning",
            "D. Methaemoglobinaemia",
        ],
        "correct_answer": "B. Carbon monoxide poisoning",
        "explanation": (
            "Cherry-red lividity is the hallmark of carbon monoxide (CO) poisoning, caused by formation of "
            "carboxyhaemoglobin, which imparts a bright red colour to blood and tissues. "
            "Cyanide poisoning may also produce cherry-red discolouration (due to histotoxic hypoxia and "
            "oxyhemoglobin accumulation in venous blood), but CO poisoning is the classic and most frequently "
            "tested answer. Methaemoglobinaemia produces chocolate-brown lividity. "
            "Drowning produces salmon-pink frothy fluid from the airways but does not cause cherry-red lividity."
        ),
        "high_yield_takeaway": (
            "Cherry-red lividity = CO poisoning (classic). Also remember: chocolate-brown = metHb; "
            "fixed lividity at 6–12 hrs; paradoxical lividity means body was moved."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ForensicMedicine", "#PostmortemLividity"],
    },

    # ── 4. MCQ ──────────────────────────────────────────────────────────────
    {
        "title": "Wounds Classification — MCQ",
        "subject": Subject.forensic_medicine,
        "content_format": ContentFormat.mcq,
        "poster_text": "One wound, four possibilities — pick the right one in the exam!",
        "caption": (
            "WOUNDS IN FORENSIC MEDICINE — QUICK CLASSIFICATION\n\n"
            "Mechanical injuries are classified by causative weapon:\n\n"
            "• Abrasion: tangential scrape; epidermis only; shows direction of force; heals without scar\n"
            "• Contusion (Bruise): blunt force; extravasation of blood into tissues; no break in skin\n"
            "• Laceration: tearing of skin/tissues by blunt force; irregular margins, bridging strands\n"
            "• Incised wound: sharp-edged weapon; clean cut edges, longer than deep, no bridging\n"
            "• Stab wound: sharp pointed weapon; depth > length; most dangerous due to deep organ injury\n"
            "• Chop wound: heavy sharp-edged weapon (e.g., axe); bone involvement common\n"
            "• Firearm wounds: entry has inverted edges + abrasion collar; exit has everted, irregular edges\n\n"
            "Bridging tissue strands in the wound = laceration (blunt force), NOT incised.\n"
            "A wound more deep than wide = stab wound — always check depth vs length."
        ),
        "question": (
            "A 30-year-old assault victim is brought to the emergency department. Examination of the wound "
            "on the forearm reveals irregular margins, tissue bridging at the base, and surrounding contusion. "
            "The depth of the wound is less than its length. Which type of wound is this?"
        ),
        "options": [
            "A. Incised wound",
            "B. Stab wound",
            "C. Laceration",
            "D. Chop wound",
        ],
        "correct_answer": "C. Laceration",
        "explanation": (
            "The wound described — irregular margins, tissue bridging (nerves/vessels crossing the wound base), "
            "surrounding contusion, and length greater than depth — is characteristic of a laceration caused "
            "by blunt force. Tissue bridging is the key distinguishing feature from incised wounds, which have "
            "clean, regular margins, no bridging, and no surrounding bruising. "
            "Stab wounds are deeper than wide. Chop wounds involve heavy cutting weapons and frequently "
            "damage underlying bone."
        ),
        "high_yield_takeaway": (
            "Tissue bridging + irregular margins + surrounding bruise = Laceration (blunt force). "
            "Incised wound: clean edges, longer than deep. Stab: deeper than wide."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ForensicMedicine", "#WoundsClassification"],
    },

    # ── 5. Concise Notes ────────────────────────────────────────────────────
    {
        "title": "Estimation of Time of Death",
        "subject": Subject.forensic_medicine,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "The clock starts at death — forensic medicine reads it.",
        "caption": (
            "ESTIMATION OF TIME OF DEATH (TOD)\n\n"
            "SECTION 1 — PHYSICAL METHODS\n"
            "• Algor Mortis: body loses ~1°C/hr (first 6 hrs under standard conditions)\n"
            "  Formula (Henssge nomogram): TOD = 98.6°F − rectal temp / 1.5\n"
            "  Modifiers: obesity (slow), thin build/wind (fast), clothing, immersion\n"
            "• Rigor Mortis:\n"
            "  — 0–2 hrs: absent\n"
            "  — 2–12 hrs: developing (partial)\n"
            "  — 12 hrs: complete\n"
            "  — 24–48 hrs: disappearing (secondary relaxation)\n"
            "• Livor Mortis:\n"
            "  — 1–2 hrs: appears\n"
            "  — 6–12 hrs: fixed (no blanching on pressure)\n\n"
            "SECTION 2 — CHEMICAL METHODS\n"
            "• Vitreous potassium: rises 0.17 mmol/L/hr after death → useful when >24 hrs\n"
            "• CSF and blood pH: decline with time\n"
            "• Synovial fluid hypoxanthine level: proportional to time since death\n\n"
            "SECTION 3 — BIOLOGICAL METHODS\n"
            "• Stomach contents: if undigested = death within 1–2 hrs of last meal\n"
            "• Blowfly (Calliphora): first insects arrive within hours; larval stages help estimate days\n"
            "  Calliphora vicina = most important medicolegal blowfly in India\n"
            "• Plant growth through remains\n\n"
            "SECTION 4 — DECOMPOSITION STAGES\n"
            "• 24–48 hrs: greenish discolouration (RIF)\n"
            "• 3–5 days: bloating, skin slippage\n"
            "• 1–2 weeks: skeletonisation begins in tropical climates\n\n"
            "EXAM TIP: Vitreous humour is the most RELIABLE fluid for biochemical TOD estimation "
            "because it is protected from contamination and bacteria."
        ),
        "high_yield_takeaway": (
            "Vitreous potassium = most reliable biochemical TOD marker. "
            "Rigor complete at 12 hrs; fixed lividity at 6–12 hrs. Stomach contents help for first 2 hrs post-meal."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ForensicMedicine", "#TimeOfDeath"],
    },

    # ── 6. PYQ Concept ──────────────────────────────────────────────────────
    {
        "title": "Medico-Legal Autopsy — PYQ Pattern",
        "subject": Subject.forensic_medicine,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Autopsy PYQs repeat — master this table once, score forever.",
        "caption": (
            "MEDICO-LEGAL AUTOPSY — HIGH-YIELD PYQ PATTERN TABLE\n\n"
            "TYPES OF AUTOPSY:\n"
            "┌──────────────────────┬──────────────────────────────────────┐\n"
            "│ Type                 │ Purpose / Authority                  │\n"
            "├──────────────────────┼──────────────────────────────────────┤\n"
            "│ Medico-legal autopsy │ Court order / Magistrate; Cr.PC 174  │\n"
            "│ Clinical autopsy     │ Hospital; with family consent        │\n"
            "│ Anatomical autopsy   │ Teaching; unclaimed bodies           │\n"
            "└──────────────────────┴──────────────────────────────────────┘\n\n"
            "SECTION 175 CrPC: Police can summon a Registered Medical Practitioner to examine a dead body.\n"
            "SECTION 174 CrPC: Police investigation of suspicious deaths (suicide, homicide, sudden unnatural).\n\n"
            "INQUEST TYPES:\n"
            "• Police inquest (S.174): most common in India; no power to fix culpability\n"
            "• Magistrate inquest (S.176): mandatory in deaths in custody, dowry deaths, rape victims\n"
            "• Coroner's inquest: only in Mumbai; coroner has judicial powers\n\n"
            "WHO PERFORMS MEDICO-LEGAL AUTOPSY:\n"
            "• Government Medical Officer (not private practitioner) — unless exceptional circumstances\n"
            "• With police requisition; body identified by police\n\n"
            "EXHUMATION:\n"
            "• Order by Executive Magistrate or High Court\n"
            "• Performed in presence of Magistrate\n"
            "• Application: re-examination when foul play suspected after burial\n\n"
            "FREQUENTLY TESTED POINTS:\n"
            "• Autopsy report is NOT a dying declaration\n"
            "• Brain is examined LAST during autopsy (after chest & abdomen)\n"
            "• Ideal time: daylight hours (natural light preferred)\n"
            "• McCallum's probe — used to trace firearm wound tract\n"
            "• Virtopsy = virtual (CT/MRI-based) autopsy — non-invasive"
        ),
        "high_yield_takeaway": (
            "Magistrate inquest (S.176) is MANDATORY for custody deaths and dowry deaths. "
            "Coroner's inquest only in Mumbai. Brain examined last during autopsy. Exhumation needs Magistrate order."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ForensicMedicine", "#Autopsy"],
    },

    # ── 7. Mnemonic ─────────────────────────────────────────────────────
    {
        "title": "Mnemonic: Poisoning Antidotes — The 'A' List",
        "subject": Subject.forensic_medicine,
        "content_format": ContentFormat.mnemonic,
        "poster_text": "Mnemonic: 'A-List' — Atropine for organophosphates, Activated charcoal for most poisons, Acetylcysteine for paracetamol",
        "caption": (
            "Antidote mnemonics: Organophosphate = Atropine + Pralidoxime (2-PAM). Paracetamol = N-acetylcysteine (NAC). Opioids = Naloxone. Benzodiazepines = Flumazenil. Cyanide = Amyl nitrite + Sodium nitrite + Sodium thiosulfate (Lilly's cocktail). Methanol/Ethylene glycol = Fomepizole (first-line) or Ethanol. Carbon monoxide = 100% O₂ or hyperbaric O₂. Iron = Desferrioxamine. Arsenic/Mercury = BAL (Dimercaprol). Lead = EDTA + BAL. Copper = D-penicillamine. Digitalis = Digoxin-specific Fab antibodies."
        ),
        "high_yield_takeaway": "OP poisoning: Atropine (muscarinic) + Pralidoxime (nicotinic). Paracetamol: NAC within 8-10 hours. Cyanide: Lilly's cocktail. Methanol: Fomepizole > Ethanol.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ForensicMedicine", "#Mnemonic", "#Antidotes"],
    },

    # ── 8. Flashcard ────────────────────────────────────────────────────
    {
        "title": "Flashcard: Burns — Wallace Rule of Nine and Management",
        "subject": Subject.forensic_medicine,
        "content_format": ContentFormat.flashcard,
        "poster_text": "Wallace Rule of Nine: Each arm 9%, each leg 18%, front trunk 18%, back trunk 18%, head 9%",
        "caption": (
            "Burns assessment and management. Rule of Nine for adults (head 9%, each arm 9%, front trunk 18%, back trunk 18%, each leg 18%, perineum 1%). Palmer method (patient's palm = 1%). Degree classification: 1st (epidermis, erythema); 2nd (dermis, blisters); 3rd (full thickness, charred, painless). Fluid resuscitation: Parkland formula (4 mL × BSA% × weight in kg, half in first 8 hrs, half in next 16 hrs)."
        ),
        "question": "A 70-kg man has burns on front trunk, both legs, and perineum. What BSA% is burned and what is the Parkland fluid requirement for the first 8 hours?",
        "correct_answer": "BSA = 18% (front trunk) + 36% (both legs) + 1% (perineum) = 55%. Parkland: 4 × 55 × 70 = 15,400 mL in 24 hrs. Half (7,700 mL) in first 8 hrs. Fluid: Ringer's Lactate.",
        "high_yield_takeaway": "Wallace Rule of 9: head 9, each arm 9, front 18, back 18, each leg 18, perineum 1. Parkland: 4 mL/kg/% burn RL. Half in 8 hrs.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ForensicMedicine", "#Flashcard", "#Burns"],
    },

    # ── 9. True/False ───────────────────────────────────────────────────
    {
        "title": "True or False: Diatoms in bone marrow is diagnostic of drowning",
        "subject": Subject.forensic_medicine,
        "content_format": ContentFormat.true_false,
        "poster_text": "Diatoms in bone marrow = confirmatory for ante-mortem drowning — but false positives exist",
        "caption": (
            "Diatom test principle: microscopic algae from water enter circulation during drowning and reach bone marrow. True positive = diatoms in bone marrow/closed organs. False positives: diatoms in lung only (not bone marrow) can occur from post-mortem immersion. False negatives: dry drowning (laryngeal spasm), no diatoms in water source. The test is confirmatory but must be interpreted with caution."
        ),
        "question": "The presence of diatoms in bone marrow is definitive proof of ante-mortem drowning.",
        "correct_answer": "FALSE",
        "explanation": "Diatoms in bone marrow is a STRONG indicator of ante-mortem drowning but not definitive. False positives can occur from contamination during autopsy or from inhalation of diatom-containing aerosolized water. Diatoms in lungs alone without bone marrow = inconclusive (could be post-mortem immersion).",
        "high_yield_takeaway": "Diatoms in bone marrow = strong evidence for drowning, but not 100% definitive. Absent diatoms do not rule out drowning (dry drowning 10-15%).",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ForensicMedicine", "#TrueFalse", "#Diatoms"],
    },

    # ── 10. One-liner Recall ────────────────────────────────────────────
    {
        "title": "One-liner Recall: Insect Succession on Decomposing Body",
        "subject": Subject.forensic_medicine,
        "content_format": ContentFormat.one_liner_recall,
        "poster_text": "Forensic entomology: blowflies arrive first (within hours) — their larval stage helps estimate PMI",
        "caption": (
            "Fill in the blank: \"The first insects to arrive on a decomposing body within hours of death are ___ flies, specifically the genus ___.\" Answer: \"Blowflies (Calliphora vicina in India).\" Then explain: Calliphora arrives first (within hours), followed by flesh flies (Sarcophaga), beetles (Dermestes), and finally cheese flies (Piophila). Larval stage (1st, 2nd, 3rd instar) and pupal stage help estimate post-mortem interval (PMI)."
        ),
        "question": "The first insects to arrive on a decomposing body within hours of death are ___ flies, specifically the genus ___.",
        "correct_answer": "Blowflies, Calliphora vicina",
        "high_yield_takeaway": "Blowflies (Calliphora) = first arrivals. Larval stage helps estimate PMI. Accumulated Degree Hours (ADH) used for precise estimation.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ForensicMedicine", "#OneLiner", "#Entomology"],
    },
]
