from typing import Dict, List, Any
from ..intelligence.brave_searcher import BraveSearcher

class ResponseResearcher:
    def __init__(self):
        self.brave_searcher = BraveSearcher()
        self.knowledge_system = None

    def set_knowledge_system(self, knowledge_system):
        """Set the knowledge system reference"""
        self.knowledge_system = knowledge_system

    async def research_response(self, mention: Dict) -> Dict[str, Any]:
        """Research context for a response to a mention"""
        # Extract key information from mention
        text = mention.get('text', '').lower()
        
        # Remove the @mention part
        text = ' '.join([word for word in text.split() if not word.startswith('@')])
        
        # Extract key topics and queries
        research_queries = self._generate_research_queries(text)
        
        # Conduct research
        research_results = []
        for query in research_queries:
            try:
                results = await self.brave_searcher._search_topic(query)
                if results:
                    research_results.extend(results)
            except Exception as e:
                print(f'Error researching query {query}: {str(e)}')

        # Analyze findings
        analysis = self._analyze_research_results(research_results)
        
        return {
            'original_text': text,
            'research_results': research_results,
            'analysis': analysis,
            'response_recommendations': self._generate_response_recommendations(analysis)
        }

    def _generate_research_queries(self, text: str) -> List[str]:
        """Generate research queries based on mention text"""
        queries = []
        
        # Basic cleanup
        text = text.replace('?', ' ').replace('!', ' ')
        words = text.split()
        
        # Look for key phrases
        key_phrases = []
        for i in range(len(words)):
            if i+2 < len(words):
                phrase = ' '.join(words[i:i+3])
                if self._is_relevant_phrase(phrase):
                    key_phrases.append(phrase)
        
        # Generate specific queries
        if key_phrases:
            for phrase in key_phrases:
                queries.append(f'"{phrase}" corporate influence recent')
                queries.append(f'"{phrase}" privacy implications')
                queries.append(f'"{phrase}" regulation policy')
        else:
            # Fallback to topic extraction
            queries = self._extract_topic_queries(text)
        
        return queries[:3]  # Limit to top 3 most relevant queries