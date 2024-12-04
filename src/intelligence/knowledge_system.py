from typing import Dict, List, Any
from datetime import datetime, timezone
import json
import os

class KnowledgeSystem:
    def __init__(self):
        self.current_insights = {}
        self.pattern_database = []
        self.historical_context = {}
        
        # Initialize knowledge categories
        self.categories = {
            'corporate_tactics': {
                'manipulation_patterns': set(),
                'known_actors': set(),
                'impact_assessment': {}
            },
            'tech_developments': {
                'privacy_concerns': set(),
                'emerging_threats': set(),
                'regulatory_changes': set()
            },
            'social_impacts': {
                'affected_groups': set(),
                'resistance_movements': set(),
                'success_stories': set()
            }
        }
    
    def analyze_finding(self, finding: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a new finding and extract insights"""
        insights = {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'topic': finding.get('topic'),
            'patterns': self._extract_patterns(finding),
            'actors': self._identify_actors(finding),
            'impact': self._assess_impact(finding),
            'recommendations': self._generate_recommendations(finding)
        }
        
        # Update knowledge base
        self._update_knowledge(insights)
        return insights
    
    def _extract_patterns(self, finding: Dict[str, Any]) -> List[str]:
        """Extract manipulation patterns from finding"""
        patterns = []
        text = f"{finding.get('title', '')} {finding.get('description', '')}".lower()
        
        # Pattern recognition logic would go here
        # For now, using simple keyword matching
        pattern_indicators = {
            'data_harvesting': ['collect data', 'user data', 'personal information'],
            'attention_manipulation': ['engagement', 'algorithm change', 'feed update'],
            'narrative_control': ['policy update', 'content moderation', 'community guidelines'],
            'market_dominance': ['acquisition', 'merger', 'market share'],
            'regulatory_capture': ['lobbying', 'regulation', 'compliance'],
        }
        
        for pattern, indicators in pattern_indicators.items():
            if any(indicator in text for indicator in indicators):
                patterns.append(pattern)
        
        return patterns
    
    def _identify_actors(self, finding: Dict[str, Any]) -> List[str]:
        """Identify key actors involved"""
        # This would involve entity recognition and actor classification
        # For now, using placeholder logic
        text = f"{finding.get('title', '')} {finding.get('description', '')}".lower()
        actors = []
        
        # Example actor identification
        major_tech = ['google', 'meta', 'amazon', 'apple', 'microsoft']
        for company in major_tech:
            if company in text:
                actors.append(company)
        
        return actors
    
    def _assess_impact(self, finding: Dict[str, Any]) -> Dict[str, Any]:
        """Assess potential impact of the finding"""
        impact = {
            'severity': self._calculate_severity(finding),
            'affected_areas': self._identify_affected_areas(finding),
            'timeline': self._estimate_timeline(finding),
            'resistance_potential': self._assess_resistance_potential(finding)
        }
        return impact
    
    def _calculate_severity(self, finding: Dict[str, Any]) -> float:
        """Calculate severity score based on various factors"""
        severity = 0.5  # Base severity
        
        # Factor in immediacy
        if finding.get('age', '').lower() in ['hour', 'hours', 'day']:
            severity += 0.2
            
        # Factor in reach/scope
        text = f"{finding.get('title', '')} {finding.get('description', '')}".lower()
        scope_terms = ['worldwide', 'global', 'all users', 'billion', 'million']
        if any(term in text for term in scope_terms):
            severity += 0.2
            
        return min(severity, 1.0)
    
    def _generate_recommendations(self, finding: Dict[str, Any]) -> List[str]:
        """Generate actionable recommendations"""
        recommendations = []
        patterns = self._extract_patterns(finding)
        
        # Map patterns to specific recommendations
        recommendation_map = {
            'data_harvesting': [
                'Use privacy-focused alternatives',
                'Encrypt your communications',
                'Regularly audit your data permissions'
            ],
            'attention_manipulation': [
                'Use content blockers',
                'Set strict usage limits',
                'Curate your information sources'
            ],
            'narrative_control': [
                'Diversify your news sources',
                'Support independent journalism',
                'Join decentralized platforms'
            ],
            'market_dominance': [
                'Support local alternatives',
                'Push for anti-trust action',
                'Use open-source solutions'
            ],
            'regulatory_capture': [
                'Contact your representatives',
                'Support digital rights organizations',
                'Join advocacy groups'
            ]
        }
        
        for pattern in patterns:
            if pattern in recommendation_map:
                recommendations.extend(recommendation_map[pattern])
        
        return list(set(recommendations))  # Remove duplicates
    
    def _update_knowledge(self, insights: Dict[str, Any]):
        """Update internal knowledge base with new insights"""
        topic = insights.get('topic')
        if not topic:
            return
            
        # Update pattern database
        self.pattern_database.extend(insights.get('patterns', []))
        
        # Update current insights
        self.current_insights[topic] = {
            'last_updated': insights['timestamp'],
            'patterns': insights.get('patterns', []),
            'actors': insights.get('actors', []),
            'impact': insights.get('impact', {})
        }
        
        # Update relevant categories
        if 'corporate' in topic:
            self.categories['corporate_tactics']['manipulation_patterns'].update(insights.get('patterns', []))
            self.categories['corporate_tactics']['known_actors'].update(insights.get('actors', []))
        elif 'tech' in topic:
            self.categories['tech_developments']['emerging_threats'].update(insights.get('patterns', []))
        elif 'social' in topic:
            self.categories['social_impacts']['affected_groups'].update(self._identify_affected_groups(insights))
    
    def _identify_affected_groups(self, insights: Dict[str, Any]) -> set:
        """Identify groups affected by the insights"""
        # This would involve more sophisticated analysis
        # For now, using placeholder logic
        return {'users', 'consumers', 'citizens'}
    
    def get_current_assessment(self) -> Dict[str, Any]:
        """Get current assessment of the situation"""
        return {
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'active_patterns': list(set(self.pattern_database[-50:])),  # Most recent patterns
            'key_actors': list(self.categories['corporate_tactics']['known_actors']),
            'threat_assessment': self._generate_threat_assessment(),
            'recommended_actions': self._generate_action_plan()
        }
    
    def _generate_threat_assessment(self) -> Dict[str, Any]:
        """Generate comprehensive threat assessment"""
        # This would involve analyzing patterns and trends
        # For now, using placeholder logic
        return {
            'severity': self._calculate_overall_severity(),
            'trends': self._identify_trends(),
            'emerging_threats': list(self.categories['tech_developments']['emerging_threats'])
        }
    
    def _calculate_overall_severity(self) -> float:
        """Calculate overall severity based on current knowledge"""
        if not self.current_insights:
            return 0.5
            
        severities = []
        for topic_data in self.current_insights.values():
            if 'impact' in topic_data and 'severity' in topic_data['impact']:
                severities.append(topic_data['impact']['severity'])
        
        return sum(severities) / len(severities) if severities else 0.5
    
    def _identify_trends(self) -> List[str]:
        """Identify current trends from knowledge base"""
        # This would involve trend analysis
        # For now, using placeholder logic
        return list(self.pattern_database[-10:])  # Most recent patterns