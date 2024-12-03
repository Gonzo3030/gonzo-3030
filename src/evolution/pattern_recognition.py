from typing import Dict, List, Optional, Set
from datetime import datetime
from langchain_anthropic import ChatAnthropic
from langchain.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough

class PatternRecognition:
    def __init__(self):
        self.llm = ChatAnthropic(model="claude-3-sonnet-20240229")
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

    async def analyze_pattern(self, content: str, pattern_type: str = "general") -> Dict:
        """Analyze content for patterns of specified type."""
        chain = self.analysis_chains.get(pattern_type, self.analysis_chains["general"])
        pattern_data = self.pattern_types.get(pattern_type, self.pattern_types["manipulation"])
        
        analysis = await chain.ainvoke({
            "content": content,
            "known_patterns": list(pattern_data["confirmed_patterns"])
        })
        
        # Update pattern database with new findings
        await self._update_patterns(pattern_type, analysis)
        
        return {
            "analysis": analysis,
            "new_patterns": self._extract_new_patterns(analysis),
            "warnings": self._extract_warnings(analysis)
        }

    async def evolve_understanding(self, feedback: Dict) -> None:
        """Evolve pattern recognition based on feedback."""
        try:
            pattern_type = feedback.get("type", "general")
            patterns = feedback.get("patterns", set())
            success = feedback.get("success", False)
            
            if pattern_type not in self.pattern_types:
                pattern_type = "manipulation"  # Default fallback
            
            # Update pattern tracking based on success
            if success:
                # Move successful patterns to confirmed
                self.pattern_types[pattern_type]["confirmed_patterns"].update(patterns)
                if pattern_type == "resistance_strategies":
                    self.pattern_types["resistance_strategies"]["successful"].update(patterns)
            else:
                # Track failed patterns
                if pattern_type == "resistance_strategies":
                    self.pattern_types["resistance_strategies"]["failed"].update(patterns)
                
                # Record in evolution tracking for analysis
                evolution_tracking = self.pattern_types[pattern_type]["evolution_tracking"]
                for pattern in patterns:
                    if pattern not in evolution_tracking:
                        evolution_tracking[pattern] = {
                            "failures": 1,
                            "first_seen": datetime.now().isoformat(),
                            "last_update": datetime.now().isoformat()
                        }
                    else:
                        evolution_tracking[pattern]["failures"] += 1
                        evolution_tracking[pattern]["last_update"] = datetime.now().isoformat()
            
        except Exception as e:
            print(f"Error in evolve_understanding: {str(e)}")

    def _create_analysis_chain(self):
        """Create general pattern analysis chain."""
        prompt = ChatPromptTemplate.from_template(
            """Analyze the following content for patterns, maintaining Gonzo's dystopian attorney perspective:

Content: {content}
Known Patterns: {known_patterns}

Identify new patterns and potential timeline divergences."""
        )
        
        return prompt | self.llm

    def _create_manipulation_chain(self):
        """Create manipulation detection chain."""
        prompt = ChatPromptTemplate.from_template(
            """As Gonzo-3030, analyze this content for signs of narrative manipulation:

Content: {content}
Known Manipulation Patterns: {known_patterns}

Identify any corporate manipulation techniques."""
        )
        
        return prompt | self.llm

    def _create_tactics_chain(self):
        """Create corporate tactics analysis chain."""
        prompt = ChatPromptTemplate.from_template(
            """From your perspective in 3030, analyze these corporate actions:

Content: {content}
Known Tactics: {known_patterns}

Identify tactics that lead to the dystopian future."""
        )
        
        return prompt | self.llm

    def _create_resistance_chain(self):
        """Create resistance strategy analysis chain."""
        prompt = ChatPromptTemplate.from_template(
            """As a dystopian attorney, evaluate these resistance strategies:

Content: {content}
Known Strategies: {known_patterns}

Assess effectiveness and suggest improvements."""
        )
        
        return prompt | self.llm

    async def _update_patterns(self, pattern_type: str, analysis: str) -> None:
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
        patterns = set()
        for line in str(analysis).split('\n'):
            if 'pattern:' in line.lower():
                patterns.add(line.split('pattern:', 1)[1].strip())
        return patterns

    def _extract_warnings(self, analysis: str) -> List[str]:
        """Extract relevant warnings from analysis."""
        warnings = []
        for line in str(analysis).split('\n'):
            if any(term in line.lower() for term in ['warning:', 'alert:', 'caution:', 'danger:']):
                warnings.append(line.strip())
        return warnings