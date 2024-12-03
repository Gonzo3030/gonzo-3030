from typing import Dict, List, Optional
from datetime import datetime
from .x_api_client import XAPIClient
from .content_generator import ContentGenerator, ContentType
from .x_engagement_system import XEngagementSystem, EngagementType
from .safety_manager import SafetyManager

class XIntegration:
    def __init__(self):
        self.api_client = XAPIClient()
        self.content_generator = ContentGenerator()
        self.engagement_system = XEngagementSystem()
        self.safety_manager = SafetyManager()

    async def post_content(self, content_type: ContentType, context: Optional[Dict] = None) -> Dict:
        """Generate and post Gonzo content"""
        try:
            # Check technical limits
            if not self.safety_manager.check_rate_limit():
                raise Exception('Rate limit exceeded')

            # Generate content using Gonzo's system
            content = await self.content_generator.generate_content(content_type, context)
            
            # Post content
            if len(content) <= 280:
                response = self.api_client.create_post(content)
                if response:
                    self.safety_manager.record_post()
                return response
            else:
                lines = content.split('\n')
                chunks = self._chunk_content(lines)
                response = self.api_client.create_thread(chunks)
                if response:
                    for _ in chunks:
                        self.safety_manager.record_post('thread')
                return response
                
        except Exception as e:
            self.safety_manager.log_api_error('POSTING_ERROR', str(e))
            raise

    async def handle_engagement(self, 
                              trigger_content: Dict,
                              priority: str = 'medium') -> Dict:
        """Handle engagement based on Gonzo's system"""
        try:
            # Check technical limits
            if not self.safety_manager.check_rate_limit():
                raise Exception('Rate limit exceeded')

            # Analyze engagement opportunity
            should_engage, priority = await self.engagement_system.analyze_engagement_opportunity(trigger_content)
            
            if not should_engage:
                return None

            # Generate response using Gonzo's system
            engagement_type = 'THREAD' if priority in ['CRITICAL', 'HIGH'] else 'REPLY'
            response = await self.engagement_system.generate_response(
                content=trigger_content,
                engagement_type=engagement_type
            )
            
            # Post the response
            if engagement_type == 'THREAD':
                result = self.api_client.create_thread(response)
                if result:
                    for _ in response:
                        self.safety_manager.record_post('thread')
                return result
            else:
                result = self.api_client.create_post(response)
                if result:
                    self.safety_manager.record_post('reply')
                return result
                
        except Exception as e:
            self.safety_manager.log_api_error('ENGAGEMENT_ERROR', str(e))
            raise

    def _chunk_content(self, lines: List[str], max_length: int = 280) -> List[str]:
        """Break content into tweet-sized chunks while preserving line breaks"""
        chunks = []
        current_chunk = []
        current_length = 0

        for line in lines:
            line_length = len(line) + 1  # +1 for newline
            
            if current_length + line_length > max_length:
                if current_chunk:
                    chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_length = line_length
            else:
                current_chunk.append(line)
                current_length += line_length
        
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
            
        return chunks
    
    def get_system_status(self) -> Dict:
        """Get technical system status"""
        return {
            'operational': self.safety_manager.is_operational(),
            'stats': self.safety_manager.get_technical_stats()
        }