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
        if not self._get_user_id():
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