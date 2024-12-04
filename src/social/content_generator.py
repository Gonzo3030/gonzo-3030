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