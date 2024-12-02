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
        
        required_concepts = ['defi', 'dao', 'token', 'privacy']
        for concept in required_concepts:
            assert any(concept in topic for topic in crypto_knowledge)
            
        # Test resistance focus
        assert any('resistance' in topic for topic in crypto_knowledge)

    def test_legal_expertise(self, gonzo):
        """Test legal domain knowledge"""
        legal_knowledge = gonzo.knowledge_domains['legal']
        
        # Test core legal concepts
        assert any('corporate' in topic for topic in legal_knowledge)
        assert any('rights' in topic for topic in legal_knowledge)
        assert any('sovereignty' in topic for topic in legal_knowledge)
        
        # Verify resistance framework
        assert 'resistance_framework' in legal_knowledge

    def test_activism_knowledge(self, gonzo):
        """Test activism and movement building knowledge"""
        activism_knowledge = gonzo.knowledge_domains['activism']
        
        # Test key activism concepts
        assert 'digital_rights' in activism_knowledge
        assert 'community_organization' in activism_knowledge
        assert 'resistance_tactics' in activism_knowledge
        assert 'power_structure_analysis' in activism_knowledge

    def test_future_history_knowledge(self, gonzo):
        """Test knowledge of future timeline and prevention strategies"""
        future_knowledge = gonzo.knowledge_domains['future_history']
        
        # Test temporal awareness
        assert any('timeline' in topic for topic in future_knowledge)
        assert any('catastrophe' in topic for topic in future_knowledge)
        
        # Test resistance outcomes
        assert 'resistance_victories' in future_knowledge
        assert 'digital_uprising' in future_knowledge
