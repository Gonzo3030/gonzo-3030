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
    
    def _generate_journalistic_warning(self, severity: float, patterns: List[str], actors: List[str], context: Dict) -> str:
        """Generate warning in journalistic style"""
        # Choose dynamic components
        headline_verbs = ['BREAKING', 'ALERT', 'EXCLUSIVE', 'DEVELOPING']
        impact_phrases = [
            'threatens digital rights',
            'signals dangerous precedent',
            'raises major concerns',
            'shows troubling pattern'
        ]
        
        headline = random.choice(headline_verbs)
        pattern = random.choice(patterns) if patterns else 'corporate manipulation'
        actor = random.choice(actors) if actors else 'major tech companies'
        impact = random.choice(impact_phrases)
        
        return f"{headline}: New evidence of {pattern} by {actor} {impact}. Your attorney from 3030 urges vigilance. Details and countermeasures incoming..."
    
    def _generate_legal_warning(self, severity: float, patterns: List[str], actors: List[str], context: Dict) -> str:
        """Generate warning in legal style"""
        # Legal-themed components
        legal_terms = [
            'NOTICE OF VIOLATION',
            'CEASE AND DESIST ADVISORY',
            'LEGAL ALERT',
            'RIGHTS VIOLATION WARNING'
        ]
        
        violations = [
            'digital rights infringement',
            'privacy violation',
            'data sovereignty breach',
            'algorithmic manipulation'
        ]
        
        header = random.choice(legal_terms)
        pattern = random.choice(patterns) if patterns else random.choice(violations)
        
        return f"{header}: As your attorney from 3030, I must advise of ongoing {pattern}. Timeline precedents show catastrophic outcomes. Documenting violations and preparing countermeasures..."
