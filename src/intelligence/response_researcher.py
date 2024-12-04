    def _determine_response_type(self, analysis: Dict) -> str:
        """Determine the best type of response based on analysis"""
        if not analysis.get('patterns') and not analysis.get('implications'):
            return 'general'
            
        patterns = analysis.get('patterns', [])
        implications = analysis.get('implications', [])
        
        if 'corporate_control' in patterns or 'privacy_violation' in patterns:
            return 'warning'
        elif 'resistance' in patterns:
            return 'supportive'
        elif 'privacy_risk' in implications or 'control_increase' in implications:
            return 'advisory'
        else:
            return 'informative'
    
    def _extract_key_points(self, analysis: Dict) -> List[str]:
        """Extract key points for response"""
        points = []
        
        # Add key findings
        for finding in analysis.get('key_findings', []):
            if finding.get('title'):
                points.append(finding['title'])
        
        # Add pattern insights
        for pattern in analysis.get('patterns', []):
            points.append(f"Pattern detected: {pattern.replace('_', ' ').title()}")
        
        # Add implications
        for implication in analysis.get('implications', []):
            points.append(f"Potential impact: {implication.replace('_', ' ').title()}")
        
        return points[:3]  # Limit to top 3 points
    
    def _determine_tone(self, analysis: Dict) -> str:
        """Determine appropriate tone for response"""
        patterns = analysis.get('patterns', [])
        implications = analysis.get('implications', [])
        
        if 'privacy_risk' in implications or 'rights_reduction' in implications:
            return 'urgent'
        elif 'corporate_control' in patterns or 'manipulation' in patterns:
            return 'warning'
        elif 'resistance' in patterns or 'resistance_opportunity' in implications:
            return 'encouraging'
        else:
            return 'informative'
    
    def _generate_action_items(self, analysis: Dict) -> List[str]:
        """Generate actionable recommendations"""
        actions = []
        
        # Map patterns to actions
        pattern_actions = {
            'corporate_control': [
                'Support decentralized alternatives',
                'Join anti-monopoly movements',
                'Advocate for stronger regulations'
            ],
            'privacy_violation': [
                'Use privacy-focused services',
                'Encrypt your communications',
                'Opt out of data collection'
            ],
            'manipulation': [
                'Diversify information sources',
                'Use content blockers',
                'Support independent platforms'
            ],
            'resistance': [
                'Join digital rights groups',
                'Support grassroots movements',
                'Share knowledge with others'
            ]
        }
        
        # Add relevant actions based on patterns
        for pattern in analysis.get('patterns', []):
            if pattern in pattern_actions:
                actions.extend(pattern_actions[pattern])
        
        return list(set(actions))[:3]  # Remove duplicates and limit to top 3