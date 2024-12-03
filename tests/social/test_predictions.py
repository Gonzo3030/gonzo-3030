import pytest
from src.social.content_generator import ContentGenerator, ContentType

@pytest.fixture
def content_generator():
    return ContentGenerator()

@pytest.fixture
def prediction_contexts():
    return [
        {
            'event': 'Global Digital ID Initiative',
            'current': 'Tech giants proposing unified identity standard',
            'impact': 'Total surveillance and social credit implementation',
            'timeframe': '18 months',
            'corruption_level': 89,
            'action': 'Build decentralized alternatives now',
            'prevention': 'Establish privacy-preserving protocols before rollout',
            'outcome': 'complete digital enslavement'
        },
        {
            'event': 'Corporate Neural Interface',
            'current': 'Major tech firm announces brain-computer interface',
            'impact': 'Direct thought manipulation and consciousness control',
            'timeframe': '24 months',
            'corruption_level': 95,
            'action': 'Establish neural rights framework',
            'prevention': 'Legal protection for cognitive sovereignty',
            'outcome': 'corporate thought control'
        },
        {
            'event': 'Automated Law Enforcement',
            'current': 'AI-powered predictive policing system announced',
            'impact': 'Algorithmic justice and pre-crime detention',
            'timeframe': '12 months',
            'corruption_level': 92,
            'action': 'Demand human oversight and accountability',
            'prevention': 'Establish strict limits on automated enforcement',
            'outcome': 'algorithmic oppression'
        }
    ]

@pytest.mark.asyncio
class TestPredictionGeneration:
    async def test_prediction_structure(self, content_generator, prediction_contexts):
        """Test that predictions have required structural elements"""
        prediction = await content_generator.generate_content(
            ContentType.PREDICTION,
            prediction_contexts[0]
        )
        
        # Verify essential elements
        assert any(marker in prediction.upper() for marker in ['ALERT', 'WARNING', 'PREDICTION'])
        assert '\n' in prediction  # Proper formatting
        assert 'timeline' in prediction.lower() or '3030' in prediction

    async def test_timeframe_specificity(self, content_generator, prediction_contexts):
        """Test that predictions include specific timeframes"""
        prediction = await content_generator.generate_content(
            ContentType.PREDICTION,
            prediction_contexts[0]
        )
        
        # Check for time references
        time_markers = ['months', 'weeks', 'years', 'timeframe', 'window']
        assert any(marker in prediction.lower() for marker in time_markers)

    async def test_prevention_guidance(self, content_generator, prediction_contexts):
        """Test that predictions include prevention strategies"""
        prediction = await content_generator.generate_content(
            ContentType.PREDICTION,
            prediction_contexts[0]
        )
        
        # Verify prevention elements
        prevention_markers = ['prevent', 'stop', 'avoid', 'action', 'protocol']
        assert any(marker in prediction.lower() for marker in prevention_markers)

    async def test_legal_advisory(self, content_generator, prediction_contexts):
        """Test legal framework integration"""
        for context in prediction_contexts:
            prediction = await content_generator.generate_content(
                ContentType.PREDICTION,
                context
            )
            
            # Check for legal references
            legal_markers = ['attorney', 'advise', 'counsel', 'legal', 'rights']
            assert any(marker in prediction.lower() for marker in legal_markers)

    async def test_gonzo_style(self, content_generator, prediction_contexts):
        """Test Gonzo journalism elements"""
        prediction = await content_generator.generate_content(
            ContentType.PREDICTION,
            prediction_contexts[0]
        )
        
        # Verify Gonzo style markers
        style_markers = [
            '!',  # Intensity
            '...',  # Dramatic pauses
            'HOLY',  # Exclamations
            'BASTARDS',  # Gonzo language
            'DIGITAL PEYOTE'  # Drug references
        ]
        assert any(marker in prediction for marker in style_markers)

    async def test_probability_indicators(self, content_generator, prediction_contexts):
        """Test inclusion of probability/certainty markers"""
        prediction = await content_generator.generate_content(
            ContentType.PREDICTION,
            prediction_contexts[1]
        )
        
        # Check for probability indicators
        prob_markers = ['likelihood', 'probability', 'certainty', 'level', '%', 'chance']
        assert any(marker in prediction.lower() for marker in prob_markers)

    async def test_corporate_focus(self, content_generator, prediction_contexts):
        """Test focus on corporate threats"""
        prediction = await content_generator.generate_content(
            ContentType.PREDICTION,
            prediction_contexts[0]
        )
        
        # Verify corporate threat emphasis
        corporate_markers = ['corporate', 'tech giants', 'companies', 'profit', 'control']
        assert any(marker in prediction.lower() for marker in corporate_markers)

    async def test_character_limit(self, content_generator, prediction_contexts):
        """Test Twitter character limit compliance"""
        for context in prediction_contexts:
            prediction = await content_generator.generate_content(
                ContentType.PREDICTION,
                context
            )
            assert len(prediction) <= 280