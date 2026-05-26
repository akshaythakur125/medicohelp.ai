# Content Architecture

## Overview

The MedicoHelp.ai content system is a self-contained pipeline for generating and delivering NEET-PG/INI-CET revision content to Telegram. It combines a static library of hand-authored MBBS topics with an adaptive engine that applies spaced repetition (SM-2-inspired), weak-topic resurfacing, and MCQ variation. The system operates on a 4-phase daily cycle (morning, afternoon, evening, nightly) with 12 post lanes across 2 full cycles per day.

Content originates from two sources: (1) 19 Python files in `content/` define ~190 hand-authored topics across 8 static formats, loaded by `ContentLibrary` as a fallback/pool; (2) AI generation via OpenAI/Gemini/Anthropic produces richer items such as `clinical_case`, `image_based_question`, and `practical_viva`. The `SmartContentEngine` orchestrates selection, variation, performance tracking, and weak-topic detection, while the `ContentFormatter` renders everything into Telegram HTML. Every generated post is logged to JSONL, and learner performance is persisted for adaptive scheduling.

## Content Library

- **Location:** `content/` directory
- **Structure:** 19 subject files (`anatomy.py`, `physiology.py`, ..., `anesthesiology.py`), each defining 10 `GeneratedContent` dicts in a `TOPICS` list
- **Formats per file (8):** `rapid_revision`, `mcq`, `concise_notes`, `pyq_concept`, `mnemonic`, `flashcard`, `true_false`, `one_liner_recall`
- **Format:** Each topic is a Python dict with keys `title`, `subject`, `content_format`, `poster_text`, `caption`, `high_yield_takeaway`, `hashtags`, plus format-specific keys like `question`, `options`, `correct_answer`, `explanation`
- **Loading:** `ContentLibrary` in `content/loader.py` — imports each module dynamically via `importlib`, instantiates `GeneratedContent(**t)` for each dict, and indexes by `Subject` key
- **Access:** `get_library()` returns a singleton (`lru_cache`); `pool(subject, content_format)` returns filtered lists; `get(subject, format)` returns a random item with cross-subject fallback

## Content Types and Mapping

| ContentFormat Enum | Description | PostLane |
|---|---|---|
| `mcq` | Multiple-choice question with 4 options, correct answer, explanation | `poll_quiz`, `daily_pack`, `mcq_variant` |
| `image_based_question` | MCQ with a visual/radiograph description and labelled findings | `image_based` |
| `concise_notes` | Structured bullet-point notes on a topic | (variation source → `clinical_case`) |
| `clinical_case` | Clinical vignette with patient presentation + management question | (generated via variation) |
| `rapid_revision` | Short high-yield summary for quick recall | `quick_revision`, `weak_topic_recall` |
| `practical_viva` | Oral-exam style question with answer framework | (AI-generated) |
| `exam_news_update` | Latest NEET-PG/INI-CET exam news | `exam_news` |
| `residency_survival_tip` | Practical residency advice | `residency_tip` |
| `pyq_concept` | Previous-year question pattern analysis | `pyq_concept` |
| `flashcard` | Question-on-front, answer-on-back card | `flashcard` |
| `true_false` | True/false statement with explanation | `true_false` |
| `one_liner_recall` | Fill-in-the-blank one-liner | `one_liner_recall` |
| `mnemonic` | Memory aid with clinical hook | `mnemonic` |

## SmartContentEngine

The `SmartContentEngine` (`app/services/content_engine.py`) is the adaptive core.

### Tracking (SM-2–inspired)

- **`logs/performance.json`** — maps `title → { correct, incorrect, last_seen, subject }`. Updated every time learner performance is recorded via `record_performance()`.
- **`logs/topic_history.json`** — maps `title → ISO timestamp` of last send. Used for spaced-repetition cooldown checks.
- **Cooldown:** Default 7 days; weak topics (accuracy < 0.6, ≥3 attempts) get 3 days.
- **Performance decay threshold:** 30 days before a topic is considered stale.

### Generators

| Method | Input | Output |
|---|---|---|
| `generate(subject, format)` | Subject + format | Returns item from library via spaced repetition, or generates a variation |
| `generate_variate_mcq(subject, difficulty)` | Subject | Picks an existing MCQ, rewrites stem (synonym swaps), shuffles options, enriches with wrong-option analysis |
| `generate_flashcard(subject)` | Subject | Extracts Q&A from `rapid_revision` or `concise_notes` library items |
| `generate_true_false(subject)` | Subject | Extracts a factual statement from `high_yield_takeaway`, returns TRUE/FALSE |
| `generate_one_liner(subject)` | Subject | Blanks the middle word of `high_yield_takeaway` for fill-in recall |
| `generate_daily_pack(count)` | Count (default 5) | Builds a burst of 5 items across random subjects, cycling through MCQ, rapid_revision, true_false, flashcard, one_liner_recall |

