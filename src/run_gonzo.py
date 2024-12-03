import asyncio
import random
from datetime import datetime, timedelta
from social.x_integration import XIntegration
from social.content_generator import ContentType

class GonzoRunner:
    def __init__(self):
        self.x_system = XIntegration()
        self.running = False
        
        # Base timing settings
        self.min_post_interval = timedelta(hours=2)  # Min time between posts
        self.max_post_interval = timedelta(hours=4)  # Max time between posts
        
    async def start(self):
        """Start Gonzo's operations"""
        print("🚨 Initializing Gonzo-3030...")
        self.running = True
        
        try:
            while self.running:
                if self.x_system.safety_manager.is_operational():
                    await self._run_cycle()
                    
                    # Random interval between posts
                    sleep_seconds = random.randint(
                        int(self.min_post_interval.total_seconds()),
                        int(self.max_post_interval.total_seconds())
                    )
                    print(f"Waiting {sleep_seconds//3600} hours until next post...")
                    await asyncio.sleep(sleep_seconds)
                else:
                    print("⚠️ System in emergency shutdown. Waiting 1 hour...")
                    await asyncio.sleep(3600)  # Wait an hour before checking again
                    
        except KeyboardInterrupt:
            print("\n🛑 Shutting down Gonzo-3030...")
            self.running = False
            
        except Exception as e:
            print(f"❌ Error in main loop: {str(e)}")
            self.x_system.safety_manager.log_api_error('RUNTIME_ERROR', str(e))
            raise
    
    async def _run_cycle(self):
        """Run one cycle of Gonzo's operations"""
        try:
            # Randomly choose content type
            content_type = random.choice(list(ContentType))
            
            print(f"\n🔮 Generating {content_type.value} content...")
            response = await self.x_system.post_content(content_type)
            
            if response:
                print("✅ Posted successfully!")
                status = self.x_system.get_system_status()
                print(f"📊 System Stats: {status['stats']}")
            else:
                print("❌ Posting failed")
                
        except Exception as e:
            print(f"❌ Error in cycle: {str(e)}")
            self.x_system.safety_manager.log_api_error('CYCLE_ERROR', str(e))

if __name__ == "__main__":
    print("""
    🚨 GONZO-3030 ACTIVATION SEQUENCE 🚨
    Your attorney from the future is coming online...
    Press Ctrl+C to shutdown
    """)
    
    runner = GonzoRunner()
    asyncio.run(runner.start())