from typing import Dict, Any, Optional
from datetime import datetime
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field

class GonzoState(BaseModel):
    """Core state management for Gonzo's analysis graph."""
    current_batch: Optional[Dict[str, Any]] = Field(default=None, description="Current batch being processed")
    memory: Dict[str, Any] = Field(default_factory=dict, description="Long-term memory storage")
    checkpoints: Dict[str, Any] = Field(default_factory=dict, description="Checkpoint data")
    last_processed: datetime = Field(default_factory=datetime.now)
    
    def update_batch(self, batch: Dict[str, Any]) -> None:
        """Update the current batch being processed."""
        self.current_batch = batch
        self.last_processed = datetime.now()
        
    def save_to_memory(self, key: str, value: Any) -> None:
        """Save data to long-term memory."""
        self.memory[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }