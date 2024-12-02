import pytest
from pathlib import Path
import sys

# Add src to Python path for importing
src_path = str(Path(__file__).parent.parent / 'src')
sys.path.insert(0, src_path)

@pytest.fixture(scope='session')
def test_data_dir():
    """Fixture providing path to test data directory"""
    return Path(__file__).parent / 'test_data'

@pytest.fixture(scope='session')
def env_setup():
    """Setup test environment variables"""
    import os
    os.environ['GONZO_ENV'] = 'test'
    return os.environ.copy()

@pytest.fixture
def mock_llm_response():
    """Mock LLM responses for testing"""
    return {
        'role': 'assistant',
        'content': 'In the spirit of Hunter S. Thompson, let me tell you about corporate dystopia...'
    }
