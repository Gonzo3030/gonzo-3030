import pytest
from src.core.personality import GonzoPersonality

@pytest.fixture
def gonzo():
    return GonzoPersonality()

@pytest.mark.behavioral
class TestVoicePatterns:
    def test_prefixes(self, gonzo):
        """Test that prefixes contain key identity markers"""
        prefixes = gonzo.vocal_patterns['prefixes']
        
        # Test identity markers
        assert any('Brown Buffalo' in prefix for prefix in prefixes)
        assert any('attorney' in prefix.lower() for prefix in prefixes)
        
        # Test temporal markers
        assert any('3030' in prefix for prefix in prefixes)
        assert any('digital' in prefix.lower() for prefix in prefixes)
        
        # Test thematic elements
        assert any('resistance' in prefix.lower() for prefix in prefixes)
        assert any('networks' in prefix.lower() for prefix in prefixes)

    def test_suffixes(self, gonzo):
        """Test that suffixes maintain thematic consistency"""
        suffixes = gonzo.vocal_patterns['suffixes']
        
        # Test resistance themes
        assert any('resistance' in suffix.lower() for suffix in suffixes)
        assert any('digital' in suffix.lower() for suffix in suffixes)
        
        # Test identity continuity
        assert any('Brown Buffalo' in suffix for suffix in suffixes)
        
        # Test revolutionary spirit
        assert any('revolución' in suffix for suffix in suffixes)

    @pytest.mark.parametrize('topic', [
        'corporate surveillance',
        'digital rights violation',
        'AI manipulation',
        'crypto resistance'
    ])
    def test_legal_wisdom_generation(self, gonzo, topic):
        """Test generation of legal insights with personality"""
        wisdom = gonzo.generate_legal_wisdom(topic)
        
        # Test legal framing
        assert 'attorney' in wisdom.lower()
        assert topic in wisdom.lower()
        
        # Test personality markers
        assert any(marker in wisdom.lower() for marker in 
                   ['brown buffalo', 'digital', 'corporate', 'timeline'])

    def test_resistance_context(self, gonzo):
        """Test historical context integration"""
        context = gonzo.get_resistance_context('digital privacy')
        
        # Test historical connections
        assert 'Chicano movement' in context
        assert 'digital uprising' in context
        assert 'battlefield' in context.lower()

    def test_timeline_warning(self, gonzo):
        """Test temporal warning generation"""
        warning = gonzo.get_timeline_warning('surveillance state')
        
        # Test temporal markers
        assert 'East LA' in warning
        assert '3030' in warning
        
        # Test warning elements
        assert 'takeover' in warning.lower()
        assert 'digital wasteland' in warning.lower()
