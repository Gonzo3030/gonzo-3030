import unittest
import asyncio
from datetime import datetime
from typing import Dict, List

from src.core.personality import GonzoPersonality
from src.core.response_crafter import ResponseCrafter, ResponseTone
from src.social.twitter_client import TwitterClient
from src.config.settings import Config

class TestGonzoBasics(unittest.TestCase):
    """Basic tests to verify Gonzo's core functionality"""
    
    def setUp(self):
        """Set up test environment"""
        self.config = Config()
        
    def test_env_loading(self):
        """Test that environment variables are loading"""
        self.assertIsNotNone(self.config.twitter.api_key)
        self.assertIsNotNone(self.config.twitter.api_secret)

class TestTwitterConnection(unittest.TestCase):
    """Test Twitter connectivity"""
    
    def setUp(self):
        self.config = Config()
        self.client = TwitterClient(self.config)
    
    def test_client_initialization(self):
        """Test Twitter client setup"""
        self.assertIsNotNone(self.client)

def run_tests():
    unittest.main()

if __name__ == '__main__':
    run_tests()