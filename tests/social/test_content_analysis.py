import pytest
from src.social.content_generator import ContentGenerator, ContentType

@pytest.fixture
def content_generator():
    return ContentGenerator()

@pytest.fixture
def sample_analysis_contexts():
    return [
        {
            'subject': 'Corporate AI Deployment',
            'current': 'Major tech firms rolling out autonomous decision systems',
            'warnings': 'Lack of human oversight, opacity in decision making',
            'impact': 'Creation of unaccountable algorithmic power structures',
            'solution': 'Mandatory human-in-the-loop protocols and public audits',
            'analysis': 'The machines aren\'t the threat - it\'s the corporate bastards controlling them.',
        },
        {
            'subject': 'Digital Identity Systems',
            'current': 'Global finance platform launches unified ID verification',
            'warnings': 'Centralized control, privacy erosion, social scoring risk',
            'impact': 'Total surveillance of financial behavior and social control',
            'solution': 'Decentralized identity systems and privacy-preserving protocols',
            'analysis': 'They\'re building the infrastructure of oppression one "convenience" at a time.',
        },
    ]

@pytest.mark.asyncio
class TestAnalysisGeneration:
    async def test_analysis_structure(self, content_generator, sample_analysis_contexts):
        """Test that analysis follows required structural patterns"""
        analysis = await content_generator.generate_content(
            ContentType.ANALYSIS,
            sample_analysis_contexts[0]
        )
        
        # Verify basic structure
        assert 'ANALYSIS' in analysis.upper()
        assert '\n' in analysis  # Proper formatting
        assert len(analysis.split('\n')) > 2  # Multiple lines

    async def test_gonzo_style_markers(self, content_generator, sample_analysis_contexts):
        """Test that analysis maintains Gonzo's voice"""
        analysis = await content_generator.generate_content(
            ContentType.ANALYSIS,
            sample_analysis_contexts[0]
        )
        
        # Check for Gonzo style elements
        gonzo_markers = [
            'magnificent bastards',
            'NEON',
            'your attorney',
            'trust',
            'Pattern #'
        ]
        assert any(marker.lower() in analysis.lower() for marker in gonzo_markers)

    async def test_pattern_recognition(self, content_generator, sample_analysis_contexts):
        """Test for pattern recognition and correlation elements"""
        analysis = await content_generator.generate_content(
            ContentType.ANALYSIS,
            sample_analysis_contexts[0]
        )
        
        pattern_markers = ['pattern', 'correlation', 'matches', 'template']
        assert any(marker.lower() in analysis.lower() for marker in pattern_markers)

    async def test_legal_perspective(self, content_generator, sample_analysis_contexts):
        """Test that legal expertise is incorporated"""
        analysis = await content_generator.generate_content(
            ContentType.ANALYSIS,
            sample_analysis_contexts[0]
        )
        
        legal_markers = ['attorney', 'counsel', 'advise', 'legal', 'rights']
        assert any(marker.lower() in analysis.lower() for marker in legal_markers)

    async def test_temporal_awareness(self, content_generator, sample_analysis_contexts):
        """Test for references to timeline and temporal elements"""
        analysis = await content_generator.generate_content(
            ContentType.ANALYSIS,
            sample_analysis_contexts[0]
        )
        
        temporal_markers = ['3030', 'timeline', 'future', 'Corporate Wars', 'Pattern #']
        assert any(marker in analysis for marker in temporal_markers)

    async def test_character_limit(self, content_generator, sample_analysis_contexts):
        """Test that analysis can fit in a tweet thread"""
        analysis = await content_generator.generate_content(
            ContentType.ANALYSIS,
            sample_analysis_contexts[0]
        )
        
        # Should be tweetable in parts
        sections = analysis.split('\n\n')
        for section in sections:
            assert len(section) <= 280  # Twitter's character limit

    async def test_contextual_integration(self, content_generator, sample_analysis_contexts):
        """Test that analysis incorporates provided context"""
        context = sample_analysis_contexts[1]  # Using Digital Identity context
        analysis = await content_generator.generate_content(
            ContentType.ANALYSIS,
            context
        )
        
        # Verify key context elements are present
        assert context['subject'].lower() in analysis.lower()
        assert any(word in analysis.lower() for word in ['identity', 'privacy', 'control'])
