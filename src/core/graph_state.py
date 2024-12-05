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
    
    class Config:
        arbitrary_types_allowed = True
