import pytest
from src.social.content_generator import ContentGenerator, ContentType

@pytest.fixture
def content_generator():
    return ContentGenerator()

@pytest.fixture
def sample_contexts():
    return [
        {
            'current_event': 'New privacy policy allows unrestricted data sharing',
            'pattern': 'corporate data consolidation',
            'event': 'mass privacy violation'
        },
        {
            'current_event': 'Global banks announce unified digital identity system',
            'pattern': 'financial surveillance expansion',
            'event': 'monetary control grid'
        },
        {
            'current_event': 'AI-powered fact-checking system mandatory for all posts',
            'pattern': 'automated truth filtering',
            'event': 'digital thought control'
        }
    ]

@pytest.mark.asyncio
class TestWarningGeneration:
    async def test_warning_structure(self, content_generator, sample_contexts):
        """Test that warnings follow required structural patterns"""
        warning = await content_generator.generate_content(
            ContentType.WARNING,
            sample_contexts[0]
        )
        
        # Verify warning contains key elements
        assert '🚨' in warning or 'ALERT' in warning.upper()
        assert any(marker in warning.upper() for marker in ['WARNING', 'ATTENTION', 'ALERT'])
        assert '\n' in warning  # Proper formatting with line breaks

    async def test_dystopian_event_matching(self, content_generator):
        """Test that current events are matched to appropriate dystopian futures"""
        # Test privacy violation matching
        context = {'current_event': 'Company announces enhanced user data collection'}
        warning = await content_generator.generate_content(ContentType.WARNING, context)
        assert any(phrase in warning.lower() for phrase in ['privacy', 'digital', 'data'])
        
        # Test financial control matching
        context = {'current_event': 'Major bank merger announced'}
        warning = await content_generator.generate_content(ContentType.WARNING, context)
        assert any(phrase in warning.lower() for phrase in ['bank', 'surveillance', 'financial'])

    async def test_warning_personalization(self, content_generator, sample_contexts):
        """Test that warnings incorporate provided context"""
        context = sample_contexts[0]
        warning = await content_generator.generate_content(ContentType.WARNING, context)
        
        # Verify context integration
        assert context['current_event'] in warning
        assert context['pattern'] in warning or context['event'] in warning

    async def test_gonzo_style_elements(self, content_generator):
        """Test that warnings maintain Gonzo's voice"""
        context = {'current_event': 'Corporate merger announcement'}
        warning = await content_generator.generate_content(ContentType.WARNING, context)
        
        # Check for Gonzo style markers
        gonzo_markers = [
            '3030',
            'TEMPORAL',
            'ATTENTION',
            'RESISTANCE',
            'timeline',
            'synthetic gods'
        ]
        assert any(marker.lower() in warning.lower() for marker in gonzo_markers)

    async def test_temporal_elements(self, content_generator):
        """Test that warnings properly reference timeline elements"""
        warning = await content_generator.generate_content(
            ContentType.WARNING,
            {'current_event': 'Social credit score system proposed'}
        )
        
        # Verify temporal references
        temporal_markers = ['timeline', 'future', '3030', 'began', 'led to']
        assert any(marker in warning.lower() for marker in temporal_markers)

    async def test_character_limit(self, content_generator, sample_contexts):
        """Test that warnings respect Twitter's character limit"""
        for context in sample_contexts:
            warning = await content_generator.generate_content(
                ContentType.WARNING,
                context
            )
            assert len(warning) <= 280  # Twitter's character limit

    async def test_multiple_warning_uniqueness(self, content_generator):
        """Test that multiple warnings about same event aren't identical"""
        context = {'current_event': 'Digital ID system announced'}
        warnings = [
            await content_generator.generate_content(ContentType.WARNING, context)
            for _ in range(3)
        ]
        
        # Verify warnings aren't identical
        assert len(set(warnings)) > 1  # At least 2 unique warnings