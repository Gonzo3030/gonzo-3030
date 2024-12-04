from typing import Dict, List, Optional
from datetime import datetime
import random
from enum import Enum

class ContentType(Enum):
    WARNING = "warning"
    ANALYSIS = "analysis"
    INSIGHT = "insight"
    ACTION = "action"
    RESPONSE = "response"

class ContentGenerator:
    def __init__(self):
        self.last_types = []  # Track recent content types for variety
        self.knowledge_system = None  # Will be set by orchestrator
        self.max_history = 5  # Keep track of last 5 content types
        
    def set_knowledge_system(self, knowledge_system):
        """Set the knowledge system reference"""
        self.knowledge_system = knowledge_system
    
    def generate_content(self, content_type: ContentType, context: Optional[Dict] = None) -> str:
        """Generate dynamic content based on type and context"""
        if not context:
            context = {}
            
        if not self.knowledge_system:
            return self._generate_fallback_content(content_type)
            
        # Get current assessment
        assessment = self.knowledge_system.get_current_assessment()
        
        content = ""
        if content_type == ContentType.WARNING:
            content = self._generate_warning(assessment, context)
        elif content_type == ContentType.ANALYSIS:
            content = self._generate_analysis(assessment, context)
        elif content_type == ContentType.INSIGHT:
            content = self._generate_insight(assessment, context)
        elif content_type == ContentType.ACTION:
            content = self._generate_action_call(assessment, context)
        else:
            content = self._generate_response(assessment, context)
            
        # Track content type
        self.last_types = (self.last_types + [content_type])[-self.max_history:]
        
        return content