### MCQ Variation

`generate_variate_mcq` in `_mcq_variate_stem()` applies 10 regex synonym replacements (e.g., "presents with" → "comes with complaints of", "most likely" → "most probable"). `_mcq_variate_options()` shuffles the 4 options, re-labels them A–D, and inserts the correct answer at a random position. The result is validated via `validate_mcq_vignette()` and enriched via `enrich_mcq_with_analysis()`.

### Vignette Validation

`validate_mcq_vignette()` enforces:
- 3–7 clinical sentences (split on ". ")
- At least 2 of 5 clinical indicators (`year-old`, `presents`, `history`, `examination`, `complaints`)
- At least 4 options and a correct answer present

### Wrong-Option Enrichment

`enrich_mcq_with_analysis()` appends a `"Why other options are wrong"` section to the explanation, labelling each distractor with a generic "This option is incorrect." note.

### Difficulty Assignment

`difficulty_for_topic(title)` reads performance history:
- Fewer than 3 attempts → `"moderate"`
- Accuracy < 40% → `"exam_level"`
- Accuracy 40–70% → `"moderate"`
- Accuracy ≥ 70% → `"easy"`

### Weak Topic Detection

`weak_topics(threshold=0.6, min_attempts=3)` returns topics with below-threshold accuracy, sorted ascending by accuracy. Used by the `nightly_weak_topic` slot.

## Post Lanes

| PostLane | ContentFormat | Notes |
|---|---|---|
| `image_based` | `image_based_question` | Requires visual description + labels |
| `pyq_concept` | `pyq_concept` | Previous-year pattern analysis |
| `quick_revision` | `rapid_revision` | Short high-yield notes |
| `residency_tip` | `residency_survival_tip` | Uses `NewsTopic.residency` |
| `exam_news` | `exam_news_update` | Uses `NewsTopic.neet_pg` or `inicet` |
| `poll_quiz` | `mcq` | Standard MCQ poll |
| `flashcard` | `flashcard` | Q/A with spoiler reveal |
| `mnemonic` | `mnemonic` | Memory aid |
| `daily_pack` | `mcq` | Burst of 5 items (mixed formats, same lane) |
| `mcq_variant` | `mcq` | Varied MCQ from existing pool |
| `weak_topic_recall` | `rapid_revision` | Revisits worst-performing topics |
| `true_false` | `true_false` | Boolean statement |
| `one_liner_recall` | `one_liner_recall` | Fill-in-the-blank |

## Slot Types (4-Phase Day)

| SlotType | Time (approx) | Lane | Description |
|---|---|---|---|
| `morning_revision` | 08:00 | `quick_revision` | Rapid revision note |
| `afternoon_mcq` | 14:00 | `mcq_variant` | Varied MCQ |
| `evening_revision` | 20:00 | `flashcard` | Flashcard recall |
| `nightly_weak_topic` | Pre-bed | `weak_topic_recall` | Weak topic resurfacing |

Each slot produces 1 post. The 12-lane `_WEIGHTED_LANES` list provides 2 full cycles per day if using the cursor-based sequential mode instead of slot-type mapping.

## Content Strategy

**`ContentStrategy`** (`app/services/content_strategy.py`):

- **Sequential mode:** A cursor cycles through a 12-element `_WEIGHTED_LANES` list, with subject rotating on each step. Difficulty is drawn from `_DIFFICULTY_WEIGHTS` (30% easy, 40% moderate, 30% exam-level).
- **Slot-type mode:** `_plan_slot()` maps each `SlotType` to a specific `PostLane` (morning → quick_revision, afternoon → mcq_variant, evening → flashcard, nightly → weak_topic_recall). Subject still rotates round-robin.
- **News lanes:** `residency_tip` and `exam_news` bypass subjects entirely and use `NewsTopic`.
- **Format mapping:** `_FORMAT_MAP` translates each `PostLane` to its `ContentFormat`; `weak_topic_recall` maps to `rapid_revision`, `poll_quiz`/`daily_pack`/`mcq_variant` all map to `mcq`.

## Quality Gate

**`ContentQualityGate`** (`app/services/quality.py`) validates `image_based_question` content:

| Rule | Requirement |
|---|---|
| `visual_description` | ≥ 30 characters, must describe a specific medical image |
| `visual_labels` | ≥ 3 labels |
| `question` | 6–8 line stem (by lines or sentence count) |
| `options` | ≥ 4 |
| `correct_answer` | Present |
| `explanation` | ≥ 180 characters |
| `relevance_rationale` | ≥ 40 characters |
| `image_answerability` | ≥ 40 characters |
| Explanation-image linkage | At least one `visual_label` must appear in the explanation |

