import os
import requests
import time
from requests_oauthlib import OAuth1
from datetime import datetime, timedelta
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
    
    def _get_user_id(self) -> Optional[str]:
        """Get the authenticated user's ID with rate limiting"""
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