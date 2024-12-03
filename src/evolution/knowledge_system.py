from typing import Dict, List, Optional, Set
from datetime import datetime
import asyncio
from langchain_anthropic import ChatAnthropic
from langchain.memory import ConversationBufferMemory

class KnowledgeSystem:
    def __init__(self):
        # Use simple memory storage initially
        self.memory_store = {}
        
        # Different types of memory
        self.short_term = ConversationBufferMemory(k=100)  # Recent interactions
        self.pattern_memory = {}
        self.relationship_memory = {}
        
        # Track evolving narratives and predictions
        self.observed_patterns = {
            "corporate_tactics": set(),
            "manipulation_methods": set(),
            "resistance_strategies": set(),
            "successful_predictions": set()
        }
        
        # Knowledge confidence levels
        self.confidence_scores = {
            "predictions": {},
            "warnings": {},
            "analyses": {}
        }
    
    async def learn_from_interaction(self, 
                                   interaction: Dict,
                                   engagement_metrics: Dict) -> None:
        """Learn from each interaction and its outcomes."""
        # Store interaction with timestamp
        timestamp = datetime.now().isoformat()
        self.memory_store[timestamp] = {
            "interaction": interaction,
            "metrics": engagement_metrics
        }
        
        # Update pattern recognition
        await self._update_patterns(interaction)
        
        # Adjust confidence based on engagement
        await self._adjust_confidence(interaction, engagement_metrics)
        
        # Prune outdated information
        await self._prune_outdated_knowledge()

    async def get_relevant_knowledge(self, 
                                   context: Dict,
                                   min_confidence: float = 0.3) -> Dict:
        """Retrieve relevant knowledge based on simple matching."""
        relevant_knowledge = {}
        context_type = context.get("type", "")
        context_content = str(context.get("content", "")).lower()
        
        # Simple keyword matching for now
        for timestamp, data in self.memory_store.items():
            interaction = data["interaction"]
            # Match by type and content keywords
            if (context_type in interaction.get("type", "") or
                any(word in str(interaction).lower() for word in context_content.split())):
                relevant_knowledge[timestamp] = interaction
        
        return relevant_knowledge

    async def _update_patterns(self, interaction: Dict) -> None:
        """Update recognized patterns based on new information."""
        if "corporate_action" in interaction:
            self.observed_patterns["corporate_tactics"].add(
                interaction["corporate_action"]
            )
        
        if "manipulation" in interaction:
            self.observed_patterns["manipulation_methods"].add(
                interaction["manipulation"]
            )
            
        if "prediction_outcome" in interaction:
            if interaction["prediction_outcome"]["accurate"]:
                self.observed_patterns["successful_predictions"].add(
                    interaction["prediction_outcome"]["prediction"]
                )

    async def _adjust_confidence(self, 
                               interaction: Dict,
                               engagement_metrics: Dict) -> None:
        """Adjust confidence based on feedback."""
        engagement_score = engagement_metrics.get("engagement_score", 0)
        prediction_id = interaction.get("prediction_id")
        
        if prediction_id:
            current_confidence = self.confidence_scores["predictions"].get(
                prediction_id, 0.5
            )
            new_confidence = self._calculate_new_confidence(
                current_confidence,
                engagement_score,
                interaction.get("was_accurate", None)
            )
            self.confidence_scores["predictions"][prediction_id] = new_confidence

    def _calculate_new_confidence(self,
                                current: float,
                                engagement: float,
                                accuracy: Optional[bool]) -> float:
        """Calculate new confidence score."""
        adjustment = 0.0
        adjustment += min(0.1, engagement / 100)
        if accuracy is not None:
            adjustment += 0.2 if accuracy else -0.2
        return max(0.0, min(1.0, current + adjustment))

    async def _prune_outdated_knowledge(self) -> None:
        """Remove outdated information."""
        current_time = datetime.now()
        
        # Remove old memories (older than 30 days)
        self.memory_store = {
            timestamp: data
            for timestamp, data in self.memory_store.items()
            if (current_time - datetime.fromisoformat(timestamp)).days <= 30
        }
        
        # Clear short-term memory
        self.short_term.clear()