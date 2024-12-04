import os
import requests
import time
from requests_oauthlib import OAuth1
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
from dotenv import load_dotenv

class XAPIClient:
    def __init__(self):
        load_dotenv()
        
        # Load credentials
        self.api_key = os.getenv('X_API_KEY')
        self.api_secret = os.getenv('X_API_SECRET')
        self.access_token = os.getenv('X_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('X_ACCESS_SECRET')
        
        if not all([self.api_key, self.api_secret, self.access_token, self.access_token_secret]):
            raise ValueError("Missing required X API credentials in .env file")
        
        # Set up OAuth
        self.auth = OAuth1(
            self.api_key,
            self.api_secret,
            self.access_token,
            self.access_token_secret
        )
        
        self.base_url = 'https://api.twitter.com/2'
        self.user_id = None  # Will be set on first use
        
        # Rate limiting parameters
        self.rate_limits = {
            'mentions': {'calls': 0, 'reset_time': time.time(), 'max_calls': 180, 'window': 900},  # 180 calls per 15 min
            'posts': {'calls': 0, 'reset_time': time.time(), 'max_calls': 50, 'window': 900},      # 50 posts per 15 min
            'general': {'calls': 0, 'reset_time': time.time(), 'max_calls': 180, 'window': 900}    # 180 calls per 15 min
        }
        
        # Store last mention ID for pagination
        self.last_mention_id = None

    def _check_rate_limit(self, endpoint_type: str) -> bool:
        """Check if we're within rate limits for the specified endpoint type"""
        now = time.time()
        limit_info = self.rate_limits[endpoint_type]
        
        # Reset counters if window has passed
        if now >= limit_info['reset_time'] + limit_info['window']:
            limit_info['calls'] = 0
            limit_info['reset_time'] = now
            return True
        
        # Check if we're at the limit
        return limit_info['calls'] < limit_info['max_calls']
    
    def _increment_rate_limit(self, endpoint_type: str):
        """Increment the rate limit counter for the specified endpoint type"""
        self.rate_limits[endpoint_type]['calls'] += 1
    
    def _get_rate_limit_reset(self, endpoint_type: str) -> int:
        """Get seconds until rate limit reset"""
        now = time.time()
        limit_info = self.rate_limits[endpoint_type]
        return max(0, int(limit_info['reset_time'] + limit_info['window'] - now))
    
    def _wait_for_rate_limit(self, endpoint_type: str):
        """Wait if rate limit is exceeded"""
        while not self._check_rate_limit(endpoint_type):
            reset_time = self._get_rate_limit_reset(endpoint_type)
            print(f'Rate limit exceeded for {endpoint_type}. Waiting {reset_time} seconds...')
            time.sleep(min(reset_time + 1, 60))  # Wait up to 60 seconds
    
    def get_user_id(self) -> Optional[str]:
        """Get the authenticated user's ID"""
        if self.user_id:
            return self.user_id
            
        try:
            self._wait_for_rate_limit('general')
                
            endpoint = f'{self.base_url}/users/me'
            response = requests.get(
                endpoint,
                auth=self.auth
            )
            
            self._increment_rate_limit('general')
            
            if response.status_code == 429:  # Rate limit exceeded
                reset_time = int(response.headers.get('x-rate-limit-reset', 900))
                print(f'Rate limit exceeded for user lookup. Reset in {reset_time} seconds.')
                return None
                
            response.raise_for_status()
            self.user_id = response.json().get('data', {}).get('id')
            return self.user_id
            
        except Exception as e:
            print(f'Error getting user ID: {str(e)}')
            return None

    def _format_datetime(self, dt: datetime) -> str:
        """Format datetime for X API in ISO 8601 format."""
        # Ensure datetime is UTC
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        elif dt.tzinfo != timezone.utc:
            dt = dt.astimezone(timezone.utc)
        
        # Format with RFC 3339 format (required by X API)
        return dt.strftime('%Y-%m-%dT%H:%M:%SZ')
    
    def get_mentions(self, since_minutes: int = 5) -> List[Dict]:
        """Get recent mentions of the account"""
        if not self.get_user_id():
            return []
            
        try:
            self._wait_for_rate_limit('mentions')
            
            # Calculate start time with proper timezone handling
            start_time = datetime.now(timezone.utc) - timedelta(minutes=since_minutes)
            
            # Build query parameters
            params = {
                'expansions': 'author_id,referenced_tweets.id',
                'tweet.fields': 'created_at,text'
            }
            
            # Use either since_id or start_time, not both
            if self.last_mention_id:
                params['since_id'] = self.last_mention_id
            else:
                params['start_time'] = self._format_datetime(start_time)
            
            # Make request
            endpoint = f'{self.base_url}/users/{self.user_id}/mentions'
            response = requests.get(
                endpoint,
                params=params,
                auth=self.auth
            )
            
            self._increment_rate_limit('mentions')
            
            if response.status_code == 429:  # Rate limit exceeded
                reset_time = int(response.headers.get('x-rate-limit-reset', 900))
                print(f'Rate limit exceeded for mentions. Reset in {reset_time} seconds.')
                return []
            
            response.raise_for_status()
            data = response.json()
            
            # Update last mention ID if we got results
            if data.get('data'):
                self.last_mention_id = data['data'][0]['id']
                return data['data']
            return []
            
        except Exception as e:
            print(f'Error getting mentions: {str(e)}')
            return []
    
    def create_post(self, text: str) -> Dict:
        """Create a new post with rate limiting"""
        try:
            self._wait_for_rate_limit('posts')
            
            endpoint = f'{self.base_url}/tweets'
            headers = {'Content-Type': 'application/json'}
            data = {'text': str(text)[:280]}  # Ensure text is a string and within limits
            
            response = requests.post(
                endpoint,
                headers=headers,
                json=data,
                auth=self.auth
            )
            
            self._increment_rate_limit('posts')
            
            if response.status_code == 429:  # Rate limit exceeded
                reset_time = int(response.headers.get('x-rate-limit-reset', 900))
                print(f'Rate limit exceeded for posting. Reset in {reset_time} seconds.')
                return None
            
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            print(f'Error creating post: {str(e)}')
            return None

    def create_thread(self, posts: List[str]) -> List[Dict]:
        """Create a thread with rate limiting"""
        if not posts:
            return None
            
        responses = []
        previous_tweet_id = None
        
        for post in posts:
            try:
                self._wait_for_rate_limit('posts')
                
                endpoint = f'{self.base_url}/tweets'
                headers = {'Content-Type': 'application/json'}
                
                # Ensure post is a string and within limits
                text = str(post)[:280]
                data = {'text': text}
                
                if previous_tweet_id:
                    data['reply'] = {
                        'in_reply_to_tweet_id': previous_tweet_id
                    }
                
                response = requests.post(
                    endpoint,
                    headers=headers,
                    json=data,
                    auth=self.auth
                )
                
                self._increment_rate_limit('posts')
                
                if response.status_code == 429:  # Rate limit exceeded
                    reset_time = int(response.headers.get('x-rate-limit-reset', 900))
                    print(f'Rate limit exceeded in thread creation. Reset in {reset_time} seconds.')
                    break
                
                response.raise_for_status()
                result = response.json()
                responses.append(result)
                previous_tweet_id = result.get('data', {}).get('id')
                
                # Small delay between thread posts to prevent rapid-fire posting
                time.sleep(2)
                
            except Exception as e:
                print(f'Error in thread creation: {str(e)}')
                return None
            
        return responses