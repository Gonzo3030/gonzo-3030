import asyncio
import random
from datetime import datetime, timedelta
from social.x_integration import XIntegration
from social.content_generator import ContentType
from social.x_engagement_system import EngagementPriority

class GonzoRunner:
    def __init__(self):
        self.x_system = XIntegration()
        self.running = False
        
    async def start(self):
        """Start Gonzo's operations"""
        print("🚨 Initializing Gonzo-3030...")
        self.running = True
        
        try:
            while self.running:
                if self.x_system.safety_manager.is_operational():
                    # Check daily limits
                    stats = self.x_system.get_system_status()['stats']
                    daily_limits = self.x_system.engagement_system.daily_limits
                    
                    if stats['posts'] < sum(daily_limits.values()):
                        await self._run_cycle()
                        
                        # Dynamic sleep based on priority and engagement
                        priority = await self._assess_current_priority()
                        sleep_seconds = self._get_priority_wait_time(priority)
                        
                        print(f"Priority: {priority}. Waiting {sleep_seconds//60} minutes until next check...")
                        await asyncio.sleep(sleep_seconds)
                    else:
                        print("Daily limits reached. Waiting for next day...")
                        await asyncio.sleep(3600)  # Check again in an hour
                else:
                    print("⚠️ System in emergency shutdown. Waiting 1 hour...")
                    await asyncio.sleep(3600)
                    
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
            # Check for engagement opportunities first
            content = await self._get_latest_content()  # You'll need to implement this
            should_engage, priority = await self.x_system.engagement_system.analyze_engagement_opportunity(content)
            
            if should_engage:
                print(f"\n💬 Engaging with priority {priority}...")
                response = await self.x_system.handle_engagement(content, priority)
            else:
                # Generate standalone content if no engagement needed
                content_type = random.choice(list(ContentType))
                print(f"\n🔮 Generating {content_type.value} content...")
                response = await self.x_system.post_content(content_type)
            
            if response:
                print("✅ Action completed successfully!")
                status = self.x_system.get_system_status()
                print(f"📊 System Stats: {status['stats']}")
            else:
                print("❌ Action failed")
                
        except Exception as e:
            print(f"❌ Error in cycle: {str(e)}")
            self.x_system.safety_manager.log_api_error('CYCLE_ERROR', str(e))
    
    async def _assess_current_priority(self) -> str:
        """Assess current priority based on various factors"""
        # Implement priority assessment based on time, events, etc.
        # For now, return medium as default
        return "MEDIUM"
    
    def _get_priority_wait_time(self, priority: str) -> int:
        """Get wait time in seconds based on priority"""
        priority_times = {
            "CRITICAL": 300,      # 5 minutes
            "HIGH": 3600,       # 1 hour
            "MEDIUM": 14400,    # 4 hours
            "LOW": 28800       # 8 hours
        }
        return priority_times.get(priority, 14400)  # Default to MEDIUM timing

if __name__ == "__main__":
    print("""
    🚨 GONZO-3030 ACTIVATION SEQUENCE 🚨
    Your attorney from the future is coming online...
    Press Ctrl+C to shutdown
    """)
    
    runner = GonzoRunner()
    asyncio.run(runner.start())