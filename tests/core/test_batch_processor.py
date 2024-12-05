import pytest
import asyncio
from datetime import datetime
from unittest.mock import Mock, patch
from src.core.batch_processor import BatchProcessor, EventBatch
from src.core.embeddings import EmbeddingProcessor

@pytest.fixture
def batch_processor():
    return BatchProcessor(
        batch_size=3,
        similarity_threshold=0.8,
        max_batch_wait=30
    )

@pytest.fixture
def mock_embedding_processor():
    with patch('src.core.batch_processor.EmbeddingProcessor') as mock:
        processor = Mock()
        processor.get_embeddings.return_value = [[0.1, 0.2], [0.15, 0.25]]
        processor.calculate_cosine_similarity.return_value = 0.9
        mock.return_value = processor
        yield mock

@pytest.mark.asyncio
async def test_add_event(batch_processor):
    """Test adding a single event to the batch processor."""
    event = {
        'id': '1',
        'content': 'Test event content',
        'timestamp': datetime.now().timestamp()
    }
    
    await batch_processor.add_event(event, 'test_category')
    assert len(batch_processor.pending_events['test_category']) == 1
    assert batch_processor.pending_events['test_category'][0] == event

@pytest.mark.asyncio
async def test_batch_threshold_processing(batch_processor):
    """Test that batches are processed when they reach the size threshold."""
    events = [
        {'id': str(i), 'content': f'Test content {i}'}
        for i in range(3)
    ]
    
    for event in events[:-1]:
        await batch_processor.add_event(event, 'test_category')
        assert len(batch_processor.pending_events['test_category']) > 0
        
    # This should trigger processing
    with patch.object(batch_processor, '_create_checkpoint') as mock_checkpoint:
        await batch_processor.add_event(events[-1], 'test_category')
        assert mock_checkpoint.called

@pytest.mark.asyncio
async def test_batch_creation(batch_processor):
    """Test batch creation and metadata."""
    events = [
        {'id': '1', 'content': 'First test event'},
        {'id': '2', 'content': 'Second test event'}
    ]
    
    for event in events:
        await batch_processor.add_event(event, 'test_category')
        
    batch = await batch_processor.process_batch('test_category')
    assert isinstance(batch, EventBatch)
    assert batch.batch_id.startswith('batch_test_category_')
    assert batch.checkpoint_id is not None

@pytest.mark.asyncio
async def test_empty_category_handling(batch_processor):
    """Test handling of empty event categories."""
    result = await batch_processor.process_batch('nonexistent_category')
    assert result is None

@pytest.mark.asyncio
async def test_similarity_grouping(batch_processor, mock_embedding_processor):
    """Test event grouping based on similarity."""
    events = [
        {'id': '1', 'content': 'AI technology news'},
        {'id': '2', 'content': 'Latest AI developments'}
    ]
    
    grouped_events = await batch_processor._group_similar_events(events)
    assert len(grouped_events) > 0
    # Events should be grouped together due to similarity
    assert any(len(group) == 2 for group in grouped_events)

@pytest.mark.asyncio
async def test_batch_monitoring(batch_processor):
    """Test monitoring of pending batches."""
    old_event = {
        'id': '1',
        'content': 'Old event',
        'timestamp': asyncio.get_event_loop().time() - 100
    }
    
    await batch_processor.add_event(old_event, 'test_category')
    
    # Run monitoring for one cycle
    with patch.object(batch_processor, 'process_batch') as mock_process:
        await batch_processor.monitor_pending_batches()
        assert mock_process.called

@pytest.mark.asyncio
async def test_checkpoint_integration(batch_processor):
    """Test integration with checkpoint system."""
    events = [{'id': '1', 'content': 'Test event'}]
    
    with patch.object(batch_processor, '_save_checkpoint') as mock_save:
        checkpoint_id = await batch_processor._create_checkpoint(events)
        
        assert checkpoint_id is not None
        assert mock_save.called
        
        checkpoint_data = mock_save.call_args[0][1]
        assert 'events' in checkpoint_data
        assert 'timestamp' in checkpoint_data
        assert checkpoint_data['status'] == 'pending'

@pytest.mark.asyncio
async def test_batch_similarity_calculation(batch_processor, mock_embedding_processor):
    """Test similarity calculation for batched events."""
    events = [
        {'content': 'First AI news', 'embedding': [0.1, 0.2]},
        {'content': 'Second AI news', 'embedding': [0.15, 0.25]}
    ]
    
    similarity = await batch_processor._calculate_batch_similarity([events])
    assert 0 <= similarity <= 1  # Similarity should be normalized