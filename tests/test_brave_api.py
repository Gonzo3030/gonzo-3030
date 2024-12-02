from unittest.mock import patch
from brave_api_client import BraveAPIClient

class TestGonzoWithMockedBraveAPI(TestCase):
    @patch('brave_api_client.BraveAPIClient.search')
    async def test_gonzo_brave_api_integration(self, mock_search):
        mock_search.return_value = {
            "results": [
                {
                    "title": "Decentralization is the Future",
                    "url": "https://example.com/decentralization-article",
                    "relevance": 0.85
                },
                # ... other mock results
            ]
        }

        # Test Gonzo's behavior when interacting with the mocked Brave API
        response = await gonzo.process_input("What is the future of crypto?")
        self.assertIn("Decentralization is the Future", response)
        # Add more assertions to verify Gonzo's response
