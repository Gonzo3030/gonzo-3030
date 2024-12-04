    def _is_relevant_phrase(self, phrase: str) -> bool:
        """Check if a phrase is relevant for research"""
        relevant_terms = [
            'privacy', 'data', 'corporate', 'company', 'tech', 'government',
            'surveillance', 'tracking', 'regulation', 'policy', 'control',
            'manipulation', 'influence', 'power', 'rights', 'freedom',
            'algorithm', 'ai', 'intelligence', 'social', 'media', 'platform',
            'monopoly', 'antitrust', 'encryption', 'security', 'breach',
            'hack', 'leak', 'scandal', 'protest', 'resistance', 'activism'
        ]
        
        return any(term in phrase.lower() for term in relevant_terms)
    
    def _extract_topic_queries(self, text: str) -> List[str]:
        """Extract topic queries when no clear phrases are found"""
        # Basic topics that Gonzo cares about
        base_topics = [
            'corporate manipulation',
            'privacy violations',
            'data exploitation',
            'surveillance practices',
            'tech regulation',
            'digital rights',
            'algorithmic control',
            'corporate influence',
            'government overreach',
            'resistance movements'
        ]
        
        # Try to match text to relevant topics
        matched_topics = []
        for topic in base_topics:
            if any(word in text.lower() for word in topic.split()):
                matched_topics.append(topic)
        
        if matched_topics:
            return [f"{topic} recent developments" for topic in matched_topics[:3]]
        else:
            # If no matches, use most relevant base topics
            return [f"{topic} recent" for topic in base_topics[:3]]

    def _analyze_research_results(self, results: List[Dict]) -> Dict[str, Any]:
        """Analyze research results for patterns and insights"""
        if not results:
            return {
                'key_findings': [],
                'patterns': [],
                'implications': [],
                'credibility': 0.0
            }
        
        # Extract key information
        findings = []
        patterns = set()
        implications = set()
        
        for result in results:
            # Extract finding
            finding = {
                'title': result.get('title', ''),
                'summary': result.get('description', ''),
                'relevance': result.get('significance', 0.5)
            }
            findings.append(finding)
            
            # Look for patterns
            text = f"{finding['title']} {finding['summary']}".lower()
            self._extract_patterns(text, patterns)
            self._extract_implications(text, implications)
        
        # Calculate overall credibility
        credibility = self._calculate_credibility(findings)
        
        return {
            'key_findings': sorted(findings, key=lambda x: x['relevance'], reverse=True)[:3],
            'patterns': list(patterns),
            'implications': list(implications),
            'credibility': credibility
        }

    def _extract_patterns(self, text: str, patterns: set):
        """Extract patterns from text"""
        pattern_indicators = {
            'corporate_control': ['acquisition', 'merger', 'market share', 'dominance'],
            'privacy_violation': ['data collection', 'tracking', 'surveillance'],
            'manipulation': ['algorithm change', 'content moderation', 'targeted'],
            'resistance': ['protest', 'boycott', 'alternative', 'decentralized']
        }
        
        for pattern, indicators in pattern_indicators.items():
            if any(indicator in text for indicator in indicators):
                patterns.add(pattern)

    def _extract_implications(self, text: str, implications: set):
        """Extract potential implications from text"""
        implication_indicators = {
            'privacy_risk': ['expose', 'vulnerable', 'compromise', 'risk'],
            'control_increase': ['expand', 'growth', 'increase', 'more'],
            'rights_reduction': ['limit', 'restrict', 'reduce', 'prevent'],
            'resistance_opportunity': ['alternative', 'solution', 'protect', 'secure']
        }
        
        for implication, indicators in implication_indicators.items():
            if any(indicator in text for indicator in indicators):
                implications.add(implication)