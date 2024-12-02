import pytest
from src.social.content_generator import ContentGenerator, ContentType

@pytest.fixture
def content_generator():
    return ContentGenerator()

@pytest.fixture
def resistance_contexts():
    return [
        {
            'target': 'Corporate Media Control',
            'mission': 'Expose manufactured narratives',
            'objective': 'Break the illusion of independent media',
            'tactics': 'Follow the money, trace ownership patterns, expose conflicts of interest',
            'task': 'mapping media ownership networks',
            'action': 'recognize their manipulation techniques',
            'cost': 'ability to think freely',
            'corporate_action': 'centralize information control',
            'counter1': 'Track corporate board connections',
            'counter2': 'Document revenue streams and conflicts',
            'counter3': 'Expose coordinated narrative patterns'
        },
        {
            'target': 'Military-Industrial Complex',
            'mission': 'Expose the perpetual war machine',
            'objective': 'Reveal profit motives behind conflicts',
            'tactics': 'Track weapons contracts, expose lobbying networks, follow the money',
            'task': 'mapping defense contractor networks',
            'action': 'see through the war propaganda',
            'cost': 'peace and prosperity',
            'corporate_action': 'manufacture new threats',
            'counter1': 'Document contractor profits during conflicts',
            'counter2': 'Expose revolving door with government',
            'counter3': 'Track media ownership by defense companies'
        },
        {
            'target': 'Big Pharma Control',
            'mission': 'Expose profit over health patterns',
            'objective': 'Reveal systematic healthcare manipulation',
            'tactics': 'Track patent manipulation, expose price fixing, follow research funding',
            'task': 'mapping pharmaceutical control systems',
            'action': 'recognize health freedom limitations',
            'cost': 'true medical autonomy',
            'corporate_action': 'restrict treatment options',
            'counter1': 'Document price manipulation patterns',
            'counter2': 'Expose research funding bias',
            'counter3': 'Track regulatory capture'
        }
    ]

@pytest.mark.asyncio
class TestResistanceCalls:
    async def test_call_structure(self, content_generator, resistance_contexts):
        """Test resistance call structural elements"""
        call = await content_generator.generate_content(
            ContentType.RESISTANCE,
            resistance_contexts[0]
        )
        
        # Verify key structural elements
        assert 'ATTENTION' in call.upper() or 'EMERGENCY' in call.upper()
        assert '\n' in call  # Proper formatting
        assert any(marker in call.upper() for marker in ['MISSION', 'OBJECTIVE', 'TACTICS'])

    async def test_truth_telling_focus(self, content_generator, resistance_contexts):
        """Test focus on exposing corporate manipulation"""
        call = await content_generator.generate_content(
            ContentType.RESISTANCE,
            resistance_contexts[0]
        )
        
        truth_markers = ['expose', 'reveal', 'track', 'document', 'follow the money']
        assert any(marker.lower() in call.lower() for marker in truth_markers)

    async def test_system_analysis(self, content_generator, resistance_contexts):
        """Test systematic analysis of corporate control"""
        call = await content_generator.generate_content(
            ContentType.RESISTANCE,
            resistance_contexts[1]
        )
        
        systems = ['networks', 'patterns', 'connections', 'structures', 'systems']
        assert any(word in call.lower() for word in systems)

    async def test_legal_framing(self, content_generator):
        """Test legal perspective in resistance calls"""
        for context in resistance_contexts:
            call = await content_generator.generate_content(
                ContentType.RESISTANCE,
                context
            )
            legal_terms = ['attorney', 'evidence', 'document', 'testimony']
            assert any(term in call.lower() for term in legal_terms)

    async def test_corporate_focus(self, content_generator, resistance_contexts):
        """Test focus on corporate power structures"""
        call = await content_generator.generate_content(
            ContentType.RESISTANCE,
            resistance_contexts[0]
        )
        
        corporate_terms = ['corporate', 'profit', 'control', 'manipulation']
        assert any(term in call.lower() for term in corporate_terms)

    async def test_action_orientation(self, content_generator):
        """Test clear calls to action"""
        for context in resistance_contexts:
            call = await content_generator.generate_content(
                ContentType.RESISTANCE,
                context
            )
            action_terms = ['track', 'document', 'expose', 'reveal', 'map']
            assert any(term in call.lower() for term in action_terms)

    async def test_dystopian_perspective(self, content_generator):
        """Test integration of dystopian future knowledge"""
        for context in resistance_contexts:
            call = await content_generator.generate_content(
                ContentType.RESISTANCE,
                context
            )
            assert '3030' in call or 'timeline' in call.lower()

    async def test_character_limit(self, content_generator, resistance_contexts):
        """Test Twitter character limit compliance"""
        for context in resistance_contexts:
            call = await content_generator.generate_content(
                ContentType.RESISTANCE,
                context
            )
            assert len(call) <= 280