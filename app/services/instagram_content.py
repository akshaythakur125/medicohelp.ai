"""AI-powered Instagram carousel content generator for medicohelp.ai.

5 rotating post formats + topic dedup ring buffer for maximum algorithmic reach.
"""

from __future__ import annotations

import json
import logging
import random
import re
from collections import deque

from app.services.carousel_generator import CarouselSpec

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Topic bank  (rotated randomly; dedup ring buffer prevents repeats)
# ---------------------------------------------------------------------------

OPHTHO_TOPICS = [
    "common causes of blurry vision",
    "signs you need glasses",
    "digital eye strain prevention",
    "glaucoma warning signs",
    "cataract symptoms and treatment",
    "dry eye syndrome tips",
    "diabetic eye disease and prevention",
    "children's eye health milestones",
    "UV protection for eyes",
    "floaters and flashes — when to worry",
    "age-related macular degeneration",
    "eye nutrition myths vs facts",
    "when to see an eye doctor urgently",
    "20-20-20 rule and screen time",
    "contact lens safety tips",
    "pink eye types and treatment",
    "night blindness causes and care",
    "eye allergy symptoms and relief",
    "corneal problems explained",
    "LASIK — who is a good candidate",
]

# ---------------------------------------------------------------------------
# 5 rotating post formats — thumb-stopping hooks
# ---------------------------------------------------------------------------

POST_FORMATS = [
    "numbered_warning",
    "myth_buster",
    "shocking_stat",
    "question_hook",
    "warning",
]

POST_FORMAT_LABELS = {
    "numbered_warning": "⚠️ Numbered Warning",
    "myth_buster": "❌ Myth Buster",
    "shocking_stat": "📊 Shocking Stat",
    "question_hook": "❓ Question Hook",
    "warning": "🚨 Warning",
}

# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------


