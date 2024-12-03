import asyncio
import os
from src.core.orchestrator import GonzoOrchestrator
from src.social.x_api_client import XApiClient
from src.core.personality import GonzoPersonality
from src.intelligence.brave_searcher import BraveSearcher

class GonzoLauncher:
    def __init__(self):
        self.orchestrator = GonzoOrchestrator()
        self.x_api_client = XApiClient()
        self.personality = GonzoPersonality()
        self.brave_searcher = BraveSearcher()

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
                if self.x_api_client.safety_manager.is_operational():
                    # Check for mentions and interactions
                    mentions = await self.x_api_client.get_mentions(since_minutes=5)
                    if mentions:
                        for mention in mentions:
                            await self.handle_mention(mention)

                    # Check for significant new developments
                    findings = await self.brave_searcher.monitor_topics()
                    if findings:
                        for finding in findings:
                            await self.handle_finding(finding)

                    # Get system status
                    status = await self.x_api_client.get_system_status()

                    if status['stats']['posts'] < self.x_api_client.engagement_system.daily_limits['standalone']:
                        # Generate and post content if needed
                        content = await self.orchestrator.process_input({
                            "type": "content_generation",
                            "content": "Generate next social post"
                        })

                        await self.x_api_client.post_content(
                            content_type=content.get('type', 'WARNING'),
                            context=content
                        )

                    # Dynamic wait based on activity
                    had_activity = bool(mentions or findings)
                    wait_time = await self.x_api_client.calculate_next_check_delay(had_activity)
                    print(f"⏳ Waiting {wait_time//60} minutes until next check...")
                    await asyncio.sleep(wait_time)
                else:
                    print("⚠️ Technical systems in recovery. Waiting...")
                    await asyncio.sleep(3600)

        except KeyboardInterrupt:
            print("🛑 Shutting down Gonzo-3030...")
            await self.orchestrator.process_input({"type": "system_shutdown", "content": "Emergency shutdown initiated"})

        except Exception as e:
            print(f"❌ Critical error: {str(e)}")
            self.x_api_client.safety_manager.log_api_error('CRITICAL_ERROR', str(e))
            raise

    async def handle_mention(self, mention: dict):
        """Handle a mention or interaction"""
        try:
            response = await self.orchestrator.process_input({
                "type": "mention",
                "content": mention.get('text', ''),
                "author_id": mention.get('author_id'),
                "tweet_id": mention.get('id')
            })

            await self.x_api_client.handle_engagement(
                trigger_content=response,
                priority='HIGH'  # Mentions get high priority
            )
        except Exception as e:
            print(f"Error handling mention: {str(e)}")

    async def handle_finding(self, finding: dict):
        """Handle a significant finding from Brave search"""
        try:
            response = await self.orchestrator.process_input({
                "type": "intelligence",
                "content": f"{finding.get('title')} {finding.get('description')}"
            })

            await self.x_api_client.handle_engagement(
                trigger_content=response,
                priority='MEDIUM'  # Findings get medium priority
            )
        except Exception as e:
            print(f"Error handling finding: {str(e)}")
