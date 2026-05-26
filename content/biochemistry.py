"""High-yield Biochemistry content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ───────────────────────────────────────────────────────
    {
        "title": "Urea Cycle — Key Enzymes & Intermediates",
        "subject": Subject.biochemistry,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Urea cycle: Liver mitochondria + cytosol; defect → hyperammonaemia",
        "caption": (
            "Urea Cycle — Rapid Revision\n\n"
            "Location: Starts in mitochondria (steps 1–2), completed in cytosol (steps 3–5)\n\n"
            "Substrates: 2 NH₃ + 1 CO₂ + 3 ATP → 1 Urea\n\n"
            "Steps & Enzymes:\n"
            "1. NH₃ + CO₂ → Carbamoyl phosphate  [CPS-I — mitochondria; rate-limiting]\n"
            "   Activated by N-acetylglutamate (NAG); cofactors: biotin + ATP\n"
            "2. Carbamoyl-P + Ornithine → Citrulline  [OTC — mitochondria]\n"
            "3. Citrulline + Aspartate → Argininosuccinate  [ASS — cytosol]\n"
            "4. Argininosuccinate → Arginine + Fumarate  [ASL — cytosol]\n"
            "5. Arginine → Ornithine + Urea  [Arginase — cytosol]\n\n"
            "Key Facts:\n"
            "• OTC deficiency: Most common urea cycle defect; X-linked; ↑ orotic acid in urine\n"
            "• CPS-I deficiency: ↓ orotic acid (distinguishes from OTC)\n"
            "• Hyperammonaemia → cerebral oedema, asterixis, encephalopathy\n"
            "• Fumarate links urea cycle to TCA cycle\n"
            "• N-acetylglutamate (NAG) is the essential allosteric activator of CPS-I\n"
            "• Aspartate provides the second nitrogen atom (step 3)\n\n"
            "⚠️ Exam Trap: OTC deficiency → ↑ orotic acid; CPS-I deficiency → normal orotic acid."
        ),
        "high_yield_takeaway": "OTC deficiency (X-linked) = most common urea cycle defect; ↑ orotic acid in urine distinguishes it from CPS-I deficiency.",
        "hashtags": ["#MedicoHelp", "#Biochemistry", "#MBBS", "#NEETPG", "#UreaCycle"],
    },
    {
        "title": "HMP Shunt — Pentose Phosphate Pathway",
        "subject": Subject.biochemistry,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "HMP shunt: NADPH for protection & Ribose-5-P for nucleotides — no ATP produced",
        "caption": (
            "HMP Shunt (Pentose Phosphate Pathway) — Rapid Revision\n\n"
            "Location: Cytosol; most active in liver, RBCs, adrenal cortex, lactating mammary gland\n\n"
            "Two Phases:\n"
            "OXIDATIVE (irreversible):\n"
            "• G6P → 6-Phosphogluconolactone  [G6PD — rate-limiting; 1 NADPH produced]\n"
            "• 6-Phosphogluconolactone → Ribulose-5-phosphate  [1 NADPH produced]\n"
            "• Net: 1 G6P → 2 NADPH + CO₂ + Ribulose-5-P\n\n"
            "NON-OXIDATIVE (reversible):\n"
            "• Interconverts sugar phosphates via transketolase (requires TPP/Vit B1) & transaldolase\n"
            "• Produces Ribose-5-P (for nucleotide & nucleic acid synthesis)\n\n"
            "NADPH Uses:\n"
            "• Glutathione reductase (RBC oxidative protection)\n"
            "• Fatty acid & cholesterol synthesis\n"
            "• Cytochrome P450 reactions\n"
            "• NADPH oxidase in neutrophils (respiratory burst)\n\n"
            "G6PD Deficiency:\n"
            "• X-linked recessive; most common enzyme deficiency worldwide\n"
            "• Triggers: Primaquine, dapsone, sulfonamides, fava beans, infections\n"
            "• ↓ NADPH → ↓ reduced glutathione → RBC oxidative haemolysis\n"
            "• Blood film: Heinz bodies (denatured Hb) + bite cells\n\n"
            "⚠️ Exam Trap: Transketolase requires Thiamine (B1); RBC transketolase assay detects B1 deficiency."
        ),
        "high_yield_takeaway": "G6PD is rate-limiting in HMP shunt; NADPH protects RBCs. G6PD deficiency → oxidative haemolysis, Heinz bodies, bite cells on PBS.",
        "hashtags": ["#MedicoHelp", "#Biochemistry", "#MBBS", "#NEETPG", "#G6PD"],
    },
    # ── MCQ ───────────────────────────────────────────────────────────────────
    {
        "title": "Phenylketonuria (PKU) — MCQ",
        "subject": Subject.biochemistry,
        "content_format": ContentFormat.mcq,
        "poster_text": "PKU: Phenylalanine hydroxylase deficiency → musty odour, fair skin, intellectual disability",
        "caption": "MCQ: Phenylketonuria clinical presentation and biochemical defect",
        "question": (
            "A 4-month-old infant is brought with fair skin and hair compared to siblings, a musty "
            "body odour, and progressive intellectual disability. Newborn screening (Guthrie test) "
            "done on day 5 of life was positive. Dietary phenylalanine restriction is started. "
            "Which enzyme is deficient in this condition, and what is the immediate metabolite that accumulates?"
        ),
        "options": [
            "A. Homogentisate oxidase; homogentisic acid",
            "B. Phenylalanine hydroxylase; phenylalanine",
            "C. Tyrosinase; tyrosine",
            "D. Fumarylacetoacetase; succinylacetone",
        ],
        "correct_answer": "B. Phenylalanine hydroxylase; phenylalanine",
        "explanation": (
            "PKU (Phenylketonuria) is caused by deficiency of phenylalanine hydroxylase (PAH), "
            "which normally converts phenylalanine → tyrosine using tetrahydrobiopterin (BH4) as cofactor. "
            "Accumulation of phenylalanine leads to conversion via transamination to phenylpyruvate, "
            "phenyllactate, and phenylacetate — the latter giving the musty/mousy odour. Tyrosine becomes "
            "conditionally essential, and reduced melanin synthesis explains the fair phenotype. "
            "Option A describes alkaptonuria (dark urine, ochronosis); C describes oculocutaneous albinism; "
            "D describes tyrosinaemia type I (hepatotoxic). Guthrie test screens blood phenylalanine on day 3–5."
        ),
        "high_yield_takeaway": "PKU = PAH deficiency → ↑ phenylalanine → musty odour, fair hair/skin, intellectual disability. Guthrie test screens on day 3–5 of life.",
        "hashtags": ["#MedicoHelp", "#Biochemistry", "#MBBS", "#NEETPG", "#PKU"],
    },
    {
        "title": "Glycogen Storage Diseases — MCQ",
        "subject": Subject.biochemistry,
        "content_format": ContentFormat.mcq,
        "poster_text": "Von Gierke = G6Pase; Pompe = acid maltase; McArdle = muscle phosphorylase",
        "caption": "MCQ: Glycogen storage disease identification from clinical features",
        "question": (
            "A 3-year-old child presents with markedly enlarged liver and severe hypoglycaemia during "
            "fasting. Laboratory investigations reveal lactic acidosis, hyperuricaemia, and hyperlipidaemia. "
            "Glucagon administration fails to raise blood glucose. Liver biopsy shows excess glycogen and "
            "fat accumulation. Which enzyme is most likely deficient in this child?"
        ),
        "options": [
            "A. Lysosomal acid alpha-glucosidase (acid maltase)",
            "B. Glucose-6-phosphatase",
            "C. Muscle glycogen phosphorylase",
            "D. Debranching enzyme (amylo-1,6-glucosidase)",
        ],
        "correct_answer": "B. Glucose-6-phosphatase",
        "explanation": (
            "This is Von Gierke disease (GSD Type Ia) caused by Glucose-6-phosphatase (G6Pase) deficiency. "
            "G6P cannot be converted to free glucose, so both glycogenolysis and gluconeogenesis fail to "
            "raise blood glucose — hence glucagon is ineffective. Accumulated G6P is shunted to lactate "
            "(lactic acidosis), triglycerides (hyperlipidaemia), and via purine degradation to uric acid "
            "(hyperuricaemia). Hepatomegaly results from glycogen and fat accumulation. "
            "Pompe (Type II) = acid maltase deficiency → cardiomegaly and hypotonia without hypoglycaemia. "
            "McArdle (Type V) = muscle phosphorylase → exercise intolerance, myoglobinuria, no rise in lactate with ischaemic exercise."
        ),
        "high_yield_takeaway": "Von Gierke (GSD I) = G6Pase deficiency → fasting hypoglycaemia, hepatomegaly, lactic acidosis, glucagon unresponsive. Pompe = acid maltase → cardiomegaly.",
        "hashtags": ["#MedicoHelp", "#Biochemistry", "#MBBS", "#NEETPG", "#GSD"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "Collagen Biosynthesis — Steps & Vitamin C Role",
        "subject": Subject.biochemistry,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "Collagen synthesis: Gly-X-Y repeats; Vit C for hydroxylation; cross-linking by lysyl oxidase",
        "caption": (
            "Collagen Biosynthesis — Concise Notes\n\n"
            "Most abundant protein in the body; scaffold of connective tissue, bone, tendons\n\n"
            "Steps of Synthesis:\n"
            "1. TRANSLATION (RER): Pro-alpha chains synthesised; key = Gly-X-Y repeats\n"
            "   (X = Proline; Y = Hydroxyproline/Hydroxylysine)\n"
            "2. HYDROXYLATION (RER): Pro → Hydroxyproline; Lys → Hydroxylysine\n"
            "   Enzymes: Prolyl/Lysyl hydroxylase; Cofactor: Vitamin C — ESSENTIAL\n"
            "   Deficiency → scurvy (bleeding gums, perifollicular haemorrhage)\n"
            "3. GLYCOSYLATION (RER): Galactose/glucose added to hydroxylysine\n"
            "4. TRIPLE HELIX FORMATION (RER): 3 alpha-chains → procollagen\n"
            "5. SECRETION via Golgi → extracellular space\n"
            "6. CLEAVAGE (extracellular): N- & C-propeptides cleaved → tropocollagen\n"
            "   Defect → Dermatosparaxis-type Ehlers-Danlos\n"
            "7. CROSS-LINKING (extracellular): Lysyl oxidase (Cu²⁺-dependent)\n"
            "   Defect: Menkes disease (↓ Cu²⁺); lathyrism (BAPN inhibits lysyl oxidase)\n\n"
            "Collagen Types:\n"
            "• Type I — Bone, skin, tendon, dentin (most abundant)\n"
            "• Type II — Cartilage, vitreous humour\n"
            "• Type III — Blood vessels, healing wounds (first to appear)\n"
            "• Type IV — Basement membrane (non-fibrillar)\n\n"
            "Disease Associations:\n"
            "• Osteogenesis Imperfecta: Type I collagen Gly→X mutation → brittle bones, blue sclerae\n"
            "• Ehlers-Danlos: Defective cross-linking → hyperextensible joints\n"
            "• Alport Syndrome: Type IV collagen defect → haematuria, sensorineural deafness"
        ),
        "high_yield_takeaway": "Vitamin C required for prolyl/lysyl hydroxylation → scurvy if deficient. Lysyl oxidase (Cu-dependent) cross-links collagen extracellularly. Type III = first in wound healing.",
        "hashtags": ["#MedicoHelp", "#Biochemistry", "#MBBS", "#NEETPG", "#Collagen"],
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "Enzyme Kinetics — PYQ Pattern",
        "subject": Subject.biochemistry,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Km, Vmax, inhibition types: The most repeated biochemistry concept in NEET-PG",
        "caption": (
            "Enzyme Kinetics — PYQ Concept (Michaelis-Menten)\n\n"
            "NEET-PG tests this in graph interpretation and drug-mechanism questions yearly.\n\n"
            "Core Parameters:\n"
            "• Km: [S] at which V = ½ Vmax; Low Km = High affinity; High Km = Low affinity\n"
            "• Vmax: Maximum velocity; proportional to total enzyme concentration\n\n"
            "Inhibition Types — Most Tested Table:\n"
            "──────────────────────────────────────────────────\n"
            "Type            Km          Vmax      Reversible?\n"
            "──────────────────────────────────────────────────\n"
            "Competitive     ↑ apparent  Unchanged Yes\n"
            "Non-competitive Unchanged   ↓         No\n"
            "Uncompetitive   ↓           ↓         No\n"
            "Mixed           ↑ or ↓      ↓         No\n"
            "──────────────────────────────────────────────────\n\n"
            "Lineweaver-Burk Plot (1/V vs 1/[S]):\n"
            "• Competitive: Intersect on Y-axis (same Vmax, different Km)\n"
            "• Non-competitive: Intersect on X-axis (same Km, different Vmax)\n"
            "• Uncompetitive: Parallel lines (both change equally)\n\n"
            "Classic NEET-PG Drug Examples:\n"
            "• Methotrexate: Competitive inhibitor of DHFR → ↑ Km, same Vmax\n"
            "• Allopurinol: Competitive inhibitor of xanthine oxidase\n"
            "• Aspirin: Irreversible COX inhibitor (suicide inhibitor)\n"
            "• Penicillin: Irreversible inhibitor of transpeptidase (PBP)\n\n"
            "Kinetics Orders:\n"
            "• Zero-order: Rate constant regardless of [S] (Alcohol, Phenytoin, Aspirin high-dose)\n"
            "• First-order: Rate proportional to [S] — most drugs at therapeutic doses"
        ),
        "high_yield_takeaway": "Competitive inhibition: ↑ Km, same Vmax. Non-competitive: same Km, ↓ Vmax. Lineweaver-Burk: competitive lines cross Y-axis; non-competitive cross X-axis.",
        "hashtags": ["#MedicoHelp", "#Biochemistry", "#MBBS", "#NEETPG", "#PYQ"],
    },
]
