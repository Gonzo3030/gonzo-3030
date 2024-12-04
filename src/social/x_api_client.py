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