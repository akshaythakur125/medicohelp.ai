"""High-yield Microbiology content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ───────────────────────────────────────────────────────
    {
        "title": "Gram Staining & Bacterial Classification",
        "subject": Subject.microbiology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Gram +ve = purple (thick peptidoglycan); Gram -ve = pink (thin wall + outer membrane)",
        "caption": (
            "Gram Staining & Bacterial Classification — Rapid Revision\n\n"
            "GRAM STAINING STEPS:\n"
            "1. Crystal violet (primary stain) — both +ve and -ve stain purple\n"
            "2. Gram's iodine (mordant) — fixes crystal violet-iodine complex\n"
            "3. Acetone/alcohol (decoloriser) — washes out from thin-walled Gram -ve cells\n"
            "4. Safranin (counterstain) — stains decolourised Gram -ve cells pink\n\n"
            "GRAM-POSITIVE (Purple — thick peptidoglycan, no outer membrane):\n"
            "Cocci:\n"
            "• Staphylococcus — clusters; S. aureus (coagulase +ve), S. epidermidis, S. saprophyticus\n"
            "• Streptococcus — chains; S. pyogenes (β-haemolytic), S. pneumoniae (α-haemolytic, lancet-shaped diplococci)\n"
            "• Enterococcus — pairs/chains; intrinsic vancomycin resistance in E. faecium\n"
            "Bacilli:\n"
            "• Spore-forming: Bacillus anthracis, Clostridium spp.\n"
            "• Non-spore: Listeria, Corynebacterium, Lactobacillus\n\n"
            "GRAM-NEGATIVE (Pink — thin peptidoglycan + outer membrane with LPS):\n"
            "Cocci:\n"
            "• Neisseria meningitidis, N. gonorrhoeae — diplococci (kidney-bean shaped)\n"
            "Bacilli:\n"
            "• Enterobacteriaceae: E. coli, Klebsiella, Salmonella, Shigella, Proteus\n"
            "• Non-enteric: Pseudomonas, H. influenzae, Brucella, Legionella\n\n"
            "NEITHER (Atypicals — no cell wall / cannot be Gram stained):\n"
            "• Mycoplasma — no cell wall; smallest bacterium; cholesterol in membrane\n"
            "• Mycobacteria — acid-fast (rich in mycolic acids); ZN stain used\n"
            "• Treponema — too thin for light microscopy; darkfield used\n"
            "• Rickettsia, Chlamydia — obligate intracellular\n\n"
            "⚠️ Exam Trap: S. pneumoniae is Gram +ve but bile-soluble and optochin-sensitive. "
            "Legionella is Gram -ve but stains poorly — use silver stain (Dieterle)."
        ),
        "high_yield_takeaway": "Gram +ve = purple, thick peptidoglycan. Gram -ve = pink, outer membrane with LPS. Mycoplasma = no cell wall (Gram stain useless). Mycobacteria = acid-fast.",
        "hashtags": ["#MedicoHelp", "#Microbiology", "#MBBS", "#NEETPG", "#GramStain"],
    },
    {
        "title": "Hepatitis B Serology Interpretation",
        "subject": Subject.microbiology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "HBsAg = current infection; Anti-HBs = immunity; Anti-HBc IgM = acute HBV",
        "caption": (
            "Hepatitis B Serology Interpretation — Rapid Revision\n\n"
            "KEY MARKERS & MEANING:\n"
            "• HBsAg (surface antigen): Marker of INFECTION (acute or chronic); first to appear\n"
            "• Anti-HBs (surface antibody): IMMUNITY — either vaccine-induced or post-recovery; protective\n"
            "• HBeAg (e antigen): Marker of HIGH REPLICATION and HIGH INFECTIVITY\n"
            "• Anti-HBe: Seroconversion from HBeAg → lower replication; still possible to have HBV DNA\n"
            "• Anti-HBc IgM: ACUTE infection marker; appears during window period\n"
            "• Anti-HBc IgG: Past infection or chronic carrier; persists for life\n"
            "• HBV DNA: Best marker of active replication; guides treatment\n\n"
            "SEROLOGICAL PATTERNS:\n"
            "──────────────────────────────────────────────────────────\n"
            "Pattern              HBsAg  Anti-HBs  Anti-HBc  HBeAg\n"
            "──────────────────────────────────────────────────────────\n"
            "Acute HBV            +      -         IgM+      +\n"
            "Window period        -      -         IgM+      -\n"
            "Chronic (active)     +      -         IgG+      +\n"
            "Chronic (inactive)   +      -         IgG+      -\n"
            "Resolved HBV         -      +         IgG+      -\n"
            "Vaccinated           -      +         -         -\n"
            "──────────────────────────────────────────────────────────\n\n"
            "WINDOW PERIOD: HBsAg gone, Anti-HBs not yet appeared; only Anti-HBc IgM positive\n\n"
            "CHRONIC HBV: HBsAg positive for >6 months\n\n"
            "TREATMENT: Tenofovir (TDF) or Entecavir (first-line)\n"
            "Peg-interferon-α: immune-active disease (finite duration)\n\n"
            "⚠️ Exam Trap: Vaccinated = ONLY Anti-HBs positive (no Anti-HBc — vaccine is HBsAg only)."
        ),
        "high_yield_takeaway": "Window period = only anti-HBc IgM positive. Vaccinated = only anti-HBs positive. Chronic HBV = HBsAg positive >6 months. HBeAg = high infectivity.",
        "hashtags": ["#MedicoHelp", "#Microbiology", "#MBBS", "#NEETPG", "#HepatitisB"],
    },
    # ── MCQ ───────────────────────────────────────────────────────────────────
    {
        "title": "TORCH Infections — MCQ",
        "subject": Subject.microbiology,
        "content_format": ContentFormat.mcq,
        "poster_text": "TORCH: Toxoplasma, Others, Rubella, CMV, Herpes — congenital infection triad",
        "caption": "MCQ: Identifying the TORCH infection from congenital presentation",
        "question": (
            "A neonate is born to a mother who had a febrile illness with a diffuse maculopapular rash "
            "descending from the face downward during the first trimester. The neonate is found to have "
            "sensorineural hearing loss, cataracts, and a patent ductus arteriosus on echocardiography. "
            "Which congenital infection is MOST LIKELY responsible for this clinical triad?"
        ),
        "options": [
            "A. Congenital Cytomegalovirus (CMV)",
            "B. Congenital Toxoplasmosis",
            "C. Congenital Rubella Syndrome",
            "D. Congenital Herpes Simplex Virus (HSV)",
        ],
        "correct_answer": "C. Congenital Rubella Syndrome",
        "explanation": (
            "The classic triad of Congenital Rubella Syndrome (CRS) is: sensorineural deafness (most common), "
            "cataracts/glaucoma (eye defects), and congenital heart defects (PDA, pulmonary artery stenosis). "
            "The descending maculopapular rash in the mother following a febrile illness is characteristic of Rubella. "
            "Risk is highest with first-trimester maternal infection (>80% transmission). "
            "Congenital CMV presents with periventricular calcifications, hepatosplenomegaly, petechiae, and "
            "sensorineural deafness — but without cataracts or PDA. "
            "Congenital Toxoplasmosis: chorioretinitis, intracranial calcifications (diffuse, scattered), hydrocephalus. "
            "Congenital HSV: vesicular skin lesions, encephalitis, disseminated disease — no cardiac defects."
        ),
        "high_yield_takeaway": "Congenital Rubella = deafness + cataracts + PDA (classic triad). CMV = periventricular calcifications. Toxoplasma = chorioretinitis + diffuse calcifications + hydrocephalus.",
        "hashtags": ["#MedicoHelp", "#Microbiology", "#MBBS", "#NEETPG", "#TORCH"],
    },
    {
        "title": "HIV Pathogenesis & CD4 Count — MCQ",
        "subject": Subject.microbiology,
        "content_format": ContentFormat.mcq,
        "poster_text": "CD4 <200 = AIDS defining; OIs depend on CD4 count thresholds",
        "caption": "MCQ: HIV-related opportunistic infection matched to CD4 count",
        "question": (
            "A 35-year-old man known to be HIV-positive and not on antiretroviral therapy presents "
            "with 3 weeks of progressive headache, fever, and neck stiffness. CSF examination shows "
            "↑ opening pressure, lymphocytic pleocytosis, low glucose, and India ink preparation reveals "
            "encapsulated yeast forms with a large polysaccharide capsule. His CD4 count is 60 cells/μL. "
            "Which is the MOST LIKELY diagnosis?"
        ),
        "options": [
            "A. Toxoplasma gondii encephalitis",
            "B. Cryptococcal meningitis",
            "C. Tuberculous meningitis",
            "D. Progressive multifocal leukoencephalopathy (PML)",
        ],
        "correct_answer": "B. Cryptococcal meningitis",
        "explanation": (
            "The India ink preparation showing encapsulated yeast with a large polysaccharide capsule is "
            "pathognomonic of Cryptococcus neoformans. Cryptococcal meningitis occurs at CD4 <100 cells/μL "
            "and presents as subacute meningitis with high intracranial pressure. "
            "Diagnosis confirmed by India ink, cryptococcal antigen (CrAg) in CSF/serum (most sensitive). "
            "Treatment: Amphotericin B + Flucytosine (induction 2 weeks) → Fluconazole (consolidation/maintenance). "
            "Toxoplasma encephalitis occurs at CD4 <100 but shows ring-enhancing lesions on CT/MRI with multiple foci. "
            "PML (JC virus) occurs at CD4 <200 with white matter demyelination, no meningeal signs. "
            "TB meningitis is not CD4-restricted but AFB smear/culture positive with basilar exudate on imaging."
        ),
        "high_yield_takeaway": "India ink = Cryptococcus neoformans. Occurs at CD4 <100. Treat with Amphotericin B + Flucytosine → Fluconazole. CD4 <200 = AIDS; <100 = Cryptococcus/Toxoplasma risk.",
        "hashtags": ["#MedicoHelp", "#Microbiology", "#MBBS", "#NEETPG", "#HIV"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "Antimicrobial Resistance Mechanisms",
        "subject": Subject.microbiology,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "Resistance: enzymatic inactivation, efflux pumps, target modification, porin loss",
        "caption": (
            "Antimicrobial Resistance Mechanisms — Concise Notes\n\n"
            "FOUR MAJOR MECHANISMS:\n\n"
            "1. ENZYMATIC INACTIVATION\n"
            "• Beta-lactamases: Hydrolyse β-lactam ring (penicillins/cephalosporins)\n"
            "  – ESBL: Klebsiella, E. coli (destroy all penicillins + cephalosporins)\n"
            "  – Carbapenemases: KPC, NDM-1 — resist even carbapenems\n"
            "• Aminoglycoside-modifying enzymes (acetyltransferases, phosphotransferases)\n"
            "• Chloramphenicol acetyltransferase (CAT)\n\n"
            "2. TARGET SITE MODIFICATION\n"
            "• MRSA: mecA gene → PBP2a (low affinity for all β-lactams)\n"
            "• 23S rRNA methylation → erythromycin/macrolide resistance\n"
            "• DNA gyrase/Topoisomerase IV mutation → fluoroquinolone resistance\n"
            "• VRE: vanA/vanB → D-Ala-D-Lac (instead of D-Ala-D-Ala) → vancomycin cannot bind\n\n"
            "3. EFFLUX PUMPS\n"
            "• Active drug export from cell\n"
            "• Tetracycline resistance (Gram -ve); MexAB-OprM (Pseudomonas)\n\n"
            "4. REDUCED PERMEABILITY\n"
            "• Loss of OmpC/OmpF porins → carbapenem resistance in Gram -ve\n"
            "• OprD loss → imipenem resistance in Pseudomonas\n\n"
            "RESISTANCE TRANSFER:\n"
            "• Conjugation: R-plasmid transfer (most common MDR mechanism)\n"
            "• Transformation: Uptake of naked DNA (S. pneumoniae)\n"
            "• Transduction: Phage-mediated (S. aureus toxins)\n"
            "• Transposons: Jump between plasmids/chromosomes\n\n"
            "TREATMENT:\n"
            "• MRSA: Vancomycin or Linezolid or Daptomycin\n"
            "• ESBL: Carbapenems (meropenem)\n"
            "• CRE: Colistin/Polymyxin B ± combination therapy"
        ),
        "high_yield_takeaway": "MRSA = PBP2a (mecA gene) → β-lactam resistance. ESBL = hydrolyse all penicillins + cephalosporins. VRE = D-Ala-D-Lac modification. Conjugation = most common resistance transfer.",
        "hashtags": ["#MedicoHelp", "#Microbiology", "#MBBS", "#NEETPG", "#AMR"],
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "Acid-Fast Bacilli & TB Diagnosis — PYQ Pattern",
        "subject": Subject.microbiology,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "ZN stain = red AFB on blue; culture on LJ medium (6–8 weeks); gold standard = culture",
        "caption": (
            "Acid-Fast Bacilli & TB Diagnosis — PYQ Concept\n\n"
            "NEET-PG repeatedly tests microbiological diagnosis of tuberculosis.\n\n"
            "M. TUBERCULOSIS — Key Properties:\n"
            "• AFB: Rich in mycolic acid → retains red dye after acid-alcohol wash\n"
            "• Non-motile, obligate aerobe (prefers O₂-rich apex of lung)\n"
            "• Slow growing: doubling time 15–20 hours\n\n"
            "DIAGNOSTIC METHODS:\n"
            "• ZN Smear: Red AFB on blue background; needs ≥5,000 AFB/mL; hours turnaround\n"
            "• Auramine-Rhodamine: Fluorescent microscopy; more sensitive than ZN\n"
            "• LJ Culture: Gold standard; rough buff dry colonies; 6–8 weeks\n"
            "• MGIT (liquid): Automated fluorescence; 1–3 weeks\n"
            "• GeneXpert MTB/RIF: PCR; detects rifampicin resistance; 2 hours; WHO recommended\n"
            "• IGRA (QuantiFERON-TB): Latent TB; measures IFN-γ; no BCG cross-reaction\n"
            "• Mantoux (TST): Latent TB; false +ve with BCG vaccination\n\n"
            "CULTURE MEDIA:\n"
            "• LJ (egg-based): Eugonic (M. tuberculosis) vs dysgonic (M. bovis) growth\n"
            "• Niacin test: Positive only in M. tuberculosis\n\n"
            "ZN STAIN: Carbol fuchsin (hot) → acid-alcohol decolouriser → methylene blue counterstain\n"
            "AFB: Bright red/pink rods on blue background\n\n"
            "GRADING (RNTCP): Scanty = 1–9 AFB/100 fields; "
            "1+ = 10–99/100 fields; 2+ = 1–10/field; 3+ = >10/field\n\n"
            "⚠️ Exam Trap: GeneXpert MTB/RIF = WHO recommended; detects rifampicin resistance (MDR-TB surrogate) within 2 hours."
        ),
        "high_yield_takeaway": "ZN stain = red AFB. Culture on LJ medium = gold standard (6–8 weeks). GeneXpert = rapid diagnosis + rifampicin resistance detection. IGRA preferred over Mantoux in BCG-vaccinated individuals.",
        "hashtags": ["#MedicoHelp", "#Microbiology", "#MBBS", "#NEETPG", "#PYQ"],
    },
    # ── Mnemonic ──────────────────────────────────────────────────────────────
    {
        "title": "Mnemonic: SPACE — Encapsulated Bacteria (Polysaccharide Capsule)",
        "subject": Subject.microbiology,
        "content_format": ContentFormat.mnemonic,
        "poster_text": "Encapsulated bacteria: S. pneumoniae, H. influenzae b, N. meningitidis, K. pneumoniae, Group B Strep, E. coli K1. Mnemonic: 'SHiNK' — anti-phagocytic virulence factor.",
        "caption": "Explain the high-yield encapsulated bacteria for NEET-PG: Streptococcus pneumoniae (polysaccharide vaccine), Haemophilus influenzae type b (Hib vaccine), Neisseria meningitidis (ACWY + B vaccines), Klebsiella pneumoniae, Escherichia coli (K1 capsule — neonatal meningitis), Group B Streptococcus (S. agalactiae — neonatal sepsis), Cryptococcus neoformans (polysaccharide capsule — India ink stain), Pseudomonas aeruginosa (alginate capsule in CF). Capsule = virulence factor (anti-phagocytic). Vaccines target capsule polysaccharides.",
        "high_yield_takeaway": "Encapsulated bacteria: S. pneumoniae, H. influenzae b, N. meningitidis, K. pneumoniae, Group B Strep, E. coli K1. Capsule = anti-phagocytic. Splenectomy patients most vulnerable to these.",
        "hashtags": ["#MedicoHelp", "#Microbiology", "#MBBS", "#NEETPG", "#Mnemonic", "#EncapsulatedBacteria"],
    },
    # ── Flashcard ─────────────────────────────────────────────────────────────
    {
        "title": "Flashcard: Chlamydia trachomatis Life Cycle — Elementary vs Reticulate Bodies",
        "subject": Subject.microbiology,
        "content_format": ContentFormat.flashcard,
        "poster_text": "Chlamydia: Elementary body (infectious, spore-like) → Reticulate body (replicative, intracellular)",
        "caption": "Chlamydia trachomatis life cycle. Elementary body (EB) — 0.3 μm, infectious, metabolically inert, survives extracellularly, attaches to host cell. EB → endocytosis → conversion to Reticulate body (RB) — 0.5-1 μm, non-infectious, metabolically active, replicates by binary fission inside vacuole (inclusion body). RB → reorganises back to EB → released by cell lysis. Cycle: 48-72 hours. Detection: Intracytoplasmic inclusion bodies on Giemsa stain (large, perinuclear). Serovars: A-C (trachoma), D-K (STI, inclusion conjunctivitis, neonatal pneumonia), L1-L3 (LGV). Treatment: Doxycycline or Azithromycin. NOT penicillin sensitive (no cell wall).",
        "question": "In the Chlamydia trachomatis life cycle, which form is infectious but metabolically inert, and which form replicates intracellularly?",
        "correct_answer": "Elementary body (EB) = infectious, spore-like, survives extracellularly. Reticulate body (RB) = non-infectious, replicates by binary fission inside the host cell.",
        "high_yield_takeaway": "EB = infectious, RB = replicative. Cycle 48-72 hrs. Intracytoplasmic inclusions on Giemsa. Doxycycline/azithromycin = treatment.",
        "hashtags": ["#MedicoHelp", "#Microbiology", "#MBBS", "#NEETPG", "#Flashcard", "#Chlamydia"],
    },
    # ── True/False ────────────────────────────────────────────────────────────
    {
        "title": "True or False: All Clostridium species are Gram-positive, spore-forming, and obligate anaerobes",
        "subject": Subject.microbiology,
        "content_format": ContentFormat.true_false,
        "poster_text": "Clostridium: Gram +ve, spore-forming, obligate anaerobes — but C. perfringens is aerotolerant",
        "caption": "Clostridium genus: Gram-positive rods, spore-forming (terminal/subterminal), obligate anaerobes (except C. perfringens is aerotolerant). Key species: C. tetani (drum-stick spore, tetanus, tetanospasmin toxin — blocks inhibitory neurotransmitters), C. botulinum (spores in honey, botulinum toxin — blocks ACh release, flaccid paralysis), C. perfringens (most common gas gangrene, α-toxin = lecithinase/phospholipase C, double zone haemolysis, Nagler's reaction reversed by antitoxin), C. difficile (pseudomembranous colitis, toxin A enterotoxin + toxin B cytotoxin, following antibiotic use).",
        "question": "All Clostridium species are Gram-positive, spore-forming, and obligate anaerobes.",
        "correct_answer": "FALSE",
        "explanation": "While most Clostridium species are obligate anaerobes, Clostridium perfringens is aerotolerant (can grow in the presence of small amounts of oxygen). All are Gram-positive rods and spore-forming. C. perfringens is the most common cause of gas gangrene and shows double zone haemolysis on blood agar.",
        "high_yield_takeaway": "Clostridium: Gram+ spore-forming rods. C. perfringens = aerotolerant. C. tetani = drum-stick spore. C. botulinum = honey in infants. C. difficile = pseudomembranous colitis.",
        "hashtags": ["#MedicoHelp", "#Microbiology", "#MBBS", "#NEETPG", "#TrueFalse", "#Clostridium"],
    },
    # ── One-liner Recall ──────────────────────────────────────────────────────
    {
        "title": "One-liner Recall: Mode of Action of Major Antibiotic Classes",
        "subject": Subject.microbiology,
        "content_format": ContentFormat.one_liner_recall,
        "poster_text": "Antibiotic MOA: cell wall, protein synthesis, DNA/RNA, cell membrane, folate — know which drug does what",
        "caption": "Fill in the blank: \"Tetracyclines act by binding to the ___ ribosomal subunit and inhibiting ___.\" Answer: \"30S ribosomal subunit, inhibiting aminoacyl-tRNA binding.\" Then list major classes: Cell wall (β-lactams, vancomycin, daptomycin). Protein synthesis — 30S (aminoglycosides, tetracyclines). Protein synthesis — 50S (macrolides, chloramphenicol, linezolid, clindamycin). DNA gyrase (fluoroquinolones). RNA polymerase (rifampicin). Cell membrane (polymyxins). Folate synthesis (sulfonamides, trimethoprim).",
        "question": "Tetracyclines act by binding to the ___ ribosomal subunit and inhibiting ___.",
        "correct_answer": "30S, aminoacyl-tRNA binding",
        "high_yield_takeaway": "30S: aminoglycosides + tetracyclines. 50S: macrolides + chloramphenicol + linezolid + clindamycin. Cell wall: β-lactams + vancomycin. DNA gyrase: fluoroquinolones.",
        "hashtags": ["#MedicoHelp", "#Microbiology", "#MBBS", "#NEETPG", "#OneLiner", "#Antibiotics"],
    },
]