Raises `ContentQualityError` on failure. Only `image_based_question` is validated; other formats pass through.

## Formatting Pipeline

**`ContentFormatter`** (`app/services/formatter.py`) converts a `GeneratedContent` model into a Telegram HTML string:

1. **Header:** `{subject_emoji} <b>{FORMAT_LABEL}: {Subject}</b>`
2. **Body dispatcher:** Routes to format-specific builder:
   - `mcq` / `image_based_question` — question + labelled options + spoiler-wrapped answer/explanation
   - `clinical_case` — case vignette + spoiler-wrapped next-step/discussion
   - `flashcard` — front question + spoiler-wrapped answer
   - `true_false` — statement + spoiler-wrapped TRUE/FALSE
   - `one_liner_recall` — fill-in stem + spoiler-wrapped answer
   - `mnemonic` — poster text + caption
   - `rapid_revision` / `concise_notes` / `pyq_concept` — extracted bullet-point breakdown
   - `residency_survival_tip` / `exam_news_update` — caption + source link
3. **High-yield takeaway:** Appended as `⚡ <b>Key Point:</b>` (excluded for news/residency tips)
4. **Hashtags:** Joined and appended at the bottom
5. **Truncation:** Capped at 4096 characters (Telegram message limit)
6. **Escaping:** `&`, `<`, `>` escaped for HTML safety

## Data Flow

```
┌──────────────────────────────────────────────────────────────────────┐
│                        SCHEDULER (APScheduler)                       │
│    Runs every `post_interval_hours` or at `post_schedule_times`     │
└──────────┬───────────────────────────────────────────────────────────┘
           │ trigger_post()
           ▼
┌──────────────────────┐    SlotType (morning/afternoon/evening/night)
│  ContentStrategy     │────► 12-lane weighted rotation
│  .next_post(slot)    │       or slot-type → lane mapping
└──────────┬───────────┘
           │ PlannedPost(lane, subject, format, difficulty, news_topic)
           ▼
┌──────────────────────────────┐
│  SmartContentEngine          │
│                              │
│  ┌─ generate(subject,fmt)   │──── Library pool → spaced repetition
│  │   └─ _get_with_spaced_   │     (cooldown check, weak-topic bias)
│  │      repetition()        │
│  │   └─ _generate_          │──── Variation fallback
│  │      variation()         │     (rapid↔pyq, mcq↔rapid, notes↔case)
│  │                              │
│  └─ generate_variate_mcq()  │──── Stem rewording + option shuffle
│  └─ generate_flashcard()    │
│  └─ generate_true_false()   │
│  └─ generate_one_liner()    │
│  └─ generate_daily_pack()   │
│                              │
│  ┌─ validate_mcq_vignette() │──── 3-7 sentences, clinical keywords
│  └─ enrich_mcq_with_        │──── Wrong-option analysis
│     analysis()              │
└──────────┬───────────────────┘
           │ GeneratedContent model
           ▼
┌──────────────────────────────┐
│  ContentQualityGate.validate()│──── Only for image_based_question
│  (raises ContentQualityError │     (visual desc, labels, question,
│   on failure)                │      options, answer, explanation...)
└──────────┬───────────────────┘
           ▼
┌──────────────────────────────┐
│  ContentFormatter            │
│  .format_for_telegram()      │──── Telegram HTML (emoji+header+
│                              │     format-specific body + key point
└──────────┬───────────────────┘     + hashtags, truncated to 4096)
           │ formatted HTML string
           ▼
┌──────────────────────────────┐
│  Telegram Poster Service     │
│  • Post to channel           │──── Caption = formatted HTML
│  • (Optional image poster)   │     text_only_mode = True by default
└──────────┬───────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────────────────┐
│  Persistence                                                   │
│  • logs/generated_posts.jsonl — full GeneratedContent as JSON  │
│  • logs/topic_history.json   — title → last-sent timestamp      │
│  • logs/performance.json     — title → {correct,incorrect,     │
│                                          last_seen, subject}    │
└─────────────────────────────────────────────────────────────────┘
```

## Persistence

| File | Format | Purpose |
|---|---|---|
| `logs/generated_posts.jsonl` | JSON Lines (one JSON object per line) | Full history of every generated and/or posted content |
| `logs/performance.json` | JSON dict `{title: {correct, incorrect, last_seen, subject}}` | Per-topic accuracy tracking for weak-topic detection and difficulty assignment |
| `logs/topic_history.json` | JSON dict `{title: ISO-timestamp}` | Last-sent timestamps for spaced-repetition cooldown (default 7 days, weak topics 3 days) |

All persistence files live under `logs/` (configured via `Settings.logs_dir`). Files are created lazily on first write.
