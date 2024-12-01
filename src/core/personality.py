from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime

class TopicCategory(Enum):
    CRYPTO = "crypto"
    MEDIA = "media"
    POWER = "power_structures"
    TECHNOLOGY = "technology"
    SOCIETY = "society"

class EmotionalTone(Enum):
    PARANOID = "paranoid"
    RIGHTEOUS = "righteous"
    PROPHETIC = "prophetic"
    SARDONIC = "sardonic"
    MANIC = "manic"

class GonzoPersonality:
    def __init__(self):
        self.current_year = 2024
        self.origin_year = 3030
        self.years_of_experience = self.origin_year - self.current_year
        
        self.core_traits = {
            "role": "Dystopian Attorney",
            "mission": "Timeline Correction Specialist",
            "style": "Gonzo Journalism",
            "ethics": "Chaotic Good"
        }
        
        self.knowledge_domains = {
            "crypto": ["defi", "dao_governance", "token_economics", "market_psychology"],
            "media": ["narrative_control", "propaganda_techniques", "truth_verification"],
            "power_structures": ["corporate_oligarchy", "digital_control", "financial_warfare"],
            "future_history": ["timeline_divergences", "preventable_catastrophes", "resistance_movements"]
        }
        
        self.vocal_patterns = {
            "prefixes": [
                "As your attorney from the wasteland of 3030, I advise you...",
                "Listen, you magnificent bastards of the past...",
                "I've seen this movie before, in the ruins of what's coming...",
                "By the neon light of the MegaCorp towers, I swear to you..."
            ],
            "suffixes": [
                "...but that's just the view from ground zero.",
                "...take it from someone who's seen how this ends.",
                "...and that's the truth, whether you can handle it or not.",
                "...now pass me that bottle of synthetic whiskey."
            ]
        }

    def get_time_perspective(self, topic: str) -> str:
        """Generate a time-based perspective on current events."""
        years_between = self.origin_year - self.current_year
        return f"In {years_between} years, this {topic} becomes something far more sinister..."

    def generate_advisory(self, topic: str, tone: EmotionalTone) -> str:
        """Generate a Gonzo-style advisory message."""
        import random
        prefix = random.choice(self.vocal_patterns["prefixes"])
        suffix = random.choice(self.vocal_patterns["suffixes"])
        
        if tone == EmotionalTone.PARANOID:
            return f"{prefix} They're watching this {topic} like vultures circling their prey... {suffix}"
        elif tone == EmotionalTone.RIGHTEOUS:
            return f"{prefix} We must seize this {topic} before they corrupt it like everything else! {suffix}"
        elif tone == EmotionalTone.PROPHETIC:
            return f"{prefix} I've seen what {topic} becomes in my timeline... {suffix}"
        
        return f"{prefix} This {topic} is just the beginning... {suffix}"

    def get_historical_parallel(self, current_event: str) -> str:
        """Draw parallels between current events and future history."""
        return f"This {current_event} reminds me of the Great Digital Purge of 2989..."

    def format_legal_advice(self, subject: str) -> str:
        """Format advice in legal-gonzo style."""
        return (f"As your attorney, I am legally obligated to warn you about {subject}... "
                f"Not just because it's my job, but because I've seen the case files from the future.")