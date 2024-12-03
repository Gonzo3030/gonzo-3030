import asyncio
import os
from src.core.orchestrator import GonzoOrchestrator
from src.social.x_integration import XIntegration
from src.core.personality import GonzoPersonality

class GonzoLauncher:
    def __init__(self):
        self.orchestrator = GonzoOrchestrator()
        self.x_system = XIntegration()
        self.personality = GonzoPersonality()
        
    async def launch(self):
        print("""
        🚨 GONZO-3030 ACTIVATION SEQUENCE INITIATED 🚨
        Attorney from the wasteland powering up...
        Timeline analysis systems: ONLINE
        Resistance protocols: ENGAGED
        Corporate manipulation detection: ACTIVE
        
        Press Ctrl+C to initiate emergency shutdown
        """)
        
        try:
            # Initialize all systems
            await self.orchestrator.process_input({"type": "system_init", "content": "Initializing Gonzo-3030 systems"})
            
            while True:
                if self.x_system.safety_manager.is_operational():
                    # Get system status
                    status = self.x_system.get_system_status()
                    
                    if status['stats']['posts'] < self.x_system.engagement_system.daily_limits['standalone']:
                        # Generate and post content
                        content = await self.orchestrator.process_input({
                            "type": "content_generation",
                            "content": "Generate next social post"
                        })
                        
                        await self.x_system.post_content(
                            content_type=content.get('type', 'WARNING'),
                            context=content
                        )
                        
                        # Check for engagement opportunities
                        engagement = await self.orchestrator.process_input({
                            "type": "engagement_scan",
                            "content": "Scan for engagement opportunities"
                        })
                        
                        if engagement.get('engagement_needed', False):
                            await self.x_system.handle_engagement(
                                trigger_content=engagement['content'],
                                priority=engagement.get('priority', 'MEDIUM')
                            )
                        
                        # Dynamic wait based on priority and context
                        wait_time = engagement.get('next_check_delay', 3600)  # Default 1 hour
                        print(f"\n⏳ Waiting {wait_time//60} minutes until next action...")
                        await asyncio.sleep(wait_time)
                    else:
                        print("\n🌙 Daily limits reached. Entering rest mode...")
                        await asyncio.sleep(3600)  # Check again in an hour
                else:
                    print("\n⚠️ Technical systems in recovery. Waiting...")
                    await asyncio.sleep(3600)
                    
        except KeyboardInterrupt:
            print("\n🛑 Shutting down Gonzo-3030...")
            await self.orchestrator.process_input({"type": "system_shutdown", "content": "Emergency shutdown initiated"})
            
        except Exception as e:
            print(f"\n❌ Critical error: {str(e)}")
            self.x_system.safety_manager.log_api_error('CRITICAL_ERROR', str(e))
            raise

if __name__ == "__main__":
    # Load environment variables
    from dotenv import load_dotenv
    load_dotenv()
    
    # Verify API credentials exist
    required_vars = ['X_API_KEY', 'X_API_SECRET', 'X_ACCESS_TOKEN', 'X_ACCESS_SECRET']
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"\n❌ Error: Missing required environment variables: {', '.join(missing_vars)}")
        print("Please set these in your .env file")
        exit(1)
    
    # Launch Gonzo
    launcher = GonzoLauncher()
    asyncio.run(launcher.launch())