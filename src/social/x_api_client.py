import os
import requests
from datetime import datetime
from dotenv import load_dotenv

class XAPIClient:
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('X_API_KEY')
        self.api_secret = os.getenv('X_API_SECRET')
        self.access_token = os.getenv('X_ACCESS_TOKEN')
        self.access_token_secret = os.getenv('X_ACCESS_SECRET')
        self.base_url = 'https://api.twitter.com/2'
        
    def _get_headers(self):
        return {
            'Authorization': f'Bearer {self.access_token}',
            'Content-Type': 'application/json'
        }
    
    def create_post(self, text):
        """Create a new post"""
        endpoint = f'{self.base_url}/tweets'
        headers = self._get_headers()
        data = {'text': text}
        
        try:
            response = requests.post(endpoint, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            print(f'Error creating post: {str(e)}')
            return None

    def create_thread(self, posts):
        """Create a thread from a list of posts"""
        responses = []
        previous_tweet_id = None
        
        for post in posts:
            endpoint = f'{self.base_url}/tweets'
            headers = self._get_headers()
            
            data = {
                'text': post
            }
            
            if previous_tweet_id:
                data['reply'] = {
                    'in_reply_to_tweet_id': previous_tweet_id
                }
            
            try:
                response = requests.post(endpoint, headers=headers, json=data)
                response.raise_for_status()
                result = response.json()
                responses.append(result)
                previous_tweet_id = result.get('data', {}).get('id')
            except Exception as e:
                print(f'Error in thread creation: {str(e)}')
                return None
        
        return responses