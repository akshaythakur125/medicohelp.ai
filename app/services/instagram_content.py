"""AI-powered Instagram carousel content generator for medicohelp.ai."""

from __future__ import annotations

import json
import logging
import random
import re
from collections import deque

from app.services.carousel_generator import CarouselSpec

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Topic bank  (rotated; 3x daily = ~20 unique topics per week)
# ---------------------------------------------------------------------------

OPHTHO_TOPICS = [
    "common causes of blurry vision",
    "signs you need glasses urgently",
    "digital eye strain and screen damage",
    "glaucoma — the silent thief of sight",
    "cataract symptoms and modern treatment",
    "dry eye syndrome and daily triggers",
    "diabetic eye disease prevention",
    "children's eye health warning signs",
    "UV damage and sunglasses facts",
    "floaters and flashes — when to panic",
    "age-related macular degeneration",
    "eye nutrition myths vs real science",
    "eye emergencies that can't wait",
    "20-20-20 rule and screen time",
    "contact lens safety mistakes",
    "pink eye — viral vs bacterial vs allergy",
    "night blindness causes and care",
    "eye allergy symptoms and relief",
    "corneal health and contact lens dangers",
    "LASIK — facts, myths, who qualifies",
]

# ---------------------------------------------------------------------------
# Rotating post formats — keeps feed variety high
# ---------------------------------------------------------------------------

_POST_FORMATS = [
    {
        "name": "numbered_warning",
        "cover_hint": "Use a number + urgent outcome. E.g.: '5 Warning Signs You May Lose Vision'",
        "cover_example": "5 SIGNS YOUR EYES NEED HELP NOW",
    },
    {
        "name": "myth_buster",
        "cover_hint": "Bust one widespread myth. E.g.: 'MYTH: Only Old People Get Glaucoma'",
        "cover_example": "THE EYE MYTH MOST INDIANS BELIEVE",
    },
    {
        "name": "shocking_stat",
        "cover_hint": "Lead with a shocking India-relevant percentage. E.g.: '80% OF BLINDNESS IS PREVENTABLE'",
        "cover_example": "80% OF EYE DAMAGE IS PREVENTABLE",
    },
    {
        "name": "question_hook",
        "cover_hint": "Ask a question the viewer will answer 'yes' to. Create a 'that could be me' moment.",
        "cover_example": "ARE YOU DAMAGING YOUR EYES DAILY?",
    },
    {
        "name": "warning",
        "cover_hint": "Use WARNING: + a surprising action people do daily without realising the damage.",
        "cover_example": "WARNING: STOP DOING THIS TO YOUR EYES",
    },
]


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------


