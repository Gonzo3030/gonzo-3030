from typing import List, Dict, Any

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

    async def monitor_topics(self) -> List[Dict[str, Any]]:
        """Monitor topics for significant developments.

        Returns:
            List of significant findings.
        """
        all_findings = []
        for topic in self.topics:
            try:
                findings = await self._search_topic(topic)
                all_findings.extend(findings)
            except Exception as e:
                print(f'Error searching topic {topic}: {str(e)}')
        return all_findings

    async def _search_topic(self, topic: str) -> List[Dict[str, Any]]:
        """Search for a single topic using Brave search.

        Args:
            topic: Topic to search for.

        Returns:
            List of significant findings for the topic.
        """
        try:
            # Use the provided brave_web_search function
            query = f'"{topic}" news articles recent developments'
            response = await brave_web_search(
                query=query,
                count=10  # Get 10 results per topic
            )
            
            if not response:
                return []
                
            # Process results
            findings = []
            for result in response.get('web', []):
                finding = {
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'description': result.get('description', ''),
                    'published_date': result.get('published_time', ''),
                    'topic': topic,
                    'significance': self._calculate_significance(result)
                }
                findings.append(finding)
                
            # Sort by significance and return top findings
            findings.sort(key=lambda x: x['significance'], reverse=True)
            return findings[:3]  # Return top 3 most significant findings
            
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
        # Start with base score
        score = 0.5
        
        # Factor in age of content if available
        if result.get('age'):
            if 'hour' in result['age']:
                score += 0.3
            elif 'day' in result['age'] and int(result['age'].split()[0]) <= 2:
                score += 0.2
            elif 'day' in result['age'] and int(result['age'].split()[0]) <= 7:
                score += 0.1
                
        # Factor in title relevance
        title = result.get('title', '').lower()
        if 'breaking' in title or 'urgent' in title:
            score += 0.2
        if 'announced' in title or 'reveals' in title:
            score += 0.1
            
        # Cap at 1.0
        return min(score, 1.0)
