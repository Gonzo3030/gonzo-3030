import asyncio
from config.settings import Config
from social.twitter_client import TwitterClient
from core.response_crafter import ResponseCrafter, ResponseTone

async def test_first_tweet():
    config = Config()
    twitter = TwitterClient(config)
    crafter = ResponseCrafter()
    
    # Craft Gonzo's first tweet
    first_tweet = await crafter.craft_response(
        context={"type": "introduction"},
        tone=ResponseTone.PROPHETIC,
        knowledge={},
        patterns={}
    )
    
    # Post the tweet
    response = await twitter.post_tweet(first_tweet)
    print(f"Tweet posted! ID: {response['id']}")

if __name__ == "__main__":
    asyncio.run(test_first_tweet())