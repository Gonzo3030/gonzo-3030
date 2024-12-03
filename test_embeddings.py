from openai import OpenAI
import os
from dotenv import load_dotenv

def test_embeddings():
    load_dotenv()
    
    # Initialize the client with your API key
    client = OpenAI()
    
    try:
        # Try to create an embedding
        response = client.embeddings.create(
            model="text-embedding-ada-002",
            input="Testing Gonzo's embedding access."
        )
        print("✅ Embedding access confirmed!")
        print(f"Embedding dimensions: {len(response.data[0].embedding)}")
        return True
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_embeddings()