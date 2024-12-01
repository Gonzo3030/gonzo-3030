from typing import Dict, List, Optional
from datetime import datetime
import asyncio

class BraveIntelligence:
    def __init__(self):
        self.search_categories = {
            "crypto": {
                "queries": [
                    "cryptocurrency regulation news",
                    "defi governance proposals",
                    "crypto privacy developments",
                    "blockchain censorship resistance",
                    "web3 corporate adoption risks"
                ],
                "relevance_threshold": 0.7
            },
            "corporate_control": {
                "queries": [
                    "big tech surveillance",
                    "corporate data collection",
                    "privacy violation news",
                    "digital rights erosion",
                    "tech company merger monopoly"
                ],
                "relevance_threshold": 0.8
            },
            "resistance": {
                "queries": [
                    "decentralization movement",
                    "privacy tech advancement",
                    "anti-surveillance tools",
                    "digital freedom projects",
                    "data sovereignty initiatives"
                ],
                "relevance_threshold": 0.6
            }
        }

    async def gather_intel(self) -> Dict:
        """Gather intelligence from Brave Search across all categories."""
        intel_results = {}
        
        for category, config in self.search_categories.items():
            category_results = []
            for query in config["queries"]:
                results = await self._execute_brave_search(query)
                filtered_results = self._filter_results(
                    results, 
                    config["relevance_threshold"]
                )
                category_results.extend(filtered_results)
            intel_results[category] = category_results
        
        return self._analyze_intel(intel_results)

    async def _execute_brave_search(self, query: str) -> Dict:
        """Execute a search using Brave's API."""
        try:
            # Use the brave_web_search function
            results = await self._brave_web_search(query)
            return self._parse_search_results(results)
        except Exception as e:
            print(f"Error in Brave search: {e}")
            return {"results": [], "error": str(e)}

    async def _brave_web_search(self, query: str) -> Dict:
        """Wrapper for Brave search API call."""
        return await self._call_brave_api({
            "query": query,
            "count": 10  # Limit to top 10 results per query
        })

    def _parse_search_results(self, raw_results: Dict) -> List[Dict]:
        """Parse and structure the raw search results."""
        parsed_results = []
        for result in raw_results.get("results", []):
            parsed_results.append({
                "title": result.get("title", ""),
                "description": result.get("description", ""),
                "url": result.get("url", ""),
                "timestamp": datetime.now().isoformat(),
                "relevance_score": self._calculate_initial_relevance(result)
            })
        return parsed_results

    def _calculate_initial_relevance(self, result: Dict) -> float:
        """Calculate initial relevance score for a search result."""
        score = 0.0
        content = (f"{result.get('title', '')} {result.get('description', '')}").lower()
        
        # Key indicators that increase relevance
        indicators = {
            "high": [
                "privacy", "surveillance", "control", "regulation",
                "corporate", "monopoly", "resistance", "freedom"
            ],
            "medium": [
                "blockchain", "cryptocurrency", "defi", "web3",
                "decentralized", "governance"
            ],
            "low": [
                "technology", "digital", "future", "development"
            ]
        }
        
        # Calculate score based on indicators
        for indicator in indicators["high"]:
            if indicator in content:
                score += 0.3
        for indicator in indicators["medium"]:
            if indicator in content:
                score += 0.2
        for indicator in indicators["low"]:
            if indicator in content:
                score += 0.1
                
        return min(1.0, score)

    def _filter_results(self, results: List[Dict], threshold: float) -> List[Dict]:
        """Filter results based on relevance threshold."""
        return [r for r in results if r["relevance_score"] >= threshold]

    def _analyze_intel(self, intel_results: Dict) -> Dict:
        """Analyze gathered intelligence for actionable insights."""
        analysis = {
            "urgent_warnings": [],
            "trends": [],
            "resistance_opportunities": [],
            "educational_content": []
        }
        
        # Process each category
        for category, results in intel_results.items():
            for result in results:
                if self._is_urgent_warning(result):
                    analysis["urgent_warnings"].append(self._format_warning(result))
                if self._is_trend(result):
                    analysis["trends"].append(self._format_trend(result))
                if self._is_resistance_opportunity(result):
                    analysis["resistance_opportunities"].append(
                        self._format_opportunity(result)
                    )
                if self._is_educational(result):
                    analysis["educational_content"].append(
                        self._format_educational(result)
                    )
        
        return analysis

    def _format_warning(self, result: Dict) -> Dict:
        """Format an urgent warning from a result."""
        return {
            "type": "warning",
            "title": result["title"],
            "threat_level": self._assess_threat_level(result),
            "dystopian_parallel": self._find_dystopian_parallel(result),
            "action_needed": self._suggest_action(result)
        }

    def _format_trend(self, result: Dict) -> Dict:
        """Format a trend analysis from a result."""
        return {
            "type": "trend",
            "pattern": result["title"],
            "implications": self._analyze_implications(result),
            "timeline_impact": self._predict_timeline_impact(result)
        }

    def _is_urgent_warning(self, result: Dict) -> bool:
        """Determine if a result constitutes an urgent warning."""
        urgent_indicators = [
            "regulation", "control", "surveillance",
            "merger", "acquisition", "compliance"
        ]
        return any(indicator in result["title"].lower() for indicator in urgent_indicators)

    def _is_trend(self, result: Dict) -> bool:
        """Determine if a result represents a significant trend."""
        trend_indicators = [
            "growing", "emerging", "rising", "increasing",
            "adoption", "movement", "shift"
        ]
        return any(indicator in result["description"].lower() for indicator in trend_indicators)

    def _find_dystopian_parallel(self, result: Dict) -> str:
        """Find parallel between current event and dystopian future."""
        # Implementation for finding dystopian parallels
        pass