class InstagramContentGenerator:
    """Generates structured carousel content using AI (Anthropic) or mock data.

    Features:
      - 5 rotating post formats picked randomly each call
      - Topic dedup ring buffer (no repeat within last 10 posts)
      - Scroll-stopping hooks designed for Indian patient audiences
    """

    _recent_topics: deque = deque(maxlen=10)  # class-level dedup buffer

    def __init__(self, settings) -> None:
        self.settings = settings
        self._anthropic_client = None
        self._init_ai_client()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def generate_carousel(self, topic: str | None = None) -> CarouselSpec:
        """Generate a CarouselSpec for *topic* using a random post format.

        If *topic* is None a random topic is chosen from OPHTHO_TOPICS,
        avoiding the last 10 posted topics.  Falls back to a mock carousel
        if AI is not configured or the call fails.
        """
        if topic is None:
            topic = self._pick_topic()

        fmt = random.choice(POST_FORMATS)
        logger.info("Generating Instagram carousel [%s]: %s", fmt, topic)

        if self._anthropic_client is None:
            logger.info("AI client not configured, using mock carousel")
            return self._mock_carousel(topic, fmt)

        try:
            return await self._call_ai(topic, fmt)
        except Exception as exc:
            logger.warning("AI call failed (%s), falling back to mock carousel", exc)
            return self._mock_carousel(topic, fmt)

    def _pick_topic(self) -> str:
        """Select a random topic not in the recent-topics ring buffer."""
        pool = [t for t in OPHTHO_TOPICS if t not in self._recent_topics]
        if not pool:
            pool = OPHTHO_TOPICS
        chosen = random.choice(pool)
        self._recent_topics.append(chosen)
        return chosen

    # ------------------------------------------------------------------
    # AI interaction
    # ------------------------------------------------------------------

    async def _call_ai(self, topic: str, fmt: str) -> CarouselSpec:
        """Call Anthropic Claude to generate carousel JSON, then parse it."""
        import asyncio

        prompt = self._build_prompt(topic, fmt)
        loop = asyncio.get_event_loop()
        raw_response = await loop.run_in_executor(None, self._sync_ai_call, prompt)
        return self._parse_response(raw_response, topic)

    def _sync_ai_call(self, prompt: str) -> str:
        """Synchronous Anthropic API call (runs in a thread executor)."""
        model = getattr(self.settings, "ai_model", "claude-haiku-4-5-20251001")
        message = self._anthropic_client.messages.create(
            model=model,
            max_tokens=1500,
            messages=[{"role": "user", "content": prompt}],
        )
        return message.content[0].text

    def _parse_response(self, raw: str, topic: str) -> CarouselSpec:
        """Extract JSON payload from AI response and build a CarouselSpec."""
        json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", raw, re.DOTALL)
        if json_match:
            raw_json = json_match.group(1)
        else:
            brace_match = re.search(r"\{.*\}", raw, re.DOTALL)
            if brace_match:
                raw_json = brace_match.group(0)
            else:
                raise ValueError("No JSON object found in AI response")

        data = json.loads(raw_json)
        return CarouselSpec(
            cover_title=data.get("cover_title", topic.upper()),
            cover_subtitle=data.get("cover_subtitle", "Expert tips from Dr. Akshay Thakur"),
            points=data.get("points", []),
            caption=data.get("caption", ""),
            hashtags=data.get(
                "hashtags", ["EyeHealth", "DrAkshayThakur", "MSOphthalmologist"]
            ),
            first_comment=data.get("first_comment", ""),
        )

    # ------------------------------------------------------------------
    # Prompt builder  —  format-aware, structure-driven
    # ------------------------------------------------------------------

    def _build_prompt(self, topic: str, fmt: str) -> str:
        format_label = POST_FORMAT_LABELS[fmt]
        return f"""You are Dr. Akshay Thakur, MS Ophthalmologist practising in India.

Create an Instagram carousel about: {topic}
Post format: {format_label}

Return ONLY valid JSON (no markdown, no preamble) with this exact structure:

{{
  "cover_title": "SCROLL-STOPPING HOOK IN CAPS (max 7 words, start with a number or power word like Warning, Myth, Secret, Signs)",
  "cover_subtitle": "One-line hook in sentence case that creates curiosity (max 10 words)",
  "points": [
    {{
      "label": "THE PROBLEM",
      "body": "One shocking statistic or a relatable Indian scenario. End with: Here's what most people don't realize..."
    }},
    {{
      "label": "THE KEY INSIGHT",
      "body": "The single most save-worthy fact. Specific, surprising, and directly relevant to Indian patients."
    }},
    {{
      "label": "TIP 1",
      "body": "Actionable daily-life tip for Indian patients. Easy to do, no expensive equipment needed."
    }},
    {{
      "label": "TIP 2",
      "body": "Second actionable tip. Practical, specific, and tailored for Indian households."
    }}
  ],
  "caption": "First line = matches cover energy (NEVER start with Welcome or Today). 2-3 sentences explaining the topic simply. End with: Save this 💾 Then ask a comment-bait question.",
  "hashtags": ["DrAkshayThakur", "MSOphthalmologist", "EyeHealth", "VisionCare", "IndiaEyeCare", "Ophthalmology", "EyeTips", "HealthyEyes", "EyeDoctor", "BlurryVision"],
  "first_comment": "Rephrased version of the caption's comment-bait question + 10 niche hashtags: EyeSpecialist, OphthalmologyEducation, DoctorOfInstagram, MedicalAdvice, EyeDisease, VisionHealth, IndianHealthcare, EyeClinic, EyeSurgeon, MedEd"
}}

RULES:
- Provide exactly 4 points: THE PROBLEM, THE KEY INSIGHT, TIP 1, TIP 2.
- Each body must be 2-3 sentences, plain language, NO medical jargon.
- Use {format_label} energy:
  • If numbered_warning — start cover with a number (e.g. "5 WARNING SIGNS...")
  • If myth_buster — start cover with "MYTH" or "FACT"
  • If shocking_stat — start cover with a percentage or number
  • If question_hook — start cover as a question
  • If warning — start cover with "WARNING"
- Caption must end with "Save this 💾" and a comment-bait question (e.g. "How many hours do you spend on screens? 👇")
- hashtags must have exactly 10, always including DrAkshayThakur and MSOphthalmologist.
- first_comment must be a rephrased version of the caption question + the exact 10 hashtags: EyeSpecialist, OphthalmologyEducation, DoctorOfInstagram, MedicalAdvice, EyeDisease, VisionHealth, IndianHealthcare, EyeClinic, EyeSurgeon, MedEd
- Return ONLY the raw JSON object, nothing else.
"""

    # ------------------------------------------------------------------
    # Mock / fallback  — 3 rotating variants matching new format
    # ------------------------------------------------------------------

    def _mock_carousel(self, topic: str, fmt: str | None = None) -> CarouselSpec:
        """Hardcoded fallback carousel — matches new format structure.

        Three variants rotate to avoid repetitive fallback content.
        """
        if fmt is None:
            fmt = random.choice(POST_FORMATS)

        variants = {
            "numbered_warning": CarouselSpec(
                cover_title="5 WARNING SIGNS OF GLAUCOMA",
                cover_subtitle="The silent thief of sight — are you at risk?",
                points=[
                    {
                        "label": "THE PROBLEM",
                        "body": (
                            "90% of glaucoma cases in India go undetected until permanent damage is done. "
                            "Most people assume they need symptoms to have a problem. "
                            "Here's what most people don't realize..."
                        ),
                    },
                    {
                        "label": "THE KEY INSIGHT",
                        "body": (
                            "Glaucoma damages the optic nerve slowly and painlessly — by the time you notice "
                            "vision loss, 40% of nerve fibres may already be gone. "
                            "Annual eye pressure checks after age 35 are your best defence."
                        ),
                    },
                    {
                        "label": "TIP 1",
                        "body": (
                            "Book a comprehensive eye exam every year after age 35, even if your vision feels fine. "
                            "Most city clinics offer this for under ₹500."
                        ),
                    },
                    {
                        "label": "TIP 2",
                        "body": (
                            "If you have a family history of glaucoma or diabetes, start annual checks at age 30. "
                            "Early detection can save your sight for life."
                        ),
                    },
                ],
                caption=(
                    "Glaucoma doesn't send a warning — that's why it's called the silent thief. "
                    "But here's the good news: caught early, it's completely manageable. "
                    "Save this 💾\nWhen was your last eye check-up? 👇"
                ),
                hashtags=[
                    "DrAkshayThakur", "MSOphthalmologist", "Glaucoma", "EyeHealth",
                    "VisionCare", "IndiaEyeCare", "BlindnessPrevention", "EyeTips",
                    "HealthyEyes", "SilentThiefOfSight",
                ],
                first_comment=(
                    "When was YOUR last eye check-up? Comment below and let's normalise "
                    "annual eye exams in India! 👇\n\n"
                    "#EyeSpecialist #OphthalmologyEducation #DoctorOfInstagram #MedicalAdvice "
                    "#EyeDisease #VisionHealth #IndianHealthcare #EyeClinic #EyeSurgeon #MedEd"
                ),
            ),
            "myth_buster": CarouselSpec(
                cover_title="MYTH: CARROTS FIX YOUR VISION",
                cover_subtitle="What actually works for healthy eyes",
                points=[
                    {
                        "label": "THE PROBLEM",
                        "body": (
                            "Your mother told you to eat carrots for good eyesight — but vitamin A deficiency "
                            "is rare in India. Most vision problems have nothing to do with carrots. "
                            "Here's what most people don't realize..."
                        ),
                    },
                    {
                        "label": "THE KEY INSIGHT",
                        "body": (
                            "Vitamin A from carrots helps night vision — but it won't fix nearsightedness, "
                            "cataracts, or glaucoma. The real heroes for Indian eyes are "
                            "lutein (found in spinach and methi) and omega-3s (from fish and flaxseeds)."
                        ),
                    },
                    {
                        "label": "TIP 1",
                        "body": (
                            "Add one bowl of palak or methi to your daily meals. These green leafy vegetables "
                            "are rich in lutein — nature's built-in sunglasses for your retina."
                        ),
                    },
                    {
                        "label": "TIP 2",
                        "body": (
                            "Wear UV-protective sunglasses when stepping out in Indian summers. "
                            "Prolonged UV exposure accelerates cataract formation — and no, carrots won't undo that."
                        ),
                    },
                ],
                caption=(
                    "Carrots are good — but they're not a cure-all. Your eyes need real nutrition "
                    "and protection, especially in the Indian sun. "
                    "Save this 💾\nWhat eye myth did you believe growing up? 👇"
                ),
                hashtags=[
                    "DrAkshayThakur", "MSOphthalmologist", "MythBuster", "EyeHealth",
                    "NutritionForEyes", "IndiaEyeCare", "VisionCare", "EyeTips",
                    "HealthyEyes", "Lutein",
                ],
                first_comment=(
                    "My grandma also told me to eat carrots! What eye myth did YOU "
                    "grow up believing? Spill in the comments! 👇\n\n"
                    "#EyeSpecialist #OphthalmologyEducation #DoctorOfInstagram #MedicalAdvice "
                    "#EyeDisease #VisionHealth #IndianHealthcare #EyeClinic #EyeSurgeon #MedEd"
                ),
            ),
            "shocking_stat": CarouselSpec(
                cover_title="70% OF BLINDNESS IN INDIA IS AVOIDABLE",
                cover_subtitle="Simple steps that can save your sight",
                points=[
                    {
                        "label": "THE PROBLEM",
                        "body": (
                            "India is home to 20% of the world's blind population — and 7 in 10 cases "
                            "could have been prevented with basic eye care. "
                            "Here's what most people don't realize..."
                        ),
                    },
                    {
                        "label": "THE KEY INSIGHT",
                        "body": (
                            "Untreated cataract causes 60% of blindness in India, but cataract surgery "
                            "costs as little as ₹8,000 under government schemes. "
                            "The surgery takes 15 minutes and restores vision the next day."
                        ),
                    },
                    {
                        "label": "TIP 1",
                        "body": (
                            "If you're over 50 and notice cloudy or blurry vision, visit an eye camp or "
                            "district hospital near you. Free cataract surgeries are available under "
                            "the National Blindness Control Programme."
                        ),
                    },
                    {
                        "label": "TIP 2",
                        "body": (
                            "Don't wait for vision loss — get a free eye screening at any government "
                            "hospital. Early detection of cataract, glaucoma, and diabetic eye disease "
                            "can literally save your sight."
                        ),
                    },
                ],
                caption=(
                    "7 in 10 cases of blindness in India can be prevented. "
                    "Share this with your parents and grandparents — it might save their sight. "
                    "Save this 💾\nWhen did your family last get an eye check-up? 👇"
                ),
                hashtags=[
                    "DrAkshayThakur", "MSOphthalmologist", "BlindnessPrevention", "EyeHealth",
                    "IndiaEyeCare", "CataractAwareness", "VisionCare", "EyeTips",
                    "HealthyEyes", "NationalBlindnessProgramme",
                ],
                first_comment=(
                    "When did your parents last visit an eye doctor? Tag them below — "
                    "it could save their sight! 👇\n\n"
                    "#EyeSpecialist #OphthalmologyEducation #DoctorOfInstagram #MedicalAdvice "
                    "#EyeDisease #VisionHealth #IndianHealthcare #EyeClinic #EyeSurgeon #MedEd"
                ),
            ),
        }

        base = variants.get(fmt, variants["shocking_stat"])
        return base

    # ------------------------------------------------------------------
    # Initialisation
    # ------------------------------------------------------------------

    def _init_ai_client(self) -> None:
        """Initialise the Anthropic client if an API key is available."""
        api_key = getattr(self.settings, "anthropic_api_key", None)
        if not api_key:
            logger.debug("No Anthropic API key; AI carousel generation disabled")
            return
        try:
            import anthropic

            self._anthropic_client = anthropic.Anthropic(api_key=api_key)
            logger.debug("Anthropic client initialised for Instagram content generation")
        except ImportError:
            logger.warning("anthropic package not installed; AI carousel generation disabled")
