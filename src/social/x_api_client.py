import os
import requests
from requests_oauthlib import OAuth1
from datetime import datetime
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
    
    def create_post(self, text: str) -> dict:
        """Create a new post with proper authentication"""
        endpoint = f'{self.base_url}/tweets'
        headers = {'Content-Type': 'application/json'}
        data = {'text': str(text)[:280]}  # Ensure text is a string and within limits
        
        try:
            response = requests.post(
                endpoint,
                headers=headers,
                json=data,
                auth=self.auth
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'Error creating post: {str(e)}')
            return None

    def create_thread(self, posts: list) -> list:
        """Create a thread from a list of posts"""
        if not posts:
            return None
            
        responses = []
        previous_tweet_id = None
        
        for post in posts:
            endpoint = f'{self.base_url}/tweets'
            headers = {'Content-Type': 'application/json'}
            
            # Ensure post is a string and within limits
            text = str(post)[:280]
            data = {'text': text}
            
            if previous_tweet_id:
                data['reply'] = {
                    'in_reply_to_tweet_id': previous_tweet_id
                }
            
            try:
                response = requests.post(
                    endpoint,
                    headers=headers,
                    json=data,
                    auth=self.auth
                )
                response.raise_for_status()
                result = response.json()
                responses.append(result)
                previous_tweet_id = result.get('data', {}).get('id')
            except Exception as e:
                print(f'Error in thread creation: {str(e)}')
                return None
            
        return responses