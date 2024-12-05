import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, patch
from src.core.batch_processor import BatchProcessor, EventBatch

@pytest.fixture
def batch_processor():
    return BatchProcessor(
        batch_size=3,
        similarity_threshold=0.8,
        max_batch_wait=30
    )

@pytest.mark.asyncio
async def test_add_event(batch_processor):
    event = {
        "id": "1",
        "type": "news",
        "content": "Test event content",
        "timestamp": datetime.now().timestamp()
    }
    
    await batch_processor.add_event(event, "news")
    assert len(batch_processor.pending_events["news"]) == 1
    assert batch_processor.pending_events["news"][0] == event

@pytest.mark.asyncio
async def test_batch_processing_threshold(batch_processor):
    # Add events until we hit the batch threshold
    events = [
        {"id": str(i), "type": "news", "content": f"Test event {i}"}
        for i in range(3)
    ]
    
    for event in events:
        await batch_processor.add_event(event, "news")
        
    # Verify batch was processed
    assert len(batch_processor.pending_events["news"]) == 0

@pytest.mark.asyncio
async def test_similarity_grouping(batch_processor):
    similar_events = [
        {"content": "Breaking news about technology"},
        {"content": "More tech news updates"},
        {"content": "Latest technology developments"}
    ]
    
    # Mock the embedding function
    with patch.object(batch_processor, '_get_embeddings') as mock_embeddings:
        mock_embeddings.return_value = [
            [0.1, 0.2, 0.3],
            [0.15, 0.25, 0.35],
            [0.12, 0.22, 0.32]
        ]
        
        grouped = await batch_processor._group_similar_events(similar_events)
        assert len(grouped) > 0
        # All events should be in the same group due to similarity
        assert len(grouped[0]) == 3

@pytest.mark.asyncio
async def test_checkpoint_creation(batch_processor):
    events = [{"id": "1", "content": "Test event"}]
    
    with patch.object(batch_processor, '_save_checkpoint') as mock_save:
        checkpoint_id = await batch_processor._create_checkpoint(events)
        
        assert checkpoint_id is not None
        assert mock_save.called
        
        # Verify checkpoint data structure
        checkpoint_data = mock_save.call_args[0][1]
        assert "events" in checkpoint_data
        assert "timestamp" in checkpoint_data
        assert "status" in checkpoint_data
        assert checkpoint_data["status"] == "pending"

@pytest.mark.asyncio
async def test_batch_monitoring(batch_processor):
    # Add an event with old timestamp
    old_event = {
        "id": "1",
        "content": "Old event",
        "timestamp": asyncio.get_event_loop().time() - 100  # Way past max_batch_wait
    }
    
    await batch_processor.add_event(old_event, "news")
    
    # Run monitor for one iteration
    with patch.object(batch_processor, 'process_batch') as mock_process:
        await batch_processor.monitor_pending_batches()
        assert mock_process.called

@pytest.mark.asyncio
async def test_batch_similarity_calculation(batch_processor):
    events = [
        {"content": "Tech news 1", "embedding": [0.1, 0.2, 0.3]},
        {"content": "Tech news 2", "embedding": [0.15, 0.25, 0.35]}
    ]
    
    similarity = await batch_processor._calculate_batch_similarity([events])
    assert 0 <= similarity <= 1  # Similarity should be normalized

@pytest.mark.asyncio
async def test_empty_batch_handling(batch_processor):
    result = await batch_processor.process_batch("nonexistent_category")
    assert result is None
    
    empty_similarity = await batch_processor._calculate_batch_similarity([])
    assert empty_similarity == 0.0

@pytest.mark.asyncio
async def test_batch_event_fields(batch_processor):
    event = {
        "id": "1",
        "type": "news",
        "content": "Test content",
        "timestamp": datetime.now().timestamp(),
        "metadata": {"source": "test"}
    }
    
    await batch_processor.add_event(event, "news")
    assert batch_processor.pending_events["news"][0]["id"] == "1"
    assert batch_processor.pending_events["news"][0]["type"] == "news"
    assert "metadata" in batch_processor.pending_events["news"][0]