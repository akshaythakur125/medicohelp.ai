"""High-yield Psychiatry content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── Rapid Revision ───────────────────────────────────────────────────────
    {
        "title": "Schizophrenia — Schneider's First-Rank Symptoms",
        "subject": Subject.psychiatry,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Schneider's First-Rank Symptoms of schizophrenia — memorise all 11 for NEET-PG!",
        "caption": (
            "Schizophrenia — Schneider's First-Rank Symptoms (FRS)\n\n"
            "Definition: Symptoms considered pathognomonic of schizophrenia when organic cause excluded.\n\n"
            "AUDITORY HALLUCINATIONS (3 types):\n"
            "1. Voices heard arguing/discussing the patient in 3rd person\n"
            "2. Voices giving running commentary on patient's actions\n"
            "3. Echo de la pensée — thought echo (hearing own thoughts repeated aloud)\n\n"
            "PASSIVITY PHENOMENA (Made experiences):\n"
            "4. Made feelings — emotions felt as imposed from outside\n"
            "5. Made impulses — urges felt as externally controlled\n"
            "6. Made actions — movements controlled by external force\n"
            "7. Somatic passivity — bodily sensations imposed from outside\n\n"
            "THOUGHT DISTURBANCES:\n"
            "8. Thought insertion — thoughts put into the mind by external agency\n"
            "9. Thought withdrawal — thoughts removed from the mind\n"
            "10. Thought broadcasting — thoughts broadcast to/shared with others\n\n"
            "DELUSIONAL PERCEPTION:\n"
            "11. A normal perception given a delusional meaning (e.g., seeing a red car → knows he is the Messiah)\n\n"
            "Key Note: FRS are NOW called 'positive symptoms' in modern classification; ICD-11 and DSM-5 "
            "no longer give FRS special diagnostic priority, but they remain high-yield for NEET-PG exams.\n\n"
            "Positive symptoms: Hallucinations, delusions, disorganised speech, catatonia\n"
            "Negative symptoms (4 A's): Alogia, Avolition, Anhedonia, Affective blunting"
        ),
        "high_yield_takeaway": "Schneider's 11 FRS: 3 auditory hallucinations + 4 passivity phenomena + 3 thought disorders + 1 delusional perception. Still very high-yield for NEET-PG.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Psychiatry", "#Schizophrenia"],
    },
    {
        "title": "Antipsychotic Side Effects — Typical vs Atypical",
        "subject": Subject.psychiatry,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Antipsychotic side effects — D2 blockade, metabolic syndrome, and all the high-yield traps!",
        "caption": (
            "Antipsychotic Side Effects — Rapid Revision\n\n"
            "TYPICAL ANTIPSYCHOTICS (D2 receptor blockers):\n"
            "• Chlorpromazine, haloperidol, trifluoperazine, fluphenazine\n\n"
            "Extrapyramidal Side Effects (EPS) — D2 blockade in striatum:\n"
            "1. Acute dystonia: Within hours–days; spasms of neck, eyes, tongue; Tx: benztropine/procyclidine\n"
            "2. Akathisia: Days–weeks; subjective motor restlessness; Tx: propranolol, benzodiazepines\n"
            "3. Parkinsonism: Weeks–months; bradykinesia, rigidity, tremor; Tx: anticholinergics\n"
            "4. Tardive dyskinesia (TD): Months–years; orofacial involuntary movements; irreversible; Tx: clozapine, tetrabenazine\n\n"
            "Neuroleptic Malignant Syndrome (NMS):\n"
            "• Fever + Rigidity + Autonomic instability + Altered consciousness\n"
            "• ↑CPK, leukocytosis, myoglobinuria → renal failure\n"
            "• Treatment: STOP drug; dantrolene, bromocriptine; ICU care\n\n"
            "Hyperprolactinemia (D2 blockade in tuberoinfu ndibular pathway):\n"
            "• Galactorrhoea, amenorrhoea, sexual dysfunction, gynaecomastia\n\n"
            "Other: Anticholinergic (dry mouth, blurred vision), antihistamine (sedation), alpha-blockade (orthostatic hypotension)\n\n"
            "ATYPICAL ANTIPSYCHOTICS (D2 + 5-HT2A blockers):\n"
            "• Clozapine: Best for treatment-resistant schizophrenia; agranulocytosis risk (monitor WBC weekly)\n"
            "• Risperidone: Highest prolactin elevation among atypicals\n"
            "• Olanzapine, quetiapine: Metabolic syndrome (weight gain, diabetes, dyslipidaemia)\n"
            "• Aripiprazole: Partial D2 agonist; least metabolic effects; no prolactin rise"
        ),
        "high_yield_takeaway": "NMS: Fever + Rigidity + ↑CPK → stop drug, give dantrolene. TD: irreversible, treat with clozapine. Clozapine: agranulocytosis, monitor CBC weekly.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Psychiatry", "#Antipsychotics"],
    },
    # ── MCQ ──────────────────────────────────────────────────────────────────
    {
        "title": "DSM-5 Major Depressive Disorder Criteria — MCQ",
        "subject": Subject.psychiatry,
        "content_format": ContentFormat.mcq,
        "poster_text": "How many DSM-5 criteria are needed to diagnose Major Depressive Disorder?",
        "caption": (
            "DSM-5 Major Depressive Disorder (MDD) — Criteria Summary\n\n"
            "SIGECAPS Mnemonic (at least 5 symptoms for ≥ 2 weeks, must include #1 or #2):\n"
            "S — Sleep disturbance (insomnia or hypersomnia)\n"
            "I — Interest loss (anhedonia)\n"
            "G — Guilt / worthlessness\n"
            "E — Energy loss / fatigue\n"
            "C — Concentration difficulty\n"
            "A — Appetite / weight change (≥ 5% in 1 month)\n"
            "P — Psychomotor agitation or retardation\n"
            "S — Suicidal ideation / thoughts of death\n\n"
            "Core features (either must be present):\n"
            "1. Depressed mood — most of the day, nearly every day\n"
            "2. Anhedonia — markedly diminished interest/pleasure in activities\n\n"
            "Duration: ≥ 2 weeks\n"
            "Impairment: Must cause social/occupational dysfunction\n"
            "Exclusions: Not attributable to substance, medical condition, or bereavement (bereavement exclusion removed in DSM-5)\n\n"
            "Treatment:\n"
            "• Mild–moderate: Psychotherapy (CBT) ± SSRI\n"
            "• Moderate–severe: SSRI (fluoxetine, sertraline — first-line); + psychotherapy\n"
            "• Severe with psychotic features: Antidepressant + antipsychotic\n"
            "• Refractory: ECT (most effective acute treatment for severe/psychotic depression)"
        ),
        "question": (
            "A 32-year-old woman presents with a 3-week history of persistent sadness, loss of interest in her hobbies, "
            "early morning awakening, weight loss of 4 kg, fatigue, difficulty concentrating at work, and recurrent thoughts "
            "that she would be better off dead. She denies any substance use. Physical examination and thyroid function tests are normal. "
            "How many DSM-5 criteria does she meet, and what is the most appropriate first-line pharmacotherapy?"
        ),
        "options": [
            "A. Meets 5 criteria; first-line treatment is benzodiazepine for immediate symptom relief",
            "B. Meets 7 criteria; first-line pharmacotherapy is an SSRI such as sertraline or fluoxetine",
            "C. Meets 4 criteria (insufficient for diagnosis); watchful waiting is recommended",
            "D. Meets 7 criteria; first-line treatment is a tricyclic antidepressant such as amitriptyline",
        ],
        "correct_answer": "B. Meets 7 criteria; first-line pharmacotherapy is an SSRI such as sertraline or fluoxetine",
        "explanation": (
            "The patient meets 7 of the 9 DSM-5 MDD criteria: depressed mood, anhedonia (loss of interest), sleep disturbance (early wakening = insomnia), weight loss (appetite change), fatigue (energy loss), concentration difficulty, and suicidal ideation. "
            "DSM-5 requires at least 5 symptoms present for ≥ 2 weeks, with at least one being depressed mood or anhedonia, causing functional impairment — all fulfilled here. "
            "First-line pharmacotherapy for moderate-to-severe MDD is an SSRI (sertraline, fluoxetine, escitalopram); they have the best efficacy-to-tolerability ratio. "
            "Benzodiazepines are not antidepressants and are not first-line for MDD; they may exacerbate suicidal ideation. "
            "Tricyclic antidepressants (amitriptyline) are effective but have a narrow therapeutic index, significant anticholinergic side effects, and are dangerous in overdose, making them second- or third-line agents."
        ),
        "high_yield_takeaway": "MDD DSM-5: ≥ 5 of 9 SIGECAPS criteria for ≥ 2 weeks; must include depressed mood or anhedonia. First-line Rx: SSRI. ECT for severe/refractory cases.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Psychiatry", "#Depression"],
    },
    {
        "title": "Bipolar Disorder — Classification and Management MCQ",
        "subject": Subject.psychiatry,
        "content_format": ContentFormat.mcq,
        "poster_text": "Manic episode criteria, mood stabilizers, and bipolar I vs II — crack this NEET-PG favourite!",
        "caption": (
            "Bipolar Disorder — Key Revision Points\n\n"
            "MANIC EPISODE (DSM-5):\n"
            "• Elevated/expansive/irritable mood + increased goal-directed activity for ≥ 7 days (or any duration if hospitalised)\n"
            "• At least 3 of DIG FAST: Distractibility, Indiscretion (risky behaviour), Grandiosity, Flight of ideas, "
            "Activity increase, Sleep decreased (without fatigue), Talkativeness (pressured speech)\n\n"
            "HYPOMANIC EPISODE: Same features but ≥ 4 days, no hospitalisation, no psychosis, no marked impairment\n\n"
            "CLASSIFICATION:\n"
            "• Bipolar I: Full manic episodes (with or without depressive episodes)\n"
            "• Bipolar II: Hypomanic episodes + major depressive episodes (never full mania)\n"
            "• Cyclothymia: ≥ 2 years of hypomania + depressive symptoms (not meeting MDD criteria)\n\n"
            "MOOD STABILIZERS — Exam Favourite Associations:\n"
            "• Lithium: Drug of choice for mania + bipolar prophylaxis; narrow therapeutic index (0.8–1.2 mEq/L)\n"
            "  — Toxicity: Tremor, polyuria/polydipsia (nephrogenic DI), hypothyroidism, teratogen (Ebstein's anomaly)\n"
            "• Valproate: Preferred in rapid cycling, mixed states; teratogen (neural tube defects)\n"
            "• Carbamazepine: Useful but many drug interactions\n"
            "• Lamotrigine: Best for bipolar depression maintenance; risk of SJS\n"
            "• Olanzapine/Quetiapine: Acute mania + maintenance"
        ),
        "question": (
            "A 27-year-old man is brought by his family with a 10-day history of decreased need for sleep (sleeping only 2 hours/night but feeling energetic), "
            "grandiose beliefs that he has invented a cure for cancer, pressured speech, spending all his savings, and making multiple phone calls at 3 AM. "
            "He has no prior psychiatric history. Which of the following is the most appropriate acute treatment and long-term prophylactic mood stabilizer?"
        ),
        "options": [
            "A. Diazepam for acute sedation; fluoxetine for long-term mood stabilisation",
            "B. Haloperidol for acute control; lithium for long-term prophylaxis",
            "C. Lithium alone is sufficient for both acute mania and long-term prophylaxis",
            "D. Lorazepam for acute mania; lamotrigine is the first-line prophylactic agent for manic episodes",
        ],
        "correct_answer": "B. Haloperidol for acute control; lithium for long-term prophylaxis",
        "explanation": (
            "This patient has a classic manic episode (Bipolar I) — elevated mood, decreased sleep without fatigue, grandiosity, pressured speech, and impulsive behaviour lasting > 7 days with significant functional impairment. "
            "Acute management of severe mania typically requires an antipsychotic (haloperidol, olanzapine, or risperidone) for rapid symptom control, often combined with a benzodiazepine (lorazepam) for agitation. "
            "Lithium is the gold-standard long-term mood stabiliser for bipolar I disorder with established efficacy in preventing both manic and depressive recurrences; therapeutic range is 0.8–1.2 mEq/L. "
            "Fluoxetine (SSRI) is contraindicated as monotherapy in bipolar disorder as it can precipitate a manic switch. "
            "Lamotrigine is particularly effective for preventing bipolar depression but has less evidence for preventing manic episodes and is not appropriate as first-line prophylaxis for Bipolar I with predominant manic features."
        ),
        "high_yield_takeaway": "Mania: ≥ 7 days, DIG FAST criteria. Acute Rx: antipsychotic ± benzodiazepine. Lithium = gold-standard prophylaxis. SSRIs alone → manic switch risk.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Psychiatry", "#BipolarDisorder"],
    },
    # ── Concise Notes ─────────────────────────────────────────────────────────
    {
        "title": "Defense Mechanisms — Classification and Examples",
        "subject": Subject.psychiatry,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "Defense mechanisms classified and explained — high-yield for psychiatry NEET-PG and USMLE!",
        "caption": (
            "Defense Mechanisms — Concise Notes\n\n"
            "Definition: Unconscious psychological strategies used by the ego to manage conflict between id impulses, "
            "superego demands, and reality.\n\n"
            "MATURE (NEUROTIC-HEALTHY) DEFENSES:\n"
            "• Sublimation: Channelling unacceptable impulse into socially acceptable activity\n"
            "  (e.g., aggressive person becomes a surgeon)\n"
            "• Humour: Using comedy to deal with painful situations\n"
            "• Altruism: Meeting own needs by meeting others' needs\n"
            "• Suppression: Conscious decision to postpone dealing with a conflict\n\n"
            "NEUROTIC (INTERMEDIATE) DEFENSES:\n"
            "• Repression: Involuntarily keeping painful thoughts out of consciousness\n"
            "• Displacement: Shifting feelings from original object to a safer target\n"
            "  (e.g., angry at boss → kicks the dog)\n"
            "• Rationalization: Intellectual justification of unacceptable behaviour\n"
            "• Reaction formation: Turning unacceptable impulse into its opposite (e.g., hate → excessive love)\n"
            "• Undoing: Symbolic act to reverse an unacceptable thought/action (OCD-related)\n"
            "• Isolation of affect: Separating the emotional component from a thought\n\n"
            "IMMATURE (PRIMITIVE/PSYCHOTIC) DEFENSES:\n"
            "• Splitting: Everything is all good or all bad (black and white thinking); borderline PD\n"
            "• Projection: Attributing own unacceptable feelings to others (paranoia)\n"
            "• Denial: Refusing to acknowledge painful reality (common in substance abuse, terminal illness)\n"
            "• Regression: Returning to earlier developmental stage under stress\n"
            "• Acting out: Expressing unconscious conflict through action rather than reflection\n"
            "• Introjection: Internalising qualities of another (identification with aggressor)\n"
            "• Projective identification: Projecting feelings onto others AND inducing those feelings in them\n\n"
            "EXAM ASSOCIATIONS:\n"
            "• OCD: Undoing, isolation of affect, reaction formation\n"
            "• Borderline PD: Splitting\n"
            "• Paranoid PD: Projection\n"
            "• Conversion disorder: Dissociation"
        ),
        "high_yield_takeaway": "Mature: sublimation, humour, altruism. Neurotic: repression, reaction formation. Immature: splitting (BPD), projection (paranoia), denial. Undoing → OCD.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Psychiatry", "#DefenseMechanisms"],
    },
    # ── PYQ Concept ───────────────────────────────────────────────────────────
    {
        "title": "Suicide Risk Assessment — PYQ Pattern",
        "subject": Subject.psychiatry,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Suicide risk factors and assessment — repeatedly tested in NEET-PG and clinical exams!",
        "caption": (
            "Suicide Risk Assessment — PYQ High-Yield Concept\n\n"
            "EPIDEMIOLOGY:\n"
            "• Attempted suicide (parasuicide) more common in females (3:1)\n"
            "• Completed suicide more common in males (3–4:1)\n"
            "• Most common method in India: Hanging (males), poisoning (females)\n"
            "• Peak age for suicide: Middle-aged men (45–65 years)\n\n"
            "HIGH-RISK FACTORS (Mnemonic — SAD PERSONS):\n"
            "S — Sex (male)\n"
            "A — Age (elderly or adolescent)\n"
            "D — Depression (most common psychiatric illness associated with suicide)\n"
            "P — Previous attempt (#1 risk factor for future completed suicide)\n"
            "E — Ethanol/substance abuse\n"
            "R — Rational thinking loss (psychosis)\n"
            "S — Social support lacking\n"
            "O — Organised/serious plan\n"
            "N — No spouse (divorced, widowed, separated)\n"
            "S — Sickness (chronic physical illness, chronic pain)\n\n"
            "FEATURES INDICATING HIGH LETHALITY:\n"
            "• Detailed, specific plan\n"
            "• Lethal method chosen (firearms, hanging > pills)\n"
            "• Low chance of rescue (isolated location, timed)\n"
            "• Final acts (writing a note, giving away possessions)\n"
            "• No help-seeking behaviour\n\n"
            "PSYCHIATRIC DISORDERS AND SUICIDE RISK:\n"
            "• Highest risk: Major depression with psychotic features, bipolar disorder (depressive phase)\n"
            "• Schizophrenia: 5–10% lifetime risk (command hallucinations)\n"
            "• Borderline PD: Chronic suicidal ideation + impulsive attempts\n"
            "• Alcohol dependence: Significantly increases risk\n\n"
            "MANAGEMENT:\n"
            "• Immediate safety assessment: MSE, direct questioning about suicidal intent\n"
            "• Voluntary vs involuntary admission criteria\n"
            "• Safety planning, means restriction counselling\n"
            "• Treat underlying psychiatric disorder\n"
            "• Lithium: Only medication proven to reduce suicide risk in bipolar disorder\n"
            "• Clozapine: Reduces suicidality in schizophrenia\n\n"
            "PYQ ANSWER KEY:\n"
            "Q: Most common psychiatric illness in suicide? → Major Depression\n"
            "Q: Best single predictor of future suicide? → Previous attempt\n"
            "Q: Drug proven to reduce suicide in bipolar? → Lithium\n"
            "Q: Drug proven to reduce suicide in schizophrenia? → Clozapine\n"
            "Q: Completed suicide more common in which sex? → Males"
        ),
        "high_yield_takeaway": "Previous attempt = #1 risk factor. Males complete, females attempt. Lithium reduces bipolar suicide; clozapine reduces schizophrenia suicide. SAD PERSONS mnemonic.",
        "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#Psychiatry", "#PYQ"],
    },
]
