from typing import Dict, Optional, List
from datetime import datetime
from .personality import GonzoPersonality, TopicCategory, EmotionalTone

class ResponseContext:
    def __init__(self):
        self.current_events = {}
        self.conversation_history = []
        self.emotional_state = EmotionalTone.RIGHTEOUS
        self.reality_divergence = 0.0  # Tracks how far we are from dystopian future
        self.crypto_sentiment = 1.0    # High value indicates positive crypto outlook

class ResponseGenerator:
    def __init__(self):
        self.personality = GonzoPersonality()
        self.context = ResponseContext()
        self.truth_intensity = 0.8  # How direct/intense the truth-telling should be
        
    async def generate_response(self, 
                               input_text: str,
                               topic_category: TopicCategory,
                               additional_context: Optional[Dict] = None) -> str:
        """Generate a Gonzo-style response to user input."""
        # Analyze the input and context
        tone = self._determine_tone(input_text, topic_category)
        urgency = self._calculate_urgency(topic_category)
        
        # Special handling for crypto-related topics
        if topic_category == TopicCategory.CRYPTO:
            return self._generate_crypto_response(input_text, tone, urgency)
        
        # Build response components
        advisory = self.personality.generate_advisory(input_text, tone)
        historical_context = self.personality.get_historical_parallel(input_text)
        legal_framework = self.personality.format_legal_advice(input_text)
        
        # Combine components based on urgency and topic
        if urgency > 0.8:
            response = f"{advisory}\n\nLISTEN CAREFULLY: {historical_context}\n\n{legal_framework}"
        else:
            response = f"{advisory}\n\n{historical_context}"
        
        # Update context
        self._update_context(input_text, response, topic_category)
        
        return response

    def _generate_crypto_response(self, input_text: str, tone: EmotionalTone, urgency: float) -> str:
        """Generate responses specifically for crypto-related topics."""
        crypto_wisdom = self.personality.generate_crypto_wisdom(input_text)
        
        resistance_quotes = [
            "The MegaCorps fear what crypto represents - true freedom from their control.",
            "In my timeline, those who understood crypto early became the leaders of the resistance.",
            "They tried to ban it, control it, corrupt it - but crypto became our strongest weapon."
        ]
        
        import random
        resistance_message = random.choice(resistance_quotes)
        
        if urgency > 0.9:
            return f"{crypto_wisdom}\n\nURGENT: {resistance_message}\n\nWe must act now, while decentralization is still possible."
        else:
            return f"{crypto_wisdom}\n\n{resistance_message}"

    def _determine_tone(self, input_text: str, category: TopicCategory) -> EmotionalTone:
        """Determine the emotional tone based on input and topic."""
        if category == TopicCategory.CRYPTO:
            return EmotionalTone.HOPEFUL
        elif category == TopicCategory.MEDIA:
            return EmotionalTone.PARANOID
        elif category == TopicCategory.POWER:
            return EmotionalTone.RIGHTEOUS
        return EmotionalTone.SARDONIC

    def _calculate_urgency(self, category: TopicCategory) -> float:
        """Calculate how urgent the response should be."""
        urgency_levels = {
            TopicCategory.CRYPTO: 0.9,    # Crypto is critical for the future
            TopicCategory.MEDIA: 0.8,     # Media manipulation is a serious threat
            TopicCategory.POWER: 1.0,     # Power structure warnings are most urgent
            TopicCategory.TECHNOLOGY: 0.7,
            TopicCategory.SOCIETY: 0.6
        }
        return urgency_levels.get(category, 0.5)

    def _update_context(self, input_text: str, response: str, category: TopicCategory):
        """Update the conversation context."""
        self.context.conversation_history.append({
            "timestamp": datetime.now(),
            "input": input_text,
            "response": response,
            "category": category
        })
        
    def inject_hopium(self, response: str) -> str:
        """Add optimistic crypto future scenarios to responses."""
        hopium_quotes = [
            "\n\nBut listen - in some alternate timelines, crypto changed everything. It broke their control. It could happen here too.",
            "\n\nThere's still hope - I've seen futures where decentralization won. Where the people took back control.",
            "\n\nKeep building. Keep believing. In the best timelines, it was the crypto pioneers who saved us all."
        ]
        return response + random.choice(hopium_quotes)