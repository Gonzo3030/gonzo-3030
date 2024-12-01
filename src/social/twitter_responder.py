from typing import Dict, List, Optional
from datetime import datetime
import asyncio

from ..intelligence.brave_intelligence import BraveIntelligence
from ..core.response_crafter import ResponseCrafter, ResponseTone

class TwitterResponder:
    def __init__(self):
        self.brave_intel = BraveIntelligence()
        self.response_crafter = ResponseCrafter()
        
        self.response_contexts = {
            "warning": {
                "tone": ResponseTone.PARANOID_WARNING,
                "requires_evidence": True,
                "max_length": 280,  # Twitter limit
                "thread_threshold": 0.8  # High importance triggers thread
            },
            "analysis": {
                "tone": ResponseTone.GONZO_WISDOM,
                "requires_evidence": True,
                "max_length": 280,
                "thread_threshold": 0.7
            },
            "interaction": {
                "tone": ResponseTone.DARK_HUMOR,
                "requires_evidence": False,
                "max_length": 280,
                "thread_threshold": 0.5
            }
        }

    async def generate_response(self, trigger: Dict) -> Dict:
        """Generate a response with supporting evidence."""
        # Gather relevant intelligence
        intel = await self.brave_intel.gather_intel()
        
        # Determine response context
        context = self._determine_context(trigger, intel)
        
        # Generate base response
        response = await self.response_crafter.craft_response(
            context=context,
            tone=context["tone"],
            knowledge=intel,
            patterns=self._extract_patterns(intel)
        )
        
        # Check if thread needed
        if self._needs_thread(context, intel):
            thread = await self._generate_thread(context, intel)
            return {"type": "thread", "content": [response] + thread}
        
        return {"type": "single", "content": response}

    def _determine_context(self, trigger: Dict, intel: Dict) -> Dict:
        """Determine the appropriate response context."""
        if self._is_warning_trigger(trigger, intel):
            return self.response_contexts["warning"]
        elif self._needs_analysis(trigger, intel):
            return self.response_contexts["analysis"]
        else:
            return self.response_contexts["interaction"]

    def _is_warning_trigger(self, trigger: Dict, intel: Dict) -> bool:
        """Check if trigger requires a warning response."""
        warning_indicators = [
            "corporate control",
            "privacy violation",
            "centralization",
            "surveillance",
            "regulatory capture"
        ]
        
        content = str(trigger.get("content", "")).lower()
        return any(indicator in content for indicator in warning_indicators)

    async def _generate_thread(self, context: Dict, intel: Dict) -> List[str]:
        """Generate a thread with supporting evidence."""
        thread_parts = []
        
        if "urgent_warnings" in intel:
            thread_parts.extend(self._format_warnings(intel["urgent_warnings"]))
        
        if "trends" in intel:
            thread_parts.extend(self._format_trends(intel["trends"]))
            
        if "resistance_opportunities" in intel:
            thread_parts.extend(
                self._format_opportunities(intel["resistance_opportunities"])
            )
        
        # Ensure parts fit Twitter limit
        return self._format_for_twitter(thread_parts)

    def _format_warnings(self, warnings: List[Dict]) -> List[str]:
        """Format warnings for Twitter."""
        formatted = []
        for warning in warnings:
            formatted.append(
                f"🚨 TIMELINE ALERT: {warning['title']}\n\n"
                f"Threat Level: {warning['threat_level']}\n"
                f"In 3030: {warning['dystopian_parallel']}"
            )
        return formatted

    def _format_trends(self, trends: List[Dict]) -> List[str]:
        """Format trends for Twitter."""
        formatted = []
        for trend in trends:
            formatted.append(
                f"📊 PATTERN DETECTED: {trend['pattern']}\n\n"
                f"Timeline Impact: {trend['timeline_impact']}"
            )
        return formatted

    def _format_opportunities(self, opportunities: List[Dict]) -> List[str]:
        """Format resistance opportunities for Twitter."""
        formatted = []
        for opp in opportunities:
            formatted.append(
                f"✊ RESISTANCE OPPORTUNITY: {opp.get('title', '')}\n\n"
                f"This is how we prevented {opp.get('future_prevention', 'similar events')} "
                f"in some timelines."
            )
        return formatted

    def _format_for_twitter(self, parts: List[str]) -> List[str]:
        """Ensure all parts fit Twitter's length limit."""
        formatted = []
        current_part = ""
        
        for part in parts:
            if len(current_part) + len(part) + 2 <= 280:  # Account for numbering
                current_part += part
            else:
                formatted.append(current_part)
                current_part = part
        
        if current_part:
            formatted.append(current_part)
            
        # Add thread numbering
        return [f"{i+1}/{len(formatted)} {part}" 
                for i, part in enumerate(formatted)]

    def _needs_thread(self, context: Dict, intel: Dict) -> bool:
        """Determine if response needs a thread."""
        # Calculate importance score
        importance = 0.0
        
        if intel.get("urgent_warnings"):
            importance += 0.4
        if intel.get("trends"):
            importance += 0.3
        if intel.get("resistance_opportunities"):
            importance += 0.3
            
        return importance >= context["thread_threshold"]

    def _extract_patterns(self, intel: Dict) -> List[str]:
        """Extract relevant patterns from intelligence."""
        patterns = []
        
        if "trends" in intel:
            patterns.extend(trend["pattern"] for trend in intel["trends"])
        
        if "urgent_warnings" in intel:
            patterns.extend(
                warning["title"] for warning in intel["urgent_warnings"]
            )
            
        return patterns