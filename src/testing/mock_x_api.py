from typing import Dict, List, Optional
from datetime import datetime, timezone
import json
import os

class MockXAPI:
    def __init__(self):
        self.posts = []
        self.mentions = []
        self.user_id = "mock_user_123"
        self.test_data_dir = "test_data"
        self._ensure_test_dir_exists()
    
    def _ensure_test_dir_exists(self):
        """Create test data directory if it doesn't exist"""
        if not os.path.exists(self.test_data_dir):
            os.makedirs(self.test_data_dir)
    
    def create_post(self, text: str) -> Dict:
        """Simulate creating a post"""
        post_id = f"post_{len(self.posts) + 1}"
        post = {
            "id": post_id,
            "text": text,
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        self.posts.append(post)
        
        # Save post for analysis
        self._save_post(post)
        return {"data": post}
    
    def _save_post(self, post: Dict):
        """Save post to test data directory for analysis"""
        filename = os.path.join(self.test_data_dir, f"post_{post['id']}.json")
        with open(filename, 'w') as f:
            json.dump(post, f, indent=2)
    
    def get_mentions(self, since_minutes: int = 5) -> List[Dict]:
        """Simulate getting mentions"""
        return self.mentions
    
    def add_test_mention(self, text: str, author_id: str = "test_user"):
        """Add a test mention for development"""
        mention = {
            "id": f"mention_{len(self.mentions) + 1}",
            "text": text,
            "author_id": author_id,
            "created_at": datetime.now(timezone.utc).isoformat()
        }
        self.mentions.append(mention)
    
    def create_thread(self, posts: List[str]) -> List[Dict]:
        """Simulate creating a thread"""
        responses = []
        for post in posts:
            response = self.create_post(post)
            responses.append(response)
        return responses
    
    def get_posts(self) -> List[Dict]:
        """Get all posts for analysis"""
        return self.posts
    
    def clear_data(self):
        """Clear all test data"""
        self.posts = []
        self.mentions = []
        for file in os.listdir(self.test_data_dir):
            if file.endswith(".json"):
                os.remove(os.path.join(self.test_data_dir, file))