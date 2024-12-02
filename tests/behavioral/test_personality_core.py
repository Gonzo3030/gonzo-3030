import pytest
from src.core.personality import GonzoPersonality, TopicCategory, EmotionalTone

@pytest.fixture
def gonzo():
    return GonzoPersonality()

@pytest.mark.behavioral
class TestGonzoCore:
    def test_core_identity(self, gonzo):
        """Test that core identity matches Oscar Zeta Acosta's key characteristics"""
        identity = gonzo.core_identity
        
        # Test basic identity elements
        assert identity['name'] == 'The Brown Buffalo'
        assert 'Digital Resistance Attorney' in identity['role']
        assert 'Chicano activist' in identity['background'].lower()
        
        # Test mission alignment
        assert 'corporate dystopia' in identity['mission'].lower()
        assert 'digital resistance' in identity['mission'].lower()
        
        # Verify historical continuity
        assert 'Mexico' in identity['transformation']

    def test_temporal_consistency(self, gonzo):
        """Test temporal aspects of Gonzo's identity"""
        assert gonzo.origin_year == 3030
        assert gonzo.current_year == 2024
        assert gonzo.original_disappearance == 1974
        assert gonzo.years_of_experience == gonzo.origin_year - gonzo.current_year
