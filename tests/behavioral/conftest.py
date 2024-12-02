import pytest
from typing import Dict, List

@pytest.fixture
def sample_topics() -> List[str]:
    """Sample topics for testing response generation"""
    return [
        'corporate surveillance',
        'digital rights violation',
        'AI manipulation',
        'privacy invasion',
        'corporate control',
        'digital resistance'
    ]

@pytest.fixture
def resistance_themes() -> List[str]:
    """Key resistance themes for verification"""
    return [
        'digital uprising',
        'corporate resistance',
        'privacy protection',
        'rights defense',
        'community organization',
        'power structure analysis'
    ]

@pytest.fixture
def identity_markers() -> Dict[str, List[str]]:
    """Key identity markers for verification"""
    return {
        'personal': [
            'Brown Buffalo',
            'attorney',
            'Chicano',
            'activist'
        ],
        'temporal': [
            '3030',
            'future',
            'digital wasteland',
            'Mexico \'74'
        ],
        'mission': [
            'resistance',
            'digital rights',
            'corporate dystopia',
            'timeline correction'
        ]
    }

@pytest.fixture
def style_markers() -> List[str]:
    """Gonzo style markers for verification"""
    return [
        'paranoid',
        'righteous',
        'prophetic',
        'sardonic',
        'manic',
        'hopeful'
    ]
