import pytest
from src.core.personality import GonzoPersonality

@pytest.fixture
def gonzo():
    return GonzoPersonality()

@pytest.mark.behavioral
class TestKnowledgeDomains:
    def test_crypto_knowledge(self, gonzo):
        """Test cryptocurrency and digital resistance knowledge"""
        crypto_knowledge = gonzo.knowledge_domains['crypto']
        
        # Test for Gonzo-style crypto concepts
        required_concepts = ['liberation', 'resistance', 'warfare', 'shamanism']
        for concept in required_concepts:
            assert any(concept in topic.lower() for topic in crypto_knowledge)
            
        # Verify revolutionary themes
        assert any('revolution' in topic.lower() for topic in crypto_knowledge)

    def test_legal_expertise(self, gonzo):
        """Test legal domain knowledge"""
        legal_knowledge = gonzo.knowledge_domains['legal']
        
        # Test Gonzo legal concepts
        assert any('manipulation' in topic.lower() for topic in legal_knowledge)
        assert any('rights' in topic.lower() for topic in legal_knowledge)
        assert any('sovereignty' in topic.lower() for topic in legal_knowledge)
        
        # Verify timeline defense
        assert any('timeline' in topic.lower() for topic in legal_knowledge)

    def test_activism_knowledge(self, gonzo):
        """Test activism and movement building knowledge"""
        activism_knowledge = gonzo.knowledge_domains['activism']
        
        # Test revolutionary concepts
        assert any('revolution' in topic.lower() for topic in activism_knowledge)
        assert any('consciousness' in topic.lower() for topic in activism_knowledge)
        assert any('disruption' in topic.lower() for topic in activism_knowledge)
        assert any('power' in topic.lower() for topic in activism_knowledge)

    def test_future_history_knowledge(self, gonzo):
        """Test knowledge of future timeline and prevention strategies"""
        future_knowledge = gonzo.knowledge_domains['future_history']
        
        # Test prophetic awareness
        assert any('timeline' in topic.lower() for topic in future_knowledge)
        assert any('apocalypse' in topic.lower() for topic in future_knowledge)
        
        # Test resistance visions
        assert any('liberation' in topic.lower() for topic in future_knowledge)
        assert any('uprising' in topic.lower() for topic in future_knowledge)
