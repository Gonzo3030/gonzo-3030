import asyncio
import os
import signal
from typing import Dict
from src.core.orchestrator import GonzoOrchestrator
from src.social.x_integration import XIntegration
from src.core.personality import GonzoPersonality
from src.intelligence.brave_searcher import BraveSearcher

class GonzoLauncher:
    def __init__(self):
        self.orchestrator = GonzoOrchestrator()
        self.x_system = XIntegration()
        self.personality = GonzoPersonality()
        self.brave_searcher = BraveSearcher()
        self.shutdown_event = asyncio.Event()
        
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
            
            while not self.shutdown_event.is_set():
                if self.x_system.safety_manager.is_operational():
                    # Check for mentions and interactions
                    mentions = self.x_system.api_client.get_mentions(since_minutes=5)
                    if mentions:
                        for mention in mentions:
                            if self.shutdown_event.is_set():
                                break
                            await self.handle_mention(mention)
                    
                    # Check for significant new developments
                    findings = await self.brave_searcher.monitor_topics()
                    if findings:
                        for finding in findings:
                            if self.shutdown_event.is_set():
                                break
                            await self.handle_finding(finding)
                    
                    # Get system status
                    status = self.x_system.get_system_status()
                    
                    if status['stats']['posts'] < self.x_system.engagement_system.daily_limits['standalone']:
                        # Generate and post content if needed
                        content = await self.orchestrator.process_input({
                            "type": "content_generation",
                            "content": "Generate next social post"
                        })
                        
                        await self.x_system.post_content(
                            content_type=content.get('type', 'WARNING'),
                            context=content
                        )
                    
                    # Dynamic wait based on activity
                    had_activity = bool(mentions or findings)
                    wait_time = 300 if had_activity else 900  # 5 mins if active, 15 if not
                    print(f"\n⏳ Waiting {wait_time//60} minutes until next check...")
                    try:
                        await asyncio.wait_for(self.shutdown_event.wait(), timeout=wait_time)
                    except asyncio.TimeoutError:
                        continue
                else:
                    print("\n⚠️ Technical systems in recovery. Waiting...")
                    try:
                        await asyncio.wait_for(self.shutdown_event.wait(), timeout=3600)
                    except asyncio.TimeoutError:
                        continue
                    
        except Exception as e:
            print(f"\n❌ Critical error: {str(e)}")
            self.x_system.safety_manager.log_api_error('CRITICAL_ERROR', str(e))
            raise
        finally:
            print("\n🛑 Shutting down Gonzo-3030...")
            await self.orchestrator.process_input({"type": "system_shutdown", "content": "Emergency shutdown initiated"})
    
    async def handle_mention(self, mention: Dict):
        """Handle a mention or interaction"""
        try:
            response = await self.orchestrator.process_input({
                "type": "mention",
                "content": mention.get('text', ''),
                "author_id": mention.get('author_id'),
                "tweet_id": mention.get('id')
            })
            
            await self.x_system.handle_engagement(
                trigger_content=response,
                priority='HIGH'  # Mentions get high priority
            )
        except Exception as e:
            print(f"Error handling mention: {str(e)}")
    
    async def handle_finding(self, finding: Dict):
        """Handle a significant finding from Brave search"""
        try:
            # Prepare the content with finding details
            content = {
                "type": "intelligence",
                "source": finding.get('url', ''),
                "title": finding.get('title', ''),
                "summary": finding.get('description', ''),
                "significance": finding.get('significance', 0.5),
                "published_date": finding.get('published_date', '')
            }
            
            response = await self.orchestrator.process_input(content)
            
            # Post based on significance
            if finding.get('significance', 0.5) > 0.7:
                await self.x_system.post_content(
                    content_type='WARNING',
                    context=response
                )
            else:
                await self.x_system.post_content(
                    content_type='ANALYSIS',
                    context=response
                )
                
        except Exception as e:
            print(f"Error handling finding: {str(e)}")
    
    def shutdown(self):
        """Trigger a clean shutdown"""
        print("\n🚨 Initiating shutdown sequence...")
        self.shutdown_event.set()

def handle_shutdown(signum, frame):
    """Handle shutdown signals"""
    if hasattr(asyncio, 'get_running_loop'):
        try:
            loop = asyncio.get_running_loop()
            if hasattr(loop, 'launcher'):
                loop.launcher.shutdown()
        except RuntimeError:
            pass

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
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, handle_shutdown)
    signal.signal(signal.SIGTERM, handle_shutdown)
    
    # Launch Gonzo
    launcher = GonzoLauncher()
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.launcher = launcher  # Store reference for signal handler
    try:
        loop.run_until_complete(launcher.launch())
    finally:
        loop.close()