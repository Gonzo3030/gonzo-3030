from typing import Dict, List
import asyncio
from datetime import datetime, timedelta

class BraveSearcher:
    def __init__(self):
        self.last_search_time = {}
        self.cached_results = {}
        self.monitoring_topics = [
            "corporate manipulation",
            "AI regulation",
            "privacy rights",
            "decentralization",
            "digital resistance",
            "surveillance state",
            "corporate oligarchy",
            "tech monopolies",
            "narrative control",
            "data exploitation"
        ]
    
    async def monitor_topics(self, max_age_hours: int = 24) -> List[Dict]:
        """Monitor key topics for new developments"""
        new_findings = []
        
        for topic in self.monitoring_topics:
            # Only search if we haven't recently or if cache is old
            if self._should_search(topic, max_age_hours):
                results = await self._search_topic(topic)
                significant_updates = self._filter_significant(results, topic)
                if significant_updates:
                    new_findings.extend(significant_updates)
                    self.cached_results[topic] = results
                self.last_search_time[topic] = datetime.now()
        
        return new_findings
    
    async def _search_topic(self, topic: str) -> List[Dict]:
        """Search Brave for a specific topic"""
        try:
            response = await self._brave_search(topic)
            return response.get('results', [])
        except Exception as e:
            print(f"Error searching topic {topic}: {str(e)}")
            return []
    
    async def _brave_search(self, query: str) -> Dict:
        """Execute Brave search"""
        from brave_web_search import brave_web_search
        
        response = await brave_web_search(query=query)
        return response
    
    def _should_search(self, topic: str, max_age_hours: int) -> bool:
        """Determine if we should search for a topic again"""
        if topic not in self.last_search_time:
            return True
            
        time_since_last = datetime.now() - self.last_search_time[topic]
        return time_since_last > timedelta(hours=max_age_hours)
    
    def _filter_significant(self, results: List[Dict], topic: str) -> List[Dict]:
        """Filter for significant new information"""
        if not results or topic not in self.cached_results:
            return results
            
        # Get previously seen URLs
        old_urls = {r.get('url') for r in self.cached_results[topic]}
        
        # Filter for new results
        new_results = [r for r in results if r.get('url') not in old_urls]
        
        # Add basic significance scoring
        scored_results = []
        for result in new_results:
            score = self._calculate_significance(result, topic)
            if score > 0.5:  # Only include relatively significant results
                result['significance'] = score
                scored_results.append(result)
        
        return scored_results
    
    def _calculate_significance(self, result: Dict, topic: str) -> float:
        """Calculate significance score for a result"""
        score = 0.0
        
        # Age factor (newer is better)
        if 'published_date' in result:
            age_hours = (datetime.now() - datetime.fromisoformat(result['published_date'])).total_seconds() / 3600
            score += max(0, 1 - (age_hours / (24 * 7)))  # Full score if < 24h old, declining over a week
        
        # Relevance factor
        if 'relevance_score' in result:
            score += result['relevance_score'] * 0.3
        
        # Source credibility (if we had it)
        if 'source_credibility' in result:
            score += result['source_credibility'] * 0.2
        
        # Keyword matching
        text = (result.get('title', '') + ' ' + result.get('description', '')).lower()
        resistance_keywords = ['resistance', 'privacy', 'rights', 'freedom', 'decentralized', 'exposed', 'revealed']
        corporate_keywords = ['corporation', 'monopoly', 'control', 'surveillance', 'tracking', 'manipulation']
        
        keyword_score = sum(1 for k in resistance_keywords + corporate_keywords if k in text) / len(resistance_keywords + corporate_keywords)
        score += keyword_score * 0.3
        
        return min(1.0, score)  # Normalize to 0-1