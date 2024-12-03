from typing import Dict, List, Optional, Set
from datetime import datetime
import asyncio
from openai import OpenAI
from langchain_chroma import Chroma
from langchain.memory import ConversationBufferMemory

class KnowledgeSystem:
    def __init__(self):
        # Initialize OpenAI client directly
        self.client = OpenAI()
        
        # Vector store for semantic search and pattern matching
        self.vector_store = Chroma(
            embedding_function=self.client.embeddings,
            collection_name="gonzo_knowledge"
        )
        
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
        # Store interaction in vector database for pattern matching
        text = str(interaction)
        response = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        embedding = response.data[0].embedding
        
        self.vector_store.add_texts(
            texts=[text],
            metadatas=[{"timestamp": datetime.now().isoformat()}],
            embeddings=[embedding]
        )
        
        # Update pattern recognition
        await self._update_patterns(interaction)
        
        # Adjust confidence based on engagement
        await self._adjust_confidence(interaction, engagement_metrics)
        
        # Prune outdated information
        await self._prune_outdated_knowledge()

    async def get_relevant_knowledge(self, 
                                   context: Dict,
                                   min_confidence: float = 0.3) -> Dict:
        """Retrieve relevant knowledge above confidence threshold."""
        # Get embedding for query
        text = str(context)
        response = self.client.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        query_embedding = response.data[0].embedding
        
        # Search vector store with embedding
        docs_and_scores = self.vector_store.similarity_search_by_vector(
            embedding=query_embedding,
            k=5  # Get top 5 relevant pieces of information
        )
        
        # Filter by confidence
        confident_knowledge = {}
        for doc in docs_and_scores:
            doc_id = doc.metadata.get("id")
            if doc_id in self.confidence_scores["predictions"]:
                if self.confidence_scores["predictions"][doc_id] >= min_confidence:
                    confident_knowledge[doc_id] = doc.page_content
        
        return confident_knowledge

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
        
        # Prune old short-term memories
        self.short_term.clear()