"""High-yield General Surgery content for NEET-PG / INI-CET revision."""
from app.models import ContentFormat, Subject

TOPICS = [
    # ── 1. Rapid Revision ───────────────────────────────────────────────────
    {
        "title": "Types of Hernias",
        "subject": Subject.general_surgery,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Hernia classification is surgical anatomy made exam-ready",
        "caption": (
            "HERNIAS — CLASSIFICATION & HIGH-YIELD FACTS\n\n"
            "INGUINAL HERNIAS (most common overall):\n\n"
            "INDIRECT INGUINAL HERNIA:\n"
            "• Passes through deep inguinal ring → inguinal canal → may enter scrotum\n"
            "• Most common type; more common in young males\n"
            "• Congenital (patent processus vaginalis)\n"
            "• Covered by all 3 layers of spermatic fascia\n"
            "• Lies LATERAL to inferior epigastric vessels\n\n"
            "DIRECT INGUINAL HERNIA:\n"
            "• Pushes through Hesselbach's triangle (posterior wall of inguinal canal)\n"
            "• Hesselbach's triangle: inferior epigastric a. (lateral), rectus sheath (medial), inguinal ligament (inferior)\n"
            "• Lies MEDIAL to inferior epigastric vessels\n"
            "• Acquired (weakness of transversalis fascia); older men, straining\n"
            "• Rarely enters scrotum; rarely strangulates\n\n"
            "FEMORAL HERNIA:\n"
            "• Through femoral ring (medial to femoral vein, below inguinal ligament)\n"
            "• More common in women (but inguinal still more common in women overall)\n"
            "• HIGH risk of strangulation (narrow neck) — always operate\n"
            "• Lies BELOW and LATERAL to pubic tubercle\n\n"
            "OTHER HERNIAS:\n"
            "• Umbilical hernia: through umbilical ring; common in infants (closes by age 2)\n"
            "• Para-umbilical hernia: adjacent to umbilicus; adults; always operate\n"
            "• Incisional hernia: through surgical scar; commonest at midline laparotomy\n"
            "• Richter's hernia: only antimesenteric wall of bowel in sac — no obstruction\n"
            "• Littre's hernia: Meckel's diverticulum in sac\n"
            "• Obturator hernia: through obturator foramen; 'little old lady hernia'\n"
            "• Spigelian hernia: through semilunar line (linea semilunaris)\n\n"
            "STRANGULATION = vascular compromise: requires emergency surgery"
        ),
        "high_yield_takeaway": (
            "Indirect = lateral to inferior epigastric vessels, through deep ring. "
            "Direct = Hesselbach's triangle, medial to inf. epigastric. Femoral hernia: always operate (high strangulation risk)."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralSurgery", "#MBBS", "#NEETPG", "#Hernia"],
    },

    # ── 2. Rapid Revision ───────────────────────────────────────────────────
    {
        "title": "Acute Appendicitis — Alvarado Score",
        "subject": Subject.general_surgery,
        "content_format": ContentFormat.rapid_revision,
        "poster_text": "Alvarado score: MANTRELS — 7+ means operate",
        "caption": (
            "ACUTE APPENDICITIS — ALVARADO SCORE (MANTRELS)\n\n"
            "MNEMONIC — MANTRELS (Maximum score = 10):\n\n"
            "M — Migration of pain to RIF          → 1\n"
            "A — Anorexia                           → 1\n"
            "N — Nausea/vomiting                    → 1\n"
            "T — Tenderness in RIF                  → 2\n"
            "R — Rebound tenderness (Blumberg)      → 1\n"
            "E — Elevated temperature (>37.3°C)     → 1\n"
            "L — Leucocytosis (WBC >10,000)         → 2\n"
            "S — Shift to left (neutrophilia)       → 1\n\n"
            "INTERPRETATION:\n"
            "• ≤4: Low probability → discharge / observe\n"
            "• 5–6: Moderate → observe, serial examination\n"
            "• 7–10: High probability → surgery (appendicectomy)\n\n"
            "CLINICAL SIGNS:\n"
            "• McBurney's point: 1/3rd of line from ASIS to umbilicus (max tenderness)\n"
            "• Rovsing's sign: pressure in LIF → pain in RIF (peritoneal irritation)\n"
            "• Psoas sign: hip extension increases pain (retrocaecal appendix)\n"
            "• Obturator sign: internal rotation of flexed hip (pelvic appendix)\n"
            "• Dunphy's sign: increased RIF pain on coughing\n"
            "• Ten Horn sign: pain on gentle traction of right testis\n\n"
            "INVESTIGATIONS:\n"
            "• USS: appendix >6mm, non-compressible, hyperaemia = appendicitis\n"
            "• CT abdomen: most accurate (sensitivity 94–98%)\n"
            "• In pregnancy: USS first; MRI if inconclusive (avoid CT radiation)\n\n"
            "PERFORATION RISK: highest in extremes of age (elderly and infants)"
        ),
        "high_yield_takeaway": (
            "Alvarado ≥7 = operate. McBurney's = 1/3 from ASIS to umbilicus. "
            "Psoas sign = retrocaecal appendix. CT is most accurate investigation."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralSurgery", "#MBBS", "#NEETPG", "#Appendicitis"],
    },

    # ── 3. MCQ ──────────────────────────────────────────────────────────────
    {
        "title": "Intestinal Obstruction — MCQ",
        "subject": Subject.general_surgery,
        "content_format": ContentFormat.mcq,
        "poster_text": "Obstruction or pseudo-obstruction? Know the difference cold",
        "caption": (
            "INTESTINAL OBSTRUCTION — KEY CONCEPTS\n\n"
            "MECHANICAL OBSTRUCTION — CAUSES:\n"
            "• Adults: Adhesions (MC in India), hernia, carcinoma, volvulus\n"
            "• Neonates: Hirschsprung's disease, anorectal malformations, meconium ileus\n"
            "• Children: Intussusception (MC cause of obstruction in 6 months–2 years)\n\n"
            "SIMPLE vs STRANGULATED:\n"
            "• Simple: blood supply intact; no necrosis\n"
            "• Strangulated: vascular compromise → fever, tachycardia, constant pain, peritonism\n\n"
            "CLOSED LOOP OBSTRUCTION: both ends blocked → rapid distension → high perforation risk\n"
            "• Sigmoid volvulus: commonest site; 'coffee bean' sign on X-ray; Gastrografin enema (deflation)\n"
            "• Caecal volvulus: clockwise rotation; kidney-shaped gas shadow in LUQ\n\n"
            "X-RAY FINDINGS:\n"
            "• Small bowel obstruction: central, multiple air-fluid levels, valvulae conniventes (complete across bowel)\n"
            "• Large bowel obstruction: peripheral, haustral folds (incomplete across bowel)\n"
            "• Pneumoperitoneum: free air under diaphragm (erect CXR) = perforation\n\n"
            "PSEUDO-OBSTRUCTION (Ogilvie's syndrome): colonic dilation without mechanical cause; ICU patients\n"
            "Treatment: Neostigmine IV (parasympathomimetic) ± colonoscopic decompression"
        ),
        "question": (
            "A 65-year-old man presents with a 3-day history of abdominal distension, inability to "
            "pass stool or flatus, vomiting, and colicky abdominal pain. He has a midline scar from "
            "a previous surgery 10 years ago. Erect abdominal X-ray shows multiple central air-fluid "
            "levels with a 'step-ladder' pattern. What is the MOST likely cause of this patient's obstruction?"
        ),
        "options": [
            "A. Carcinoma of the sigmoid colon",
            "B. Post-operative adhesions",
            "C. Sigmoid volvulus",
            "D. Intussusception",
        ],
        "correct_answer": "B. Post-operative adhesions",
        "explanation": (
            "The central air-fluid levels in a step-ladder pattern on erect X-ray are characteristic of "
            "small bowel obstruction. In an adult with a history of previous abdominal surgery, post-operative "
            "adhesions are the most common cause of small bowel obstruction. Colonic carcinoma and sigmoid "
            "volvulus would produce large bowel obstruction with peripheral haustra-patterned distension. "
            "Intussusception is predominantly seen in children aged 6 months to 2 years. Adhesions form "
            "fibrous bands that kink or compress bowel loops and are especially common after midline laparotomy."
        ),
        "high_yield_takeaway": (
            "Post-op adhesions = MC cause of SBO in adults. Step-ladder air-fluid levels = SBO. "
            "Sigmoid volvulus = coffee-bean sign. Intussusception = MC obstruction in 6m–2yr children."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralSurgery", "#MBBS", "#NEETPG", "#IntestinalObstruction"],
    },

    # ── 4. MCQ ──────────────────────────────────────────────────────────────
    {
        "title": "Surgical Signs in Abdomen — MCQ",
        "subject": Subject.general_surgery,
        "content_format": ContentFormat.mcq,
        "poster_text": "Surgical eponymous signs — they hide in MCQ stems every year",
        "caption": (
            "SURGICAL ABDOMINAL SIGNS — RAPID TABLE\n\n"
            "SIGN                  DISEASE           DESCRIPTION\n"
            "─────────────────────────────────────────────────────────────────\n"
            "Murphy's sign         Acute cholecystitis  Arrest of inspiration on deep RUQ palpation\n"
            "Boas' sign            Acute cholecystitis  Referred pain to right shoulder tip (phrenic)\n"
            "Cullen's sign         Acute pancreatitis   Periumbilical bruising\n"
            "Grey Turner's sign    Acute pancreatitis   Flank bruising\n"
            "Fox's sign            Pancreatitis         Bruising over inguinal ligament\n"
            "Rovsing's sign        Appendicitis         LIF pressure → RIF pain\n"
            "Psoas sign            Appendicitis         Hip extension → RIF pain (retrocaecal)\n"
            "Obturator sign        Appendicitis         Internal hip rotation → pain (pelvic app.)\n"
            "Dance sign            Intussusception      Empty RIF on palpation\n"
            "Courvoisier's sign    Pancreatic Ca/CBD    Palpable non-tender gallbladder + jaundice\n"
            "Sister Mary Joseph   GI malignancy        Umbilical nodule (peritoneal metastasis)\n"
            "Trousseau's sign      Pancreatic cancer    Migratory thrombophlebitis\n"
            "Charcot's triad       Ascending cholangitis Fever + jaundice + RUQ pain\n"
            "Reynolds pentad       Ascending cholangitis Charcot's triad + shock + altered sensorium\n\n"
            "EXAM TIP: Courvoisier's law — in obstructive jaundice, if gallbladder is palpable it is "
            "NOT due to gallstones (chronic inflammation → fibrotic GB). Suspect malignancy."
        ),
        "question": (
            "A 55-year-old man presents with progressive painless jaundice over 4 weeks, significant "
            "weight loss, and a palpable non-tender mass in the right hypochondrium. Ultrasound shows "
            "a dilated common bile duct and a dilated, thinned gallbladder. Which eponymous sign best "
            "describes this finding, and what does it indicate?"
        ),
        "options": [
            "A. Murphy's sign — acute cholecystitis",
            "B. Courvoisier's sign — malignant biliary obstruction",
            "C. Charcot's triad — ascending cholangitis",
            "D. Grey Turner's sign — acute pancreatitis",
        ],
        "correct_answer": "B. Courvoisier's sign — malignant biliary obstruction",
        "explanation": (
            "A palpable, non-tender, distended gallbladder in the setting of painless obstructive jaundice "
            "is Courvoisier's sign. Courvoisier's law states that in obstructive jaundice, if the gallbladder "
            "is palpable, the cause is unlikely to be gallstones — because chronic cholelithiasis leads to "
            "a fibrosed, non-distensible gallbladder. A dilated gallbladder points to malignant obstruction, "
            "typically carcinoma of the head of pancreas, ampulla of Vater, or cholangiocarcinoma. "
            "Murphy's sign (painful arrest of inspiration during deep RUQ palpation) indicates cholecystitis."
        ),
        "high_yield_takeaway": (
            "Courvoisier's sign: painless jaundice + palpable non-tender GB = malignancy (NOT gallstones). "
            "Cullen's + Grey Turner's = acute pancreatitis (haemorrhagic)."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralSurgery", "#MBBS", "#NEETPG", "#SurgicalSigns"],
    },

    # ── 5. Concise Notes ────────────────────────────────────────────────────
    {
        "title": "Post-operative Complications Timeline",
        "subject": Subject.general_surgery,
        "content_format": ContentFormat.concise_notes,
        "poster_text": "Every post-op complication has a timeline — know the clock",
        "caption": (
            "POST-OPERATIVE COMPLICATIONS — TIMELINE APPROACH\n\n"
            "SECTION 1 — IMMEDIATE (0–24 hours post-op):\n"
            "• Primary haemorrhage: occurs during or immediately after surgery\n"
            "• Reactionary haemorrhage: within 6 hours; due to BP rising → dislodged clot\n"
            "• Anaphylaxis (to anaesthetic agents, antibiotics, latex)\n"
            "• Respiratory: atelectasis (MC early respiratory complication), laryngospasm\n"
            "• Hypotension due to anaesthetic agents\n\n"
            "SECTION 2 — EARLY (1–7 days post-op):\n"
            "• Day 1–2: Atelectasis, fever (Wind — atelectasis most common early fever)\n"
            "• Day 2–5: DVT (Virchow's triad: stasis, hypercoagulability, endothelial injury)\n"
            "• Day 3–5: UTI (catheter-associated; Water — urine)\n"
            "• Day 5–7: Wound infection (Wound) — most likely Staphylococcus aureus\n"
            "• Day 5–7: Anastomotic leak — fever + pain + peritonism; most serious complication\n\n"
            "W MNEMONIC (causes of post-op fever by day):\n"
            "Day 1–2: Wind (atelectasis)\n"
            "Day 3–5: Water (UTI)\n"
            "Day 4–6: Wound (infection)\n"
            "Day 5–8: Walking (DVT/PE)\n"
            "Day 7+:  Wonder drugs (drug fever) / Deep infection\n\n"
            "SECTION 3 — LATE (weeks to months post-op):\n"
            "• Secondary haemorrhage: 7–14 days; due to vessel wall erosion by infection\n"
            "• Incisional hernia: 3 months to years; at surgical scar\n"
            "• Adhesion-related SBO: months to years post-op\n"
            "• Anastomotic stricture: weeks to months\n"
            "• Dumping syndrome (post-gastrectomy): early and late subtypes\n\n"
            "SECTION 4 — SPECIFIC WOUND COMPLICATIONS:\n"
            "• Seroma: serous fluid collection; most common after mastectomy, axillary dissection\n"
            "• Haematoma: blood collection; Rx drainage if expanding\n"
            "• Dehiscence: superficial; 'pink fluid' (serosanguineous) = warning sign\n"
            "• Burst abdomen (evisceration): deep; requires emergency return to theatre\n\n"
            "EXAM TIP: Burst abdomen classically occurs on day 5–8 post-op; risk factors include "
            "malnutrition, obesity, wound infection, chronic steroid use, and heavy coughing."
        ),
        "high_yield_takeaway": (
            "Post-op fever: Wind (day1-2) → Water (day3-5) → Wound (day4-6) → Walking/DVT (day5-8). "
            "Secondary haemorrhage at 7–14 days (vessel erosion by infection). Pink fluid = impending dehiscence."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralSurgery", "#MBBS", "#NEETPG", "#PostOpComplications"],
    },

    # ── 6. PYQ Concept ──────────────────────────────────────────────────────
    {
        "title": "GI Perforation & Pneumoperitoneum — PYQ Pattern",
        "subject": Subject.general_surgery,
        "content_format": ContentFormat.pyq_concept,
        "poster_text": "Pneumoperitoneum: free air under diaphragm = surgical emergency",
        "caption": (
            "GI PERFORATION & PNEUMOPERITONEUM — HIGH-YIELD PYQ TABLE\n\n"
            "CAUSES OF PNEUMOPERITONEUM (Free air under diaphragm):\n"
            "SURGICAL CAUSES (majority):\n"
            "• Peptic ulcer perforation: MC cause; sudden severe 'board-like' rigidity\n"
            "• Hollow viscus perforation: trauma, diverticulitis, appendicitis, typhoid (Peyer's patches)\n"
            "• Post-laparoscopy: air deliberately insufflated; persists 3–7 days (normal finding)\n\n"
            "NON-SURGICAL CAUSES (air without true perforation):\n"
            "• Post-procedure: colonoscopy, ERCP, laparoscopy\n"
            "• Pneumatosis cystoides intestinalis\n"
            "• Rupture of gas cyst\n\n"
            "X-RAY FINDINGS:\n"
            "• Erect CXR: crescent of air under right hemidiaphragm (commonest site; liver prevents L side)\n"
            "  Minimum 1 mL air detectable on erect CXR\n"
            "• Lateral decubitus (left side down): air rises to right flank — used if patient cannot stand\n"
            "• Rigler's sign: both sides of bowel wall visible (air inside + outside the bowel)\n"
            "• Football sign: large oval air shadow outlining abdominal cavity (in infants)\n"
            "• Cupola sign: air under central tendon of diaphragm\n\n"
            "PEPTIC ULCER PERFORATION — PYQ SPECIFICS:\n"
            "Site: Anterior wall of first part of duodenum (MC site of perforation)\n"
            "Posterior wall duodenum → erosion of gastroduodenal artery → haemorrhage\n"
            "Lesser curve of stomach → perforates into lesser sac\n\n"
            "MANAGEMENT:\n"
            "• Resuscitate → erect CXR + USS → CT (if doubt)\n"
            "• Graham's omental patch repair (PU perforation) — most common emergency procedure\n"
            "• Definitive surgery: highly selective vagotomy (now largely replaced by PPIs)\n\n"
            "EXAM TRAP: Post-laparoscopy pneumoperitoneum up to 3–7 days is NORMAL and does NOT "
            "indicate anastomotic leak or perforation unless accompanied by peritoneal signs."
        ),
        "high_yield_takeaway": (
            "Free air under right hemidiaphragm = peptic ulcer perforation until proven otherwise. "
            "Anterior duodenal wall = MC perforation site. Graham patch = emergency repair. "
            "Post-laparoscopy air up to 7 days is normal."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralSurgery", "#MBBS", "#NEETPG", "#Pneumoperitoneum"],
    },

    # ── 7. Mnemonic ──────────────────────────────────────────────────────────
    {
        "title": "Mnemonic: SIGNS OF CHOLELITHIASIS — 'Female, Forty, Fertile, Fair, Fat'",
        "subject": Subject.general_surgery,
        "content_format": ContentFormat.mnemonic,
        "poster_text": "Mnemonic: '5 F's of Gallstones' — Female, Forty, Fertile, Fair, Fat",
        "caption": (
            "Explain the 5 F's mnemonic for gallstone risk: Female (oestrogen increases cholesterol saturation), "
            "Forty (age >40), Fertile (multiparity — more oestrogen), Fair (Caucasian ethnicity — Pima Indians "
            "highest), Fat (obesity — ↑ cholesterol secretion). Also discuss: rapid weight loss (bariatric surgery), "
            "total parenteral nutrition, cirrhosis, haemolytic anaemias (pigment stones), Crohn's disease. "
            "Types: cholesterol (80%, radiolucent, mixed), pigment (black = sterile bile, brown = infected bile). "
            "Most gallstones are asymptomatic; indication for surgery = symptomatic stones."
        ),
        "high_yield_takeaway": (
            "5 F's: Female, Forty, Fertile, Fair, Fat. Cholesterol stones = radiolucent, most common. "
            "Pigment stones = radiopaque, haemolysis. Symptomatic stones = cholecystectomy."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralSurgery", "#MBBS", "#NEETPG", "#Mnemonic", "#Gallstones"],
    },

    # ── 8. Flashcard ────────────────────────────────────────────────────────
    {
        "title": "Flashcard: Acute Pancreatitis — Ranson's Criteria",
        "subject": Subject.general_surgery,
        "content_format": ContentFormat.flashcard,
        "poster_text": "Ranson's criteria: ≥3 = severe pancreatitis. Signs at admission (5) + at 48 hours (6) = 11 total",
        "caption": (
            "Ranson's criteria for acute pancreatitis severity. At admission (age >55, WBC >16,000, glucose >200, "
            "LDH >350, AST >250). At 48 hours (Hct drop >10%, BUN rise >5, Ca <8, PaO2 <60, base deficit >4, "
            "fluid sequestration >6L). Mortality: 0-2 = <1%, 3-5 = 10-20%, ≥6 = >50%. Alternative scores: "
            "APACHE II, BISAP, CTSI (CT severity index). Gallstones vs alcohol as cause. Treatment: aggressive "
            "IV fluids (LR preferred), NOT prophylactic antibiotics. Indications for ICU: ≥3 Ranson's, organ "
            "failure, pancreatic necrosis."
        ),
        "question": (
            "A 50-year-old alcoholic presents with acute pancreatitis. At admission: Age 50, WBC 18,000, "
            "Glucose 180, LDH 400, AST 280. At 48 hours: Hct drop 12%, BUN rise 6 mg/dL, Ca 7.5, PaO2 55, "
            "BD 5, fluid seq 6.5L. How many Ranson's criteria are met and what is the mortality estimate?"
        ),
        "correct_answer": "At admission: WBC, LDH, AST = 3. At 48 hrs: Hct drop, BUN rise, Ca, PaO2, BD, fluid seq = 6. Total = 9/11. Mortality >50%.",
        "high_yield_takeaway": (
            "Ranson's: 5 at admit + 6 at 48 hrs = 11 total. ≥3 = severe. LR for fluids (not NS). "
            "No prophylactic antibiotics. Necrosis = ICU + consider necrosectomy."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralSurgery", "#MBBS", "#NEETPG", "#Flashcard", "#Pancreatitis"],
    },

    # ── 9. True/False ────────────────────────────────────────────────────────
    {
        "title": "True or False: All acute appendicitis patients require emergency appendicectomy",
        "subject": Subject.general_surgery,
        "content_format": ContentFormat.true_false,
        "poster_text": "Appendicitis: not all need emergency surgery — antibiotics alone can be an option in selected patients",
        "caption": (
            "Current evidence (APPAC, CODA trials) shows that uncomplicated acute appendicitis can be managed "
            "with antibiotics alone in selected patients. Criteria: uncomplicated (no perforation, no abscess, "
            "no fecolith on CT), clinically stable, early presentation. Success rate ~70% at 1 year. However, "
            "appendicectomy remains gold standard and definitive treatment. Emergency surgery is indicated for: "
            "perforation, generalized peritonitis, fecolith, suspected tumour, failed medical therapy, children, "
            "elderly, immunocompromised. Complicated appendicitis (gangrenous/perforated) always requires surgery."
        ),
        "question": "All patients with acute appendicitis require emergency appendicectomy.",
        "correct_answer": "FALSE",
        "explanation": (
            "Selected patients with uncomplicated acute appendicitis (CT-confirmed, no fecolith, no perforation, "
            "no peritonitis) can be treated with antibiotics alone as primary therapy, with appendicectomy "
            "reserved for non-responders or recurrence. However, appendicectomy is still the gold standard."
        ),
        "high_yield_takeaway": (
            "Uncomplicated appendicitis: antibiotics alone possible (70% success). "
            "Complicated: surgery mandatory. Fecolith = always operate."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralSurgery", "#MBBS", "#NEETPG", "#TrueFalse", "#Appendicitis"],
    },

    # ── 10. One-liner Recall ──────────────────────────────────────────────────
    {
        "title": "One-liner Recall: Duodenal vs Gastric Ulcer Comparison",
        "subject": Subject.general_surgery,
        "content_format": ContentFormat.one_liner_recall,
        "poster_text": "DU = pain on empty stomach, relieved by food. GU = pain aggravated by food, weight loss.",
        "caption": (
            "Fill in the blank: \"In peptic ulcer disease, a patient with pain 2-3 hours after meals that is "
            "relieved by eating likely has a ___ ulcer.\" Answer: \"Duodenal ulcer (DU).\" Then compare: "
            "DU (young adults, epigastric pain 2-3 hr post-meal/night, relieved by food/antacids, H. pylori 95%, "
            "normal/high acid). Gastric ulcer (older, pain immediately after meals, aggravated by food, weight loss, "
            "H. pylori 70%, normal/low acid, malignancy risk → always biopsy). DU complications: perforation "
            "(anterior wall), bleeding (posterior wall → gastroduodenal artery). GU complications: bleeding, "
            "perforation, gastric outlet obstruction, malignant transformation."
        ),
        "question": (
            "A patient who experiences epigastric pain 2-3 hours after meals that is relieved by eating "
            "likely has a ___ ulcer."
        ),
        "correct_answer": "Duodenal ulcer (DU)",
        "high_yield_takeaway": (
            "DU: pain on empty stomach, relieved by food, high acid, young. "
            "GU: pain aggravated by food, weight loss, low acid, old, malignant risk. Always biopsy GU."
        ),
        "hashtags": ["#MedicoHelp", "#GeneralSurgery", "#MBBS", "#NEETPG", "#OneLiner", "#PUD"],
    },
]
