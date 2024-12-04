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
            # Use the provided brave_web_search function
            results = await self.brave_web_search(
                query=topic,
                count=10  # Get 10 results per topic
            )
            
            processed_results = []
            for result in results.get('web', {}).get('results', []):
                processed_results.append({
                    'url': result.get('url'),
                    'title': result.get('title'),
                    'description': result.get('description'),
                    'published_date': result.get('published_time'),
                    'age_hours': self._calculate_age_hours(result.get('published_time'))
                })
            
            return processed_results
            
        except Exception as e:
            print(f"Error searching topic {topic}: {str(e)}")
            return []
    
    async def brave_web_search(self, query: str, count: int = 10) -> Dict:
        """Execute Brave search using provided function"""
        try:
            function_globals = globals()
            if 'brave_web_search' in function_globals:
                return await function_globals['brave_web_search'](query=query, count=count)
            else:
                print(f"brave_web_search function not available")
                return {'web': {'results': []}}
        except Exception as e:
            print(f"Error executing Brave search: {str(e)}")
            return {'web': {'results': []}}
    
    def _should_search(self, topic: str, max_age_hours: int) -> bool:
        """Determine if we should search for a topic again"""
        if topic not in self.last_search_time:
            return True
            
        time_since_last = datetime.now() - self.last_search_time[topic]
        return time_since_last > timedelta(hours=max_age_hours)
    
    def _calculate_age_hours(self, published_time: str) -> float:
        """Calculate age of article in hours"""
        if not published_time:
            return float('inf')
            
        try:
            pub_date = datetime.fromisoformat(published_time.replace('Z', '+00:00'))
            age = datetime.now() - pub_date
            return age.total_seconds() / 3600
        except:
            return float('inf')
    
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
        age_hours = result.get('age_hours', float('inf'))
        if age_hours != float('inf'):
            score += max(0, 1 - (age_hours / (24 * 7)))  # Full score if < 24h old, declining over a week
        
        # Keyword matching
        text = (result.get('title', '') + ' ' + result.get('description', '')).lower()
        resistance_keywords = ['resistance', 'privacy', 'rights', 'freedom', 'decentralized', 'exposed', 'revealed']
        corporate_keywords = ['corporation', 'monopoly', 'control', 'surveillance', 'tracking', 'manipulation']
        
        keyword_score = sum(1 for k in resistance_keywords + corporate_keywords if k in text) / len(resistance_keywords + corporate_keywords)
        score += keyword_score * 0.3
        
        return min(1.0, score)  # Normalize to 0-1