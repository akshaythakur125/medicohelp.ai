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
            "1. HAEMOSTASIS (Immediate — minutes)\n"
            "• Platelet activation and aggregation; fibrin clot formation\n"
            "• Platelets release: PDGF (recruits fibroblasts), TGF-β, serotonin\n\n"
            "2. INFLAMMATION (Days 1–3)\n"
            "• Neutrophils first (day 1–2): debridement, ROS, proteases\n"
            "• Macrophages replace neutrophils (day 2–3): essential for wound healing\n"
            "  – Release: IL-1, TNF-α, PDGF, VEGF, TGF-β, FGF\n"
            "• Macrophages are CRITICAL — macrophage depletion → non-healing wound\n\n"
            "3. PROLIFERATION (Days 3–3 weeks)\n"
            "• Granulation tissue formation: fibroblasts + new capillaries (angiogenesis)\n"
            "• Key components: Type III collagen (early), fibronectin, hyaluronic acid\n"
            "• VEGF: angiogenesis; FGF: angiogenesis + fibroblast proliferation\n"
            "• Myofibroblasts: wound contraction (contain smooth muscle actin)\n"
            "• Re-epithelialisation: keratinocyte migration from wound edges (EGF-driven)\n\n"
            "4. REMODELLING (Weeks to months)\n"
            "• Type III collagen replaced by Type I collagen (stronger)\n"
            "• Tensile strength: 10% at 1 week → 70-80% at 3 months (never reaches 100%)\n"
            "• Matrix metalloproteinases (MMPs) remodel ECM\n\n"
            "Healing by Primary vs Secondary Intention:\n"
            "• Primary (First intention): Clean surgical wound, edges approximated; minimal scarring\n"
            "• Secondary intention: Open wound; more granulation tissue, contraction, scarring\n\n"
            "Factors Impairing Wound Healing:\n"
            "• Vitamin C deficiency (↓ collagen hydroxylation)\n"
            "• Zinc deficiency (↓ fibroblast proliferation, ↓ collagen synthesis)\n"
            "• Diabetes (↓ neutrophil function, impaired angiogenesis)\n"
            "• Corticosteroids (↓ inflammation and collagen synthesis)\n"
            "• Infection, foreign body, poor blood supply"
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
            "NEET-PG repeatedly asks candidates to distinguish apoptosis from necrosis.\n\n"
            "APOPTOSIS vs NECROSIS — Key Comparison Table:\n"
            "────────────────────────────────────────────────────────────────────\n"
            "Feature              Apoptosis                 Necrosis\n"
            "────────────────────────────────────────────────────────────────────\n"
            "Stimulus             Physiological or pathological  Always pathological\n"
            "Mechanism            Programmed; energy-dependent   Passive; energy-independent\n"
            "Cell size            Shrinkage                      Swelling\n"
            "Membrane integrity   Intact (until phagocytosed)    Disrupted early\n"
            "Nuclear changes      Pyknosis → karyorrhexis        Karyolysis\n"
            "Inflammation         NO (no leakage of contents)    YES (DAMPs released)\n"
            "DNA fragmentation    Internucleosomal (ladder)       Random smearing\n"
            "Phagocytosis         By adjacent cells/macrophages  Inflammatory infiltrate\n"
            "Apoptotic bodies     Present                        Absent\n"
            "────────────────────────────────────────────────────────────────────\n\n"
            "Apoptosis Pathways:\n"
            "• Intrinsic (Mitochondrial): DNA damage, ischaemia → ↓ Bcl-2 → cytochrome c release\n"
            "  → Apaf-1 → caspase-9 → effector caspases (3,6,7)\n"
            "• Extrinsic (Death receptor): FasL binds Fas (CD95), TNF binds TNFR → caspase-8\n\n"
            "Reversible vs Irreversible Cell Injury:\n"
            "• Reversible: ↓ ATP → Na/K ATPase fails → cellular swelling (most important early change)\n"
            "  – Fatty change (steatosis), plasma membrane blebbing, ER swelling, ribosome detachment\n"
            "• Point of No Return (Irreversible): Mitochondrial permeability transition (MPT)\n"
            "  + Cell membrane disruption + nuclear chromatin clumping\n\n"
            "Free Radical Injury:\n"
            "• Sources: Reperfusion injury, radiation, drugs, inflammation\n"
            "• Damage: Lipid peroxidation (membranes), DNA strand breaks, protein cross-linking\n"
            "• Defences: SOD, catalase, glutathione peroxidase, vitamins C & E"
        ),
        "high_yield_takeaway": "Apoptosis = programmed, no inflammation, DNA ladder pattern. Necrosis = passive, inflammatory, random DNA smearing. Earliest reversible change = cellular swelling (↓ Na/K ATPase).",
        "hashtags": ["#MedicoHelp", "#Pathology", "#MBBS", "#NEETPG", "#PYQ"],
    },
]
