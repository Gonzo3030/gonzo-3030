from typing import List, Dict, Any
from dataclasses import dataclass
from collections import defaultdict
import asyncio
from langchain.schema import BaseMessage
from langchain.chat_models import ChatOpenAI

@dataclass
class EventBatch:
    events: List[Dict[Any, Any]]
    batch_id: str
    checkpoint_id: str
    similarity_score: float

class BatchProcessor:
    def __init__(self, 
                 batch_size: int = 5,
                 similarity_threshold: float = 0.8,
                 max_batch_wait: int = 60):
        self.batch_size = batch_size
        self.similarity_threshold = similarity_threshold
        self.max_batch_wait = max_batch_wait  # Maximum seconds to wait before processing a partial batch
        self.pending_events = defaultdict(list)
        self.llm = ChatOpenAI(temperature=0)
        
    async def add_event(self, event: Dict[Any, Any], category: str) -> None:
        """Add an event to the pending batch for a given category."""
        self.pending_events[category].append(event)
        
        if len(self.pending_events[category]) >= self.batch_size:
            await self.process_batch(category)
            
    async def process_batch(self, category: str) -> EventBatch:
        """Process a batch of events in the same category."""
        if not self.pending_events[category]:
            return None
            
        events = self.pending_events[category]
        self.pending_events[category] = []
        
        # Group similar events based on semantic similarity
        grouped_events = await self._group_similar_events(events)
        
        # Create checkpoint for the batch
        checkpoint_id = await self._create_checkpoint(grouped_events)
        
        batch = EventBatch(
            events=grouped_events,
            batch_id=f"batch_{category}_{checkpoint_id}",
            checkpoint_id=checkpoint_id,
            similarity_score=await self._calculate_batch_similarity(grouped_events)
        )
        
        return batch
        
    async def _group_similar_events(self, events: List[Dict[Any, Any]]) -> List[Dict[Any, Any]]:
        """Group events based on semantic similarity to optimize LLM calls."""
        if not events:
            return []
            
        # Calculate embeddings for each event description
        embeddings = await self._get_embeddings([str(event) for event in events])
        
        # Group events with similar embeddings
        groups = defaultdict(list)
        for i, event in enumerate(events):
            group_key = self._find_nearest_group(embeddings[i], groups)
            groups[group_key].append(event)
            
        return list(groups.values())
        
    async def _create_checkpoint(self, grouped_events: List[Dict[Any, Any]]) -> str:
        """Create a checkpoint for the batch processing state."""
        # Generate a unique checkpoint ID
        checkpoint_id = f"batch_{len(grouped_events)}_{hash(str(grouped_events))}"
        
        # Store batch state and metadata
        checkpoint_data = {
            "events": grouped_events,
            "timestamp": asyncio.get_event_loop().time(),
            "status": "pending"
        }
        
        # Save checkpoint (implement actual storage logic based on your checkpointing system)
        await self._save_checkpoint(checkpoint_id, checkpoint_data)
        
        return checkpoint_id
        
    async def _calculate_batch_similarity(self, grouped_events: List[Dict[Any, Any]]) -> float:
        """Calculate the overall similarity score for events in the batch."""
        if not grouped_events:
            return 0.0
            
        # Calculate average similarity between all events in each group
        similarities = []
        for group in grouped_events:
            if len(group) > 1:
                group_similarities = await self._calculate_group_similarity(group)
                similarities.extend(group_similarities)
                
        return sum(similarities) / len(similarities) if similarities else 0.0
        
    async def monitor_pending_batches(self):
        """Monitor pending batches and process them if they exceed max wait time."""
        while True:
            current_time = asyncio.get_event_loop().time()
            
            for category, events in self.pending_events.items():
                if events and (current_time - events[0].get("timestamp", 0)) > self.max_batch_wait:
                    await self.process_batch(category)
                    
            await asyncio.sleep(5)  # Check every 5 seconds

    async def _save_checkpoint(self, checkpoint_id: str, checkpoint_data: Dict[str, Any]):
        """Save checkpoint data to persistent storage."""
        # Implement actual checkpoint storage logic
        pass

    def _find_nearest_group(self, embedding: List[float], groups: Dict[int, List[Dict[Any, Any]]]) -> int:
        """Find the nearest group for an event based on embedding similarity."""
        if not groups:
            return len(groups)
            
        max_similarity = -1
        nearest_group = len(groups)
        
        for group_id, group_events in groups.items():
            similarity = self._calculate_cosine_similarity(embedding, group_events[0]["embedding"])
            if similarity > max_similarity and similarity > self.similarity_threshold:
                max_similarity = similarity
                nearest_group = group_id
                
        return nearest_group