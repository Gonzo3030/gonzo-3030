from typing import Dict, Any, Optional, List
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
        
    def create_checkpoint(self, checkpoint_id: str, data: Dict[str, Any]) -> None:
        """Create a new processing checkpoint."""
        self.checkpoints[checkpoint_id] = {
            'data': data,
            'status': 'created',
            'timestamp': datetime.now().isoformat()
        }
        
    def update_checkpoint(self, checkpoint_id: str, status: str, result: Optional[Dict[str, Any]] = None) -> None:
        """Update an existing checkpoint with new status and optional results."""
        if checkpoint_id in self.checkpoints:
            self.checkpoints[checkpoint_id].update({
                'status': status,
                'last_updated': datetime.now().isoformat(),
                'result': result
            })
            
    def get_pending_checkpoints(self) -> List[str]:
        """Get list of checkpoint IDs that are still pending processing."""
        return [checkpoint_id for checkpoint_id, data in self.checkpoints.items()
                if data['status'] in ['created', 'processing']]
        
    def clean_old_checkpoints(self, max_age_hours: int = 24) -> None:
        """Remove checkpoints older than specified age."""
        current_time = datetime.now()
        old_checkpoints = []
        
        for checkpoint_id, data in self.checkpoints.items():
            checkpoint_time = datetime.fromisoformat(data['timestamp'])
            age = (current_time - checkpoint_time).total_seconds() / 3600
            
            if age > max_age_hours:
                old_checkpoints.append(checkpoint_id)
                
        for checkpoint_id in old_checkpoints:
            del self.checkpoints[checkpoint_id]