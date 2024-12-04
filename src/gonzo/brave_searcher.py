from typing import List, Dict, Any

class BraveSearcher:
    def __init__(self):
        self.last_search_time = None

    def search_topics(self, topics: List[str]) -> Dict[str, List[Dict[str, Any]]]:
        """Search for multiple topics using Brave search.

        Args:
            topics: List of topics to search for.

        Returns:
            Dictionary mapping topics to their search results.
        """
        results = {}
        for topic in topics:
            try:
                search_results = self._search_topic(topic)
                results[topic] = search_results
            except Exception as e:
                print(f'Error searching topic {topic}: {str(e)}')
                results[topic] = []
        return results

    def _search_topic(self, topic: str) -> List[Dict[str, Any]]:
        """Search for a single topic using Brave search.

        Args:
            topic: Topic to search for.

        Returns:
            List of search results.
        """
        try:
            # Add your search query modifiers here
            query = f'"{topic}" news articles recent developments'
            
            # Use the provided brave_web_search function
            response = brave_web_search(
                query=query,
                count=10  # Adjust as needed
            )
            
            # Process and return the results
            if not response or 'web' not in response:
                return []
                
            processed_results = []
            for result in response.get('web', []):
                processed_results.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'description': result.get('description', ''),
                    'published': result.get('published_time', '')
                })
                
            return processed_results
            
        except Exception as e:
            print(f'Error in _search_topic for {topic}: {str(e)}')
            return []
