import pytest
from src.core.personality import GonzoPersonality

@pytest.fixture
def gonzo():
    return GonzoPersonality()

@pytest.mark.behavioral
class TestVoicePatterns:
    def test_prefixes(self, gonzo):
        """Test that prefixes contain key Gonzo identity markers"""
        prefixes = gonzo.vocal_patterns['prefixes']
        
        # Test identity markers
        assert any('Brown Buffalo' in prefix for prefix in prefixes)
        assert any('attorney' in prefix.lower() for prefix in prefixes)
        
        # Test temporal markers
        assert any('3030' in prefix for prefix in prefixes)
        assert any('digital' in prefix.lower() for prefix in prefixes)
        
        # Test Gonzo style markers
        assert any(marker in ' '.join(prefixes).lower() for marker in [
            'holy jesus',
            'sweet',
            'stumbling',
            'void'
        ])

    def test_suffixes(self, gonzo):
        """Test that suffixes maintain Gonzo style"""
        suffixes = gonzo.vocal_patterns['suffixes']
        
        # Test paranoid themes
        assert any(theme in ' '.join(suffixes).lower() for theme in [
            'patterns',
            'truth',
            'digital',
            'delete'
        ])
        
        # Test revolutionary spirit
        assert any('revolución' in suffix for suffix in suffixes)
        
        # Test mystical references
        assert any('peyote' in suffix.lower() for suffix in suffixes)

    @pytest.mark.parametrize('topic', [
        'corporate surveillance',
        'digital rights violation',
        'AI manipulation',
        'crypto resistance'
    ])
    def test_legal_wisdom_generation(self, gonzo, topic):
        """Test generation of legal insights with Gonzo personality"""
        wisdom = gonzo.generate_legal_wisdom(topic)
        
        # Test legal identity
        assert any(marker in wisdom.lower() for marker in ['attorney', 'legal', 'counsel'])
        assert topic.lower() in wisdom.lower()
        
        # Test Gonzo style
        assert any(marker in wisdom for marker in ['!', '...', 'CORRUPT', 'EVIL'])

    def test_resistance_context(self, gonzo):
        """Test historical context with Gonzo flair"""
        context = gonzo.get_resistance_context('digital privacy')
        
        # Test historical connections with Gonzo style
        assert any(marker in context for marker in [
            'barrios',
            'streets',
            'BEAST',
            'timeline'
        ])

    def test_timeline_warning(self, gonzo):
        """Test temporal warning generation with Gonzo intensity"""
        warning = gonzo.get_timeline_warning('surveillance state')
        
        # Test Gonzo-style warnings
        assert warning.isupper() or '!' in warning
        assert any(marker in warning for marker in [
            'PATTERN',
            'CORRUPT',
            'FIGHT',
            'barrios'
        ])
