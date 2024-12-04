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