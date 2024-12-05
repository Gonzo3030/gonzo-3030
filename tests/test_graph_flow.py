import pytest
from typing import Dict, Any
from langgraph.graph import StateGraph
from src.core.graph_state import GonzoState
from src.core.batch_processor import BatchProcessor

# Example graph nodes
async def event_processor_node(state: GonzoState) -> Dict[str, Any]:
    """Initial node that processes incoming events."""
    state.start_run("event_processing")
    
    # Add some test events
    test_events = [
        {"id": "1", "content": "AI technology advancement in robotics"},
        {"id": "2", "content": "New developments in robot manufacturing"},
        {"id": "3", "content": "Climate change impact on agriculture"}
    ]
    
    # Process events through batch processor
    batch_processor = BatchProcessor()
    for event in test_events:
        await batch_processor.add_event(event, "news")
    
    # Get processed batch
    batch = await batch_processor.process_batch("news")
    state.update_batch(batch.dict() if batch else {})
    
    state.transition_to("analyze")
    state.end_run({"processed_events": len(test_events)})
    
    return {"next": "analyze"}

async def analysis_node(state: GonzoState) -> Dict[str, Any]:
    """Node that analyzes grouped events."""
    state.start_run("analysis")
    
    if state.current_batch:
        # Group similar events
        grouped_events = state.current_batch.get("events", [])
        # Save analysis results to memory
        state.save_to_memory(
            "analysis_result",
            {"grouped_events": grouped_events}
        )
    
    state.transition_to("output")
    state.end_run({"analyzed_groups": len(state.current_batch.get("events", []))})
    
    return {"next": "output"}

async def output_node(state: GonzoState) -> Dict[str, Any]:
    """Node that formats and outputs results."""
    state.start_run("output_generation")
    
    # Get analysis results from memory
    analysis_results = state.memory.get("analysis_result", {})
    
    # Format output
    output = {
        "total_events": len(analysis_results.get("grouped_events", [])),
        "timestamp": state.memory["analysis_result"]["timestamp"]
    }
    
    state.end_run({"output": output})
    return {"next": None}  # End of workflow

@pytest.mark.asyncio
async def test_graph_flow():
    """Test the complete graph flow."""
    # Initialize state and graph
    state = GonzoState()
    workflow = StateGraph(GonzoState)
    
    # Add nodes
    workflow.add_node("process", event_processor_node)
    workflow.add_node("analyze", analysis_node)
    workflow.add_node("output", output_node)
    
    # Add edges
    workflow.add_edge("process", "analyze")
    workflow.add_edge("analyze", "output")
    
    # Set entry point
    workflow.set_entry_point("process")
    
    # Compile graph
    graph = workflow.compile()
    
    # Run the graph
    final_state = await graph.arun(
        state,
        name="test_flow",
        project="gonzo-langgraph"
    )
    
    # Assertions
    assert final_state.next_step == "output"
    assert "analysis_result" in final_state.memory
    assert len(final_state.memory["analysis_result"]["grouped_events"]) > 0