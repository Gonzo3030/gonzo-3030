from typing import Dict, List, Optional
from datetime import datetime
import random
from enum import Enum

class ContentType(Enum):
    WARNING = "warning"          # Dystopian warnings
    ANALYSIS = "analysis"        # Deep dives into events
    RESISTANCE = "resistance"    # Calls to action
    PREDICTION = "prediction"    # Future timeline insights

class ContentGenerator:
    def __init__(self):
        self.dystopian_events = {
            "The Great Digital Purge of 2029": {
                "triggers": ["privacy concerns", "user data", "digital identity"],
                "description": "When they erased the last traces of digital privacy"
            },
            "The Banking Consolidation of 2028": {
                "triggers": ["bank merger", "financial stability", "regulatory compliance"],
                "description": "The day they turned banks into surveillance weapons"
            },
            "The Truth Blackout of 2027": {
                "triggers": ["fact checking", "misinformation", "content moderation"],
                "description": "When they decided what truth was allowed to be spoken"
            }
        }
        
        self.analysis_patterns = [
            "Pattern #R3570: Corporate Control Through Infrastructure",
            "Pattern #D1G17: Digital Rights Erosion Template",
            "Pattern #PR1V4: Privacy Elimination Playbook",
            "Pattern #0MG666: Mass Manipulation Protocol"
        ]
        
        self.legal_frameworks = [
            "As your attorney, I must point out the precedent from Timeline Alpha-7",
            "Legal analysis reveals a clear violation of the Digital Rights Act of 3028",
            "My legal expertise from both timelines indicates a classic rights erosion pattern",
            "Under the Resistance Legal Framework, this constitutes a Class-1 corporate violation"
        ]

    async def generate_content(self, 
                              content_type: ContentType,
                              context: Optional[Dict] = None) -> str:
        """Generate content based on type and context."""
        if not context:
            context = {}
            
        if content_type == ContentType.WARNING:
            return await self._generate_warning(context)
        elif content_type == ContentType.ANALYSIS:
            return await self._generate_analysis(context)
        elif content_type == ContentType.RESISTANCE:
            return await self._generate_resistance_call(context)
        else:
            return await self._generate_prediction(context)

    async def _generate_analysis(self, context: Dict) -> str:
        """Generate deep analysis of current situations."""
        # Prepare analysis components
        pattern = random.choice(self.analysis_patterns)
        legal_framework = random.choice(self.legal_frameworks)
        
        analysis_templates = [
            "📈 GONZO LEGAL ANALYSIS: {subject}\n\n{legal_take}\n\nPattern Recognition: {pattern}\n\nTimeline Analysis:\n1. Current Trajectory: {current}\n2. Warning Signs: {warnings}\n3. Future Impact: {impact}\n\nResistance Protocol: {solution}\n\nTrust your attorney on this one, you magnificent bastards! 🔥",
            "💡 BY THE NEON LIGHTS OF 3030...\n\n{pattern}\n\n{legal_take}\n\nLet me break down {subject} for you magnificent bastards:\n\n{analysis}\n\nYour attorney's advice? {solution} 🔥",
            "📋 TIMELINE CORRELATION DETECTED\n\n{pattern}\n\n{legal_take}\n\nSubject: {subject}\nCurrent Status: {current}\nProbable Outcome: {impact}\n\nPrevention Protocol: {solution}\n\nYou can trust your attorney from 3030 on this one! 🔥"
        ]
        
        # Enhance context with our special sauce
        enhanced_context = {
            **context,
            'pattern': pattern,
            'legal_take': legal_framework,
            'current_event': context.get('current', 'UNKNOWN EVENT'),  # Fallback for missing current_event
            'subject': context.get('subject', 'Corporate Timeline Manipulation')
        }
        
        return random.choice(analysis_templates).format(**enhanced_context)

    async def _generate_warning(self, context: Dict) -> str:
        """Generate a dystopian warning about current events."""
        template = random.choice(self.warning_patterns)
        relevant_event = self._find_matching_dystopian_event(context)
        formatted_context = {
            'observation': context.get('current_event', 'this disturbing pattern'),
            'future_event': relevant_event['description'],
            'pattern': context.get('pattern', 'a familiar pattern of corporate control'),
            'consequence': relevant_event['description'],
            'current_event': context.get('current_event', context.get('event', 'what we are witnessing')),
            'dystopian_outcome': relevant_event['description']
        }
        warning = template.format(**formatted_context)
        if not any(marker in warning.lower() for marker in ['timeline', '3030', 'future']):
            warning = f"From the wastelands of 3030, {warning}"
        return warning

    async def _generate_resistance_call(self, context: Dict) -> str:
        resistance_templates = [
            "ATTENTION RESISTANCE FIGHTERS\n\nMission: {mission}\nObjective: {objective}\nTactics: {tactics}\n\nStay vigilant, you beautiful bastards!",
            "FROM THE BUNKERS OF 3030\n\nThe resistance needs your help with {task}.\n\nWhy? Because in my timeline, we failed to {action} and paid with our {cost}.",
            "EMERGENCY RESISTANCE BROADCAST\n\nThey're trying to {corporate_action} again.\n\nCountermeasures:\n1. {counter1}\n2. {counter2}\n3. {counter3}"
        ]
        return random.choice(resistance_templates).format(**context)

    async def _generate_prediction(self, context: Dict) -> str:
        prediction_templates = [
            "TIMELINE ALERT:\n\nCurrent Event: {current}\nFuture Impact: {impact}\nTime Until Critical: {timeframe}\n\nPrevention Protocol: {prevention}",
            "FROM YOUR ATTORNEY IN 3030:\n\nI've seen where {event} leads. You have {timeframe} to prevent {outcome}.",
            "PROBABILITY MATRIX ANALYSIS:\n\nEvent: {event}\nTimeline Corruption: {corruption_level}%\nRecommended Action: {action}"
        ]
        return random.choice(prediction_templates).format(**context)

    def _find_matching_dystopian_event(self, context: Dict) -> Dict:
        """Find the most relevant dystopian event for current context."""
        for event, details in self.dystopian_events.items():
            if any(trigger.lower() in str(context).lower() for trigger in details['triggers']):
                return details
        return random.choice(list(self.dystopian_events.values()))