from typing import Dict, Any, Optional, List, TypedDict
from datetime import datetime
from pydantic import BaseModel, Field
from langchain.schema import BaseMessage
from langsmith.run_trees import RunTree

class MessageState(TypedDict):
    """State for managing messages in the graph."""
    messages: List[BaseMessage]
    next_step: str

class RunState(TypedDict):
    """State for tracking LangSmith runs."""
    run_id: str
    run_tree: Optional[RunTree]
    parent_run_id: Optional[str]

class GonzoState(BaseModel):
    """Core state management for Gonzo's analysis graph.
    Compatible with LangGraph's StateGraph and LangSmith tracking.
    """
    # Graph Flow Control
    next_step: str = Field(
        default="initialize",
        description="Next step in the graph workflow"
    )
    
    # Batch Processing State
    current_batch: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Current batch being processed"
    )
    pending_batches: Dict[str, List[Dict[str, Any]]] = Field(
        default_factory=dict,
        description="Batches waiting to be processed"
    )
    
    # Memory and Persistence
    memory: Dict[str, Any] = Field(
        default_factory=dict,
        description="Long-term memory storage"
    )
    checkpoints: Dict[str, Any] = Field(
        default_factory=dict,
        description="Checkpoint data"
    )
    
    # LangSmith Integration
    run_state: RunState = Field(
        default_factory=lambda: RunState(
            run_id="",
            run_tree=None,
            parent_run_id=None
        ),
        description="LangSmith run tracking state"
    )
    
    # Message Management
    message_state: MessageState = Field(
        default_factory=lambda: MessageState(
            messages=[],
            next_step="initialize"
        ),
        description="Message handling state"
    )
    
    def start_run(self, name: str, run_type: str = "chain") -> None:
        """Start a new LangSmith run for tracking."""
        if self.run_state["run_tree"] is not None:
            self.run_state["parent_run_id"] = self.run_state["run_id"]
        
        # Create new run tree if needed
        self.run_state["run_tree"] = RunTree(
            name=name,
            run_type=run_type,
            inputs={},
            outputs={}
        )
        self.run_state["run_id"] = self.run_state["run_tree"].id
    
    def end_run(self, outputs: Dict[str, Any]) -> None:
        """End the current LangSmith run with outputs."""
        if self.run_state["run_tree"] is not None:
            self.run_state["run_tree"].end(outputs=outputs)
            
            if self.run_state["parent_run_id"]:
                self.run_state["run_id"] = self.run_state["parent_run_id"]
                self.run_state["parent_run_id"] = None
    
    def log_step(self, step_name: str, inputs: Dict[str, Any], outputs: Dict[str, Any]) -> None:
        """Log a step within the current run."""
        if self.run_state["run_tree"] is not None:
            self.run_state["run_tree"].add_child(
                name=step_name,
                run_type="chain",
                inputs=inputs,
                outputs=outputs
            )
    
    def transition_to(self, next_step: str) -> None:
        """Transition the graph to a new state."""
        self.next_step = next_step
        self.message_state["next_step"] = next_step
        
        # Log the transition in LangSmith
        self.log_step(
            "state_transition",
            {"from": self.next_step},
            {"to": next_step}
        )
    
    def add_message(self, message: BaseMessage) -> None:
        """Add a message to the state."""
        self.message_state["messages"].append(message)
    
    def get_messages(self) -> List[BaseMessage]:
        """Get all messages in the current state."""
        return self.message_state["messages"]
    
    def update_batch(self, batch: Dict[str, Any]) -> None:
        """Update the current batch being processed."""
        self.current_batch = batch
        self.log_step(
            "batch_update",
            {"previous_batch": self.current_batch},
            {"new_batch": batch}
        )
    
    def save_to_memory(self, key: str, value: Any) -> None:
        """Save data to long-term memory."""
        self.memory[key] = {
            'value': value,
            'timestamp': datetime.now().isoformat()
        }
        self.log_step(
            "memory_save",
            {"key": key},
            {"value": value}
        )
    
    class Config:
        arbitrary_types_allowed = True
