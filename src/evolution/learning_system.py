from typing import Dict, List, Optional, Union
from datetime import datetime
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import Chroma

class LearningSystem:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings()
        self.memory = Chroma(embedding_function=self.embeddings)
        
        # Track various aspects of learning
        self.learning_metrics = {
            "successful_predictions": [],
            "failed_predictions": [],
            "engagement_patterns": {},
            "community_feedback": []
        }
        
        # Adaptation tracking
        self.adaptation_metrics = {
            "language_evolution": {
                "successful_phrases": {},
                "engagement_rates": {},
                "community_resonance": {}
            },
            "prediction_accuracy": {
                "short_term": [],
                "long_term": [],
                "pattern_matching": {}
            },
            "narrative_effectiveness": {
                "warnings": {},
                "predictions": {},
                "analyses": {}
            }
        }
    
    async def learn_from_interaction(self, interaction: Dict) -> None:
        """Process and learn from each interaction."""
        # Store interaction in vector store
        self.memory.add_texts(
            texts=[str(interaction["content"])],
            metadatas=[{
                "timestamp": datetime.now().isoformat(),
                "type": interaction["type"],
                "engagement": interaction.get("engagement_metrics", {})
            }]
        )
        
        # Update learning metrics
        await self._update_metrics(interaction)
        
        # Adapt behavior based on learning
        await self._adapt_behavior(interaction)
    
    async def _update_metrics(self, interaction: Dict) -> None:
        """Update learning metrics based on interaction."""
        # Track prediction accuracy
        if "prediction" in interaction:
            if interaction.get("was_accurate", False):
                self.learning_metrics["successful_predictions"].append({
                    "prediction": interaction["prediction"],
                    "timestamp": datetime.now().isoformat(),
                    "context": interaction.get("context", {})
                })
            else:
                self.learning_metrics["failed_predictions"].append({
                    "prediction": interaction["prediction"],
                    "timestamp": datetime.now().isoformat(),
                    "context": interaction.get("context", {})
                })
        
        # Track engagement patterns
        if "engagement_metrics" in interaction:
            engagement = interaction["engagement_metrics"]
            content_type = interaction.get("type", "general")
            
            if content_type not in self.learning_metrics["engagement_patterns"]:
                self.learning_metrics["engagement_patterns"][content_type] = []
            
            self.learning_metrics["engagement_patterns"][content_type].append({
                "engagement": engagement,
                "timestamp": datetime.now().isoformat()
            })
    
    async def _adapt_behavior(self, interaction: Dict) -> None:
        """Adapt behavior based on learning metrics."""
        # Adapt language based on engagement
        if "content" in interaction:
            await self._adapt_language(interaction)
        
        # Adapt prediction strategy
        if "prediction" in interaction:
            await self._adapt_prediction_strategy(interaction)
        
        # Adapt narrative approach
        if "narrative" in interaction:
            await self._adapt_narrative_strategy(interaction)
    
    async def _adapt_language(self, interaction: Dict) -> None:
        """Adapt language patterns based on engagement."""
        content = interaction["content"]
        engagement = interaction.get("engagement_metrics", {})
        
        # Track successful phrases
        if engagement.get("success", False):
            self.adaptation_metrics["language_evolution"]["successful_phrases"][content] = \
                self.adaptation_metrics["language_evolution"]["successful_phrases"].get(content, 0) + 1
    
    async def get_learned_patterns(self) -> Dict:
        """Retrieve learned patterns and their effectiveness."""
        return {
            "language": self._get_successful_language_patterns(),
            "predictions": self._get_prediction_accuracy(),
            "narratives": self._get_narrative_effectiveness()
        }
    
    def _get_successful_language_patterns(self) -> Dict:
        """Get most successful language patterns."""
        return {
            phrase: count 
            for phrase, count in 
            sorted(
                self.adaptation_metrics["language_evolution"]["successful_phrases"].items(),
                key=lambda x: x[1],
                reverse=True
            )[:10]  # Top 10 successful phrases
        }