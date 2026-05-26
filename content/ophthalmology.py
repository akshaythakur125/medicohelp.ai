"""High-yield Ophthalmology content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ───────────────────────────────────────────────────────
    {
        "title": "Glaucoma — Open Angle vs Closed Angle Comparison",
        "subject": Subject.ophthalmology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "POAG = silent thief of sight | PACG = sudden painful red eye — know both",
        "caption": (
            "Glaucoma — Open Angle vs Closed Angle Rapid Revision\n\n"
            "PRIMARY OPEN ANGLE GLAUCOMA (POAG):\n"
            "• Most common type worldwide\n"
            "• Pathophysiology: Increased resistance to aqueous outflow at trabecular meshwork\n"
            "• Onset: Insidious, bilateral, asymptomatic initially\n"
            "• IOP: Usually elevated (>21 mmHg), but can be normal tension glaucoma (NTG)\n"
            "• Angle: OPEN on gonioscopy\n"
            "• Visual field loss: Arcuate scotoma → nasal step → tubular vision → blindness\n"
            "• Cup-to-disc (C:D) ratio: >0.6 (pathological), asymmetry >0.2 between eyes\n"
            "• Treatment: Prostaglandin analogues (latanoprost) — first-line; also beta-blockers "
            "(timolol), alpha-agonists (brimonidine), carbonic anhydrase inhibitors (dorzolamide)\n\n"
            "PRIMARY ANGLE CLOSURE GLAUCOMA (PACG):\n"
            "• More common in Asians, hypermetropes, women\n"
            "• Pathophysiology: Pupillary block → iris bombe → drainage angle closure\n"
            "• Acute attack: Sudden severe eye pain, headache, nausea/vomiting, coloured haloes, "
            "markedly elevated IOP (40–70 mmHg)\n"
            "• Signs: Conjunctival injection, steamy/hazy cornea, fixed mid-dilated pupil (4–6 mm), "
            "shallow anterior chamber\n"
            "• Angle: CLOSED on gonioscopy\n"
            "• Treatment (acute): IV acetazolamide + IV mannitol (hyperosmotic) + pilocarpine 2% "
            "(miotic) + topical beta-blocker; definitive = Laser peripheral iridotomy (LPI)\n\n"
            "GONIOSCOPY — ANGLE CLASSIFICATION (SHAFFER):\n"
            "• Grade IV: Wide open (35–45°)\n"
            "• Grade III: Open (25–35°)\n"
            "• Grade II: Moderately narrow (20°) — possible closure\n"
            "• Grade I: Very narrow (10°) — likely to close\n"
            "• Grade 0: Closed\n\n"
            "⚠️ Exam Traps:\n"
            "• Normal IOP: 10–21 mmHg (Goldmann applanation tonometry = gold standard)\n"
            "• Normal tension glaucoma: IOP normal but glaucomatous optic neuropathy — look for "
            "Flammer syndrome (cold hands, low BP, migraines)\n"
            "• Optic disc haemorrhage (Drance haemorrhage) = sign of active progression in NTG\n"
            "• Pilocarpine CONTRAINDICATED in open angle glaucoma crisis (pupil miosis reduces outflow)"
        ),
        "high_yield_takeaway": (
            "POAG: open angle, insidious, arcuate scotoma. PACG: closed angle, acute pain, fixed mid-dilated pupil. "
            "LPI is definitive for PACG."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Ophthalmology", "#Glaucoma"],
        "question": None,
        "options": [],
        "correct_answer": None,
        "explanation": None,
    },
    {
        "title": "Retinal Artery vs Vein Occlusion — Rapid Revision",
        "subject": Subject.ophthalmology,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "CRAO = cherry-red spot | CRVO = blood and thunder fundus — both cause sudden vision loss",
        "caption": (
            "Retinal Artery vs Vein Occlusion — Rapid Revision\n\n"
            "CENTRAL RETINAL ARTERY OCCLUSION (CRAO):\n"
            "• Aetiology: Thromboembolism (carotid artery plaque most common), giant cell arteritis\n"
            "• Presentation: Sudden, PAINLESS, profound vision loss (counting fingers or worse), "
            "RAPD (relative afferent pupillary defect) present\n"
            "• Fundus: Pale, whitish retina (ischaemic oedema) with CHERRY-RED SPOT at fovea "
            "(choroidal circulation preserved at fovea)\n"
            "• Arteries: Attenuated; 'cattle trucking' of blood column; box-carring\n"
            "• Window period: 90–120 minutes for treatment efficacy\n"
            "• Management (controversial, limited evidence): Ocular massage (dislodge embolus), "
            "IOP lowering (acetazolamide, paracentesis), hyperbaric oxygen, thrombolysis if within 4.5 h\n"
            "• Systemic workup: Carotid Doppler, echo, ECG (AF), lipid profile, ESR/CRP\n\n"
            "BRANCH RETINAL ARTERY OCCLUSION (BRAO):\n"
            "• Wedge-shaped area of retinal whitening along distribution of occluded branch\n"
            "• Altitudinal or sectoral visual field defect\n\n"
            "CENTRAL RETINAL VEIN OCCLUSION (CRVO):\n"
            "• Aetiology: Hypertension, diabetes, hyperviscosity, glaucoma, hypercoagulable states\n"
            "• Presentation: Sudden, PAINLESS vision loss (less severe than CRAO usually)\n"
            "• Fundus: 'Blood and thunder' — disc oedema, dilated tortuous veins, "
            "FLAME-SHAPED haemorrhages in ALL 4 quadrants, cotton wool spots\n"
            "• Types: Ischaemic (>10 disc areas of capillary non-perfusion, NVG risk) vs "
            "Non-ischaemic (better prognosis)\n"
            "• Complications: Neovascular glaucoma (NVG) — 100-day glaucoma or 3-month glaucoma\n"
            "• Management: Anti-VEGF (bevacizumab/ranibizumab) for macular oedema; "
            "laser (PRP) for neovascularisation; IOP control\n\n"
            "BRANCH RETINAL VEIN OCCLUSION (BRVO):\n"
            "• Haemorrhages confined to one quadrant (usually superotemporal)\n"
            "• Occurs at AV crossings (arteriovenous nipping)\n\n"
            "⚠️ Exam Traps:\n"
            "• Cherry-red spot = CRAO (but also seen in Tay-Sachs, Niemann-Pick, Gaucher's disease)\n"
            "• RAPD (Marcus Gunn pupil) is present in CRAO but NOT typically in CRVO\n"
            "• NVG complicates ischaemic CRVO (not CRAO)"
        ),
        "high_yield_takeaway": (
            "CRAO: cherry-red spot + RAPD + cattle-trucking arteries. CRVO: blood-and-thunder fundus + NVG at 3 months. "
            "Both cause sudden painless vision loss."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Ophthalmology", "#RetinalOcclusion"],
        "question": None,
        "options": [],
        "correct_answer": None,
        "explanation": None,
    },
    # ── MCQ ──────────────────────────────────────────────────────────────────
    {
        "title": "Diabetic Retinopathy Staging — MCQ",
        "subject": Subject.ophthalmology,
        "content_format": ContentFormat.mcq,
        "poster_text": "Diabetic retinopathy staging: NPDR vs PDR — when to treat is the key exam question",
        "caption": (
            "MCQ: Diabetic Retinopathy Staging\n\n"
            "A 52-year-old man with type 2 diabetes of 14 years duration presents for routine eye check. "
            "He has no visual symptoms. On fundus examination: multiple dot and blot haemorrhages in all 4 "
            "quadrants, hard exudates near the macula, and 4 areas of intraretinal microvascular "
            "abnormalities (IRMA). Optical coherence tomography (OCT) shows subfoveal fluid with central "
            "macular thickness of 320 μm. Visual acuity is 6/18 in the right eye. What is the CORRECT "
            "classification and most appropriate initial management?"
        ),
        "question": (
            "A 52-year-old diabetic man has dot-blot haemorrhages in all 4 quadrants, hard exudates, "
            "IRMA, and OCT-confirmed diabetic macular oedema (DMO) with VA 6/18. What is the CORRECT "
            "classification and management?"
        ),
        "options": [
            "A. Mild NPDR with DMO — start laser photocoagulation (focal/grid)",
            "B. Severe NPDR with centre-involving DMO — intravitreal anti-VEGF is first-line",
            "C. Proliferative DR (PDR) with DMO — urgent panretinal photocoagulation (PRP)",
            "D. Moderate NPDR with DMO — observe for 3 months and recheck",
        ],
        "correct_answer": "B. Severe NPDR with centre-involving DMO — intravitreal anti-VEGF is first-line",
        "explanation": (
            "The International Clinical DR Severity Scale classifies this as Severe NPDR — the 4-2-1 rule: "
            "≥20 dot/blot haemorrhages in all 4 quadrants, OR venous beading in ≥2 quadrants, OR IRMA in ≥1 "
            "quadrant. The absence of neovascularisation (NVE or NVD) excludes PDR. The OCT finding of "
            "subfoveal fluid with central macular thickness >250 μm with VA 6/18 confirms centre-involving "
            "clinically significant DMO (CI-DMO). Current NICE/AAO guidelines recommend intravitreal "
            "anti-VEGF agents (ranibizumab, bevacizumab, aflibercept) as first-line for CI-DMO, as they are "
            "superior to laser. Laser (focal/grid) is now second-line. PRP is indicated for PDR. "
            "Observation alone (Option D) is inappropriate when there is centre-involving DMO with vision loss."
        ),
        "high_yield_takeaway": (
            "Severe NPDR = 4-2-1 rule. CI-DMO with VA loss: anti-VEGF is 1st line, laser is 2nd line. "
            "PRP for PDR. No NVE/NVD = not yet PDR."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Ophthalmology", "#DiabeticRetinopathy"],
    },
    {
        "title": "Red Eye Differential Diagnosis — MCQ",
        "subject": Subject.ophthalmology,
        "content_format": ContentFormat.mcq,
        "poster_text": "Red eye: Vision loss + pain = emergency | No pain + discharge = infection",
        "caption": (
            "MCQ: Red Eye Differential Diagnosis\n\n"
            "A 35-year-old contact lens wearer presents with a 2-day history of severe left eye pain, "
            "photophobia, and watering. Vision in the affected eye is 6/36 (reduced from 6/6). Slit-lamp "
            "examination shows conjunctival and ciliary injection, a 3 mm white corneal ulcer with "
            "surrounding stromal oedema, and a 1 mm hypopyon. Fluorescein staining confirms epithelial "
            "defect over the ulcer. What is the MOST likely diagnosis?"
        ),
        "question": (
            "A 35-year-old contact lens wearer presents with severe eye pain, photophobia, reduced vision "
            "to 6/36, ciliary injection, a white corneal ulcer with hypopyon, and a positive fluorescein "
            "stain. What is the MOST likely diagnosis?"
        ),
        "options": [
            "A. Viral (herpetic) keratitis — start oral acyclovir",
            "B. Bacterial keratitis — start intensive topical antibiotics (fluoroquinolones)",
            "C. Allergic keratoconjunctivitis — start topical antihistamines",
            "D. Acute angle closure glaucoma — start IV acetazolamide",
        ],
        "correct_answer": "B. Bacterial keratitis — start intensive topical antibiotics (fluoroquinolones)",
        "explanation": (
            "The combination of contact lens use, a white stromal infiltrate with overlying epithelial defect "
            "on fluorescein staining, hypopyon, and significant vision reduction is classic for bacterial "
            "keratitis (microbial keratitis). The most common organisms in contact lens-related keratitis are "
            "Pseudomonas aeruginosa and Staphylococcus aureus. Management: corneal scrape for Gram stain "
            "and culture, then intensive topical fluoroquinolones (ciprofloxacin 0.3% or moxifloxacin hourly "
            "for the first 24–48 hours). Herpetic keratitis (Option A) typically shows dendritic ulcer "
            "(branching pattern) with terminal bulbs, reduced corneal sensation, and recurrent episodes. "
            "Allergic keratoconjunctivitis (Option C) has no ulcer, no hypopyon, and bilateral itch. "
            "Acute angle closure (Option D) shows a hazy cornea, fixed mid-dilated pupil, rock-hard eye, "
            "and no ulcer."
        ),
        "high_yield_takeaway": (
            "Corneal ulcer + hypopyon + contact lens use = bacterial keratitis. Scrape for culture, then hourly topical fluoroquinolones."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Ophthalmology", "#RedEye"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "Cataract: Types, Features and Management",
        "subject": Subject.ophthalmology,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "Cataract: Most common cause of blindness in India — types and surgery explained",
        "caption": (
            "Cataract — Concise Notes\n\n"
            "DEFINITION: Opacity of the crystalline lens causing visual impairment\n\n"
            "TYPES BY LOCATION:\n"
            "• Nuclear: Most common age-related; brown/brunescent; 'second sight' (index myopia)\n"
            "• Cortical: Spoke-like opacities; vacuoles and water clefts\n"
            "• PSC (posterior subcapsular): Steroids, diabetes, uveitis; worst for reading/glare\n"
            "• Anterior subcapsular: Atopic dermatitis (shield cataract)\n\n"
            "TYPES BY CAUSE:\n"
            "• Senile: Most common overall\n"
            "• Congenital: Rubella (pearly white nuclear), galactosaemia (oil-droplet), Lowe syndrome\n"
            "• Traumatic: Rosette-shaped (blunt trauma)\n"
            "• Metabolic: Diabetes (snowflake cataract in juveniles); hypocalcaemia (punctate)\n"
            "• Drug-induced: Steroids → PSC; chlorpromazine → anterior capsule star-shaped\n"
            "• Complicated: Secondary to uveitis, CRVO, high myopia\n\n"
            "SURGICAL OPTIONS:\n"
            "• Phacoemulsification (PHACO): Gold standard; 2.8–3.2 mm incision; foldable IOL\n"
            "• SICS: 6–7 mm; cost-effective; preferred for hard cataracts\n"
            "• ECCE: 10–11 mm; largely replaced by PHACO\n"
            "• ICCE: Entire lens + capsule; historical; rarely done now\n\n"
            "COMPLICATIONS:\n"
            "• PCO (after-cataract): Most common late complication → Nd:YAG laser capsulotomy\n"
            "• Endophthalmitis: Most dreaded; S. epidermidis most common organism\n\n"
            "⚠️ Exam Traps:\n"
            "• Second sight = nuclear sclerosis → index myopia (temporary near vision improvement)\n"
            "• Steroid cataract = PSC\n"
            "• Rubella cataract = pearly white nuclear; avoid surgery in acute phase (live virus)"
        ),
        "high_yield_takeaway": (
            "PSC = steroids/diabetes; worst for reading. Rubella = nuclear. Phaco = gold standard. "
            "PCO (after-cataract) = Nd:YAG laser capsulotomy."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Ophthalmology", "#Cataract"],
        "question": None,
        "options": [],
        "correct_answer": None,
        "explanation": None,
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "Optic Neuritis vs Papilloedema — PYQ Pattern",
        "subject": Subject.ophthalmology,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Optic neuritis: pain on movement + RAPD | Papilloedema: bilateral + no RAPD — classic PYQ",
        "caption": (
            "Optic Neuritis vs Papilloedema — PYQ Concept\n\n"
            "Both cause disc swelling — differentiation is a perennial NEET PG/INI-CET question.\n\n"
            "OPTIC NEURITIS:\n"
            "• Most common cause in young adults: Multiple sclerosis (20–30% develop MS)\n"
            "• Laterality: Usually UNILATERAL\n"
            "• Vision: Subacute painful vision loss; dyschromatopsia (red desaturation)\n"
            "• Pain: Eye pain on eye movement — HALLMARK\n"
            "• RAPD: Present (Marcus Gunn pupil)\n"
            "• Disc: Swollen in papillitis; NORMAL in retrobulbar neuritis\n"
            "  ('Patient sees nothing, doctor sees nothing')\n"
            "• VEP: Prolonged P100 latency — most sensitive test\n"
            "• Treatment: IV methylprednisolone 1 g/day × 3 days (speeds recovery)\n\n"
            "PAPILLOEDEMA:\n"
            "• Definition: Disc swelling due to raised ICP\n"
            "• Laterality: BILATERAL (almost always)\n"
            "• Vision: Initially PRESERVED; transient visual obscurations; late → atrophy\n"
            "• Pain: Headache; NO eye-movement pain\n"
            "• RAPD: ABSENT\n"
            "• Causes: Brain tumour, IIH, meningitis, hydrocephalus\n"
            "• Frisen grading: Grade 0 (normal) to Grade 5 (total disc obscuration)\n\n"
            "QUICK COMPARISON:\n"
            "• Vision: ON = reduced | Papilloedema = normal initially\n"
            "• Pain on eye movement: ON = yes | Papilloedema = no\n"
            "• Laterality: ON = unilateral | Papilloedema = bilateral\n"
            "• RAPD: ON = present | Papilloedema = absent\n\n"
            "⚠️ PYQ Traps:\n"
            "• IIH: Obese young women; CSF >25 cmH₂O; normal MRI; acetazolamide + weight loss\n"
            "• Foster-Kennedy: Atrophy one eye + papilloedema other (frontal lobe tumour)"
        ),
        "high_yield_takeaway": (
            "Optic neuritis: unilateral + RAPD + pain on eye movement + reduced vision. "
            "Papilloedema: bilateral + no RAPD + vision initially normal. VEP = best test for ON."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Ophthalmology", "#OpticNeuritis"],
        "question": None,
        "options": [],
        "correct_answer": None,
        "explanation": None,
    },
    # ── Mnemonic ──────────────────────────────────────────────────────────────
    {
        "title": "Mnemonic: Extraocular Muscles — LR6 SO4 rest by O3",
        "subject": Subject.ophthalmology,
        "content_format": ContentFormat.mnemonic,
        "poster_text": "Mnemonic: LR6 SO4 — Lateral Rectus (CN VI), Superior Oblique (CN IV), rest by Oculomotor (CN III)",
        "caption": (
            "Extraocular muscles innervation mnemonic: LR6 (Lateral Rectus = Abducens / CN VI). "
            "SO4 (Superior Oblique = Trochlear / CN IV). "
            "Rest = Oculomotor / CN III (Medial Rectus, Inferior Rectus, Superior Rectus, Inferior Oblique). "
            "Also explain actions of each muscle: SR (elevation + adduction + intorsion), "
            "IR (depression + adduction + extorsion), MR (adduction), LR (abduction), "
            "SO (depression + abduction + intorsion — \"SO\" = \"SOnk down, turn in\"), "
            "IO (elevation + abduction + extorsion). "
            "Three axes of Fick: X (horizontal), Y (vertical), Z (anteroposterior)."
        ),
        "high_yield_takeaway": (
            "LR6 SO4 rest O3. SO: 'SO turns the eye down and out.' "
            "IO: 'I O-u-t-turn the eye up and out.' Test: H-pattern of gaze for each muscle."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Ophthalmology", "#Mnemonic", "#ExtraocularMuscles"],
        "question": None,
        "options": [],
        "correct_answer": None,
        "explanation": None,
    },
    # ── Flashcard ─────────────────────────────────────────────────────────────
    {
        "title": "Flashcard: Conjunctivitis — Bacterial vs Viral vs Allergic Comparison",
        "subject": Subject.ophthalmology,
        "content_format": ContentFormat.flashcard,
        "poster_text": "Conjunctivitis: Bacterial = purulent, sticky | Viral = watery, pre-auricular node | Allergic = itchy, bilateral",
        "caption": (
            "Compare types of conjunctivitis. "
            "Bacterial: mucopurulent discharge, sticky eyelids, no pre-auricular lymphadenopathy, "
            "responds to topical antibiotics (chloramphenicol, moxifloxacin). "
            "Viral: watery discharge, pre-auricular lymphadenopathy, follicular reaction on tarsal conjunctiva, "
            "contagious (adenovirus most common), no specific treatment. "
            "Allergic: intense itching, bilateral, cobblestone papillae, gelatinous limbal infiltration "
            "(in vernal catarrh), treatment = antihistamines + mast cell stabilisers. "
            "Ophthalmia neonatorum: chemical (silver nitrate) vs gonococcal (hyperacute, copious pus, "
            "corneal perforation risk) vs chlamydial (inclusion conjunctivitis, subacute). "
            "Neonatal prophylaxis: erythromycin ointment."
        ),
        "question": (
            "A 5-year-old child presents with itchy, bilateral red eyes, cobblestone papillae on the "
            "upper tarsal conjunctiva, and a history of asthma. What is the diagnosis and first-line treatment?"
        ),
        "correct_answer": (
            "Vernal keratoconjunctivitis (allergic). "
            "First-line: topical mast cell stabilisers (sodium cromoglycate) + antihistamines. "
            "Topical steroids for severe exacerbations."
        ),
        "high_yield_takeaway": (
            "Bacterial = purulent, antibiotics. Viral = watery, follicular, self-limiting. "
            "Allergic = itchy, cobblestone papillae. Neonatal = prophylaxis with erythromycin."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Ophthalmology", "#Flashcard", "#Conjunctivitis"],
        "options": [],
        "explanation": None,
    },
    # ── True/False ────────────────────────────────────────────────────────────
    {
        "title": "True or False: LASIK can correct all types and degrees of refractive error",
        "subject": Subject.ophthalmology,
        "content_format": ContentFormat.true_false,
        "poster_text": "LASIK: only for myopia up to -8D, hypermetropia up to +4D, astigmatism up to 5D — not for presbyopia",
        "caption": (
            "LASIK (Laser-Assisted In Situ Keratomileusis) indications: stable refraction for ≥1 year, "
            "age ≥18-21, no corneal pathology (keratoconus contraindicated), adequate corneal thickness "
            "(≥500 microns). Contraindications: thin cornea, keratoconus, severe dry eye, pregnancy, "
            "autoimmune disease, uncontrolled glaucoma/diabetes. LASIK does NOT correct presbyopia "
            "(monovision LASIK can be attempted). Alternatives: PRK (thin cornea, athletes), "
            "SMILE (minimally invasive), ICL (high myopia >-8D), RLE (presbyopia + cataract). "
            "Complications: dry eye (most common), flap complications, ectasia, under/overcorrection, "
            "haloes/glare."
        ),
        "question": "LASIK surgery can correct all types and degrees of refractive error, including presbyopia.",
        "correct_answer": "FALSE",
        "explanation": (
            "LASIK is effective for myopia (up to -8D), hypermetropia (up to +4D), and astigmatism "
            "(up to 5D) but does NOT correct presbyopia (age-related loss of accommodation). "
            "Monovision (one eye for distance, other for near) is a compromise option. "
            "High myopia >-8D needs ICL. Thin cornea contraindicates LASIK (PRK or SMILE preferred)."
        ),
        "high_yield_takeaway": (
            "LASIK: myopia ≤8D, hypermetropia ≤4D, astigmatism ≤5D. NOT for presbyopia. "
            "Contraindicated in keratoconus, thin cornea, dry eye. SMILE for small incision, PRK for thin cornea."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Ophthalmology", "#TrueFalse", "#LASIK"],
        "options": [],
    },
    # ── One-liner Recall ──────────────────────────────────────────────────────
    {
        "title": "One-liner Recall: Snellen Visual Acuity — '20/40' Meaning",
        "subject": Subject.ophthalmology,
        "content_format": ContentFormat.one_liner_recall,
        "poster_text": "Snellen acuity: 20/20 = normal. 20/40 = sees at 20 ft what normal sees at 40 ft. 20/200 = legal blindness.",
        "caption": (
            "Fill in the blank: \"A patient with Snellen visual acuity of 20/40 can read at 20 feet what "
            "a person with normal vision can read at ___ feet.\" Answer: \"40 feet.\" "
            "Then explain Snellen fraction: numerator = testing distance (20 ft = 6 m), denominator = "
            "distance at which the smallest optotype subtends 5 minutes of arc. "
            "20/20 = normal. 20/40 = 2x larger letters needed. "
            "20/200 = legal blindness in USA (Snellen equivalent in India: <6/60 or <20/200 or field <20°). "
            "Counting fingers (CF), Hand movements (HM), Perception of Light (PL), "
            "No Perception of Light (NPL) for worse vision. "
            "Landolt C and E-chart for illiterate patients."
        ),
        "question": (
            "A patient with Snellen visual acuity of 20/40 can read at 20 feet what a person with "
            "normal vision can read at ___ feet."
        ),
        "correct_answer": "40 feet",
        "high_yield_takeaway": (
            "Snellen: numerator = testing distance, denominator = normal vision distance. "
            "20/20 = normal. 20/200 = legal blindness. "
            "CF, HM, PL, NPL for severe vision loss. Pinhole improvement = refractive error (not organic disease)."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Ophthalmology", "#OneLiner", "#Snellen"],
        "options": [],
        "explanation": None,
    },
]
