import asyncio
import os
from src.core.orchestrator import Orchestrator
from src.social.x_integration import XIntegration
from src.core.personality import GonzoPersonality

class GonzoLauncher:
    def __init__(self):
        self.orchestrator = Orchestrator()
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
            await self.orchestrator.initialize()
            
            while True:
                if self.x_system.safety_manager.is_operational():
                    # Get system status
                    status = self.x_system.get_system_status()
                    
                    if status['stats']['posts'] < self.x_system.engagement_system.daily_limits['standalone']:
                        # Generate and post content
                        content = await self.orchestrator.generate_next_action()
                        await self.x_system.post_content(content['type'], content['context'])
                        
                        # Check for engagement opportunities
                        engagement = await self.orchestrator.scan_for_engagement()
                        if engagement:
                            await self.x_system.handle_engagement(
                                trigger_content=engagement['content'],
                                priority=engagement['priority']
                            )
                        
                        # Dynamic wait based on priority
                        wait_time = await self.orchestrator.calculate_next_action_delay()
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
            await self.orchestrator.shutdown()
            
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