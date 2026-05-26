"""High-yield Orthopedics content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ───────────────────────────────────────────────────────
    {
        "title": "Nerve Injuries with Fractures — Lower Limb",
        "subject": Subject.orthopedics,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Which nerve gets injured in which lower-limb fracture? High-yield NEET-PG table.",
        "caption": (
            "Nerve Injuries with Fractures — Lower Limb\n\n"
            "Posterior Hip Dislocation:\n"
            "• Sciatic nerve injury — peroneal division most vulnerable\n"
            "• Foot drop, loss of eversion, sensory loss over dorsum of foot\n\n"
            "Neck of Fibula Fracture:\n"
            "• Common peroneal (fibular) nerve wraps around fibular neck\n"
            "• Foot drop + sensory loss over dorsum of foot and 1st web space\n\n"
            "Medial Tibial Plateau / Knee Dislocation:\n"
            "• Popliteal artery (vascular emergency) + common peroneal nerve\n"
            "• Always check pedal pulses; vascular repair within 6 hours\n\n"
            "Calcaneal Fracture:\n"
            "• Lateral plantar nerve (branch of tibial nerve)\n"
            "• Heel pain + sensory loss over lateral sole\n\n"
            "Lisfranc Injury (Tarsometatarsal):\n"
            "• Deep peroneal nerve — sensory loss 1st web space\n\n"
            "Femoral Shaft Fracture:\n"
            "• Femoral nerve (rare); profunda femoris artery injury more common\n\n"
            "Key Mnemonic: POP — Posterior hip dislocation → Opposite division (peroneal) of sciatic nerve"
        ),
        "high_yield_takeaway": "Posterior hip dislocation → sciatic (peroneal division). Fibular neck fracture → common peroneal → foot drop.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Orthopedics", "#NerveInjury"],
    },
    {
        "title": "Compartment Syndrome — Diagnosis and Emergency Management",
        "subject": Subject.orthopedics,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "6 P's of compartment syndrome — recognize before it's too late!",
        "caption": (
            "Compartment Syndrome — Rapid Revision\n\n"
            "Definition: Pressure within a closed fascial compartment exceeds perfusion pressure → ischemia\n\n"
            "Common Causes:\n"
            "• Fractures (tibial shaft — #1 cause), crush injuries, tight casts, burns, reperfusion injury\n\n"
            "Classic 6 P's (in order of appearance):\n"
            "1. Pain — out of proportion, worse with passive stretch (earliest and most reliable sign)\n"
            "2. Pressure — tense, woody compartment on palpation\n"
            "3. Paresthesia — tingling/numbness from ischemic nerve\n"
            "4. Paresis/Paralysis — muscle weakness (late sign)\n"
            "5. Pallor — reduced capillary refill\n"
            "6. Pulselessness — very late; implies arterial compromise\n\n"
            "Diagnosis:\n"
            "• Compartment pressure measurement: Normal < 10 mmHg\n"
            "• Fasciotomy threshold: Pressure > 30 mmHg OR delta pressure (diastolic BP − compartment pressure) < 30 mmHg\n\n"
            "Treatment:\n"
            "• EMERGENCY fasciotomy — do not delay\n"
            "• Remove all circumferential dressings/casts immediately\n"
            "• Leg: 4-compartment fasciotomy via 2 incisions\n\n"
            "Complication if missed: Volkmann's ischemic contracture (forearm > leg)"
        ),
        "high_yield_takeaway": "Pain on passive stretch = earliest sign. Fasciotomy when delta pressure < 30 mmHg. Do NOT wait for pulselessness.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Orthopedics", "#CompartmentSyndrome"],
    },
    # ── MCQ ──────────────────────────────────────────────────────────────────
    {
        "title": "Salter-Harris Fracture Classification — MCQ",
        "subject": Subject.orthopedics,
        "content_format": ContentFormat.mcq,
        "poster_text": "A 9-year-old with wrist injury and growth plate involvement — which Salter-Harris type?",
        "caption": (
            "Salter-Harris Fracture Classification — MCQ\n\n"
            "Mnemonic — SALTR:\n"
            "• Type I — S (Slip): Through physis only; best prognosis\n"
            "• Type II — A (Above): Through physis + metaphysis; Thurstan Holland fragment; most common (75%)\n"
            "• Type III — L (Lower epiphysis): Through physis + epiphysis; intra-articular\n"
            "• Type IV — T (Through all): Metaphysis + physis + epiphysis; needs ORIF\n"
            "• Type V — R (Ram/crush): Crush injury to physis; worst prognosis; often missed acutely\n\n"
            "Prognosis rule: Higher the type number → worse the growth disturbance risk\n\n"
            "Clinical pearl: Type II is the most common; Type V has worst prognosis and may present "
            "only as premature growth arrest without acute fracture line on X-ray."
        ),
        "question": (
            "A 9-year-old boy falls off his bicycle and presents with pain and swelling over the distal radius. "
            "X-ray shows a fracture line passing through the physis and extending into the epiphysis only, "
            "with no metaphyseal involvement. Which Salter-Harris type is this, and what is the most appropriate management?"
        ),
        "options": [
            "A. Type II — conservative management with above-elbow cast immobilisation",
            "B. Type III — open reduction and internal fixation to restore the articular surface",
            "C. Type IV — closed reduction is acceptable if displacement is less than 2 mm",
            "D. Type V — urgent MRI to assess physeal crush injury",
        ],
        "correct_answer": "B. Type III — open reduction and internal fixation to restore the articular surface",
        "explanation": (
            "Salter-Harris Type III fractures extend through the physis and into the epiphysis, making them intra-articular injuries. "
            "Accurate anatomical restoration of the articular surface is mandatory to prevent growth arrest, joint incongruity, and premature osteoarthritis; "
            "therefore ORIF is the treatment of choice when significant displacement is present. "
            "Type II (the most common type, ~75%) involves the physis and metaphysis and can usually be managed conservatively with cast immobilisation. "
            "Type V is a crush injury to the physis — it is often not visible on initial X-ray and typically presents later as premature physeal arrest. "
            "The SALTR mnemonic (Slip, Above/metaphysis, Lower/epiphysis, Through all, Ram/crush) helps recall the five types in order of increasing complexity and growth-disturbance risk."
        ),
        "high_yield_takeaway": "SH Type III = physis + epiphysis (intra-articular) → ORIF. Type II = most common. Type V = worst prognosis (crush, often missed acutely).",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Orthopedics", "#PediatricFractures"],
    },
    {
        "title": "Bone Tumors: Osteosarcoma vs Ewing's Sarcoma — MCQ",
        "subject": Subject.orthopedics,
        "content_format": ContentFormat.mcq,
        "poster_text": "Teenager with bone pain and X-ray lesion — Osteosarcoma or Ewing's? Know the difference!",
        "caption": (
            "Bone Tumors: Osteosarcoma vs Ewing's Sarcoma\n\n"
            "Feature          | Osteosarcoma          | Ewing's Sarcoma\n"
            "Age              | 10–20 yrs             | 5–15 yrs\n"
            "Location         | Metaphysis (distal femur #1) | Diaphysis (flat bones too)\n"
            "X-ray sign       | Sunburst + Codman's triangle | Onion-peel periosteal reaction\n"
            "Serum marker     | Alkaline phosphatase (↑ALP) | LDH (↑LDH)\n"
            "Translocation    | None specific         | t(11;22) → EWS-FLI1 fusion\n"
            "Biopsy           | Osteoid production    | Small round blue cells\n"
            "Radiation        | Resistant             | Sensitive\n"
            "Treatment        | Surgery + chemo       | Chemo + radiation\n\n"
            "Remember: Codman's triangle = reactive periosteal elevation at tumour periphery (not specific to osteosarcoma — also in Ewing's)"
        ),
        "question": (
            "A 14-year-old boy presents with a 6-week history of progressive pain and swelling around the right knee. "
            "X-ray reveals a metaphyseal lesion in the distal femur with sunburst periosteal reaction and Codman's triangle. "
            "Alkaline phosphatase is markedly elevated. Biopsy shows pleomorphic spindle cells producing osteoid. "
            "Which of the following correctly describes this tumour's molecular characteristic and radiation sensitivity?"
        ),
        "options": [
            "A. t(11;22) translocation producing EWS-FLI1 fusion protein; highly radiation sensitive",
            "B. No specific pathognomonic translocation; radiation resistant — treated with surgery and chemotherapy",
            "C. t(9;22) Philadelphia chromosome translocation; responds to imatinib mesylate",
            "D. t(8;14) translocation; treated with radiation therapy alone",
        ],
        "correct_answer": "B. No specific pathognomonic translocation; radiation resistant — treated with surgery and chemotherapy",
        "explanation": (
            "The clinical picture — metaphyseal location in distal femur, sunburst periosteal reaction, Codman's triangle, osteoid production on biopsy, and elevated ALP — is classic for osteosarcoma. "
            "Osteosarcoma lacks a specific pathognomonic chromosomal translocation (though RB1 and TP53 mutations are associated) and is notably radiation resistant; "
            "standard treatment is neoadjuvant chemotherapy (cisplatin, doxorubicin, high-dose methotrexate) followed by limb-salvage surgery and adjuvant chemotherapy. "
            "Ewing's sarcoma, in contrast, carries the t(11;22)(q24;q12) translocation producing the EWS-FLI1 fusion protein and is exquisitely radiation sensitive. "
            "t(9;22) is the Philadelphia chromosome seen in CML, and t(8;14) is associated with Burkitt's lymphoma — both unrelated to primary bone tumours."
        ),
        "high_yield_takeaway": "Osteosarcoma: metaphysis, sunburst, ↑ALP, no specific translocation, radiation RESISTANT. Ewing's: diaphysis, onion-peel, t(11;22), radiation SENSITIVE.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Orthopedics", "#BoneTumors"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "Osteoarthritis vs Rheumatoid Arthritis — Comparison",
        "subject": Subject.orthopedics,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "OA vs RA — master the clinical, radiological and lab differences for NEET-PG.",
        "caption": (
            "Osteoarthritis vs Rheumatoid Arthritis — Concise Notes\n\n"
            "EPIDEMIOLOGY\n"
            "• OA: Age > 45, females > males, obesity, mechanical overuse\n"
            "• RA: Age 30–50, females >> males (3:1), autoimmune; HLA-DR4 association\n\n"
            "PATHOLOGY\n"
            "• OA: Non-inflammatory; cartilage degradation → subchondral sclerosis, osteophyte formation\n"
            "• RA: Inflammatory synovitis → pannus formation → cartilage and bone erosion\n\n"
            "JOINTS INVOLVED\n"
            "• OA: Weight-bearing (knee, hip, spine); DIP joints of hands (Heberden's nodes); PIP (Bouchard's nodes)\n"
            "• RA: PIP + MCP + wrist (DIP spared); symmetric; also C1-C2 → atlantoaxial subluxation risk\n\n"
            "CLINICAL FEATURES\n"
            "• OA: Morning stiffness < 30 min; pain worsens with activity; no systemic features\n"
            "• RA: Morning stiffness > 1 hour; pain worse at rest/morning; systemic (fever, fatigue, weight loss)\n"
            "• RA deformities: Swan-neck, Boutonniere, Z-thumb, ulnar deviation at MCPs\n\n"
            "RADIOLOGY\n"
            "• OA: Joint space narrowing, subchondral sclerosis, osteophytes, subchondral cysts — NO erosions\n"
            "• RA: Periarticular osteopenia, symmetric joint space narrowing, marginal erosions, subluxations\n\n"
            "LABORATORY\n"
            "• OA: Normal ESR/CRP; RF negative; synovial fluid non-inflammatory (< 2000 WBC/mm3)\n"
            "• RA: Elevated ESR/CRP; RF positive (70–80%); anti-CCP (most specific); inflammatory synovial fluid\n\n"
            "TREATMENT\n"
            "• OA: Weight loss, physiotherapy, NSAIDs, intra-articular steroids, joint replacement (definitive)\n"
            "• RA: MTX (first-line DMARD); biologics (anti-TNF, anti-IL-6); hydroxychloroquine; NSAIDs for symptoms"
        ),
        "high_yield_takeaway": "OA: DIP + Heberden's, stiffness < 30 min, osteophytes, no erosions. RA: MCP+PIP, stiffness > 1 hr, erosions, anti-CCP most specific.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Orthopedics", "#Rheumatology"],
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "Supracondylar Fracture Complications — PYQ Pattern",
        "subject": Subject.orthopedics,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Supracondylar fracture complications — most frequently tested PYQ pattern in Ortho NEET-PG!",
        "caption": (
            "Supracondylar Fracture of Humerus — PYQ High-Yield Concept\n\n"
            "Epidemiology: Most common fracture around elbow in children (age 5–10 years); "
            "extension type (98%) from fall on outstretched hand.\n\n"
            "NEUROVASCULAR INJURIES (Exam Favourite):\n"
            "• Anterior interosseous nerve (AIN — branch of median nerve) → most common nerve injured\n"
            "  — Test: Inability to make 'OK sign' (circle with thumb and index finger)\n"
            "  — Pure motor branch; no sensory loss\n"
            "• Radial nerve — rare in extension type; more common in flexion type\n"
            "• Brachial artery — most dangerous vascular injury; leads to Volkmann's ischemia if missed\n\n"
            "VOLKMANN'S ISCHEMIC CONTRACTURE:\n"
            "• Results from untreated compartment syndrome or brachial artery injury\n"
            "• Stages: Ischemia → Infarction → Fibrosis → Contracture\n"
            "• Classic posture: Pronated forearm, flexed wrist, extended fingers (intrinsic-minus hand)\n\n"
            "MALUNION — CUBITUS VARUS (Gunstock Deformity):\n"
            "• Most common late complication overall\n"
            "• Primarily cosmetic deformity; corrected by French (dome) osteotomy\n"
            "• Cubitus valgus → tardy ulnar nerve palsy (years later)\n\n"
            "GARTLAND CLASSIFICATION:\n"
            "• Type I: Undisplaced — above-elbow cast in 90° flexion\n"
            "• Type II: Displaced, posterior cortex intact — closed reduction ± K-wire pinning\n"
            "• Type III: Completely displaced — closed reduction + percutaneous K-wire fixation\n\n"
            "PYQ ANSWER KEY:\n"
            "Q: Most common nerve injured in supracondylar fracture? → AIN (branch of median nerve)\n"
            "Q: Most common late complication? → Cubitus varus (gunstock deformity)\n"
            "Q: Vascular injury leads to? → Volkmann's ischemic contracture\n"
            "Q: Most common fracture around elbow in children? → Supracondylar fracture of humerus\n"
            "Q: Correction of cubitus varus by? → French (dome) osteotomy"
        ),
        "high_yield_takeaway": "SCF complications: AIN = most common nerve; cubitus varus = most common late complication; brachial artery injury → Volkmann's contracture.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Orthopedics", "#PYQ"],
    },
]