class InstagramContentGenerator:
    """Generates structured carousel content using AI (Anthropic) or mock data."""

    def __init__(self, settings) -> None:
        self.settings = settings
        self._anthropic_client = None
        # Ring buffer — avoids repeating same topic in last 10 posts
        self._topic_history: deque[str] = deque(maxlen=10)
        self._init_ai_client()

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    async def generate_carousel(self, topic: str | None = None) -> CarouselSpec:
        """
        Generate a CarouselSpec for *topic*.

        If *topic* is None a fresh topic is chosen from OPHTHO_TOPICS,
        avoiding the last 10 used topics.
        Falls back to a mock carousel if AI is not configured or the call fails.
        """
        if topic is None:
            topic = self._pick_fresh_topic()

        post_format = random.choice(_POST_FORMATS)
        logger.info(
            "Generating Instagram carousel — topic: %s | format: %s",
            topic,
            post_format["name"],
        )

        self._topic_history.append(topic)

        if self._anthropic_client is None:
            logger.info("AI client not configured, using mock carousel")
            return self._mock_carousel(topic)

        try:
            return await self._call_ai(topic, post_format)
        except Exception as exc:
            logger.warning("AI call failed (%s), falling back to mock carousel", exc)
            return self._mock_carousel(topic)

    # ------------------------------------------------------------------
    # Topic selection
    # ------------------------------------------------------------------

    def _pick_fresh_topic(self) -> str:
        """Choose a topic not in the recent history ring buffer."""
        available = [t for t in OPHTHO_TOPICS if t not in self._topic_history]
        if not available:
            available = OPHTHO_TOPICS  # full reset if all used
        return random.choice(available)

    # ------------------------------------------------------------------
    # AI interaction
    # ------------------------------------------------------------------

    async def _call_ai(self, topic: str, post_format: dict) -> CarouselSpec:
        """Call Anthropic Claude to generate carousel JSON, then parse it."""
        import asyncio

        prompt = self._build_prompt(topic, post_format)
        loop = asyncio.get_event_loop()
        raw_response = await loop.run_in_executor(None, self._sync_ai_call, prompt)
        return self._parse_response(raw_response, topic)

    def _sync_ai_call(self, prompt: str) -> str:
        """Synchronous Anthropic API call (runs in a thread executor)."""
        model = getattr(self.settings, "ai_model", "claude-haiku-4-5-20251001")
        message = self._anthropic_client.messages.create(
            model=model,
            max_tokens=1800,
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

    def _build_prompt(self, topic: str, post_format: dict) -> str:
        return f"""You are a viral health content strategist writing for Dr. Akshay Thakur, \
MS Ophthalmologist practising in India. Create a SCROLL-STOPPING Instagram carousel about: {topic}

POST FORMAT TO USE: {post_format['name']}
COVER HOOK INSTRUCTION: {post_format['cover_hint']}
COVER EXAMPLE (adapt, do not copy): {post_format['cover_example']}

INSTAGRAM ALGORITHM RULES — FOLLOW THESE STRICTLY:
1. Cover title must STOP THE SCROLL: use a number, question, stat, warning, or power word.
2. Slide 2 = THE PROBLEM: open with a relatable scenario or shocking India-relevant stat.
   End with a teaser: "Here\'s what most people don\'t realise..."
3. Slide 3 = THE KEY INSIGHT: the single most save-worthy fact — specific, actionable, surprising.
4. Slides 4-5 = Actionable tips the reader can do TODAY.
5. Caption first line = same hook energy as the cover (this is what shows before \'more\' in the feed).
6. Caption must end with a direct question to drive comments.
7. Include "Save this" in the caption — saves are the highest-value algorithm signal.

Return ONLY valid JSON (no markdown fence, no preamble) with exactly this structure:

{{
  "cover_title": "VIRAL HOOK ALL CAPS MAX 8 WORDS — use number or power word",
  "cover_subtitle": "One sentence of curiosity or urgency — max 12 words",
  "points": [
    {{
      "label": "THE PROBLEM",
      "body": "Open with a shocking stat or relatable scenario an Indian patient would recognise. 2-3 short punchy sentences. Make them feel this affects them personally. End: 'Here\'s what most people don\'t realise...'",
      "icon_emoji": "⚠️"
    }},
    {{
      "label": "THE KEY INSIGHT",
      "body": "The single most important thing to know — the kind of info people screenshot and share. Specific, surprising, and actionable. 2-3 short sentences. This is the save-worthy slide.",
      "icon_emoji": "\U0001f4a1"
    }},
    {{
      "label": "WHAT TO DO TODAY",
      "body": "Specific action the reader can take immediately. No jargon. Practical for Indian daily life. 2-3 sentences.",
      "icon_emoji": "✅"
    }},
    {{
      "label": "COMMON MISTAKE TO AVOID",
      "body": "A widespread mistake that makes the problem worse. Why people do it + what to do instead. 2-3 short sentences.",
      "icon_emoji": "\U0001f3af"
    }}
  ],
  "caption": "HOOK LINE MATCHING COVER ENERGY — must grab attention in 1 sentence.\n\nValue teaser 2-3 lines: give them enough to feel they learned something, leave them wanting more.\n\n\U0001f4be Save this post — your future self will thank you.\n\n\U0001f447 [One specific question about the topic to drive comments — make it easy to answer]",
  "hashtags": ["DrAkshayThakur", "MSOphthalmologist", "EyeHealth", "OphthalmologyIndia", "VisionCare", "EyeCare", "HealthyEyes", "IndianDoctor", "EyeHealthTips", "SaveYourVision"]
}}

CRITICAL RULES:
- cover_title: ALL CAPS, max 8 words, must contain a number OR a power word (Warning, Secret, Truth, Myth, Mistake, Risk, Signs).
- points: exactly 4 items.
- body text: 2-3 sentences each, plain language, no medical jargon, relatable to Indian patients.
- caption: first line must be a hook — never start with 'Welcome', 'Today', 'In this post'.
- hashtags: 10 tags, always include DrAkshayThakur and MSOphthalmologist.
- Return ONLY the raw JSON object — nothing before or after it.
"""

    # ------------------------------------------------------------------
    # Mock / fallback
    # ------------------------------------------------------------------

    def _mock_carousel(self, topic: str) -> CarouselSpec:
        """Algorithm-optimised fallback carousel used when AI is unavailable."""
        return CarouselSpec(
            cover_title="5 SCREEN HABITS DESTROYING YOUR EYES",
            cover_subtitle="Most people do #3 every single day without knowing",
            points=[
                {
                    "label": "THE PROBLEM",
                    "body": (
                        "The average Indian now spends 7+ hours daily on screens. "
                        "Your eyes were never designed for this — and the damage builds silently. "
                        "Here's what most people don't realise..."
                    ),
                    "icon_emoji": "⚠️",
                },
                {
                    "label": "THE KEY INSIGHT",
                    "body": (
                        "Screen users blink only 3-5 times per minute — normal is 15-20. "
                        "That's 66% less blinking, leading to dry spots that permanently scratch your cornea over time. "
                        "A single conscious blink every 20 seconds can reverse this completely."
                    ),
                    "icon_emoji": "\U0001f4a1",
                },
                {
                    "label": "WHAT TO DO TODAY",
                    "body": (
                        "Set a phone alarm every 20 minutes: look 20 feet away for 20 seconds. "
                        "This '20-20-20 rule' relaxes the focusing muscle inside your eye. "
                        "Do it for 7 days and you will feel the difference."
                    ),
                    "icon_emoji": "✅",
                },
                {
                    "label": "COMMON MISTAKE TO AVOID",
                    "body": (
                        "Using your phone in bed with the lights off doubles eye strain — contrast is maximum. "
                        "Enable night mode after 7 PM and keep screen brightness matching room brightness. "
                        "Your eyes should never have to 'fight' the light around them."
                    ),
                    "icon_emoji": "\U0001f3af",
                },
            ],
            caption=(
                "5 screen habits that are silently destroying your eyesight \U0001f6ab\n\n"
                "Most of my patients are shocked when I explain how much daily screen time "
                "is costing their vision — because they feel fine right now.\n"
                "The damage is invisible until it isn't.\n\n"
                "\U0001f4be Save this post — your eyes will thank you in 10 years.\n\n"
                "\U0001f447 How many hours do you spend on screens daily? Comment below!"
            ),
            hashtags=[
                "DrAkshayThakur",
                "MSOphthalmologist",
                "EyeHealth",
                "DigitalEyeStrain",
                "OphthalmologyIndia",
                "VisionCare",
                "ScreenTime",
                "EyeCare",
                "HealthyEyes",
                "SaveYourVision",
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
