"""AI-powered Instagram carousel content generator for medicohelp.ai."""

from __future__ import annotations

import json
import logging
import random
import re

from app.services.carousel_generator import CarouselSpec

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Topic bank  (rotated randomly; 3x daily = ~20 topics per week)
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
# Generator
# ---------------------------------------------------------------------------


class InstagramContentGenerator:
    """Generates structured carousel content using AI (Anthropic) or mock data."""

    def __init__(self, settings) -> None:
        self.settings = settings
        self._anthropic_client = None
        self._init_ai_client()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def generate_carousel(self, topic: str | None = None) -> CarouselSpec:
        """
        Generate a CarouselSpec for *topic*.

        If *topic* is None a random topic is chosen from OPHTHO_TOPICS.
        Falls back to a mock carousel if AI is not configured or the call fails.
        """
        if topic is None:
            topic = random.choice(OPHTHO_TOPICS)

        logger.info("Generating Instagram carousel for topic: %s", topic)

        if self._anthropic_client is None:
            logger.info("AI client not configured, using mock carousel")
            return self._mock_carousel(topic)

        try:
            return await self._call_ai(topic)
        except Exception as exc:
            logger.warning("AI call failed (%s), falling back to mock carousel", exc)
            return self._mock_carousel(topic)

    # ------------------------------------------------------------------
    # AI interaction
    # ------------------------------------------------------------------

    async def _call_ai(self, topic: str) -> CarouselSpec:
        """Call Anthropic Claude to generate carousel JSON, then parse it."""
        import asyncio

        prompt = self._build_prompt(topic)
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
        )

    # ------------------------------------------------------------------
    # Prompt builder
    # ------------------------------------------------------------------

    def _build_prompt(self, topic: str) -> str:
        return f"""You are Dr. Akshay Thakur, MS Ophthalmologist practising in India. \
Create an educational Instagram carousel post about: {topic}

Return ONLY valid JSON (no markdown, no preamble) with exactly this structure:

{{
  "cover_title": "SHORT BOLD TITLE IN CAPS (max 8 words)",
  "cover_subtitle": "Compelling subtitle in sentence case (max 12 words)",
  "points": [
    {{
      "label": "POINT LABEL IN CAPS",
      "body": "2-3 sentence explanation in simple patient-friendly language. Include one practical tip.",
      "icon_emoji": "single relevant emoji"
    }}
  ],
  "caption": "Engaging 2-3 sentence Instagram caption as Dr. Akshay Thakur with a call-to-action.",
  "hashtags": ["EyeHealth", "Ophthalmology", "DrAkshayThakur", "MSOphthalmologist", "VisionCare", "IndiaEyeCare"]
}}

Rules:
- Provide exactly 4 to 5 points.
- Each point body must be 2-3 sentences, plain language, no jargon.
- Always include DrAkshayThakur and MSOphthalmologist in the hashtags array.
- cover_title must be ALL CAPS and under 8 words.
- Return only the raw JSON object, nothing else.
"""

    # ------------------------------------------------------------------
    # Mock / fallback
    # ------------------------------------------------------------------

    def _mock_carousel(self, topic: str) -> CarouselSpec:
        """Hardcoded digital eye strain carousel — safe fallback when AI is unavailable."""
        return CarouselSpec(
            cover_title="PROTECT YOUR EYES FROM SCREENS",
            cover_subtitle="Digital eye strain is more common than you think",
            points=[
                {
                    "label": "FOLLOW THE 20-20-20 RULE",
                    "body": (
                        "Every 20 minutes look at something 20 feet away for 20 seconds. "
                        "This simple habit relaxes the focusing muscles inside your eye. "
                        "Set a phone reminder to build the habit."
                    ),
                    "icon_emoji": "⏱",
                },
                {
                    "label": "BLINK MORE OFTEN",
                    "body": (
                        "Screen users blink only 5-7 times per minute instead of the normal 15-20. "
                        "Reduced blinking dries the eye surface and causes irritation. "
                        "Consciously blink fully and frequently."
                    ),
                    "icon_emoji": "\U0001f441",
                },
                {
                    "label": "ADJUST SCREEN BRIGHTNESS",
                    "body": (
                        "Match your screen brightness to the ambient light around you. "
                        "Screens that are too bright or too dark force your eyes to work harder. "
                        "Night mode after sunset reduces blue-light exposure."
                    ),
                    "icon_emoji": "\U0001f31f",
                },
                {
                    "label": "KEEP THE RIGHT DISTANCE",
                    "body": (
                        "Hold your screen at arm’s length — roughly 50-70 cm from your eyes. "
                        "The top of the screen should be at or slightly below eye level. "
                        "This reduces strain on your neck and eye muscles."
                    ),
                    "icon_emoji": "\U0001f4cf",
                },
                {
                    "label": "VISIT YOUR EYE DOCTOR ANNUALLY",
                    "body": (
                        "Uncorrected refractive errors make digital eye strain far worse. "
                        "An annual eye exam catches changes in your prescription early. "
                        "Computer glasses with anti-reflective coating can help significantly."
                    ),
                    "icon_emoji": "\U0001f3e5",
                },
            ],
            caption=(
                "Screens are unavoidable today — but digital eye strain doesn’t have to be. "
                "These five tips have helped thousands of my patients work comfortably all day. "
                "Save this post and share it with someone who stares at screens all day! \U0001f4bb\U0001f441"
            ),
            hashtags=[
                "EyeHealth",
                "DigitalEyeStrain",
                "DrAkshayThakur",
                "MSOphthalmologist",
                "VisionCare",
                "ScreenTime",
                "202020Rule",
                "IndiaEyeCare",
                "Ophthalmology",
            ],
        )

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
