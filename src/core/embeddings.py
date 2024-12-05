from typing import List, Dict, Any
import numpy as np
from langchain.embeddings import OpenAIEmbeddings

class EmbeddingProcessor:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        
    async def get_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Get embeddings for a list of texts."""
        try:
            embeddings = await self.embeddings.aembed_documents(texts)
            return embeddings
        except Exception as e:
            print(f"Error getting embeddings: {e}")
            return [[0.0] * 1536] * len(texts)  # Return zero embeddings as fallback
            
    def calculate_cosine_similarity(self, vec1: List[float], vec2: List[float]) -> float:
        """Calculate cosine similarity between two vectors."""
        if not vec1 or not vec2:
            return 0.0
            
        vec1 = np.array(vec1)
        vec2 = np.array(vec2)
        
        dot_product = np.dot(vec1, vec2)
        norm1 = np.linalg.norm(vec1)
        norm2 = np.linalg.norm(vec2)
        
        if norm1 == 0 or norm2 == 0:
            return 0.0
            
        return dot_product / (norm1 * norm2)
        
    async def calculate_group_similarity(self, events: List[Dict[Any, Any]]) -> List[float]:
        """Calculate pairwise similarities between all events in a group."""
        if len(events) < 2:
            return []
            
        embeddings = [event.get("embedding", [0.0] * 1536) for event in events]
        similarities = []
        
        for i in range(len(embeddings)):
            for j in range(i + 1, len(embeddings)):
                similarity = self.calculate_cosine_similarity(embeddings[i], embeddings[j])
                similarities.append(similarity)
                
        return similarities
        
    async def batch_process_embeddings(self, events: List[Dict[Any, Any]]) -> List[Dict[Any, Any]]:
        """Process embeddings for a batch of events."""
        texts = [str(event.get('content', '')) for event in events]
        embeddings = await self.get_embeddings(texts)
        
        for event, embedding in zip(events, embeddings):
            event['embedding'] = embedding
            
        return events