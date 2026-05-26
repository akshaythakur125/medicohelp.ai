"""High-yield ENT content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ───────────────────────────────────────────────────────
    {
        "title": "Tuning Fork Tests — Rinne, Weber, Schwabach",
        "subject": Subject.ent,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Tuning fork tests: Rinne + Weber + Schwabach — master all three for NEET PG",
        "caption": (
            "Tuning Fork Tests — Rapid Revision\n\n"
            "STANDARD TUNING FORK: 512 Hz (used for most clinical tests)\n"
            "• Lower frequencies (128, 256 Hz) have too much vibration sensation\n"
            "• Higher frequencies (1024 Hz) are less sensitive for conductive loss\n\n"
            "1. RINNE TEST:\n"
            "• Compares air conduction (AC) vs bone conduction (BC) in the SAME ear\n"
            "• Method: Place vibrating fork on mastoid (BC), then hold 1 cm from ear (AC)\n"
            "• Rinne Positive (AC > BC): NORMAL or Sensorineural Hearing Loss (SNHL)\n"
            "• Rinne Negative (BC > AC): Conductive Hearing Loss (CHL) of ≥25 dB\n"
            "• False Negative Rinne: Dead/anacusic ear — sound 'heard' via contralateral cochlea "
            "(bone conduction crosses skull); masking of the good ear is mandatory in this case\n\n"
            "2. WEBER TEST:\n"
            "• Compares bone conduction between BOTH ears simultaneously\n"
            "• Method: Vibrating fork placed on vertex/forehead midline\n"
            "• Normal (no hearing loss): Sound heard in the midline\n"
            "• Lateralises to AFFECTED (WORSE) ear: Conductive Hearing Loss\n"
            "  (Reason: background noise not conducted in CHL → perceived BC is better)\n"
            "• Lateralises to BETTER (UNAFFECTED) ear: Sensorineural Hearing Loss\n\n"
            "3. SCHWABACH TEST:\n"
            "• Compares patient's bone conduction to examiner's (assumed normal)\n"
            "• Schwabach Prolonged (patient hears longer): Conductive Hearing Loss\n"
            "• Schwabach Diminished (patient hears shorter): Sensorineural Hearing Loss\n"
            "• Schwabach Normal: No hearing loss\n\n"
            "SUMMARY TABLE:\n"
            "• Normal hearing: Rinne +ve | Weber central | Schwabach normal\n"
            "• Conductive HL: Rinne -ve | Weber → affected ear | Schwabach prolonged\n"
            "• Sensorineural HL: Rinne +ve | Weber → better ear | Schwabach diminished\n\n"
            "⚠️ Exam Traps:\n"
            "• Tuning fork of 512 Hz is STANDARD for clinical tests\n"
            "• False -ve Rinne in dead ear = do not miss (always mask the good ear)\n"
            "• Absolute Bone Conduction (ABC) test: compares BC of patient vs examiner directly\n"
            "  (same principle as Schwabach but more formal)"
        ),
        "high_yield_takeaway": (
            "CHL: Rinne -ve, Weber to bad ear, Schwabach prolonged. SNHL: Rinne +ve, Weber to good ear, "
            "Schwabach diminished. Use 512 Hz fork."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ENT", "#HearingLoss"],
        "question": None,
        "options": [],
        "correct_answer": None,
        "explanation": None,
    },
    {
        "title": "Types of Hearing Loss — Rapid Revision",
        "subject": Subject.ent,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Conductive vs Sensorineural vs Mixed hearing loss — causes and audiogram patterns",
        "caption": (
            "Types of Hearing Loss — Rapid Revision\n\n"
            "CONDUCTIVE HEARING LOSS (CHL):\n"
            "• Air-bone gap ≥15 dB; BC normal, AC reduced; maximum CHL ~60 dB\n\n"
            "Causes:\n"
            "• External ear: Wax impaction (most common overall), otitis externa, foreign body, atresia\n"
            "• Middle ear: OME/glue ear (most common in children), CSOM, TM perforation,\n"
            "  otosclerosis (most common progressive CHL in young adults), cholesteatoma\n\n"
            "SENSORINEURAL HEARING LOSS (SNHL):\n"
            "• No air-bone gap; AC = BC (both equally reduced)\n\n"
            "Causes:\n"
            "• Presbycusis: Most common bilateral SNHL; high-frequency loss first; elderly\n"
            "• NIHL: Notch at 4000 Hz on audiogram (noise-induced)\n"
            "• Meniere's disease: Fluctuating low-freq SNHL + vertigo + tinnitus + aural fullness\n"
            "• Ototoxic drugs: Aminoglycosides, cisplatin, loop diuretics (furosemide)\n"
            "• Acoustic neuroma: Unilateral SNHL + tinnitus; CP angle tumour\n\n"
            "MIXED HEARING LOSS:\n"
            "• AC and BC both reduced; air-bone gap still present\n"
            "• Causes: CSOM with cochlear involvement, otosclerosis\n\n"
            "AUDIOLOGICAL INVESTIGATIONS:\n"
            "• PTA: Gold standard for type and degree of HL\n"
            "• Tympanometry: Type A = normal; Type B = flat (OME/perforation);\n"
            "  Type As = stiff (otosclerosis); Type Ad = deep (ossicular discontinuity); Type C = ETD\n"
            "• BERA/ABR: Objective; used in infants, medico-legal, acoustic neuroma\n\n"
            "⚠️ Exam Traps:\n"
            "• Otosclerosis: AD inheritance; Schwartze sign (flamingo pink blush through TM)\n"
            "• NIHL: C5 dip at 4000 Hz on audiogram\n"
            "• Presbycusis: Bilateral, symmetrical, high-frequency SNHL; sensory type"
        ),
        "high_yield_takeaway": (
            "CHL: air-bone gap present. SNHL: no air-bone gap. Tympanogram B = OME. NIHL = notch at 4000 Hz. "
            "Otosclerosis = As pattern."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ENT", "#HearingLoss"],
        "question": None,
        "options": [],
        "correct_answer": None,
        "explanation": None,
    },
    # ── MCQ ──────────────────────────────────────────────────────────────────
    {
        "title": "Acute Otitis Media — MCQ",
        "subject": Subject.ent,
        "content_format": ContentFormat.mcq,
        "poster_text": "Acute otitis media in children: Amoxicillin is 1st line — know when to treat",
        "caption": (
            "MCQ: Acute Otitis Media\n\n"
            "A 3-year-old boy presents with fever (38.5°C) and severe left ear pain for 2 days. "
            "He has been pulling at his left ear. Otoscopy shows a bulging, erythematous, opaque "
            "tympanic membrane with loss of light reflex. He had a similar episode 4 months ago treated "
            "with antibiotics. His parents ask about current treatment. He is otherwise well and has no "
            "penicillin allergy. What is the MOST appropriate management?\n\n"
            "A. Watchful waiting for 48–72 hours with analgesia only, as most AOM resolves spontaneously\n"
            "B. Amoxicillin 80–90 mg/kg/day orally for 10 days\n"
            "C. Amoxicillin 40 mg/kg/day orally for 5 days\n"
            "D. Immediate myringotomy and insertion of grommets (ventilation tubes)"
        ),
        "question": (
            "A 3-year-old boy with fever, ear pain, and a bulging erythematous opaque tympanic membrane "
            "has a history of AOM 4 months ago. No penicillin allergy. What is the MOST appropriate management?"
        ),
        "options": [
            "A. Watchful waiting for 48–72 hours with analgesia only",
            "B. Amoxicillin 80–90 mg/kg/day orally for 10 days",
            "C. Amoxicillin 40 mg/kg/day orally for 5 days",
            "D. Immediate myringotomy and insertion of grommets",
        ],
        "correct_answer": "B. Amoxicillin 80–90 mg/kg/day orally for 10 days",
        "explanation": (
            "According to AAP/NICE guidelines, AOM in a child aged ≥6 months with severe symptoms "
            "(moderate-severe ear pain, fever ≥39°C, or bilateral AOM) mandates immediate antibiotic therapy — "
            "watchful waiting is not appropriate here. The recommended first-line antibiotic is amoxicillin "
            "at the HIGH dose of 80–90 mg/kg/day (in 2–3 divided doses) to overcome penicillin-non-susceptible "
            "Streptococcus pneumoniae, which is the most common bacterial pathogen. Standard dose (40 mg/kg/day) "
            "is only for mild cases in children ≥2 years. Duration: 10 days for children <2 years or with severe "
            "disease; 5–7 days may suffice for children ≥2 years with mild-moderate disease. "
            "Option A (watchful waiting) would be appropriate only for mild AOM in a child >2 years with no "
            "severe symptoms and reliable follow-up. Option D (grommets) is indicated for recurrent AOM "
            "(≥3 episodes in 6 months or ≥4 in 12 months) or chronic OME with hearing loss, not acute disease."
        ),
        "high_yield_takeaway": (
            "AOM 1st line: Amoxicillin 80–90 mg/kg/day (high dose) for 10 days. Grommets for recurrent AOM (≥3 in 6 months). "
            "Most common pathogen = S. pneumoniae."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ENT", "#OtitisMedia"],
    },
    {
        "title": "Epistaxis Management — MCQ",
        "subject": Subject.ent,
        "content_format": ContentFormat.mcq,
        "poster_text": "Epistaxis: Little's area bleeds — Kiesselbach's plexus is the key anatomy",
        "caption": (
            "MCQ: Epistaxis Management\n\n"
            "A 68-year-old hypertensive man on aspirin presents to the emergency department with profuse "
            "left-sided nosebleed for 30 minutes. He has had multiple episodes this year. On examination, "
            "BP is 170/100 mmHg. Direct pressure for 15 minutes and application of a topical vasoconstrictor "
            "(xylometazoline) have failed to control the bleeding. Anterior rhinoscopy does not reveal a clear "
            "bleeding point. He is haemodynamically stable. What is the MOST appropriate next step?"
        ),
        "question": (
            "A 68-year-old hypertensive man on aspirin has profuse nosebleed for 30 minutes. Pressure and "
            "topical vasoconstrictor have failed. No visible bleeding point on anterior rhinoscopy. BP is "
            "170/100, haemodynamically stable. What is the MOST appropriate next step?"
        ),
        "options": [
            "A. Anterior nasal packing with BIPP or Merocel",
            "B. Emergency external carotid artery ligation",
            "C. Posterior nasal packing (Foley catheter or Brighton balloon)",
            "D. Endoscopic sphenopalatine artery ligation",
        ],
        "correct_answer": "A. Anterior nasal packing with BIPP or Merocel",
        "explanation": (
            "The stepwise approach to epistaxis is: (1) First aid — pinch nose (soft part) for 15–20 minutes "
            "leaning forward, topical vasoconstrictor; (2) Cauterisation of visible bleeding point (silver "
            "nitrate or electrocautery); (3) Anterior nasal packing (Merocel, BIPP, or Rapid Rhino) if no "
            "visible point or cauterisation fails; (4) Posterior packing (Foley catheter balloon or Brighton "
            "balloon) if anterior packing fails — indicates posterior/nasopharyngeal bleed; "
            "(5) Endoscopic sphenopalatine artery (SPA) ligation or embolisation for refractory cases. "
            "In this case, the next step after failed first-line measures is anterior packing (Option A). "
            "Posterior packing (Option C) would be the step after anterior packing fails and if bleeding is "
            "posterior. External carotid ligation (Option B) and SPA ligation (Option D) are reserved for "
            "failure of packing or endoscopic approaches. Note: Kiesselbach's plexus (Little's area) on the "
            "anterior nasal septum is the site of 90% of epistaxis cases."
        ),
        "high_yield_takeaway": (
            "Epistaxis steps: pressure → cauterise → anterior pack → posterior pack → SPA ligation. "
            "90% from Kiesselbach's plexus (Little's area). Most common cause = trauma/nose picking."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ENT", "#Epistaxis"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "Cholesteatoma: Features and Complications",
        "subject": Subject.ent,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "Cholesteatoma: 'skin in the wrong place' — the CSOM type that destroys bone",
        "caption": (
            "Cholesteatoma — Concise Notes\n\n"
            "DEFINITION: Cyst lined by keratinising squamous epithelium with keratin debris in middle "
            "ear/mastoid. NOT a true tumour.\n\n"
            "TYPES:\n"
            "• Congenital: Behind intact TM; white pearly mass; anterosuperior quadrant; children\n"
            "• Acquired Primary: Pars flaccida (Shrapnell's) retraction → inward squamous migration\n"
            "• Acquired Secondary: Through pre-existing marginal TM perforation\n\n"
            "CLINICAL FEATURES:\n"
            "• Foul-smelling scanty non-pulsatile discharge — classic\n"
            "• Conductive hearing loss (ossicular erosion — long process of incus first)\n"
            "• Attic perforation with pearly white mass and crusting\n\n"
            "INVESTIGATIONS:\n"
            "• HRCT temporal bone: Investigation of choice — bony erosion, location, extent\n"
            "• Audiogram: Conductive HL (mixed if cochlea involved)\n\n"
            "COMPLICATIONS:\n"
            "• Local: Facial nerve palsy (horizontal segment), labyrinthine fistula (lateral SCC — "
            "positive fistula sign), tympanosclerosis\n"
            "• Extracranial: Bezold's abscess (neck); Gradenigo's syndrome "
            "(otorrhoea + retro-orbital pain + 6th nerve palsy)\n"
            "• Intracranial: Meningitis (most common) → extradural/subdural abscess → "
            "sigmoid sinus thrombophlebitis → brain abscess\n\n"
            "MANAGEMENT (Surgery mandatory):\n"
            "• Canal wall down (radical mastoidectomy): Better clearance; lifelong cavity care\n"
            "• Canal wall up (CAT): Better hearing; higher recurrence; second-look at 12 months\n\n"
            "⚠️ Exam Traps:\n"
            "• Attic perforation + foul discharge = cholesteatoma until proven otherwise\n"
            "• Long process of incus = first ossicle eroded\n"
            "• Positive fistula sign = lateral SCC erosion"
        ),
        "high_yield_takeaway": (
            "Cholesteatoma: attic perforation + foul discharge + bony erosion. CT temporal bone = best investigation. "
            "Long process of incus erodes first. Surgery mandatory."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ENT", "#Cholesteatoma"],
        "question": None,
        "options": [],
        "correct_answer": None,
        "explanation": None,
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "Foreign Bodies in ENT — PYQ Pattern",
        "subject": Subject.ent,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Foreign bodies in ENT: Ear, nose, throat, airway — site-specific management for NEET PG",
        "caption": (
            "Foreign Bodies in ENT — PYQ Concept\n\n"
            "Coin FB in oesophagus is the single most repeated NEET PG topic in this category.\n\n"
            "FB EAR:\n"
            "• Live insects: Kill with oil/spirit FIRST, then remove\n"
            "• Vegetable/hygroscopic FBs: DO NOT irrigate — swells and impacts\n"
            "• Smooth round objects: Use hook/curet; NOT forceps (pushes FB in)\n"
            "• Difficult FB in children: GA required\n\n"
            "FB NOSE:\n"
            "• Classic: Unilateral foul-smelling discharge in child = FB until proven otherwise\n"
            "• Mother's kiss: Occlude unaffected nostril, blow into child's mouth — first-line\n"
            "• Button battery: EMERGENCY — remove immediately (liquefactive necrosis)\n\n"
            "FB OESOPHAGUS:\n"
            "• Most common: Coins (children), fish/chicken bones (adults)\n"
            "• Most common site: Cricopharyngeal sphincter (C5–C6)\n"
            "• Coin in oesophagus: FACE on (coronal) on AP X-ray\n"
            "• Coin in trachea: EDGE on (sagittal) on AP X-ray\n"
            "• Management: Oesophagoscopy under GA\n\n"
            "FB AIRWAY (Bronchus):\n"
            "• Most common aspirated FB in India: Peanuts (chemical bronchitis)\n"
            "• Most common site: RIGHT main bronchus (wider, shorter, more vertical)\n"
            "• X-ray: Unilateral obstructive emphysema; mediastinal shift AWAY from FB side\n"
            "• Management: Rigid bronchoscopy under GA (investigation + treatment of choice)\n"
            "• Choking adult/child >1 yr: Heimlich manoeuvre\n"
            "• Infant <1 yr: 5 back blows + 5 chest thrusts (NOT Heimlich)\n\n"
            "⚠️ PYQ Traps:\n"
            "• Coin oesophagus = face on; Coin trachea = edge on\n"
            "• Button battery = EMERGENCY removal\n"
            "• Right bronchus > left for FB aspiration"
        ),
        "high_yield_takeaway": (
            "FB right bronchus most common. Coin in oesophagus = face on (coronal). Trachea = edge on (sagittal). "
            "Button battery = immediate removal. Heimlich for >1 yr; back blows for infants."
        ),
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ENT", "#ForeignBody"],
        "question": None,
        "options": [],
        "correct_answer": None,
        "explanation": None,
    },
    # ── Mnemonic ─────────────────────────────────────────────────────────────
    {
        "title": "Mnemonic: Ossicles — Malleus → Incus → Stapes",
        "subject": Subject.ent,
        "content_format": ContentFormat.mnemonic,
        "poster_text": "Mnemonic: 'MIS' — Malleus, Incus, Stapes (lateral to medial)",
        "caption": (
            "Ossicles Mnemonic — Lateral to Medial\n\n"
            "The three auditory ossicles from lateral (tympanic membrane) to medial (oval window):\n\n"
            "M — Malleus (Handle attached to TM; head articulates with incus)\n"
            "I — Incus (Body articulates with malleus; long process → stapes)\n"
            "S — Stapes (Footplate sits in oval window; smallest bone in body)\n\n"
            "Alternate mnemonic: 'MIS' — Malleus → Incus → Stapes\n\n"
            "Key anatomical facts:\n"
            "• Malleus: Largest ossicle; lateral process → Tympanic membrane (Mallear prominence)\n"
            "• Incus: Most vulnerable to erosion in cholesteatoma (long process)\n"
            "• Stapes: 3 mm tall; footplate 3.25 mm × 1.75 mm; annular ligament attaches to oval window\n\n"
            "Function:\n"
            "• Ossicular chain provides impedance matching (air → fluid)\n"
            "• Reduces sound amplitude by ~30 dB at oval window\n"
            "• Stapedius muscle (CN VII) dampens loud sounds → protects cochlea\n\n"
            "Clinical correlations:\n"
            "• Otosclerosis: Stapes footplate fixation → conductive hearing loss; Schwartze sign\n"
            "• Incus erosion: Cholesteatoma → ossicular discontinuity → conductive hearing loss\n"
            "• Tympanosclerosis: Calcification of TM/ossicles → CHL\n\n"
            "⚠️ Exam Trap: Long process of incus is the FIRST ossicle eroded in cholesteatoma."
        ),
        "high_yield_takeaway": "MIS: Malleus → Incus → Stapes (lateral→medial). Incus long process = first eroded in cholesteatoma. Stapes footplate = otosclerosis site.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ENT", "#Mnemonic", "#Ossicles"],
    },
    # ── Flashcard ─────────────────────────────────────────────────────────────
    {
        "title": "CSOM: Safe vs Unsafe — Types, Features, and Management",
        "subject": Subject.ent,
        "content_format": ContentFormat.flashcard,
        "poster_text": "Safe CSOM = Tubotympanic (central perforation) | Unsafe CSOM = Atticoantral (marginal/attic perforation)",
        "caption": (
            "CSOM: Safe vs Unsafe — Flashcard\n\n"
            "SAFE (TUBOTYMPANIC):\n"
            "• Perforation: Central (pars tensa)\n"
            "• Extent: Middle ear mucosa only\n"
            "• Discharge: Profuse, mucoid, non-foul, pulsatile\n"
            "• Hearing loss: Mild to moderate CHL\n"
            "• Complications: Rare (usually none)\n"
            "• Treatment: Aural toilet + antibiotics (topical ± systemic);\n"
            "  Watchful waiting in inactive safe CSOM\n"
            "• Surgery: Type I tympanoplasty (myringoplasty) AFTER 6 weeks dry ear\n\n"
            "UNSAFE (ATTICOANTRAL):\n"
            "• Perforation: Marginal/attic (pars flaccida/Shrapnell's)\n"
            "• Extent: Middle ear + mastoid air cells + bone\n"
            "• Discharge: Scanty, foul-smelling, non-pulsatile\n"
            "• Hearing loss: Moderate-severe CHL; possible mixed\n"
            "• Complications: Common (fistula, facial palsy, intracranial)\n"
            "• Treatment: Surgery mandatory — mastoidectomy (CWU or CWD)\n"
            "• Association: Cholesteatoma in most cases\n\n"
            "Key distinguishing features:\n"
            "• Attic crust (scanty foul discharge + crust over attic region) = UNSAFE\n"
            "• Positive fistula sign (nystagmus on tragal pressure) = LSC erosion\n"
            "• Aural polyp = usually unsafe (granulation tissue from cholesteatoma)\n\n"
            "⚠️ Never miss: Unsafe CSOM with headache, fever, earache → suspect intracranial complication."
        ),
        "question": "What are the key differences between safe (tubotympanic) and unsafe (atticoantral) CSOM?",
        "correct_answer": "Safe: central pars tensa perforation, medical management. Unsafe: attic/marginal pars flaccida perforation, cholesteatoma — requires surgery.",
        "high_yield_takeaway": "Safe CSOM = pars tensa, central perforation, medical management. Unsafe = pars flaccida, attic perforation, cholesteatoma, surgery mandatory.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ENT", "#Flashcard", "#CSOM"],
    },
    # ── True/False ────────────────────────────────────────────────────────────
    {
        "title": "Otitis Media with Effusion in Children — Antibiotics",
        "subject": Subject.ent,
        "content_format": ContentFormat.true_false,
        "poster_text": "Otitis Media with Effusion (OME) = GLUE EAR — antibiotics are NOT first-line treatment",
        "caption": (
            "True or False: Otitis Media with Effusion (OME) in children requires a course of oral antibiotics.\n\n"
            "ANSWER: FALSE\n\n"
            "OME (glue ear) is defined as middle ear effusion without signs of acute infection "
            "(no pain, no fever, no bulging erythematous TM). It is common in children aged 1–3 years "
            "following an episode of AOM or due to Eustachian tube dysfunction.\n\n"
            "Management of OME:\n"
            "• Watchful waiting for 3 months (60–80% resolve spontaneously)\n"
            "• Auto-inflation if tolerated (shown to improve effusion clearance)\n"
            "• Treat underlying cause: allergic rhinitis, adenoid hypertrophy\n"
            "• Speech and language assessment if bilateral and persistent\n\n"
            "Antibiotics are NOT indicated for OME alone — they do NOT improve resolution rates or "
            "long-term outcomes vs watchful waiting.\n\n"
            "WHEN TO INTERVENE (Grommets/Ventilation tubes):\n"
            "1. Persistent bilateral OME for ≥ 3 months with hearing loss ≥ 25–30 dB\n"
            "2. Bilateral OME with speech/language delay or learning difficulties\n"
            "3. Recurrent AOM (≥ 3 in 6 months or ≥ 4 in 12 months) with OME between episodes\n"
            "4. Structural TM changes (atelectasis, retraction pocket)\n\n"
            "Grommets + Adenoidectomy: Most effective surgical combination for persistent OME "
            "in children > 3 years with adenoid hypertrophy.\n\n"
            "⚠️ Exam Trap: OME = glue ear = no acute inflammation = NO antibiotics. "
            "Amoxicillin is for AOM (with bulging TM and fever), not OME."
        ),
        "question": "Otitis Media with Effusion in children requires a course of oral antibiotics.",
        "correct_answer": "FALSE",
        "explanation": "OME (glue ear) has no acute inflammation and resolves spontaneously in 60–80% of cases within 3 months. Antibiotics do not improve resolution rates. Management is watchful waiting ± grommets for persistent cases with hearing loss.",
        "high_yield_takeaway": "OME ≠ AOM. OME: watchful waiting, no antibiotics. AOM: bulging TM + fever → amoxicillin. Grommets for persistent OME ≥ 3 months with hearing loss.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ENT", "#TrueFalse", "#OME"],
    },
    # ── One-liner Recall ──────────────────────────────────────────────────────
    {
        "title": "Tonsillitis Grading — One-liner Recall",
        "subject": Subject.ent,
        "content_format": ContentFormat.one_liner_recall,
        "poster_text": "Tonsillar hypertrophy grading: Grade 1–4 based on the relationship to pharyngeal pillars",
        "caption": (
            "One-liner Recall: Tonsillitis Grading\n\n"
            "Fill in the blank:\n\n"
            "\"In tonsillar enlargement grading, Grade ___ = tonsils meet at the ___ line\"\n\n"
            "Answer: Grade 3 = tonsils meet at the MIDLINE (kissing tonsils)\n\n"
            "Full grading:\n"
            "Grade 0: Tonsils within the tonsillar fossa (post-tonsillectomy)\n"
            "Grade 1: Tonsils visible between anterior and posterior pillars (normal)\n"
            "Grade 2: Tonsils extend beyond the posterior pillar but not to midline\n"
            "Grade 3: Tonsils meet at the MIDLINE ('kissing tonsils')\n"
            "Grade 4: Tonsils extend past midline (contralateral side)\n\n"
            "Clinical significance:\n"
            "• Grades 3–4: May cause obstructive sleep apnoea, dysphagia, muffled voice\n"
            "• Indications for tonsillectomy: ≥ 7 episodes in 1 year, ≥ 5/year for 2 years, "
            "≥ 3/year for 3 years; or obstructive sleep apnoea;\n"
            "  or peritonsillar abscess (quinsy) unresponsive to drainage + antibiotics\n\n"
            "⚠️ Exam Trap: Quinsy = peritonsillar abscess = most common complication of tonsillitis. "
            "Tonsils meet at midline = Grade 3."
        ),
        "question": "In tonsillar enlargement grading, Grade ___ = tonsils meet at the ___ line",
        "correct_answer": "Grade 3 = MIDLINE",
        "high_yield_takeaway": "Tonsil grading: Grade 0 (absent) → 1 (fossa) → 2 (beyond pillars) → 3 (midline = kissing tonsils) → 4 (past midline).",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#ENT", "#OneLiner", "#Tonsillitis"],
    },
]
