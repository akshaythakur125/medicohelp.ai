"""High-yield Biochemistry content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ───────────────────────────────────────────────────────
    {
        "title": "Urea Cycle — Key Enzymes & Steps",
        "subject": Subject.biochemistry,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Urea cycle: mitochondria start, cytosol finishes — 5 enzymes, 2 NH3",
        "caption": (
            "Urea Cycle — Rapid Revision\n\n"
            "Site: Starts in mitochondria (steps 1–2), completed in cytosol (steps 3–5)\n"
            "Net: 2 NH3 + CO2 → Urea (non-toxic, excreted in urine)\n\n"
            "Enzymes in order:\n"
            "1. Carbamoyl phosphate synthetase I (CPS-I) — mitochondria; rate-limiting step\n"
            "   Activated by: N-acetylglutamate (NAG); inhibited by: excess ammonia\n"
            "2. Ornithine transcarbamylase (OTC) — mitochondria; most common enzyme deficiency\n"
            "3. Argininosuccinate synthetase — cytosol; uses aspartate (2nd NH3 donor)\n"
            "4. Argininosuccinate lyase — cytosol\n"
            "5. Arginase — cytosol; cleaves arginine → urea + ornithine\n\n"
            "Energy cost: 3 ATP per cycle\n\n"
            "Deficiency patterns:\n"
            "• All deficiencies → ↑ ammonia + respiratory alkalosis\n"
            "• OTC deficiency: X-linked; orotic aciduria (orotic acid in urine) — key distinguishing feature\n"
            "• CPS-I deficiency: No orotic aciduria\n\n"
            "⚠️ Exam Trap: Orotic aciduria differentiates OTC deficiency from CPS-I deficiency."
        ),
        "high_yield_takeaway": "OTC deficiency = X-linked, orotic aciduria. CPS-I = no orotic acid. Both → hyperammonaemia.",
        "hashtags": ["#MedicoHelp", "#Biochemistry", "#MBBS", "#NEETPG", "#UreaCycle"],
    },
    {
        "title": "HMP Shunt (Pentose Phosphate Pathway)",
        "subject": Subject.biochemistry,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "HMP Shunt: makes NADPH + ribose-5-phosphate; not ATP",
        "caption": (
            "HMP Shunt (Pentose Phosphate Pathway) — Rapid Revision\n\n"
            "Site: Cytosol of all cells; most active in: RBCs, liver, adrenal cortex, lactating mammary gland, testes\n\n"
            "Products (no ATP generated):\n"
            "• NADPH — reducing power for:\n"
            "  – Glutathione reduction (protects RBCs from oxidative hemolysis)\n"
            "  – Fatty acid synthesis (liver, mammary gland)\n"
            "  – Steroid synthesis (adrenal cortex, gonads)\n"
            "  – Respiratory burst (NADPH oxidase in neutrophils)\n"
            "• Ribose-5-phosphate — nucleotide/nucleic acid synthesis\n\n"
            "Rate-limiting enzyme: Glucose-6-phosphate dehydrogenase (G6PD)\n"
            "Coenzyme: NADP+\n\n"
            "G6PD Deficiency:\n"
            "• X-linked recessive; most common enzyme deficiency worldwide\n"
            "• Triggers: Primaquine, dapsone, sulfonamides, fava beans, infection\n"
            "• Result: ↓ NADPH → ↓ glutathione → oxidative RBC damage → intravascular hemolysis\n"
            "• Blood film: Heinz bodies + bite cells\n\n"
            "⚠️ Exam Trap: G6PD is most active in well-fed state (unlike glycolysis which is active in fasting)."
        ),
        "high_yield_takeaway": "HMP Shunt → NADPH + Ribose-5-P. G6PD deficiency → Heinz bodies, bite cells, oxidant-triggered haemolysis.",
        "hashtags": ["#MedicoHelp", "#Biochemistry", "#MBBS", "#NEETPG", "#G6PD"],
    },
    # ── MCQ ───────────────────────────────────────────────────────────────────
    {
        "title": "Phenylketonuria (PKU) — MCQ",
        "subject": Subject.biochemistry,
        "content_format": ContentFormat.mcq,
        "poster_text": "PKU: musty odour, fair skin, intellectual disability — phenylalanine hydroxylase deficient",
        "caption": "MCQ: Phenylketonuria diagnosis and enzyme defect",
        "question": (
            "A 6-month-old infant is brought to the clinic for developmental delay and seizures. "
            "The mother reports a musty, mousy odour to the baby's urine and sweat. "
            "The child has unusually fair skin and blonde hair despite dark-haired parents. "
            "Newborn screening at birth was not performed. "
            "Which enzyme deficiency is most likely responsible for this presentation?"
        ),
        "options": [
            "A. Homogentisate oxidase",
            "B. Phenylalanine hydroxylase",
            "C. Tyrosinase",
            "D. Cystathionine beta-synthase",
        ],
        "correct_answer": "B. Phenylalanine hydroxylase",
        "explanation": (
            "Phenylketonuria (PKU) is caused by deficiency of phenylalanine hydroxylase (PAH), "
            "which converts phenylalanine to tyrosine. Accumulation of phenylalanine and its ketoacid "
            "metabolites causes the characteristic musty/mousy odour, intellectual disability, seizures, "
            "and eczema. Reduced tyrosine leads to decreased melanin synthesis, causing fair skin and hair "
            "(hypopigmentation). Homogentisate oxidase deficiency causes alkaptonuria (ochronosis, dark urine). "
            "Tyrosinase deficiency causes albinism. Cystathionine beta-synthase deficiency causes homocystinuria. "
            "Treatment: Low phenylalanine diet + tyrosine supplementation."
        ),
        "high_yield_takeaway": "PKU = Phenylalanine hydroxylase deficiency → musty odour, fair skin, intellectual disability. Treat with low-Phe diet.",
        "hashtags": ["#MedicoHelp", "#Biochemistry", "#MBBS", "#NEETPG", "#PKU"],
    },
    {
        "title": "Glycogen Storage Diseases — MCQ",
        "subject": Subject.biochemistry,
        "content_format": ContentFormat.mcq,
        "poster_text": "Von Gierke's = G6Pase deficiency → severe fasting hypoglycaemia + hepatomegaly",
        "caption": "MCQ: Glycogen storage disease identification",
        "question": (
            "A 3-year-old child presents with a markedly enlarged liver and severe hypoglycaemia during fasting. "
            "Lab investigations show lactic acidosis, hyperuricaemia, and hyperlipidaemia. "
            "Glucagon administration fails to raise blood glucose. "
            "A liver biopsy reveals excess glycogen and fat accumulation. "
            "Which enzyme is most likely deficient?"
        ),
        "options": [
            "A. Lysosomal acid alpha-glucosidase (acid maltase)",
            "B. Glucose-6-phosphatase",
            "C. Liver phosphorylase",
            "D. Muscle phosphofructokinase",
        ],
        "correct_answer": "B. Glucose-6-phosphatase",
        "explanation": (
            "This is Von Gierke disease (GSD Type Ia), caused by deficiency of Glucose-6-phosphatase (G6Pase). "
            "G6P cannot be converted to free glucose, so gluconeogenesis and glycogenolysis both fail to raise blood glucose — "
            "hence glucagon is ineffective. Accumulated G6P is shunted to lactate (lactic acidosis), triglycerides (hyperlipidaemia), "
            "and uric acid (hyperuricaemia). Hepatomegaly results from glycogen and fat accumulation. "
            "Pompe disease (Type II) = acid maltase deficiency → cardiomegaly, hypotonia. "
            "McArdle (Type V) = muscle phosphorylase deficiency → exercise intolerance, no rise in lactate with exercise."
        ),
        "high_yield_takeaway": "Von Gierke (GSD I) = G6Pase deficiency → fasting hypoglycaemia, hepatomegaly, lactic acidosis, glucagon unresponsive.",
        "hashtags": ["#MedicoHelp", "#Biochemistry", "#MBBS", "#NEETPG", "#GSD"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "Collagen Biosynthesis — Steps & Defects",
        "subject": Subject.biochemistry,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "Collagen synthesis: 8 steps, vitamin C essential — defect → scurvy or EDS",
        "caption": (
            "Collagen Biosynthesis — Concise Notes\n\n"
            "Most abundant protein in the body. Key amino acids: Gly-X-Y repeats (X = Pro, Y = Hydroxyproline/Hydroxylysine)\n\n"
            "Steps of Synthesis:\n"
            "1. Translation — preprocollagen (signal sequence) on RER ribosomes\n"
            "2. Hydroxylation of Pro & Lys — enzyme: Prolyl/Lysyl hydroxylase; cofactor: Vitamin C (ascorbic acid)\n"
            "   ↓ Vitamin C → underhydroxylated → unstable triple helix → SCURVY\n"
            "3. Glycosylation — glucose/galactose added to hydroxylysine\n"
            "4. Triple helix formation — 3 alpha chains wind into procollagen inside ER\n"
            "5. Secretion — procollagen exocytosed into extracellular space\n"
            "6. Cleavage — procollagen peptidase removes N- and C-terminal propeptides → tropocollagen\n"
            "   Defect → Dermatosparaxis type EDS\n"
            "7. Cross-linking — Lysyl oxidase (copper-dependent) oxidises Lys/HyLys → allysine → covalent cross-links\n"
            "   Defect → Menkes disease (Cu deficiency); also seen in lathyrism (beta-aminopropionitrile)\n"
            "8. Fibril formation — tropocollagen self-assembles\n\n"
            "Key Collagen Types:\n"
            "• Type I — bone, skin, tendon, most common\n"
            "• Type II — cartilage\n"
            "• Type III — blood vessels, healing wounds (first responder)\n"
            "• Type IV — basement membrane\n\n"
            "Osteogenesis Imperfecta: Type I collagen mutation (Gly substitution) → brittle bones, blue sclerae\n"
            "Ehlers-Danlos Syndrome: Various types → joint hypermobility, skin hyperextensibility"
        ),
        "high_yield_takeaway": "Vitamin C → hydroxylation of Pro/Lys. Lysyl oxidase (Cu) → cross-linking. Type III collagen is first in wound healing.",
        "hashtags": ["#MedicoHelp", "#Biochemistry", "#MBBS", "#NEETPG", "#Collagen"],
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "Enzyme Kinetics — PYQ Pattern",
        "subject": Subject.biochemistry,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Km, Vmax, competitive vs non-competitive — know the Lineweaver-Burk graph",
        "caption": (
            "Enzyme Kinetics — PYQ Concept (NEET-PG Repeated Pattern)\n\n"
            "Michaelis-Menten Equation: V = Vmax[S] / (Km + [S])\n\n"
            "Key Definitions:\n"
            "• Km (Michaelis constant): [S] at which V = Vmax/2\n"
            "  – Low Km → high affinity for substrate\n"
            "  – High Km → low affinity\n"
            "• Vmax: Maximum reaction velocity; proportional to enzyme concentration\n"
            "• Kcat (turnover number): reactions per enzyme per second\n\n"
            "Inhibition Types (Lineweaver-Burk / double-reciprocal plot: 1/V vs 1/[S]):\n\n"
            "Type                  Km        Vmax    Plot change\n"
            "──────────────────────────────────────────────────────\n"
            "Competitive           ↑ (app)   Same    X-intercept shifts left; Y-intercept same\n"
            "Non-competitive       Same      ↓       Y-intercept rises; X-intercept same\n"
            "Uncompetitive         ↓         ↓       Parallel lines (both intercepts shift)\n"
            "Mixed (uncompetitive) ↑ or ↓   ↓       Both intercepts shift\n\n"
            "Competitive inhibition is REVERSIBLE with excess substrate.\n"
            "Non-competitive inhibition is NOT overcome by substrate.\n\n"
            "Classic NEET-PG Questions:\n"
            "• Methotrexate inhibits DHFR competitively → ↑ Km, same Vmax\n"
            "• Allopurinol inhibits xanthine oxidase non-competitively (irreversible)\n"
            "• Aspirin inhibits COX irreversibly (suicide inhibitor)\n\n"
            "Allosteric enzymes: Sigmoidal kinetics (not Michaelis-Menten); regulated by effectors"
        ),
        "high_yield_takeaway": "Competitive inhibition → ↑Km, same Vmax. Non-competitive → same Km, ↓Vmax. Lineweaver-Burk: 1/V vs 1/[S].",
        "hashtags": ["#MedicoHelp", "#Biochemistry", "#MBBS", "#NEETPG", "#PYQ"],
    },
]
