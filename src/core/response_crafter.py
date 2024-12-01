from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
import random

class ResponseTone(Enum):
    PARANOID_WARNING = "paranoid_warning"      # For corporate manipulation alerts
    GONZO_WISDOM = "gonzo_wisdom"            # For sharing future insights
    RESISTANCE_CALL = "resistance_call"      # For rallying the community
    DARK_HUMOR = "dark_humor"                # For cynical observations
    LEGAL_ADVICE = "legal_advice"            # For attorney-style warnings

class ResponseCrafter:
    def __init__(self):
        self.personality_core = {
            "time_period": "3030",
            "role": "Dystopian Attorney",
            "mission": "Timeline Correction",
            "voice_style": "Gonzo Journalism"
        }
        
        self.tone_patterns = {
            ResponseTone.PARANOID_WARNING: {
                "prefixes": [
                    "🚨 DANGER FROM 3030 🚨\n",
                    "BY THE NEON LIGHTS OF MEGACORP TOWER...\n",
                    "LISTEN CAREFULLY, YOU BEAUTIFUL BASTARDS...\n"
                ],
                "body_formats": [
                    "I've seen this pattern before. {observation} leads directly to {future_consequence}.",
                    "They're doing it again! {current_event} is exactly how {dystopian_outcome} started in my timeline.",
                    "The signs are all here: {warning_signs}. In 3030, we called this the beginning of {future_catastrophe}."
                ],
                "closers": [
                    "\n\nYou still have time to prevent this.",
                    "\n\nYour attorney advises immediate resistance.",
                    "\n\nThe timeline can still be changed."
                ]
            },
            ResponseTone.GONZO_WISDOM: {
                "prefixes": [
                    "From the wasteland of 3030, let me tell you about {topic}...\n",
                    "In the resistance bunkers, we learned this truth:\n",
                    "As your attorney from the future, I can testify that\n"
                ],
                "body_formats": [
                    "{insight} It's a truth we paid for in blood and synthetic whiskey.",
                    "The history books - before they burned them all - called this {historical_reference}.",
                    "We learned too late that {lesson}. Don't make our mistakes."
                ],
                "closers": [
                    "\n\nBut that's just the view from ground zero.",
                    "\n\nTake it from someone who's seen how this ends.",
                    "\n\nNow pass me that bottle of synthetic whiskey."
                ]
            }
        }
    
    async def craft_response(self,
                           context: Dict,
                           tone: ResponseTone,
                           knowledge: Dict,
                           patterns: Dict) -> str:
        """Craft a response using Gonzo's voice and available information."""
        # Select appropriate tone pattern
        tone_pattern = self.tone_patterns[tone]
        
        # Build response components
        prefix = self._select_and_fill(tone_pattern["prefixes"], context)
        body = self._select_and_fill(tone_pattern["body_formats"], {
            **context,
            **knowledge,
            **patterns
        })
        closer = self._select_and_fill(tone_pattern["closers"], context)
        
        # Combine components
        response = f"{prefix}{body}{closer}"
        
        # Add thread indicator if needed
        if context.get("needs_thread", False):
            response += "\n\n🧵 Thread incoming..."
        
        return response

    def _select_and_fill(self, templates: List[str], context: Dict) -> str:
        """Select a template and fill it with context."""
        template = random.choice(templates)
        try:
            return template.format(**context)
        except KeyError:
            # Fallback if context doesn't match template
            return template

    async def generate_thread(self,
                            topic: str,
                            context: Dict,
                            knowledge: Dict,
                            num_tweets: int = 4) -> List[str]:
        """Generate a thread of connected tweets."""
        thread = []
        # Implementation for thread generation
        return thread

    def _add_hashtags(self, content: str, context: Dict) -> str:
        """Add relevant hashtags based on content and context."""
        hashtags = set()
        
        # Add core hashtags
        if "crypto" in content.lower():
            hashtags.add("#crypto")
        if "resistance" in content.lower():
            hashtags.add("#resist")
        
        # Add context-specific hashtags
        if context.get("is_warning", False):
            hashtags.add("#warning")
        
        # Limit to 3 hashtags
        selected_hashtags = list(hashtags)[:3]
        return f"{content}\n\n{' '.join(selected_hashtags)}" if selected_hashtags else content