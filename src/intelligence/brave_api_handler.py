from typing import Dict, List, Optional
from datetime import datetime, timedelta
import asyncio

class BraveAPIHandler:
    def __init__(self):
        self.cache = {}
        self.cache_duration = timedelta(hours=1)  # Cache results for 1 hour
        
        self.search_limits = {
            "daily": 1000,         # Daily search limit
            "per_minute": 10,      # Rate limit per minute
            "concurrent": 3        # Max concurrent searches
        }
        
        self.current_searches = 0
        self.daily_searches = 0
        self.last_reset = datetime.now()
        
        # Semaphore for concurrent request limiting
        self.search_semaphore = asyncio.Semaphore(self.search_limits["concurrent"])

    async def search(self, query: str, count: int = 10) -> Dict:
        """Execute a search using Brave Search API with rate limiting."""
        # Check cache first
        cache_key = f"{query}_{count}"
        cached_result = self._get_from_cache(cache_key)
        if cached_result:
            return cached_result
        
        # Check and update rate limits
        await self._check_rate_limits()
        
        # Execute search with semaphore
        async with self.search_semaphore:
            try:
                result = await self._execute_brave_search(query, count)
                self._update_cache(cache_key, result)
                return result
            finally:
                await self._update_search_counts()

    async def _execute_brave_search(self, query: str, count: int) -> Dict:
        """Execute the actual Brave search API call."""
        try:
            result = await brave_web_search({
                "query": query,
                "count": min(count, 20)  # Ensure within API limits
            })
            
            return self._process_response(result)
        except Exception as e:
            print(f"Brave search error: {e}")
            return {"error": str(e), "results": []}

    def _process_response(self, response: Dict) -> Dict:
        """Process and structure the API response."""
        processed_results = []
        
        for result in response.get("results", []):
            processed_results.append({
                "title": result.get("title", ""),
                "description": result.get("description", ""),
                "url": result.get("url", ""),
                "timestamp": datetime.now().isoformat(),
                "metadata": {
                    "age": result.get("age"),
                    "score": result.get("score"),
                    "type": result.get("type")
                }
            })
        
        return {
            "results": processed_results,
            "total": len(processed_results),
            "timestamp": datetime.now().isoformat()
        }

    async def _check_rate_limits(self) -> None:
        """Check and enforce rate limits."""
        # Reset daily count if needed
        if datetime.now() - self.last_reset > timedelta(days=1):
            self.daily_searches = 0
            self.last_reset = datetime.now()
        
        # Check daily limit
        if self.daily_searches >= self.search_limits["daily"]:
            raise Exception("Daily search limit reached")
        
        # Check per-minute limit
        if self.current_searches >= self.search_limits["per_minute"]:
            await asyncio.sleep(60)  # Wait for a minute
            self.current_searches = 0

    async def _update_search_counts(self) -> None:
        """Update search count trackers."""
        self.current_searches += 1
        self.daily_searches += 1
        
        # Reset current searches count after a minute
        asyncio.create_task(self._reset_current_searches())

    async def _reset_current_searches(self) -> None:
        """Reset current searches count after one minute."""
        await asyncio.sleep(60)
        self.current_searches = max(0, self.current_searches - 1)

    def _get_from_cache(self, key: str) -> Optional[Dict]:
        """Get results from cache if available and fresh."""
        if key in self.cache:
            result, timestamp = self.cache[key]
            if datetime.now() - timestamp < self.cache_duration:
                return result
            else:
                del self.cache[key]  # Remove stale cache entry
        return None

    def _update_cache(self, key: str, result: Dict) -> None:
        """Update cache with new results."""
        self.cache[key] = (result, datetime.now())
        
        # Cleanup old cache entries
        self._cleanup_cache()

    def _cleanup_cache(self) -> None:
        """Remove stale entries from cache."""
        current_time = datetime.now()
        keys_to_remove = [
            key for key, (_, timestamp) in self.cache.items()
            if current_time - timestamp > self.cache_duration
        ]
        
        for key in keys_to_remove:
            del self.cache[key]