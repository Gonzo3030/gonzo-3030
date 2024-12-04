    def get_mentions(self, since_minutes: int = 5) -> List[Dict]:
        """Get recent mentions of the account with rate limiting"""
        if not self._get_user_id():
            return []
            
        try:
            self._wait_for_rate_limit('mentions')
            
            # Calculate start time
            start_time = (datetime.utcnow() - timedelta(minutes=since_minutes)).isoformat() + 'Z'
            
            # Build query parameters
            params = {
                'start_time': start_time,
                'expansions': 'author_id,referenced_tweets.id',
                'tweet.fields': 'created_at,text,context_annotations'
            }
            
            if self.last_mention_id:
                params['since_id'] = self.last_mention_id
            
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
            
            # Update last mention ID
            if data.get('data'):
                self.last_mention_id = data['data'][0]['id']
            
            return data.get('data', [])
            
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