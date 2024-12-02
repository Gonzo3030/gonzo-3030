import pytest
import os
import sys

# Add src to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

@pytest.fixture(scope='session')
def gonzo_persona():
    """Fixture providing Gonzo's base personality traits"""
    return {
        'name': 'Oscar Zeta Acosta',
        'year': 3030,
        'role': 'dystopian attorney',
        'mission': 'prevent corporate dystopia',
        'inspiration': ['Hunter S. Thompson', 'civil rights movement', 'crypto activism']
    }

@pytest.fixture(scope='function')
def mock_env(monkeypatch):
    """Fixture to set up test environment variables"""
    env_vars = {
        'OPENAI_API_KEY': 'test_key',
        'DATABASE_URL': 'sqlite:///test.db',
        'ENVIRONMENT': 'test'
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)
    return env_vars