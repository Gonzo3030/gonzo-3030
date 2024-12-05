import pytest
from datetime import datetime
from typing import Dict, Any, List
from pydantic import BaseModel
from src.core.graph_state import GonzoState

@pytest.fixture
def base_state():
    return GonzoState()

def test_state_initialization(base_state):
    """Test that state initializes with correct default values."""
    assert base_state.current_batch is None
    assert isinstance(base_state.memory, dict)
    assert isinstance(base_state.checkpoints, dict)
    assert isinstance(base_state.last_processed, datetime)

@pytest.mark.asyncio
async def test_batch_update(base_state):
    """Test batch updating functionality."""
    test_batch = {
        'id': 'test_batch_1',
        'events': [{'id': 1, 'data': 'test'}]
    }
    
    base_state.update_batch(test_batch)
    assert base_state.current_batch == test_batch
    assert (datetime.now() - base_state.last_processed).total_seconds() < 1

def test_memory_operations(base_state):
    """Test memory storage operations."""
    test_data = {'key': 'value'}
    base_state.save_to_memory('test_key', test_data)
    
    assert 'test_key' in base_state.memory
    assert base_state.memory['test_key']['value'] == test_data
    assert 'timestamp' in base_state.memory['test_key']

def test_checkpoint_creation(base_state):
    """Test checkpoint creation and management."""
    checkpoint_data = {
        'batch_id': 'test_batch',
        'status': 'pending'
    }
    
    base_state.create_checkpoint('cp_1', checkpoint_data)
    assert 'cp_1' in base_state.checkpoints
    assert base_state.checkpoints['cp_1']['status'] == 'created'
    assert 'timestamp' in base_state.checkpoints['cp_1']

def test_checkpoint_updates(base_state):
    """Test checkpoint status updates."""
    # Create initial checkpoint
    checkpoint_data = {'batch_id': 'test_batch'}
    base_state.create_checkpoint('cp_1', checkpoint_data)
    
    # Update checkpoint
    result_data = {'result': 'success'}
    base_state.update_checkpoint('cp_1', 'completed', result_data)
    
    assert base_state.checkpoints['cp_1']['status'] == 'completed'
    assert base_state.checkpoints['cp_1']['result'] == result_data

def test_pending_checkpoints(base_state):
    """Test retrieving pending checkpoints."""
    # Create multiple checkpoints with different statuses
    base_state.create_checkpoint('cp_1', {'data': 'test1'})
    base_state.create_checkpoint('cp_2', {'data': 'test2'})
    base_state.update_checkpoint('cp_2', 'completed')
    
    pending = base_state.get_pending_checkpoints()
    assert len(pending) == 1
    assert 'cp_1' in pending

def test_checkpoint_cleanup(base_state):
    """Test cleanup of old checkpoints."""
    # Create an old checkpoint by manipulating the timestamp
    old_time = datetime.now().isoformat()
    base_state.checkpoints['old_cp'] = {
        'data': 'test',
        'status': 'completed',
        'timestamp': old_time
    }
    
    # Clean checkpoints with very short max age
    base_state.clean_old_checkpoints(max_age_hours=0)
    assert 'old_cp' not in base_state.checkpoints

def test_state_validation():
    """Test that state validation works correctly."""
    # Test with invalid batch data
    with pytest.raises(ValueError):
        GonzoState(current_batch="invalid")
        
    # Test with valid data
    valid_state = GonzoState(
        current_batch={'id': 'valid_batch'},
        memory={'key': {'value': 'test', 'timestamp': datetime.now().isoformat()}}
    )
    assert valid_state.current_batch['id'] == 'valid_batch'