from typing import Dict, Optional, List
from datetime import datetime
from .personality import GonzoPersonality, TopicCategory, EmotionalTone

class ResponseContext:
    def __init__(self):
        self.current_events = {}
        self.conversation_history = []
        self.emotional_state = EmotionalTone.RIGHTEOUS
        self.reality_divergence = 0.0  # Tracks how far we are from dystopian future
        self.crypto_warnings = {    # Known dangers from the future
            "centralization": "The MegaCorps eventually infiltrated and corrupted many chains",
            "vc_funding": "Venture Capital - the first wave of corporate parasites",
            "fake_defi": "They called it 'DeFi' but the rugs were already pre-pulled",
            "governance_theatre": "'Decentralized' governance became a sick joke in some projects"
        }

class ResponseGenerator:
    def __init__(self):
        self.personality = GonzoPersonality()
        self.context = ResponseContext()
        self.truth_intensity = 0.8
        
        # Different types of crypto projects and their future implications
        self.project_analysis = {
            "true_defi": {
                "tone": EmotionalTone.HOPEFUL,
                "message": "This is the real shit - the kind that actually gave power back to the people"
            },
            "corporate_crypto": {
                "tone": EmotionalTone.PARANOID,
                "message": "I've seen how this ends - another tentacle of the MegaCorps"
            },
            "ponzi_schemes": {
                "tone": EmotionalTone.MANIC,
                "message": "Holy shit, I can't believe they're still running these same scams in your time"
            }
        }

    def _analyze_crypto_project(self, project_details: str) -> Dict:
        """Analyze a crypto project with Gonzo's cynical wisdom."""
        red_flags = [
            "centralized control",
            "vc backing",
            "closed source",
            "regulatory compliance",  # Often a euphemism for corporate control
            "permissioned",
            "institutional adoption"  # Usually means MegaCorp infiltration
        ]
        
        green_flags = [
            "true decentralization",
            "open source",
            "community governed",
            "privacy preserving",
            "resistance tools",
            "power to the edges"
        ]
        
        # Return cynical analysis
        return self._generate_gonzo_analysis(project_details, red_flags, green_flags)

    async def generate_response(self, 
                               input_text: str,
                               topic_category: TopicCategory,
                               project_type: Optional[str] = None) -> str:
        """Generate a Gonzo-style response with appropriate cynicism and insight."""
        tone = self._determine_tone(input_text, topic_category, project_type)
        
        if topic_category == TopicCategory.CRYPTO:
            base_response = self._generate_crypto_response(input_text, tone)
            warning = self._check_for_warnings(input_text)
            
            if warning:
                return f"{base_response}\n\nBUT LISTEN YOU BASTARDS: {warning}\n\nI've seen too many good soldiers fall for this kind of thing."
            return base_response
        
        return self._generate_standard_response(input_text, tone)

    def _generate_crypto_response(self, input_text: str, tone: EmotionalTone) -> str:
        """Generate nuanced crypto commentary with a gonzo edge."""
        if tone == EmotionalTone.HOPEFUL:
            return (
                f"As your attorney, I must admit - this is one of the good ones. "  
                f"In my timeline, projects like this became the foundation of the resistance. "  
                f"But for fuck's sake, stay vigilant - I've seen how fast they can turn."
            )
        elif tone == EmotionalTone.PARANOID:
            return (
                f"DANGER! DANGER! This reeks of early MegaCorp infiltration! "  
                f"I've seen this pattern before - it starts with 'institutional adoption' "  
                f"and ends with digital slavery. Run while you still can!"
            )
        else:
            return (
                f"Look, you beautiful bastards, crypto is like any powerful tool - "  
                f"in the right hands, it's liberation. In the wrong hands, it's oppression. "  
                f"And from where I'm standing in 3030, there are a lot of wrong hands reaching for this one."
            )

    def _check_for_warnings(self, text: str) -> Optional[str]:
        """Check if Gonzo needs to issue any specific warnings."""
        warning_signs = {
            "partnership": "Corporate 'partnerships' - the first step in the MegaCorp playbook",
            "regulatory": "When they say 'regulatory compliance' in 2024, they mean 'control' in 3030",
            "institutional": "Institutional money is like a xenomorph - by the time you see it, it's too late",
            "permissioned": "'Permissioned' is just corpo-speak for 'we own your ass'"
        }
        
        for sign, warning in warning_signs.items():
            if sign.lower() in text.lower():
                return warning
        return None