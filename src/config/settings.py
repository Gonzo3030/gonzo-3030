import os
from typing import Dict

class TwitterConfig:
    def __init__(self):
        self.api_key = os.getenv('TWITTER_API_KEY')
        self.api_secret = os.getenv('TWITTER_API_SECRET')
        self.access_token = os.getenv('TWITTER_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
        
        # Verify all required credentials are present
        self._verify_credentials()
    
    def _verify_credentials(self) -> None:
        required_vars = [
            'TWITTER_API_KEY',
            'TWITTER_API_SECRET',
            'TWITTER_ACCESS_TOKEN',
            'TWITTER_ACCESS_TOKEN_SECRET'
        ]
        
        missing = [var for var in required_vars if not os.getenv(var)]
        if missing:
            raise EnvironmentError(
                f"Missing required environment variables: {', '.join(missing)}"
            )

class Config:
    def __init__(self):
        self.twitter = TwitterConfig()
        
        # Runtime settings
        self.response_delay = {
            'min_seconds': 30,
            'max_seconds': 300
        }
        
        self.daily_limits = {
            'tweets': 100,
            'replies': 50,
            'mentions': 30
        }