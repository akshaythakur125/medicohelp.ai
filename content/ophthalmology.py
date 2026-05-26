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
            "• NVG complicates ischaemic CRVO (not CRAO usually)"
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
            "DEFINITION: Opacity of the crystalline lens or its capsule causing visual impairment\n\n"
            "TYPES BY LOCATION:\n"
            "• Nuclear cataract: Most common age-related; brown/brunescent; near vision preserved "
            "initially (index myopia — patient may discard reading glasses temporarily = 'second sight')\n"
            "• Cortical cataract: Spoke-like opacities; vacuoles and water clefts in cortex\n"
            "• Posterior subcapsular cataract (PSC): Most common with steroid use, diabetes, uveitis, "
            "radiation; disproportionate glare in bright light; worst symptom = reading difficulty\n"
            "• Anterior subcapsular cataract: Seen in atopic dermatitis (shield cataract)\n\n"
            "TYPES BY CAUSE:\n"
            "• Senile (age-related): Most common overall\n"
            "• Congenital: TORCH infections (rubella = 'pearly white' nuclear cataract — classic NEET image), "
            "galactosaemia (oil-droplet cataract), Down syndrome, Lowe syndrome\n"
            "• Traumatic: Rosette-shaped (blunt trauma); flower-shaped\n"
            "• Metabolic: Diabetes (snow-flake/snowstorm cataract in juveniles); "
            "hypocalcaemia (punctate iridescent opacities)\n"
            "• Drug-induced: Steroids (PSC), chlorpromazine (anterior capsule star-shaped), "
            "amiodarone (anterior capsule deposits), busulfan\n"
            "• Complicated cataract: Secondary to intraocular disease (uveitis, CRVO, high myopia)\n\n"
            "GRADING (LOCS III — Lens Opacity Classification System III):\n"
            "• Nuclear opalescence, nuclear colour, cortical opacity, PSC opacity — each graded 0.1–6\n\n"
            "SURGICAL MANAGEMENT:\n"
            "• Phacoemulsification (PHACO): Gold standard; small incision (2.8–3.2 mm); "
            "foldable IOL; rapid recovery; least induced astigmatism\n"
            "• SICS (Small Incision Cataract Surgery): 6–7 mm; rigid PMMA IOL; "
            "cost-effective; preferred in hard cataracts\n"
            "• ECCE (Extra-capsular): 10–11 mm incision; largely replaced by phaco\n"
            "• ICCE (Intra-capsular): Entire lens + capsule removed; no IOL in bag; "
            "historical; anterior chamber IOL only; now rarely performed\n\n"
            "IOL TYPES:\n"
            "• Monofocal: Standard; corrects distance only\n"
            "• Multifocal/EDOF: Distance + near; halos and glare possible\n"
            "• Toric: Corrects astigmatism\n\n"
            "COMPLICATIONS OF SURGERY:\n"
            "• Posterior capsule opacification (PCO): Most common late complication; "
            "'after-cataract'; treatment = Nd:YAG laser capsulotomy\n"
            "• Endophthalmitis: Most dreaded; organism = Staphylococcus epidermidis (most common)\n"
            "• Dropped nucleus: During PHACO — vitreoretinal surgeon required\n\n"
            "⚠️ Exam Traps:\n"
            "• Second sight = nuclear sclerosis causing index myopia (temporary improvement in near vision)\n"
            "• Steroid-induced cataract = PSC (posterior subcapsular)\n"
            "• Rubella cataract = pearly white nuclear; avoid surgery in acute phase (live virus in lens)"
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
            "WHY THIS IS REPEATEDLY ASKED:\n"
            "The distinction between optic neuritis and papilloedema is a perennial NEET PG/INI-CET "
            "question. Both cause disc swelling but differ critically in vision, pain, and laterality.\n\n"
            "OPTIC NEURITIS:\n"
            "• Definition: Inflammation of the optic nerve (demyelinating, infectious, or autoimmune)\n"
            "• Most common cause in young adults: Multiple sclerosis (MS) — 20–30% will develop MS; "
            "50% of MS patients will have optic neuritis\n"
            "• Laterality: Usually UNILATERAL\n"
            "• Vision: Subacute (hours to days) painful vision loss — dyschromatopsia (red desaturation)\n"
            "• Pain: Eye pain on eye movement (retrobulbar pain) — HALLMARK\n"
            "• RAPD: Present (positive Marcus Gunn pupil) in unilateral cases\n"
            "• Disc: Swollen in papillitis (anterior ON); normal-looking in retrobulbar neuritis "
            "(patient sees nothing, doctor sees nothing)\n"
            "• VEP: Prolonged P100 latency — most sensitive test for optic neuritis\n"
            "• MRI brain: White matter lesions (periventricular plaques) suggest MS\n"
            "• Treatment: IV methylprednisolone 1 g/day × 3 days (speeds recovery, does not improve "
            "final vision); most recover spontaneously\n\n"
            "PAPILLOEDEMA:\n"
            "• Definition: Optic disc swelling due to raised intracranial pressure (ICP)\n"
            "• Laterality: BILATERAL (almost always)\n"
            "• Vision: Initially PRESERVED (this is the key); transient visual obscurations (seconds) "
            "with posture change; late = chronic atrophy → permanent vision loss\n"
            "• Pain: Headache (ICP-related), no eye-movement pain\n"
            "• RAPD: ABSENT (because both eyes are equally affected)\n"
            "• Disc: Bilateral disc swelling; vessels obscured at disc margin; spontaneous venous "
            "pulsations absent\n"
            "• Causes: Brain tumour, pseudotumour cerebri (IIH), meningitis, hydrocephalus\n"
            "• Investigation: MRI brain/orbit, lumbar puncture (if MRI normal), CT head\n"
            "• Frisen grading of papilloedema: Grade 0 (normal) to Grade 5 (total disc obscuration)\n\n"
            "QUICK COMPARISON:\n"
            "• Vision at presentation: ON = reduced | Papilloedema = normal initially\n"
            "• Pain on eye movement: ON = yes | Papilloedema = no\n"
            "• Laterality: ON = unilateral | Papilloedema = bilateral\n"
            "• RAPD: ON = present | Papilloedema = absent\n"
            "• Colour vision: ON = severely affected | Papilloedema = relatively spared\n\n"
            "⚠️ PYQ Traps:\n"
            "• 'Patient sees nothing, doctor sees nothing' = retrobulbar neuritis (normal-looking disc)\n"
            "• IIH (pseudotumour cerebri): obese young women, headache, bilateral papilloedema, "
            "CSF pressure >25 cmH₂O, normal MRI — treat with acetazolamide + weight loss\n"
            "• Foster-Kennedy syndrome: Optic atrophy in one eye + papilloedema in other "
            "(frontal lobe tumour pressing on one optic nerve)"
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
]
