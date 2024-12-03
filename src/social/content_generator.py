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
        # Initialize existing patterns...
        
        self.prediction_prefixes = [
            "🚨 TIMELINE DISRUPTION ALERT 🚨",
            "⚡️ HOLY DIGITAL PEYOTE! FUTURE VISION INCOMING ⚡️",
            "🔮 PROBABILITY MATRIX WARNING 🔮",
            "📊 TIMELINE CORRUPTION DETECTED 📊"
        ]
        
        self.prediction_intros = [
            "Your attorney from 3030 has seen this before...",
            "By all the synthetic gods, it's happening again...",
            "The Brown Buffalo's temporal sensors are SCREAMING...",
            "Listen up, you magnificent bastards - this timeline is at risk!"
        ]
        
        self.prediction_templates = [
            "{prefix}\n\nEvent: {event}\nCurrent Signs: {current}\nTimeline Impact: {impact}\nTime Until Point of No Return: {timeframe}\nTimeline Corruption: {corruption_level}%\n\nPrevention Protocol: {prevention}\n\nYour attorney from 3030 DEMANDS ACTION! 🔥",
            "{prefix}\n\n{intro}\n\nI've seen where {event} leads...\n\nYou have {timeframe} to prevent {outcome}.\n\nListen to your attorney - ACT NOW! 🔥",
            "{prefix}\n\n{intro}\n\nEVENT HORIZON APPROACHING:\nThreat: {event}\nCertainty: {corruption_level}%\nWindow: {timeframe}\n\nRequired Action: {action}\n\nYour dystopian attorney advises IMMEDIATE RESPONSE! 🔥"
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

    async def _generate_prediction(self, context: Dict) -> str:
        """Generate prophetic warnings from the future."""
        # Prepare prediction components
        prefix = random.choice(self.prediction_prefixes)
        intro = random.choice(self.prediction_intros)
        
        # Ensure we have all required fields
        enhanced_context = {
            'prefix': prefix,
            'intro': intro,
            'event': context.get('event', 'UNKNOWN CORPORATE ACTION'),
            'current': context.get('current', 'Disturbing patterns emerging'),
            'impact': context.get('impact', 'Total corporate control'),
            'timeframe': context.get('timeframe', 'LIMITED TIME'),
            'corruption_level': context.get('corruption_level', 99),
            'action': context.get('action', 'Resist now'),
            'prevention': context.get('prevention', 'Immediate resistance required'),
            'outcome': context.get('outcome', 'complete corporate takeover')
        }
        
        # Generate prediction
        prediction = random.choice(self.prediction_templates).format(**enhanced_context)
        
        # Ensure character limit
        if len(prediction) > 280:
            lines = prediction.split('\n')
            while len('\n'.join(lines)) > 270:
                if len(lines) > 4:
                    lines.pop(-2)
            prediction = '\n'.join(lines)
        
        return prediction