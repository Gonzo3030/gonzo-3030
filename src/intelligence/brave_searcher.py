from typing import List, Dict, Any
import asyncio

class BraveSearcher:
    def __init__(self):
        self.last_search_time = None
        self.topics = [
            'corporate manipulation',
            'AI regulation',
            'privacy rights',
            'decentralization',
            'digital resistance',
            'surveillance state',
            'corporate oligarchy',
            'tech monopolies',
            'narrative control',
            'data exploitation'
        ]
        # Prevent too frequent searches
        self.min_search_interval = 300  # 5 minutes

    async def monitor_topics(self) -> List[Dict[str, Any]]:
        """Monitor topics for significant developments.

        Returns:
            List of significant findings.
        """
        try:
            # Respect minimum search interval
            if self.last_search_time and \
               (asyncio.get_event_loop().time() - self.last_search_time) < self.min_search_interval:
                return []

            all_findings = []
            for topic in self.topics:
                try:
                    findings = await self._search_topic(topic)
                    if findings:
                        all_findings.extend(findings)
                    # Small delay between searches to prevent rapid-fire API calls
                    await asyncio.sleep(1)
                except Exception as e:
                    print(f'Error searching topic {topic}: {str(e)}')

            self.last_search_time = asyncio.get_event_loop().time()
            return all_findings

        except Exception as e:
            print(f'Error in monitor_topics: {str(e)}')
            return []

    async def _search_topic(self, topic: str) -> List[Dict[str, Any]]:
        """Search for a single topic using Brave search.

        Args:
            topic: Topic to search for.

        Returns:
            List of significant findings for the topic.
        """
        try:
            # Use the provided brave_web_search function
            query = f'"{topic}" (news OR article OR report) when:7d'  # Last 7 days only
            response = await brave_web_search(
                query=query,
                count=5  # Limit to 5 results per topic to avoid overwhelming
            )
            
            if not response or not response.get('web', []):
                return []
                
            # Process results
            findings = []
            for result in response.get('web', []):
                finding = {
                    'title': result.get('title', '').strip(),
                    'url': result.get('url', '').strip(),
                    'description': result.get('description', '').strip(),
                    'published_date': result.get('published_time', ''),
                    'topic': topic,
                    'age': result.get('age', ''),
                    'significance': self._calculate_significance(result)
                }
                findings.append(finding)
                
            # Sort by significance and return top findings
            findings.sort(key=lambda x: x['significance'], reverse=True)
            return [f for f in findings[:2] if f['significance'] > 0.6]  # Only return high significance items
            
        except Exception as e:
            print(f'Error in _search_topic for {topic}: {str(e)}')
            return []
    
    def _calculate_significance(self, result: Dict[str, Any]) -> float:
        """Calculate significance score for a search result.

        Args:
            result: Search result dictionary.

        Returns:
            Significance score between 0 and 1.
        """
        score = 0.5  # Base score
        
        # Boost score based on freshness
        age = result.get('age', '').lower()
        if 'minute' in age or 'hour' in age:
            score += 0.3
        elif 'day' in age:
            try:
                days = int(age.split()[0])
                if days <= 1:
                    score += 0.25
                elif days <= 3:
                    score += 0.15
                elif days <= 7:
                    score += 0.05
            except:
                pass
                
        # Check title and description for significance indicators
        text = (result.get('title', '') + ' ' + result.get('description', '')).lower()
        
        # Breaking news and urgency indicators
        urgency_terms = ['breaking', 'urgent', 'alert', 'just in', 'developing']
        if any(term in text for term in urgency_terms):
            score += 0.2
            
        # Impact indicators
        impact_terms = ['announced', 'reveals', 'major', 'significant', 'breakthrough', 
                       'investigation', 'exclusive', 'report finds']
        if any(term in text for term in impact_terms):
            score += 0.15
            
        # Risk or warning indicators
        risk_terms = ['warning', 'risk', 'threat', 'danger', 'critical', 'urgent',
                     'vulnerability', 'exploit', 'breach', 'violation']
        if any(term in text for term in risk_terms):
            score += 0.1

        return min(score, 1.0)  # Cap at 1.0
