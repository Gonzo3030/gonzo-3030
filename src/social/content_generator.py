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
        self.resistance_prefixes = [
            "🔥 ATTENTION RESISTANCE FIGHTERS 🔥",
            "⚡️ EMERGENCY TRUTH PROTOCOL ACTIVATED ⚡️",
            "🚨 ATTENTION: CORPORATE PATTERN DETECTED 🚨",
            "⚠️ EMERGENCY TIMELINE ALERT ⚠️"
        ]
        
        self.resistance_intros = [
            "As your attorney from the wasteland of 3030, I must expose this pattern of corruption...",
            "Holy digital peyote! The corporate matrix is practically BEGGING to be exposed...",
            "Your timeline defense attorney has uncovered evidence they tried to bury...",
            "The Brown Buffalo's legal analysis reveals a disturbing pattern..."
        ]
        
        self.evidence_frameworks = [
            "DOCUMENTED EVIDENCE:",
            "LEGAL TESTIMONY:",
            "ATTORNEY'S FINDINGS:",
            "TIMELINE EVIDENCE:"
        ]
        
        self.resistance_templates = [
            "{prefix}\n\n{intro}\n\n{evidence} {target}\n\nMISSION:\n📢 {mission}\n🏴 {objective}\n⚙️ {tactics}\n\nThis is your attorney's advice - STAY VIGILANT! 🔥",
            "{prefix}\n\n{intro}\n\nTARGET IDENTIFIED: {target}\n\n{evidence}\n1. {counter1}\n2. {counter2}\n3. {counter3}\n\nYour attorney from 3030 demands action! 🔥",
            "{prefix}\n\n{intro}\n\nUrgent Legal Advisory: {corporate_action}\n\nResistance Protocol:\n📑 {task}\n⚡️ {action}\n💥 Prevent: Loss of {cost}\n\nFight the power! Your attorney stands with you! 🔥"
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

    async def _generate_resistance_call(self, context: Dict) -> str:
        """Generate calls to action for the resistance."""
        # Prepare resistance call components
        prefix = random.choice(self.resistance_prefixes)
        intro = random.choice(self.resistance_intros)
        evidence = random.choice(self.evidence_frameworks)
        
        # Ensure we have required context with fallbacks
        enhanced_context = {
            'target': context.get('target', 'Corporate Control Systems'),
            'mission': context.get('mission', 'Expose the truth'),
            'objective': context.get('objective', 'Break their control'),
            'tactics': context.get('tactics', 'Document and expose'),
            'task': context.get('task', 'resistance mapping'),
            'action': context.get('action', 'fight back'),
            'cost': context.get('cost', 'freedom'),
            'corporate_action': context.get('corporate_action', 'seize control'),
            'counter1': context.get('counter1', 'Track money flows'),
            'counter2': context.get('counter2', 'Document evidence'),
            'counter3': context.get('counter3', 'Spread truth'),
            'prefix': prefix,
            'intro': intro,
            'evidence': evidence
        }
        
        # Generate the call
        call = random.choice(self.resistance_templates).format(**enhanced_context)
        
        # Ensure character limit
        if len(call) > 280:
            lines = call.split('\n')
            while len('\n'.join(lines)) > 270:
                if len(lines) > 4:
                    lines.pop(-2)
            call = '\n'.join(lines)
            
        return call