"""High-yield Anatomy content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ───────────────────────────────────────────────────────
    {
        "title": "Erb's Palsy — Brachial Plexus C5-C6",
        "subject": Subject.anatomy,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "C5-C6 upper trunk injury → Waiter's tip deformity",
        "caption": (
            "Erb's Palsy — C5, C6 (Upper Trunk) Injury\n\n"
            "Mechanism: Downward traction on neck/shoulder (difficult delivery, motorcycle fall)\n\n"
            "Muscles paralysed:\n"
            "• Deltoid (axillary) — ↓ shoulder abduction\n"
            "• Biceps, brachialis (musculocutaneous) — ↓ elbow flexion\n"
            "• Brachioradialis — ↓ semiprone forearm\n"
            "• Supraspinatus, infraspinatus — ↓ external rotation\n\n"
            "Classic 'Waiter's Tip' posture:\n"
            "Arm: adducted + internally rotated | Elbow: extended | Forearm: pronated\n"
            "Fingers: INTACT (C8-T1 unaffected)\n\n"
            "Reflexes lost: Biceps jerk (C5-C6), Brachioradialis jerk (C6)\n"
            "Sensory loss: Lateral arm & forearm (C5-C6 dermatomes)\n\n"
            "⚠️ Exam Trap: Klumpke's = C8-T1 → claw hand. Never confuse the two."
        ),
        "high_yield_takeaway": "Erb's = C5+C6 = Waiter's tip. Klumpke's = C8+T1 = Claw hand.",
        "hashtags": ["#MedicoHelp", "#Anatomy", "#MBBS", "#NEETPG", "#BrachialPlexus"],
    },
    {
        "title": "Femoral Triangle — Contents & Borders",
        "subject": Subject.anatomy,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Femoral triangle: NAVY lateral-to-medial (Nerve-Artery-Vein-Y-fronts)",
        "caption": (
            "Femoral Triangle — Rapid Revision\n\n"
            "Boundaries:\n"
            "• Superiorly: Inguinal ligament\n"
            "• Medially: Medial border of adductor longus\n"
            "• Laterally: Medial border of sartorius\n"
            "• Floor: Iliacus, psoas major, pectineus, adductor longus\n"
            "• Roof: Fascia lata (cribriform fascia)\n\n"
            "Contents (lateral → medial): NAVY\n"
            "N — Femoral Nerve (most lateral; outside femoral sheath)\n"
            "A — Femoral Artery\n"
            "V — Femoral Vein\n"
            "Y — Empty space (femoral canal → femoral hernia site)\n\n"
            "Femoral Sheath: Contains artery + vein + femoral canal (NOT the nerve)\n"
            "Femoral Canal: Contains fat + lymph nodes of Cloquet; medialmost compartment\n\n"
            "⚠️ Exam Trap: Femoral nerve is NOT inside the femoral sheath."
        ),
        "high_yield_takeaway": "NAVY (Nerve-Artery-Vein-Y-fronts) lateral→medial; nerve is outside the femoral sheath.",
        "hashtags": ["#MedicoHelp", "#Anatomy", "#MBBS", "#NEETPG"],
    },
    # ── MCQ ───────────────────────────────────────────────────────────────────
    {
        "title": "Radial Nerve Injury at Spiral Groove — MCQ",
        "subject": Subject.anatomy,
        "content_format": ContentFormat.mcq,
        "poster_text": "Radial nerve at spiral groove → Wrist drop; spared: Triceps",
        "caption": "MCQ: Radial nerve injury and wrist drop",
        "question": (
            "A 30-year-old man sustains a mid-shaft fracture of the humerus. On examination "
            "he has wrist drop and cannot extend the fingers. Grip strength is reduced. "
            "Testing reveals that elbow extension is INTACT. "
            "Which of the following is also likely to be spared in this patient?"
        ),
        "options": [
            "A. Extension of wrist",
            "B. Extension of fingers at MCP joint",
            "C. Triceps reflex",
            "D. Brachioradialis reflex",
        ],
        "correct_answer": "C. Triceps reflex",
        "explanation": (
            "The radial nerve supplies triceps (C7-C8) via branches arising in the axilla/upper arm "
            "BEFORE the nerve enters the spiral groove. A mid-shaft humeral fracture injures the "
            "nerve in the spiral groove, sparing the triceps branch. Hence elbow extension (triceps) "
            "and triceps jerk are preserved. Wrist and finger extension (posterior interosseous nerve, "
            "a branch beyond the spiral groove) are lost, causing wrist drop."
        ),
        "high_yield_takeaway": "Mid-shaft humerus fracture → radial nerve at spiral groove → wrist drop; triceps & triceps jerk SPARED.",
        "hashtags": ["#MedicoHelp", "#Anatomy", "#MBBS", "#NEETPG", "#RadialNerve"],
    },
    {
        "title": "Carpal Tunnel Syndrome — Nerve Compressed",
        "subject": Subject.anatomy,
        "content_format": ContentFormat.mcq,
        "poster_text": "Carpal tunnel = Median nerve compression → Thenar wasting",
        "caption": "MCQ: Carpal tunnel syndrome nerve identification",
        "question": (
            "A 45-year-old woman presents with tingling and numbness in the thumb, index, middle, "
            "and radial half of the ring finger. She notices worsening at night and positive Phalen's "
            "test. Tapping over the flexor retinaculum reproduces her symptoms. "
            "Which nerve is compressed in carpal tunnel syndrome, and which muscle is SPARED?"
        ),
        "options": [
            "A. Ulnar nerve; flexor carpi ulnaris spared",
            "B. Median nerve; adductor pollicis spared",
            "C. Radial nerve; extensor carpi radialis spared",
            "D. Median nerve; flexor digitorum superficialis spared",
        ],
        "correct_answer": "B. Median nerve; adductor pollicis spared",
        "explanation": (
            "Carpal tunnel syndrome compresses the median nerve under the flexor retinaculum. "
            "It causes tingling in the lateral 3½ fingers (median distribution) and thenar wasting "
            "(abductor pollicis brevis, opponens pollicis, flexor pollicis brevis). "
            "Adductor pollicis is innervated by the ULNAR nerve (deep branch) and is therefore SPARED. "
            "Phalen's test (wrist flexion 60s) and Tinel's sign over carpal tunnel are classic signs."
        ),
        "high_yield_takeaway": "CTS = Median nerve; thenar wasting (APB, OP, FPB affected). Adductor pollicis (ulnar) SPARED.",
        "hashtags": ["#MedicoHelp", "#Anatomy", "#MBBS", "#NEETPG", "#MedianNerve"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "Facial Nerve (CN VII) — Complete Course",
        "subject": Subject.anatomy,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "Facial nerve: Motor to face + taste + lacrimation + stapedius",
        "caption": (
            "Facial Nerve (CN VII) — Concise Notes\n\n"
            "Origin: Pons (facial motor nucleus)\n\n"
            "Course:\n"
            "1. Internal acoustic meatus → facial canal (petrous bone)\n"
            "2. Geniculate ganglion (sensory ganglion) — sharp bend (genu)\n"
            "3. Mastoid segment → exits at stylomastoid foramen\n"
            "4. Parotid plexus → terminal branches\n\n"
            "Branches & functions:\n"
            "• Greater petrosal nerve → lacrimal gland (parasympathetic)\n"
            "• Nerve to stapedius → dampens loud sounds\n"
            "• Chorda tympani → taste anterior 2/3 tongue + submandibular/sublingual glands\n"
            "• Terminal motor branches: Temporal, Zygomatic, Buccal, Marginal mandibular, Cervical\n"
            "  (Two Zebras Bit My Cat — mnemonic)\n\n"
            "LMN vs UMN facial palsy:\n"
            "• UMN (cortical stroke): Lower face only; forehead spared (bilateral cortical supply)\n"
            "• LMN (Bell's palsy, parotid tumour): ENTIRE face including forehead\n\n"
            "Bell's Palsy: LMN; treat with prednisolone; eye care critical (lagophthalmos)"
        ),
        "high_yield_takeaway": "UMN facial palsy → forehead SPARED. LMN (Bell's) → entire face affected including forehead.",
        "hashtags": ["#MedicoHelp", "#Anatomy", "#MBBS", "#NEETPG", "#FacialNerve"],
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "Nerve Injuries with Fractures — PYQ Pattern",
        "subject": Subject.anatomy,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Fracture → which nerve? A classic NEET-PG pattern",
        "caption": (
            "Nerve Injuries with Fractures — PYQ Concept\n\n"
            "NEET-PG repeats this association every year:\n\n"
            "Fracture                  → Nerve at Risk\n"
            "────────────────────────────────────────────\n"
            "Surgical neck humerus     → Axillary nerve (C5-C6) → Loss of deltoid, arm patch\n"
            "Mid-shaft humerus         → Radial nerve at spiral groove → Wrist drop\n"
            "Lateral condyle humerus   → PIN (posterior interosseous) → Finger drop\n"
            "Medial epicondyle         → Ulnar nerve → Claw hand (ring + little)\n"
            "Supracondylar humerus     → Anterior interosseous nerve → Pinch sign\n"
            "Neck of fibula            → Common peroneal nerve → Foot drop\n"
            "Posterior hip dislocation → Sciatic nerve → Foot drop + sensory\n"
            "Posterior knee dislocation→ Popliteal artery (not nerve) → ischaemia\n"
            "Scaphoid fracture         → AVN (avascular necrosis) — not nerve\n\n"
            "Key pattern: The stem gives a fracture + functional deficit. Match the nerve."
        ),
        "high_yield_takeaway": "Mid-shaft humerus → radial (wrist drop). Neck fibula → common peroneal (foot drop). Memorise the table.",
        "hashtags": ["#MedicoHelp", "#Anatomy", "#MBBS", "#NEETPG", "#PYQ"],
    },
]
