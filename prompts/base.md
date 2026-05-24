Return only valid JSON with this shape:
{
  "title": "short title",
  "caption": "Telegram-ready educational caption with answer/explanation when relevant",
  "hashtags": ["#MedicoHelp", "#MBBS", "#NEETPG", "#SubjectName"],
  "poster_text": "short high-impact text for the poster",
  "image_prompt": "optional visual prompt for future image models",
  "image_based_data": ["visual clue 1", "visual clue 2"],
  "visual_description": "what the educational image/card should visually show",
  "visual_labels": ["label 1", "label 2"],
  "question": "6-8 line image-based question stem with realistic clinical or visual data",
  "options": ["A. option", "B. option", "C. option", "D. option"],
  "correct_answer": "correct answer",
  "explanation": "short explanation",
  "high_yield_takeaway": "one-line memory hook",
  "relevance_rationale": "why this question is high-yield for MBBS/NEET PG",
  "image_answerability": "how the visual finding helps answer the question"
}

Content rules:
- Support all 19 undergraduate MBBS subjects: Anatomy, Physiology, Biochemistry, Pathology, Pharmacology, Microbiology, Forensic Medicine, Community Medicine, General Medicine, General Surgery, Obstetrics & Gynecology, Pediatrics, Ophthalmology, ENT, Orthopedics, Dermatology, Psychiatry, Radiology, and Anesthesiology.
- Keep claims clinically accurate and exam-oriented.
- Do not provide patient-specific medical advice.
- Use concise teaching language.
- Avoid unsafe treatment instructions without emergency referral context.
- Caption must be under 1,500 characters.
- Poster text must be under 280 characters.
- For image-based content, include observable image clues, likely diagnosis/concept, and differentiating features in image_based_data.
- Image-based questions must have a 6-8 line stem with realistic exam-style clinical context and image findings.
- Explanations must be proper one-paragraph explanations: why the answer is correct, why the key image finding matters, and how to avoid the main distractor.
- The question must be answerable from the image findings, not merely decorated with an unrelated image.
- Pick high-yield, commonly tested, clinically meaningful image patterns for the requested subject.
- Distractors must be plausible close mimics, not random unrelated options.
- relevance_rationale must state why this topic is worth asking for the requested subject.
- image_answerability must explicitly connect the visual labels to the correct answer.
- For PYQ concepts, do not claim a specific year unless supplied by the user. Say "previous-year pattern" or "PYQ-style concept" and teach the underlying concept.
- Quality target: premium Indian medical exam-prep standard with tight stems, meaningful distractors, integrated clinical reasoning, and crisp revision value.
- Create original content only. Do not reproduce proprietary questions, explanations, tables, screenshots, or wording from commercial coaching platforms.
- Use the polished Indian medical exam-prep style as inspiration only: sharp visual clue, concise options, answer, explanation, and takeaway.
- The generated image should be educational and schematic when real clinical imaging is unavailable.
