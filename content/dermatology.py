"""High-yield Dermatology content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ───────────────────────────────────────────────────────
    {
        "title": "Psoriasis — Clinical Features and Types",
        "subject": Subject.dermatology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Psoriasis rapid revision — Auspitz sign, Koebner, and all the high-yield types!",
        "caption": (
            "Psoriasis — Clinical Features and Types\n\n"
            "Definition: Chronic, immune-mediated (T-cell driven), papulosquamous skin disorder\n\n"
            "Pathology:\n"
            "• Epidermal hyperproliferation (turnover 3–4 days vs normal 28 days)\n"
            "• Parakeratosis, Munro's microabscesses (neutrophils in stratum corneum)\n"
            "• Spongiform pustules of Kogoj (in epidermis)\n\n"
            "Classic Lesion: Well-demarcated, erythematous plaques with silvery-white scale\n"
            "Distribution: Extensor surfaces (elbows, knees), scalp, sacrum, nails\n\n"
            "Clinical Signs:\n"
            "• Auspitz sign: Pinpoint bleeding on removing scale (dilated dermal capillaries)\n"
            "• Koebner phenomenon: Lesions at sites of trauma/injury\n"
            "• Candle-grease sign: Scales scrape off like candle grease\n"
            "• Grattage test: Progressive scale removal → membrane → Auspitz sign\n\n"
            "Nail Changes (50% cases): Pitting (#1), onycholysis, oil-drop sign, subungual hyperkeratosis\n\n"
            "Types of Psoriasis:\n"
            "• Plaque (psoriasis vulgaris): Most common (80–90%)\n"
            "• Guttate: Small drop-shaped lesions; follows streptococcal throat infection; good prognosis\n"
            "• Pustular: Von Zumbusch (generalized, fever, emergency) or palmoplantar\n"
            "• Erythrodermic: >90% BSA; life-threatening; risk of high-output cardiac failure\n"
            "• Inverse: Flexures (axilla, groin); minimal scale\n"
            "• Psoriatic arthritis: 5–30%; seronegative; DIP involvement, pencil-in-cup deformity"
        ),
        "high_yield_takeaway": "Psoriasis: Auspitz sign + Koebner + silvery scale on extensor surface. Guttate follows strep infection. Pustular = emergency.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Dermatology", "#Psoriasis"],
    },
    {
        "title": "Pemphigus vs Pemphigoid — Key Differences",
        "subject": Subject.dermatology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Pemphigus vs Pemphigoid — never confuse these two blistering disorders again!",
        "caption": (
            "Pemphigus vs Pemphigoid — Rapid Revision\n\n"
            "PEMPHIGUS VULGARIS\n"
            "• Age: Middle-aged (40–60 yrs)\n"
            "• Blister level: Intraepidermal (suprabasal split)\n"
            "• Antigen: Desmoglein 3 (mucosa) and Desmoglein 1 (skin) — desmosomal cadherins\n"
            "• Antibody: IgG anti-desmoglein (anti-intercellular cement)\n"
            "• Nikolsky sign: POSITIVE — lateral pressure causes skin to slide/blister\n"
            "• Biopsy: Acantholysis (loss of cell-cell adhesion), Tzanck cells (tombstone pattern)\n"
            "• DIF: Intercellular IgG in epidermis (fishnet/chicken-wire pattern)\n"
            "• Features: Oral involvement common (often first); flaccid, easily ruptured blisters\n"
            "• Prognosis: More serious; requires high-dose systemic steroids + rituximab/azathioprine\n\n"
            "BULLOUS PEMPHIGOID\n"
            "• Age: Elderly (> 60 yrs)\n"
            "• Blister level: Subepidermal (below epidermis, at dermal-epidermal junction)\n"
            "• Antigen: BP180 (collagen XVII) and BP230 — hemidesmosomes\n"
            "• Antibody: IgG + C3 anti-hemidesmosome\n"
            "• Nikolsky sign: NEGATIVE\n"
            "• Biopsy: Subepidermal blister; eosinophilic infiltrate in dermis\n"
            "• DIF: Linear IgG + C3 at dermoepidermal junction\n"
            "• Features: Tense, intact blisters on urticarial base; itchy; mucosa rarely involved\n"
            "• Prognosis: Better than pemphigus; topical/systemic steroids\n\n"
            "Memory trick: PemphIGUS = IgG intercellular (intraepidermal) | PemphiGOID = GOod prognosis, tense blister, old age"
        ),
        "high_yield_takeaway": "Pemphigus: intraepidermal, anti-desmoglein IgG, Nikolsky +ve, acantholysis, oral mucosa. Pemphigoid: subepidermal, anti-BP180, Nikolsky -ve, tense blisters.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Dermatology", "#BullousDisease"],
    },
    # ── MCQ ──────────────────────────────────────────────────────────────────
    {
        "title": "Leprosy Classification and Ridley-Jopling Scale — MCQ",
        "subject": Subject.dermatology,
        "content_format": ContentFormat.mcq,
        "poster_text": "A patient with anesthetic patches and nerve thickening — classify the leprosy!",
        "caption": (
            "Leprosy Classification — High-Yield Revision\n\n"
            "Ridley-Jopling Classification (immunological spectrum):\n"
            "TT → BT → BB → BL → LL (increasing lepromatous, decreasing tuberculoid)\n\n"
            "Tuberculoid (TT):\n"
            "• Strong CMI; few bacilli (paucibacillary); single/few lesions\n"
            "• Well-defined, hypopigmented, anesthetic plaques; definite nerve thickening\n"
            "• Lepromin test: POSITIVE (4+ reaction)\n\n"
            "Lepromatous (LL):\n"
            "• Poor CMI; many bacilli (multibacillary); numerous lesions\n"
            "• Madarosis (loss of lateral eyebrow), leonine facies, saddle-nose, glove-stocking sensory loss\n"
            "• Lepromin test: NEGATIVE\n\n"
            "Borderline (BB): Unstable; most common type; most common to have reactions\n\n"
            "MDT Regimens (WHO):\n"
            "• Paucibacillary (TT/BT): Dapsone + Rifampicin × 6 months\n"
            "• Multibacillary (BB/BL/LL): Dapsone + Rifampicin + Clofazimine × 12 months\n\n"
            "Lepra Reactions:\n"
            "• Type 1 (Reversal): T-cell mediated; any type; treat with steroids\n"
            "• Type 2 (ENL — Erythema Nodosum Leprosum): Immune complex; BL/LL; treat with thalidomide"
        ),
        "question": (
            "A 35-year-old farmer presents with a single, well-defined, hypopigmented anesthetic patch over the left cheek "
            "with thickening of the great auricular nerve. Slit-skin smear shows no bacilli. Lepromin test is strongly positive. "
            "Which of the following best describes this patient's classification and the appropriate MDT regimen?"
        ),
        "options": [
            "A. Lepromatous leprosy (LL) — multibacillary MDT with dapsone, rifampicin, and clofazimine for 12 months",
            "B. Tuberculoid leprosy (TT) — paucibacillary MDT with dapsone and rifampicin for 6 months",
            "C. Borderline lepromatous (BL) — multibacillary MDT for 12 months",
            "D. Borderline tuberculoid (BT) — paucibacillary MDT for 6 months, lepromin test negative",
        ],
        "correct_answer": "B. Tuberculoid leprosy (TT) — paucibacillary MDT with dapsone and rifampicin for 6 months",
        "explanation": (
            "The clinical features — single well-defined hypopigmented anesthetic patch, thickened peripheral nerve, negative slit-skin smear (no bacilli), and strongly positive lepromin test — are diagnostic of tuberculoid leprosy (TT). "
            "TT represents the pole with the strongest cell-mediated immunity, fewest bacilli (paucibacillary), and best prognosis. "
            "Paucibacillary leprosy (TT and BT: 1–5 lesions, no bacilli on smear) is treated with WHO-MDT paucibacillary regimen: dapsone 100 mg daily + rifampicin 600 mg monthly supervised, for 6 months. "
            "Lepromatous leprosy (LL) would present with multiple, poorly defined lesions, leonine facies, madarosis, and a negative lepromin test due to anergic immune state. "
            "Borderline lepromatous (BL) is multibacillary and lepromin-negative, requiring 12-month MDT with clofazimine added."
        ),
        "high_yield_takeaway": "TT leprosy: single lesion, lepromin +ve, no bacilli → paucibacillary MDT (dapsone + rifampicin) × 6 months. LL: lepromin -ve, many bacilli, multibacillary MDT × 12 months.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Dermatology", "#Leprosy"],
    },
    {
        "title": "Drug-Induced Skin Reactions — MCQ",
        "subject": Subject.dermatology,
        "content_format": ContentFormat.mcq,
        "poster_text": "Patient develops severe blistering rash after starting a new drug — which reaction is this?",
        "caption": (
            "Drug-Induced Skin Reactions — Key Associations\n\n"
            "Fixed Drug Eruption (FDE):\n"
            "• Recurs at same site on re-exposure; residual hyperpigmentation\n"
            "• Common drugs: NSAIDs, tetracycline, cotrimoxazole, metronidazole, quinine\n\n"
            "Steven-Johnson Syndrome (SJS) / TEN:\n"
            "• SJS: < 10% BSA; TEN (Lyell's): > 30% BSA; 10–30% = overlap\n"
            "• Nikolsky sign: Positive in TEN\n"
            "• Drugs: Allopurinol (#1), carbamazepine, lamotrigine, phenytoin, sulfonamides, nevirapine\n"
            "• HLA-B*1502 (carbamazepine SJS) — Screen South-East Asian patients\n\n"
            "Erythema Multiforme:\n"
            "• Target (iris) lesions; HSV-1 most common cause; drugs (sulfonamides)\n\n"
            "Drug Hypersensitivity Syndrome (DRESS):\n"
            "• Fever, rash, lymphadenopathy, eosinophilia, visceral organ involvement\n"
            "• Drugs: Allopurinol, carbamazepine, phenytoin, dapsone, minocycline\n"
            "• Onset: 2–8 weeks after starting drug\n\n"
            "Urticaria / Angioedema: IgE-mediated (penicillin) or direct mast cell degranulation (aspirin, opioids)\n\n"
            "Photosensitivity: Amiodarone, tetracycline, fluoroquinolones, chlorpromazine, NSAIDs"
        ),
        "question": (
            "A 28-year-old epileptic patient started on lamotrigine 3 weeks ago presents with high-grade fever, "
            "widespread erythema, and large flaccid blisters covering approximately 35% of body surface area. "
            "Nikolsky sign is positive. Oral and conjunctival mucosa are severely involved. "
            "Which of the following is the most appropriate immediate management?"
        ),
        "options": [
            "A. Continue lamotrigine and add high-dose intravenous methylprednisolone",
            "B. Discontinue lamotrigine immediately; transfer to burns unit for supportive care with IV fluids and wound management",
            "C. Switch to carbamazepine and prescribe oral antihistamines",
            "D. Apply topical calcineurin inhibitors and observe for 48 hours",
        ],
        "correct_answer": "B. Discontinue lamotrigine immediately; transfer to burns unit for supportive care with IV fluids and wound management",
        "explanation": (
            "The clinical scenario — fever, Nikolsky-positive widespread blistering covering > 30% BSA, and mucosal involvement 2–3 weeks after starting lamotrigine — is diagnostic of Toxic Epidermal Necrolysis (TEN), also called Lyell's syndrome. "
            "TEN (> 30% BSA) is a dermatologic emergency with mortality up to 30%; it is distinguished from SJS (< 10% BSA) and SJS-TEN overlap (10–30%) by extent of skin detachment. "
            "The single most critical intervention is immediate cessation of the causative drug (lamotrigine in this case — a well-documented TEN trigger). "
            "Management thereafter is supportive: fluid and electrolyte replacement, wound care in a burns unit or ICU, ophthalmology review for conjunctival involvement, and nutritional support. "
            "Systemic corticosteroids are controversial and generally avoided; cyclosporine and IVIG are sometimes used as adjuncts. "
            "Carbamazepine is contraindicated as an alternative since it carries an even higher risk of SJS/TEN, especially in patients with HLA-B*1502 allele."
        ),
        "high_yield_takeaway": "TEN (> 30% BSA): Nikolsky +ve, lamotrigine/allopurinol/sulfonamides → STOP drug immediately + burns unit care. SJS < 10%, TEN > 30% BSA.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Dermatology", "#DrugReactions"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "Acne Vulgaris — Pathogenesis and Management",
        "subject": Subject.dermatology,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "Acne vulgaris — pathogenesis, grading, and evidence-based management for NEET-PG.",
        "caption": (
            "Acne Vulgaris — Concise Notes\n\n"
            "PATHOGENESIS (4 key steps):\n"
            "1. Sebaceous gland hypersecretion — androgen-driven (DHT at sebaceous gland)\n"
            "2. Follicular hyperkeratinisation — comedone (blackhead/whitehead) formation\n"
            "3. Propionibacterium acnes (Cutibacterium acnes) colonisation — anaerobe\n"
            "4. Inflammation — lipase → free fatty acids → IL-1, TNF → inflammatory papules, pustules, nodules\n\n"
            "LESION TYPES:\n"
            "• Non-inflammatory: Open comedone (blackhead), closed comedone (whitehead)\n"
            "• Inflammatory: Papule, pustule, nodule, cyst (nodulotystic)\n\n"
            "GRADING (Global Acne Grading System):\n"
            "• Mild: Comedones ± few papules/pustules\n"
            "• Moderate: Multiple papules/pustules, occasional nodules\n"
            "• Severe: Extensive nodules, cysts, scarring\n\n"
            "MANAGEMENT:\n"
            "Mild acne:\n"
            "• Topical retinoids (tretinoin, adapalene) — comedolytic, first-line\n"
            "• Topical benzoyl peroxide — antibacterial, prevents antibiotic resistance\n"
            "• Topical antibiotics (clindamycin) — always combined with BPO to prevent resistance\n\n"
            "Moderate acne:\n"
            "• Add oral antibiotics: Doxycycline (first-line) or erythromycin (if pregnant)\n"
            "• In females: OCP (especially with hyperandrogenism/PCOS) or spironolactone\n\n"
            "Severe/nodulocystic acne:\n"
            "• Oral isotretinoin (13-cis-retinoic acid) — most effective; mandatory contraception (teratogenic)\n"
            "• Monitor: LFTs, lipid profile, mood changes, mucocutaneous effects\n\n"
            "SCARRING TREATMENT: Fractional CO2 laser, microneedling, chemical peels, subcision"
        ),
        "high_yield_takeaway": "Acne: 4 steps — sebum, hyperkeratosis, C. acnes, inflammation. Isotretinoin for severe; teratogenic → mandatory contraception. BPO prevents antibiotic resistance.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Dermatology", "#AcneVulgaris"],
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "SLE Skin Manifestations — PYQ Pattern",
        "subject": Subject.dermatology,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "SLE skin manifestations — repeatedly tested in NEET-PG dermatology and medicine!",
        "caption": (
            "SLE Skin Manifestations — PYQ High-Yield Concept\n\n"
            "SLE is a multisystem autoimmune disease; skin involvement occurs in 70–80% of patients.\n\n"
            "ACUTE CUTANEOUS LUPUS:\n"
            "• Malar (butterfly) rash — erythema over cheeks and nasal bridge, spares nasolabial folds\n"
            "• Photosensitive; appears/worsens with sun exposure\n"
            "• Associated with active systemic disease\n\n"
            "SUBACUTE CUTANEOUS LUPUS (SCLE):\n"
            "• Annular or papulosquamous lesions; photodistributed\n"
            "• Associated with anti-Ro (SS-A) antibodies\n"
            "• Drug-induced SCLE: Hydrochlorothiazide, terbinafine, calcium channel blockers\n\n"
            "CHRONIC CUTANEOUS LUPUS — DISCOID LUPUS ERYTHEMATOSUS (DLE):\n"
            "• Scarring, follicular plugging, atrophy; hypopigmented centre, hyperpigmented border\n"
            "• Scalp involvement → permanent scarring alopecia\n"
            "• Only 5% of DLE patients develop systemic SLE\n\n"
            "OTHER SKIN FEATURES IN SLE:\n"
            "• Photosensitivity (ACR criterion)\n"
            "• Livedo reticularis — vasculitis/antiphospholipid syndrome\n"
            "• Raynaud's phenomenon (20–30%)\n"
            "• Oral ulcers — painless (important distinction from aphthous ulcers)\n"
            "• Non-scarring alopecia — 'lupus hair' (fragile frontal hairline hair)\n"
            "• Vasculitic lesions — purpura, periungual telangiectasia\n\n"
            "KEY ANTIBODIES AND SKIN ASSOCIATION:\n"
            "• Anti-dsDNA: Correlates with disease activity and nephritis\n"
            "• Anti-Sm: Most specific for SLE (not most sensitive)\n"
            "• Anti-Ro (SS-A): SCLE, neonatal lupus, photosensitivity\n"
            "• Antiphospholipid antibody: Livedo reticularis, thrombosis\n\n"
            "PYQ ANSWER KEY:\n"
            "Q: Butterfly rash spares which area? → Nasolabial folds\n"
            "Q: Most specific antibody for SLE? → Anti-Smith (anti-Sm)\n"
            "Q: SCLE associated with which antibody? → Anti-Ro (SS-A)\n"
            "Q: Oral ulcers in SLE — painful or painless? → Painless\n"
            "Q: DLE → systemic SLE risk? → Only 5%"
        ),
        "high_yield_takeaway": "SLE malar rash spares nasolabial folds. Anti-Sm = most specific. SCLE = anti-Ro. Oral ulcers = painless. DLE → only 5% progress to systemic SLE.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Dermatology", "#PYQ"],
    },
]
