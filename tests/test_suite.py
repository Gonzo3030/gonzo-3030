import unittest
import asyncio
from datetime import datetime
from typing import Dict, List

from src.core.personality import GonzoPersonality
from src.core.response_crafter import ResponseCrafter, ResponseTone
from src.intelligence.brave_intelligence import BraveIntelligence
from src.social.twitter_client import TwitterClient
from src.config.settings import Config

class TestGonzoPersonality(unittest.TestCase):
    def setUp(self):
        self.gonzo = GonzoPersonality()

    def test_personality_traits(self):
        """Test core personality attributes."""
        self.assertEqual(self.gonzo.core_identity["name"], "The Brown Buffalo")
        self.assertTrue("Digital Resistance Attorney" in self.gonzo.core_identity["role"])

    def test_vocal_patterns(self):
        """Test voice consistency."""
        self.assertTrue(any("Brown Buffalo" in prefix 
                          for prefix in self.gonzo.vocal_patterns["prefixes"]))
        self.assertTrue(any("resistance" in suffix 
                          for suffix in self.gonzo.vocal_patterns["suffixes"]))

class TestResponseGeneration(unittest.TestCase):
    def setUp(self):
        self.crafter = ResponseCrafter()

    async def test_response_length(self):
        """Test tweet length constraints."""
        response = await self.crafter.craft_response(
            context={"type": "test"},
            tone=ResponseTone.PROPHETIC,
            knowledge={},
            patterns={}
        )
        self.assertLessEqual(len(response), 280)  # Twitter limit

    async def test_response_tone(self):
        """Test different response tones."""
        for tone in ResponseTone:
            response = await self.crafter.craft_response(
                context={"type": "test"},
                tone=tone,
                knowledge={},
                patterns={}
            )
            self.assertIsNotNone(response)

class TestTwitterIntegration(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.client = TwitterClient(self.config)

    def test_rate_limiting(self):
        """Test rate limiting functionality."""
        self.client.daily_counts['tweets'] = self.config.daily_limits['tweets']
        with self.assertRaises(Exception):
            asyncio.run(self.client.post_tweet("Test tweet"))

    def test_thread_creation(self):
        """Test thread formatting."""
        tweets = ["Tweet 1", "Tweet 2", "Tweet 3"]
        formatted = self.client._format_thread(tweets)
        self.assertEqual(len(formatted), 3)
        self.assertTrue("1/3" in formatted[0])

class TestIntelligenceGathering(unittest.TestCase):
    def setUp(self):
        self.intelligence = BraveIntelligence()

    async def test_relevance_filtering(self):
        """Test content relevance filtering."""
        test_results = {
            "title": "Major Corporate Merger",
            "description": "Privacy concerns raised"
        }
        relevance = self.intelligence._calculate_initial_relevance(test_results)
        self.assertGreaterEqual(relevance, 0.0)
        self.assertLessEqual(relevance, 1.0)

class TestEndToEnd(unittest.TestCase):
    def setUp(self):
        self.config = Config()
        self.client = TwitterClient(self.config)
        self.crafter = ResponseCrafter()
        self.intelligence = BraveIntelligence()

    async def test_full_response_flow(self):
        """Test complete flow from intelligence to tweet."""
        # Gather intelligence
        intel = await self.intelligence.gather_intel()
        
        # Craft response
        response = await self.crafter.craft_response(
            context={"type": "test"},
            tone=ResponseTone.PROPHETIC,
            knowledge=intel,
            patterns={}
        )
        
        # Verify response
        self.assertIsNotNone(response)
        self.assertLessEqual(len(response), 280)

def run_tests():
    unittest.main()

if __name__ == '__main__':
    run_tests()