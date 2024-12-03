from typing import Dict, List, Optional, Any
import asyncio
from datetime import datetime
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma

class LearningSystem:
    def __init__(self):
        # Initialize embeddings and vector store
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = Chroma(
            embedding_function=self.embeddings,
            collection_name="gonzo_learnings"
        )
        
        # Track learning progress
        self.learning_metrics = {
            "total_interactions": 0,
            "successful_predictions": 0,
            "pattern_confirmations": 0,
            "knowledge_updates": 0
        }
        
        # Evolution tracking
        self.evolution_history = []
        self.current_evolution_stage = 0
    
    async def learn_from_interaction(self, interaction_data: Dict) -> None:
        """Process and learn from new interactions."""
        # Store interaction for future learning
        self.vector_store.add_texts(
            texts=[str(interaction_data)],
            metadatas=[{
                "timestamp": datetime.now().isoformat(),
                "type": interaction_data.get("type", "unknown")
            }]
        )
        
        # Update metrics
        self.learning_metrics["total_interactions"] += 1
        
        if interaction_data.get("prediction_success"):
            self.learning_metrics["successful_predictions"] += 1
        
        if interaction_data.get("pattern_confirmed"):
            self.learning_metrics["pattern_confirmations"] += 1
        
        # Check for evolution triggers
        await self._check_evolution_triggers()
    
    async def _check_evolution_triggers(self) -> None:
        """Check if conditions are met for system evolution."""
        total_interactions = self.learning_metrics["total_interactions"]
        success_rate = self.learning_metrics["successful_predictions"] / max(total_interactions, 1)
        pattern_confirmation_rate = self.learning_metrics["pattern_confirmations"] / max(total_interactions, 1)
        
        # Evolution conditions
        if total_interactions > 100 and success_rate > 0.7 and pattern_confirmation_rate > 0.6:
            await self._evolve_system()
    
    async def _evolve_system(self) -> None:
        """Evolve the system based on learned patterns."""
        # Record evolution event
        self.evolution_history.append({
            "stage": self.current_evolution_stage + 1,
            "timestamp": datetime.now().isoformat(),
            "metrics": self.learning_metrics.copy()
        })
        
        # Increment evolution stage
        self.current_evolution_stage += 1
        
        # Reset metrics for next evolution cycle
        self.learning_metrics = {
            "total_interactions": 0,
            "successful_predictions": 0,
            "pattern_confirmations": 0,
            "knowledge_updates": 0
        }