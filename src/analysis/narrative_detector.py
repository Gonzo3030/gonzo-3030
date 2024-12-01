from typing import Dict, List, Optional, Tuple
from enum import Enum
from datetime import datetime

class NarrativeType(Enum):
    CORPORATE_PROPAGANDA = "corporate_propaganda"
    SOCIAL_ENGINEERING = "social_engineering"
    FEAR_MONGERING = "fear_mongering"
    CONSENSUS_MANUFACTURING = "consensus_manufacturing"
    REALITY_DISTORTION = "reality_distortion"

class PropagandaTechnique(Enum):
    EMOTIONAL_MANIPULATION = "emotional_manipulation"
    FALSE_DICHOTOMY = "false_dichotomy"
    STRAWMAN = "strawman"
    APPEAL_TO_AUTHORITY = "appeal_to_authority"
    MANUFACTURED_CONSENT = "manufactured_consent"

class NarrativeDetector:
    def __init__(self):
        self.known_narratives = {
            "crypto_fear": {
                "type": NarrativeType.FEAR_MONGERING,
                "triggers": ["crypto danger", "bitcoin criminal", "defi risks"],
                "corporate_benefit": "Keeping people in traditional banking",
                "future_impact": "Led to the Banking Control Act of 2028"
            },
            "centralization_good": {
                "type": NarrativeType.CORPORATE_PROPAGANDA,
                "triggers": ["regulatory clarity", "institutional adoption", "compliant platform"],
                "corporate_benefit": "Maintaining control over financial systems",
                "future_impact": "Enabled the Great Financial Consolidation"
            },
            "privacy_danger": {
                "type": NarrativeType.SOCIAL_ENGINEERING,
                "triggers": ["nothing to hide", "public safety", "prevent crime"],
                "corporate_benefit": "Total surveillance capitalism",
                "future_impact": "The Privacy Extinction of 2029"
            }
        }
        
        self.megacorp_tactics = {
            "divide_and_conquer": [
                "creating artificial conflicts",
                "promoting tribal thinking",
                "fostering echo chambers"
            ],
            "reality_distortion": [
                "selective fact presentation",
                "context manipulation",
                "expert manufacturing"
            ],
            "consent_manufacturing": [
                "artificial grassroots",
                "controlled opposition",
                "narrative seeding"
            ]
        }

    async def analyze_narrative(self, 
                              content: str,
                              context: Optional[Dict] = None) -> Dict:
        """Analyze content for narrative manipulation patterns."""
        detected_patterns = []
        future_implications = []
        
        # Check for known narrative patterns
        for narrative_name, details in self.known_narratives.items():
            if self._matches_narrative(content, details["triggers"]):
                detected_patterns.append({
                    "narrative": narrative_name,
                    "type": details["type"],
                    "corporate_benefit": details["corporate_benefit"],
                    "future_impact": details["future_impact"]
                })
        
        # Analyze manipulation techniques
        techniques = self._detect_techniques(content)
        
        return {
            "patterns": detected_patterns,
            "techniques": techniques,
            "gonzo_analysis": self._generate_gonzo_warning(detected_patterns)
        }

    def _detect_techniques(self, content: str) -> List[PropagandaTechnique]:
        """Detect specific propaganda techniques in content."""
        techniques = []
        
        technique_patterns = {
            PropagandaTechnique.EMOTIONAL_MANIPULATION: [
                "fear", "danger", "threat", "risk", "scary"
            ],
            PropagandaTechnique.FALSE_DICHOTOMY: [
                "either", "or", "only choice", "no alternative"
            ],
            PropagandaTechnique.APPEAL_TO_AUTHORITY: [
                "experts say", "studies show", "authorities confirm"
            ]
        }
        
        return techniques

    def _generate_gonzo_warning(self, patterns: List[Dict]) -> str:
        """Generate a Gonzo-style warning about detected narratives."""
        if not patterns:
            return "No immediate narrative manipulation detected... but stay paranoid, you beautiful bastards."
        
        warnings = []
        for pattern in patterns:
            warnings.append(
                f"HOLY SHIT! This is exactly how {pattern['future_impact']} started! "  
                f"The MegaCorps are using this narrative for {pattern['corporate_benefit']}. "  
                f"I've seen this movie before, and the director's cut is a nightmare."
            )
        
        return "\n\n".join(warnings)

    def _matches_narrative(self, content: str, triggers: List[str]) -> bool:
        """Check if content matches known narrative triggers."""
        content = content.lower()
        return any(trigger.lower() in content for trigger in triggers)

    def get_historical_context(self, narrative_type: NarrativeType) -> str:
        """Provide historical context from 3030 about narrative types."""
        historical_context = {
            NarrativeType.CORPORATE_PROPAGANDA: (
                "By 3030, they didn't even try to hide it anymore. "  
                "The MegaCorps openly owned all media channels. "  
                "But in your time, they still maintain the illusion of choice."
            ),
            NarrativeType.SOCIAL_ENGINEERING: (
                "Social engineering became an art form. "  
                "They could make people demand their own oppression. "  
                "It started with small narrative seeds like this."
            )
        }
        return historical_context.get(narrative_type, 
                                     "The full horror of this narrative is still classified in 3030.")