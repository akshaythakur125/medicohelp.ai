"""High-yield Pathology content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ───────────────────────────────────────────────────────
    {
        "title": "Types of Necrosis — Key Distinctions",
        "subject": Subject.pathology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Coagulative = most common; Liquefactive = brain & abscess; Caseous = TB",
        "caption": (
            "Types of Necrosis — Rapid Revision\n\n"
            "1. COAGULATIVE NECROSIS\n"
            "• Most common type; caused by ischaemia (except brain)\n"
            "• Cell outline preserved (ghost cells); cytoplasm is eosinophilic\n"
            "• Example: Myocardial infarction, renal infarction, splenic infarction\n\n"
            "2. LIQUEFACTIVE NECROSIS\n"
            "• Brain infarction (neurons rich in lipid → liquefy)\n"
            "• Also: Bacterial abscesses (neutrophil enzymes liquefy tissue)\n"
            "• Cell outline LOST; fluid-filled cavity\n\n"
            "3. CASEOUS NECROSIS\n"
            "• Cheese-like, amorphous, granular debris\n"
            "• Pathognomonic of TB (also: deep fungal infections)\n"
            "• Ghost cells absent; central necrosis surrounded by granuloma\n\n"
            "4. FAT NECROSIS\n"
            "• Two types:\n"
            "  a) Enzymatic: Acute pancreatitis — lipase releases free fatty acids → saponification with Ca²⁺ → chalky-white deposits\n"
            "  b) Traumatic: Breast trauma → adipocytes rupture\n\n"
            "5. GANGRENOUS NECROSIS\n"
            "• Dry gangrene: Coagulative + ischaemia; limb mummification\n"
            "• Wet gangrene: Coagulative + liquefactive + bacterial superinfection; foul smell\n"
            "• Gas gangrene: Clostridium perfringens; crepitus; haemolytic toxins\n\n"
            "6. FIBRINOID NECROSIS\n"
            "• Seen in arterioles; immune-complex deposition + plasma protein leakage\n"
            "• Example: Malignant hypertension, vasculitis, SLE, PAN\n\n"
            "⚠️ Exam Trap: Brain ischaemia → Liquefactive (NOT coagulative); TB → Caseous."
        ),
        "high_yield_takeaway": "Coagulative = ischaemia (all organs except brain). Liquefactive = brain infarct + abscesses. Caseous = TB. Fibrinoid = malignant HTN + vasculitis.",
        "hashtags": ["#MedicoHelp", "#Pathology", "#MBBS", "#NEETPG", "#Necrosis"],
    },
    {
        "title": "Granuloma — TB vs Sarcoidosis",
        "subject": Subject.pathology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "TB granuloma = caseating + AFB; Sarcoidosis = non-caseating + asteroid bodies",
        "caption": (
            "Granuloma — TB vs Sarcoidosis — Rapid Revision\n\n"
            "DEFINITION: Organised aggregate of activated macrophages (epithelioid cells) ± "
            "Langhans giant cells, lymphocytes, and fibroblasts\n\n"
            "COMPARISON TABLE:\n"
            "Feature              TB Granuloma              Sarcoidosis Granuloma\n"
            "────────────────────────────────────────────────────────────────────\n"
            "Caseation            Present (caseous necrosis) Absent (non-caseating)\n"
            "Giant cells          Langhans type              Langhans + Foreign body\n"
            "Inclusions           Absent                     Asteroid bodies; Schaumann bodies\n"
            "AFB on ZN stain      Positive                   Negative\n"
            "Cause                M. tuberculosis            Unknown; Th1 hypersensitivity\n"
            "ACE levels           Normal                     Elevated (diagnostic marker)\n"
            "────────────────────────────────────────────────────────────────────\n\n"
            "OTHER GRANULOMATOUS CONDITIONS:\n"
            "• Caseating: TB, leprosy (tuberculoid), histoplasmosis, coccidioidomycosis\n"
            "• Non-caseating: Sarcoidosis, Crohn's disease, berylliosis, cat-scratch disease, "
            "  foreign body reactions, PAN (periarteritis nodosa)\n\n"
            "Langhans Giant Cell: Peripheral horseshoe/ring arrangement of nuclei\n"
            "Foreign Body Giant Cell: Randomly distributed nuclei\n\n"
            "⚠️ Exam Trap: Touton giant cells (foamy ring) → lipid granulomas (xanthoma, fat necrosis). "
            "Lepromatous leprosy has NO granuloma (anergy)."
        ),
        "high_yield_takeaway": "TB granuloma = caseating necrosis + AFB+ on ZN stain. Sarcoidosis = non-caseating + ↑ACE + asteroid/Schaumann bodies.",
        "hashtags": ["#MedicoHelp", "#Pathology", "#MBBS", "#NEETPG", "#Granuloma"],
    },
    # ── MCQ ───────────────────────────────────────────────────────────────────
    {
        "title": "Amyloidosis — MCQ",
        "subject": Subject.pathology,
        "content_format": ContentFormat.mcq,
        "poster_text": "Amyloid = Congo red stain → apple-green birefringence under polarised light",
        "caption": "MCQ: Amyloidosis type identification from clinical context",
        "question": (
            "A 60-year-old man with a 20-year history of rheumatoid arthritis presents with "
            "progressive proteinuria and renal impairment. Renal biopsy shows amorphous eosinophilic "
            "material in the glomerular mesangium and blood vessels. Congo red stain shows apple-green "
            "birefringence under polarised light. Immunostaining is positive for SAA protein. "
            "Which type of amyloidosis is this, and what is the amyloid fibril protein involved?"
        ),
        "options": [
            "A. AL amyloidosis; amyloid light chain (AL) protein",
            "B. AA amyloidosis; serum amyloid A (SAA) protein",
            "C. Aβ amyloidosis; amyloid beta (Aβ) protein",
            "D. ATTR amyloidosis; transthyretin (TTR) protein",
        ],
        "correct_answer": "B. AA amyloidosis; serum amyloid A (SAA) protein",
        "explanation": (
            "AA (secondary/reactive) amyloidosis occurs as a complication of chronic inflammatory "
            "disorders such as rheumatoid arthritis, TB, bronchiectasis, and osteomyelitis. The fibril "
            "protein is derived from serum amyloid A (SAA), an acute-phase reactant. Renal involvement "
            "(nephrotic syndrome) is the most common and serious manifestation. "
            "AL amyloidosis (primary) is associated with plasma cell dyscrasias (multiple myeloma); "
            "fibril protein = immunoglobulin light chains. "
            "Aβ amyloidosis occurs in Alzheimer's disease (brain plaques). "
            "ATTR amyloidosis involves transthyretin and causes cardiac and peripheral nerve disease in the elderly."
        ),
        "high_yield_takeaway": "AA amyloidosis = secondary to chronic inflammation (RA, TB); fibril = SAA protein; kidney most affected. AL = myeloma. Congo red → apple-green birefringence.",
        "hashtags": ["#MedicoHelp", "#Pathology", "#MBBS", "#NEETPG", "#Amyloidosis"],
    },
    {
        "title": "Tumour Markers — MCQ",
        "subject": Subject.pathology,
        "content_format": ContentFormat.mcq,
        "poster_text": "AFP = hepatocellular carcinoma + yolk sac tumour; PSA = prostate; CA-125 = ovary",
        "caption": "MCQ: Matching the correct tumour marker to clinical scenario",
        "question": (
            "A 55-year-old man with known cirrhosis due to hepatitis B infection presents with "
            "right upper quadrant pain and a 4 kg weight loss over 2 months. Ultrasound shows a "
            "4 cm heterogeneous mass in the right lobe of the liver. Which serum tumour marker is "
            "most specifically elevated in hepatocellular carcinoma and is used for screening in "
            "high-risk patients?"
        ),
        "options": [
            "A. CA 19-9",
            "B. Carcinoembryonic antigen (CEA)",
            "C. Alpha-fetoprotein (AFP)",
            "D. CA 125",
        ],
        "correct_answer": "C. Alpha-fetoprotein (AFP)",
        "explanation": (
            "Alpha-fetoprotein (AFP) is the most specific tumour marker for hepatocellular carcinoma (HCC). "
            "AFP >400 ng/mL is highly suggestive of HCC in a cirrhotic patient. It is also elevated in "
            "yolk sac tumours (endodermal sinus tumours) of the testes and ovaries, and in normal pregnancy. "
            "CA 19-9 is associated with pancreatic and biliary carcinoma. "
            "CEA is associated with colorectal carcinoma (also lung, breast, gastric — non-specific). "
            "CA 125 is associated with epithelial ovarian carcinoma. "
            "Surveillance with AFP + ultrasound every 6 months is recommended in cirrhotic patients at risk for HCC."
        ),
        "high_yield_takeaway": "AFP = HCC marker (also yolk sac tumour). PSA = prostate. CA 125 = ovarian. CA 19-9 = pancreatic. CEA = colorectal (non-specific). AFP >400 ng/mL → HCC in cirrhosis.",
        "hashtags": ["#MedicoHelp", "#Pathology", "#MBBS", "#NEETPG", "#TumourMarkers"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "Wound Healing — Phases & Key Mediators",
        "subject": Subject.pathology,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "Wound healing: Haemostasis → Inflammation → Proliferation → Remodelling",
        "caption": (
            "Wound Healing — Concise Notes\n\n"
            "Four Sequential Phases:\n\n"
            "1. HAEMOSTASIS (Immediate)\n"
            "• Platelet activation → fibrin clot; platelets release PDGF, TGF-β\n\n"
            "2. INFLAMMATION (Days 1–3)\n"
            "• Neutrophils (day 1–2): debridement, ROS, proteases\n"
            "• Macrophages (day 2–3): CRITICAL for healing; release IL-1, TNF-α, VEGF, FGF\n"
            "• Macrophage depletion → non-healing wound\n\n"
            "3. PROLIFERATION (Days 3 – 3 weeks)\n"
            "• Granulation tissue: fibroblasts + new capillaries\n"
            "• Type III collagen (early), fibronectin, hyaluronic acid deposited\n"
            "• VEGF → angiogenesis; myofibroblasts → wound contraction\n"
            "• Re-epithelialisation: keratinocyte migration (EGF-driven)\n\n"
            "4. REMODELLING (Weeks–months)\n"
            "• Type III collagen → Type I collagen (stronger)\n"
            "• Tensile strength: 10% at 1 week → 70-80% at 3 months (never 100%)\n"
            "• MMPs remodel ECM\n\n"
            "Primary vs Secondary Intention:\n"
            "• Primary: Clean edges approximated; minimal scarring\n"
            "• Secondary: Open wound; more granulation tissue and contraction\n\n"
            "Factors Impairing Healing:\n"
            "• Vitamin C deficiency (↓ collagen hydroxylation)\n"
            "• Zinc deficiency (↓ fibroblast proliferation)\n"
            "• Diabetes, corticosteroids, infection, poor blood supply"
        ),
        "high_yield_takeaway": "Macrophages are the most critical cell for wound healing. Type III collagen first, replaced by Type I. Tensile strength never exceeds 70-80% of unwounded skin.",
        "hashtags": ["#MedicoHelp", "#Pathology", "#MBBS", "#NEETPG", "#WoundHealing"],
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "Cell Injury & Death — PYQ Pattern",
        "subject": Subject.pathology,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Apoptosis vs Necrosis: The table NEET-PG asks every year",
        "caption": (
            "Cell Injury & Death — PYQ Concept\n\n"
            "NEET-PG repeatedly tests the distinction between apoptosis and necrosis.\n\n"
            "APOPTOSIS vs NECROSIS:\n"
            "────────────────────────────────────────────────────────────\n"
            "Feature           Apoptosis              Necrosis\n"
            "────────────────────────────────────────────────────────────\n"
            "Stimulus          Physiological/pathol.  Always pathological\n"
            "Mechanism         Programmed; ATP-dep.   Passive; no ATP needed\n"
            "Cell size         Shrinkage              Swelling\n"
            "Membrane          Intact                 Disrupted early\n"
            "Nuclear changes   Pyknosis → karyorrhexis Karyolysis\n"
            "Inflammation      NO                     YES (DAMPs released)\n"
            "DNA pattern       Ladder (internucleosomal) Random smear\n"
            "────────────────────────────────────────────────────────────\n\n"
            "Apoptosis Pathways:\n"
            "• Intrinsic: DNA damage → ↓ Bcl-2 → cytochrome c → Apaf-1 → caspase-9\n"
            "• Extrinsic: FasL/Fas (CD95) or TNF/TNFR → caspase-8 → caspase-3\n\n"
            "Reversible vs Irreversible Injury:\n"
            "• Reversible: ↓ ATP → Na/K ATPase fails → cellular swelling\n"
            "  Also: fatty change, membrane blebbing, ribosome detachment\n"
            "• Irreversible (point of no return): Mitochondrial permeability transition\n"
            "  + cell membrane disruption + nuclear chromatin clumping\n\n"
            "Free Radical Injury:\n"
            "• Sources: Reperfusion, radiation, drugs, inflammation\n"
            "• Damage: Lipid peroxidation, DNA breaks, protein cross-linking\n"
            "• Defences: SOD, catalase, glutathione peroxidase, vitamins C & E"
        ),
        "high_yield_takeaway": "Apoptosis = programmed, no inflammation, DNA ladder pattern. Necrosis = passive, inflammatory, random DNA smearing. Earliest reversible change = cellular swelling (↓ Na/K ATPase).",
        "hashtags": ["#MedicoHelp", "#Pathology", "#MBBS", "#NEETPG", "#PYQ"],
    },
    # ── Mnemonic ──────────────────────────────────────────────────────────────
    {
        "title": "MIST — Causes of Granulomas",
        "subject": Subject.pathology,
        "content_format": ContentFormat.mnemonic,
        "poster_text": "MIST = Mycobacteria, Immune/sarcoid, Schistosoma, Talc/foreign body",
        "caption": (
            "Mnemonic: MIST — Causes of Granulomas\n\n"
            "M — Mycobacteria\n"
            "   TB (Mycobacterium tuberculosis): CASEATING granulomas\n"
            "   Leprosy (M. leprae): non-caseating (lepromatous) or caseating (tuberculoid)\n"
            "   MAI (M. avium-intracellulare): non-caseating in immunocompromised\n\n"
            "I — Immune / Sarcoidosis\n"
            "   Sarcoidosis: NON-CASEATING granulomas (classic); bilateral hilar lymphadenopathy\n"
            "   Crohn's disease: non-caseating in bowel wall\n"
            "   Primary biliary cholangitis (PBC): granulomas in portal tracts\n\n"
            "S — Schistosoma / Parasites\n"
            "   Schistosomiasis: egg-induced granulomas in liver, bladder\n"
            "   Toxoplasma, Histoplasma, Coccidioides: fungal/parasitic granulomas\n\n"
            "T — Talc / Beryllium / Silica — Foreign body granulomas\n"
            "   Berylliosis: non-caseating; mimics sarcoidosis\n"
            "   Silicosis: 'eggshell' calcification of hilar nodes\n"
            "   Talc: IV drug users; polarisable crystals in giant cells\n\n"
            "Memory hook: Think of a MIST settling over inflamed tissue — obscuring the cause.\n\n"
            "Caseating vs Non-caseating:\n"
            "• Caseating: TB (most classic), also histoplasmosis, coccidioidomycosis\n"
            "• Non-caseating: Sarcoidosis, Crohn's, berylliosis, foreign body reactions\n\n"
            "⚠️ Exam Trap: All TB granulomas are caseating. Sarcoidosis granulomas are NEVER caseating."
        ),
        "high_yield_takeaway": "MIST = Mycobacteria (caseating), Immune/sarcoid (non-caseating), Schistosoma/parasites, Talc/beryllium. TB = caseating. Sarcoidosis = non-caseating.",
        "hashtags": ["#MedicoHelp", "#Pathology", "#MBBS", "#NEETPG", "#Mnemonic"],
    },
    # ── Flashcard ─────────────────────────────────────────────────────────────
    {
        "title": "Caseating vs Non-caseating Granuloma",
        "subject": Subject.pathology,
        "content_format": ContentFormat.flashcard,
        "poster_text": "Caseating = TB, fungi | Non-caseating = Sarcoidosis, Crohn's, berylliosis",
        "caption": (
            "Caseating vs Non-caseating Granuloma — Flashcard\n\n"
            "QUESTION: What diseases cause caseating granulomas?\n\n"
            "ANSWER: TB, Histoplasmosis, Coccidioidomycosis (and rarely Leprosy tuberculoid type)\n\n"
            "Caseating granulomas:\n"
            "• Gross: Cheese-like (caseous) necrosis in centre — hence 'caseating'\n"
            "• TB (Mycobacterium tuberculosis): most classic cause\n"
            "• Histoplasma capsulatum: endemic mycosis; Mississippi/Ohio river valley\n"
            "• Coccidioides immitis: Arizona/California; spherules seen\n"
            "• Central necrosis surrounded by epithelioid macrophages + Langhans giant cells\n\n"
            "Non-caseating granulomas:\n"
            "• Sarcoidosis (most common cause of non-caseating granulomas)\n"
            "• Crohn's disease (transmural, skip lesions)\n"
            "• Berylliosis (occupational; clinically mimics sarcoid)\n"
            "• Foreign body reaction (talc, sutures, silica)\n"
            "• Lepromatous leprosy (foamy macrophages — NOT true granulomas)\n\n"
            "⚠️ Exam Trap: Sarcoidosis NEVER caseates. If you see caseous necrosis in a lung granuloma, think TB first."
        ),
        "question": "What diseases cause caseating granulomas, and how do they differ from non-caseating granulomas?",
        "correct_answer": "Caseating: TB, Histoplasmosis, Coccidioidomycosis. Non-caseating: Sarcoidosis (most common), Crohn's disease, Berylliosis, foreign body reactions. Sarcoidosis NEVER caseates.",
        "high_yield_takeaway": "Caseating granuloma = TB (classic), fungi. Non-caseating = Sarcoidosis, Crohn's, berylliosis. Sarcoid never caseates — if caseous, think infection first.",
        "hashtags": ["#MedicoHelp", "#Pathology", "#MBBS", "#NEETPG", "#Flashcard"],
    },
    # ── True/False ────────────────────────────────────────────────────────────
    {
        "title": "Reed-Sternberg Cells — Which Lymphoma?",
        "subject": Subject.pathology,
        "content_format": ContentFormat.true_false,
        "poster_text": "Reed-Sternberg cells = Hodgkin Lymphoma (NOT Non-Hodgkin)",
        "caption": (
            "True or False: Reed-Sternberg cells are pathognomonic of Non-Hodgkin Lymphoma.\n\n"
            "ANSWER: FALSE\n\n"
            "Reed-Sternberg (RS) cells are pathognomonic of HODGKIN LYMPHOMA (HL), not Non-Hodgkin Lymphoma.\n\n"
            "Reed-Sternberg Cell:\n"
            "• Classic appearance: Binucleated or bilobed giant cell with prominent 'owl-eye' nucleoli\n"
            "• Origin: Germinal centre B-cell (despite unusual CD15+/CD30+ phenotype)\n"
            "• Immunophenotype: CD15+, CD30+, CD20−, CD45− (unusual for B-cells)\n\n"
            "Hodgkin Lymphoma subtypes (WHO):\n"
            "• Nodular Sclerosis (most common in young women): fibrous bands + lacunar RS cells\n"
            "• Mixed Cellularity: classic RS cells abundant; often EBV+\n"
            "• Lymphocyte Rich: best prognosis; few RS cells\n"
            "• Lymphocyte Depleted: worst prognosis; many RS cells; HIV-associated\n"
            "• Nodular Lymphocyte Predominant: 'Popcorn cells' (LP cells); CD20+\n\n"
            "Non-Hodgkin Lymphoma: No RS cells; monoclonal B or T cell proliferation\n\n"
            "⚠️ Exam Trap: EBV is associated with mixed cellularity HL and Burkitt lymphoma (t[8;14])."
        ),
        "question": "Reed-Sternberg cells are pathognomonic of Non-Hodgkin Lymphoma.",
        "correct_answer": "FALSE",
        "explanation": "Reed-Sternberg cells are pathognomonic of HODGKIN LYMPHOMA, not Non-Hodgkin Lymphoma. Classic RS cell = binucleated, owl-eye nucleoli, CD15+/CD30+ phenotype. Non-Hodgkin lymphomas do not contain RS cells.",
        "high_yield_takeaway": "Reed-Sternberg cells = Hodgkin Lymphoma (CD15+, CD30+). Classic owl-eye appearance. Not found in Non-Hodgkin Lymphoma. Most common HL subtype = Nodular Sclerosis.",
        "hashtags": ["#MedicoHelp", "#Pathology", "#MBBS", "#NEETPG", "#TrueFalse"],
    },
    # ── One-liner Recall ──────────────────────────────────────────────────────
    {
        "title": "Virchow's Triad — One-liner Recall",
        "subject": Subject.pathology,
        "content_format": ContentFormat.one_liner_recall,
        "poster_text": "Virchow's Triad = Hypercoagulability + Endothelial injury + Stasis",
        "caption": (
            "One-liner Recall: Virchow's Triad\n\n"
            "Fill in the blank:\n\n"
            "\"Virchow's triad = ___ + ___ + ___\"\n\n"
            "Answer: Hypercoagulability + Endothelial injury + Stasis (venous stasis)\n\n"
            "Full picture:\n"
            "• Describes the three factors predisposing to thrombus formation\n\n"
            "1. Hypercoagulability: Factor V Leiden, antiphospholipid syndrome, OCP use, malignancy, nephrotic syndrome\n"
            "2. Endothelial injury: Atherosclerosis, hypertension, trauma, infection, smoking\n"
            "3. Stasis: Prolonged immobility, AF (atrial fibrillation), varicose veins, post-op\n\n"
            "Clinical relevance:\n"
            "• DVT/PE: mainly stasis + hypercoagulability (Virchow described venous thrombosis)\n"
            "• Arterial thrombosis: mainly endothelial injury (plaque rupture)\n"
            "• Mural thrombus post-MI: stasis + endothelial injury\n\n"
            "⚠️ Exam Trap: Most common inherited cause of hypercoagulability = Factor V Leiden mutation."
        ),
        "question": "Virchow's triad = ___ + ___ + ___",
        "correct_answer": "Hypercoagulability + Endothelial injury + Stasis (venous stasis)",
        "high_yield_takeaway": "Virchow's triad = Hypercoagulability + Endothelial injury + Stasis. Most common inherited hypercoagulable state = Factor V Leiden. DVT/PE = mainly stasis + hypercoagulability.",
        "hashtags": ["#MedicoHelp", "#Pathology", "#MBBS", "#NEETPG", "#OneLiner"],
    },
]
