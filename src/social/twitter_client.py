import tweepy
from typing import Dict, List, Optional
from datetime import datetime
import asyncio

from ..config.settings import Config

class TwitterClient:
    def __init__(self, config: Config):
        self.config = config
        self.client = self._initialize_client()
        self.last_tweet_time = None
        self.daily_counts = {
            'tweets': 0,
            'replies': 0,
            'mentions': 0
        }
    
    def _initialize_client(self) -> tweepy.Client:
        """Initialize the Twitter API v2 client."""
        return tweepy.Client(
            consumer_key=self.config.twitter.api_key,
            consumer_secret=self.config.twitter.api_secret,
            access_token=self.config.twitter.access_token,
            access_token_secret=self.config.twitter.access_token_secret
        )
    
    async def post_tweet(self, content: str) -> Dict:
        """Post a tweet with rate limiting and safety checks."""
        if not self._can_tweet():
            raise Exception("Tweet limit reached or too soon since last tweet")
        
        try:
            response = self.client.create_tweet(text=content)
            self._update_counts('tweets')
            self.last_tweet_time = datetime.now()
            return response.data
        except Exception as e:
            print(f"Error posting tweet: {e}")
            raise
    
    async def post_thread(self, tweets: List[str]) -> List[Dict]:
        """Post a thread of tweets."""
        responses = []
        previous_tweet_id = None
        
        for tweet in tweets:
            if previous_tweet_id:
                response = self.client.create_tweet(
                    text=tweet,
                    in_reply_to_tweet_id=previous_tweet_id
                )
            else:
                response = self.client.create_tweet(text=tweet)
            
            responses.append(response.data)
            previous_tweet_id = response.data['id']
            self._update_counts('tweets')
            await asyncio.sleep(2)  # Small delay between thread tweets
        
        return responses
    
    async def reply_to_tweet(self, tweet_id: str, content: str) -> Dict:
        """Reply to a specific tweet."""
        if not self._can_reply():
            raise Exception("Reply limit reached")
        
        response = self.client.create_tweet(
            text=content,
            in_reply_to_tweet_id=tweet_id
        )
        self._update_counts('replies')
        return response.data
    
    def _can_tweet(self) -> bool:
        """Check if we can tweet based on limits and timing."""
        if self.daily_counts['tweets'] >= self.config.daily_limits['tweets']:
            return False
            
        if self.last_tweet_time:
            time_since_last = (datetime.now() - self.last_tweet_time).seconds
            if time_since_last < self.config.response_delay['min_seconds']:
                return False
        
        return True
    
    def _can_reply(self) -> bool:
        """Check if we can reply based on limits."""
        return self.daily_counts['replies'] < self.config.daily_limits['replies']
    
    def _update_counts(self, action_type: str) -> None:
        """Update daily action counts."""
        self.daily_counts[action_type] += 1
    
    async def listen_for_mentions(self, callback) -> None:
        """Listen for mentions and handle them with the callback."""
        # Implementation will depend on whether you want to use streaming or polling
        pass