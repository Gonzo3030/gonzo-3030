from typing import Dict, List, Optional, Set
from datetime import datetime
from langchain_community.chat_models import ChatAnthropic
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class PatternRecognition:
    def __init__(self):
        self.llm = ChatAnthropic()
        self.pattern_types = {
            "manipulation": {
                "indicators": set(),
                "confirmed_patterns": set(),
                "evolution_tracking": {}
            },
            "corporate_tactics": {
                "indicators": set(),
                "confirmed_patterns": set(),
                "evolution_tracking": {}
            },
            "resistance_strategies": {
                "successful": set(),
                "failed": set(),
                "emerging": set()
            }
        }
        
        # Initialize analysis chains
        self.analysis_chains = {
            "general": self._create_analysis_chain(),
            "manipulation": self._create_manipulation_chain(),
            "corporate_tactics": self._create_tactics_chain(),
            "resistance": self._create_resistance_chain()
        }

    def _create_analysis_chain(self) -> LLMChain:
        """Create general pattern analysis chain."""
        template = """Analyze the following content for patterns, maintaining Gonzo's dystopian attorney perspective:

Content: {content}
Known Patterns: {known_patterns}

Identify new patterns and potential timeline divergences."""
        
        return LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                template=template,
                input_variables=["content", "known_patterns"]
            )
        )

    def _create_manipulation_chain(self) -> LLMChain:
        """Create manipulation detection chain."""
        template = """As Gonzo-3030, analyze this content for signs of narrative manipulation:

Content: {content}
Known Manipulation Patterns: {known_patterns}

Identify any corporate manipulation techniques."""
        
        return LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                template=template,
                input_variables=["content", "known_patterns"]
            )
        )

    def _create_tactics_chain(self) -> LLMChain:
        """Create corporate tactics analysis chain."""
        template = """From your perspective in 3030, analyze these corporate actions:

Content: {content}
Known Tactics: {known_patterns}

Identify tactics that lead to the dystopian future."""
        
        return LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                template=template,
                input_variables=["content", "known_patterns"]
            )
        )

    def _create_resistance_chain(self) -> LLMChain:
        """Create resistance strategy analysis chain."""
        template = """As a dystopian attorney, evaluate these resistance strategies:

Content: {content}
Known Strategies: {known_patterns}

Assess effectiveness and suggest improvements."""
        
        return LLMChain(
            llm=self.llm,
            prompt=PromptTemplate(
                template=template,
                input_variables=["content", "known_patterns"]
            )
        )

    async def analyze_pattern(self, content: str, pattern_type: str = "general") -> Dict:
        """Analyze content for patterns of specified type."""
        chain = self.analysis_chains.get(pattern_type, self.analysis_chains["general"])
        pattern_data = self.pattern_types.get(pattern_type, self.pattern_types["manipulation"])
        known_patterns = pattern_data["confirmed_patterns"]
        
        analysis = await chain.arun(
            content=content,
            known_patterns=list(known_patterns)
        )
        
        # Update pattern database with new findings
        self._update_patterns(pattern_type, analysis)
        
        return {
            "analysis": analysis,
            "new_patterns": self._extract_new_patterns(analysis),
            "warnings": self._extract_warnings(analysis)
        }

    def _update_patterns(self, pattern_type: str, analysis: Dict) -> None:
        """Update pattern database with new information."""
        if pattern_type not in self.pattern_types:
            pattern_type = "manipulation"  # Default fallback
            
        new_patterns = self._extract_new_patterns(analysis)
        
        # Add to indicators first
        self.pattern_types[pattern_type]["indicators"].update(new_patterns)
        
        # If pattern is seen multiple times, move to confirmed
        for pattern in new_patterns:
            if self._pattern_frequency(pattern) > 3:
                self.pattern_types[pattern_type]["confirmed_patterns"].add(pattern)

    def _pattern_frequency(self, pattern: str) -> int:
        """Track how often a pattern has been observed."""
        frequency = 0
        for pattern_type in self.pattern_types.values():
            if pattern in pattern_type["indicators"]:
                frequency += 1
            if pattern in pattern_type.get("confirmed_patterns", set()):
                frequency += 2
        return frequency

    def _extract_new_patterns(self, analysis: str) -> Set[str]:
        """Extract new patterns from analysis."""
        # Simple extraction for now - will be enhanced
        patterns = set()
        for line in analysis.split('\n'):
            if 'pattern:' in line.lower():
                patterns.add(line.split('pattern:', 1)[1].strip())
        return patterns

    def _extract_warnings(self, analysis: str) -> List[str]:
        """Extract relevant warnings from analysis."""
        warnings = []
        for line in analysis.split('\n'):
            if any(term in line.lower() for term in ['warning:', 'alert:', 'caution:', 'danger:']):
                warnings.append(line.strip())
        return warnings

    async def evolve_understanding(self, feedback: Dict) -> None:
        """Evolve pattern recognition based on feedback."""
        pattern_type = feedback.get("type", "manipulation")
        success = feedback.get("success", False)
        
        if pattern_type in self.pattern_types:
            if success:
                # Move pattern from indicators to confirmed if successful
                self.pattern_types[pattern_type]["confirmed_patterns"].update(
                    feedback.get("patterns", set())
                )
            else:
                # Track failed patterns
                self.pattern_types[pattern_type]["evolution_tracking"].setdefault(
                    "failed_patterns", set()
                ).update(feedback.get("patterns", set()))