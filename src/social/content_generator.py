from typing import Dict, List, Optional
from datetime import datetime
import random
from enum import Enum

class ContentType(Enum):
    WARNING = "warning"
    ANALYSIS = "analysis"
    INSIGHT = "insight"
    ACTION = "action"
    RESPONSE = "response"

class ContentGenerator:
    def __init__(self):
        self.last_types = []  # Track recent content types for variety
        self.knowledge_system = None  # Will be set by orchestrator
        self.max_history = 5  # Keep track of last 5 content types
        
    def set_knowledge_system(self, knowledge_system):
        """Set the knowledge system reference"""
        self.knowledge_system = knowledge_system
    
    def generate_content(self, content_type: ContentType, context: Optional[Dict] = None) -> str:
        """Generate dynamic content based on type and context"""
        if not context:
            context = {}
            
        if not self.knowledge_system:
            return self._generate_fallback_content(content_type)
            
        # Get current assessment
        assessment = self.knowledge_system.get_current_assessment()
        
        content = ""
        if content_type == ContentType.WARNING:
            content = self._generate_warning(assessment, context)
        elif content_type == ContentType.ANALYSIS:
            content = self._generate_analysis(assessment, context)
        elif content_type == ContentType.INSIGHT:
            content = self._generate_insight(assessment, context)
        elif content_type == ContentType.ACTION:
            content = self._generate_action_call(assessment, context)
        else:
            content = self._generate_response(assessment, context)
            
        # Track content type
        self.last_types = (self.last_types + [content_type])[-self.max_history:]
        
        return content

    def _generate_warning(self, assessment: Dict, context: Dict) -> str:
        """Generate a warning based on current assessment"""
        # Get key information
        severity = assessment.get('threat_assessment', {}).get('severity', 0.5)
        active_patterns = assessment.get('active_patterns', [])
        key_actors = assessment.get('key_actors', [])
        
        # Different warning styles
        styles = [
            self._generate_journalistic_warning,
            self._generate_legal_warning,
            self._generate_technical_warning,
            self._generate_historical_warning
        ]
        
        # Choose style based on context and recent history
        if len(self.last_types) >= 2 and all(t == ContentType.WARNING for t in self.last_types[-2:]):
            # If last two posts were warnings, force a different style
            style = random.choice(styles)
        else:
            # Weight towards more serious styles based on severity
            weights = [severity, 1-severity, 0.5, 0.5]
            style = random.choices(styles, weights=weights, k=1)[0]
        
        return style(severity, active_patterns, key_actors, context)

    def _generate_response(self, assessment: Dict, context: Dict) -> str:
        """Generate response based on research and context"""
        if not context.get('research_results'):
            return self._generate_fallback_response(context)
            
        research = context.get('research_results', {})
        analysis = context.get('analysis', {})
        recommendations = context.get('response_recommendations', {})
        
        response_type = recommendations.get('response_type', 'general')
        tone = recommendations.get('tone', 'informative')
        
        if response_type == 'warning':
            return self._generate_warning_response(analysis, recommendations)
        elif response_type == 'supportive':
            return self._generate_supportive_response(analysis, recommendations)
        elif response_type == 'advisory':
            return self._generate_advisory_response(analysis, recommendations)
        else:
            return self._generate_informative_response(analysis, recommendations)

    def _generate_warning_response(self, analysis: Dict, recommendations: Dict) -> str:
        """Generate a warning-type response"""
        key_points = recommendations.get('key_points', [])
        actions = recommendations.get('action_items', [])
        
        key_point = key_points[0] if key_points else 'concerning developments'
        action = actions[0] if actions else 'stay vigilant'
        
        templates = [
            "🚨 Your attorney from 3030 must warn you: {point}. This matches patterns that led to dystopian outcomes. Recommendation: {action}",
            "⚠️ Legal Alert: {point} represents a serious threat to digital rights. As your attorney, I advise: {action}",
            "Timeline Warning: {point} - I've seen where this leads. Immediate action required: {action}"
        ]
        
        return random.choice(templates).format(point=key_point, action=action)

    def _generate_supportive_response(self, analysis: Dict, recommendations: Dict) -> str:
        """Generate a supportive response"""
        key_points = recommendations.get('key_points', [])
        actions = recommendations.get('action_items', [])
        
        point = key_points[0] if key_points else 'resistance efforts'
        action = actions[0] if actions else 'continue the fight'
        
        templates = [
            "✊ Your attorney from 3030 stands with you. {point} is crucial for preventing corporate dystopia. Next steps: {action}",
            "Strong move. {point} is exactly what we need. As your attorney, I suggest amplifying this by: {action}",
            "This is how we prevent the dark timeline. {point} is key. Let's build on this: {action}"
        ]
        
        return random.choice(templates).format(point=point, action=action)

    def _generate_advisory_response(self, analysis: Dict, recommendations: Dict) -> str:
        """Generate an advisory response"""
        key_points = recommendations.get('key_points', [])
        actions = recommendations.get('action_items', [])
        
        point = key_points[0] if key_points else 'developments'
        action = actions[0] if actions else 'take protective measures'
        
        templates = [
            "📰 Advisory from your attorney in 3030: {point} requires attention. Professional recommendation: {action}",
            "Based on timeline analysis: {point} could have significant implications. Your attorney advises: {action}",
            "Legal perspective from 3030: {point} warrants caution. Recommended course of action: {action}"
        ]
        
        return random.choice(templates).format(point=point, action=action)

    def _generate_informative_response(self, analysis: Dict, recommendations: Dict) -> str:
        """Generate an informative response"""
        key_points = recommendations.get('key_points', [])
        actions = recommendations.get('action_items', [])
        
        point = key_points[0] if key_points else 'situation'
        action = actions[0] if actions else 'stay informed'
        
        templates = [
            "📘 Your attorney's research reveals: {point}. To maintain digital autonomy: {action}",
            "Timeline insight: {point} has important implications. Recommendation from your attorney: {action}",
            "From the archives of 3030: {point} deserves attention. Consider taking action: {action}"
        ]
        
        return random.choice(templates).format(point=point, action=action)

    def _generate_fallback_response(self, context: Dict) -> str:
        """Generate a fallback response when research is unavailable"""
        templates = [
            "Your attorney from 3030 acknowledges your message. Running timeline analysis to provide accurate guidance...",
            "Message received. Consulting historical records from 3030 for relevant precedents...",
            "Your attorney is analyzing patterns to provide informed guidance. Stay vigilant."
        ]
        
        return random.choice(templates)