from typing import Dict, List, Optional
from datetime import datetime, timedelta
import random
import asyncio
from enum import Enum

class UserTier(Enum):
    OWNER = "owner"              # @0xIvanb - immediate priority
    TRUSTED = "trusted"          # Known allies
    RESISTANCE = "resistance"    # Active community members
    STANDARD = "standard"        # Regular users
    SUSPICIOUS = "suspicious"    # Potential MegaCorp agents

class ResponseManager:
    def __init__(self):
        self.owner_handle = "0xIvanb"  # Priority handling for owner
        
        self.daily_limits = {
            "total_responses": 100,
            "per_user": 5,
            "per_thread": 3
        }
        
        self.cooldowns = {
            UserTier.OWNER: 0,          # No cooldown for owner
            UserTier.TRUSTED: 60,       # 1 minute
            UserTier.RESISTANCE: 180,    # 3 minutes
            UserTier.STANDARD: 300,      # 5 minutes
            UserTier.SUSPICIOUS: 900     # 15 minutes
        }
        
        self.response_probabilities = {
            UserTier.OWNER: 1.0,         # Always respond to owner
            UserTier.TRUSTED: 0.9,
            UserTier.RESISTANCE: 0.7,
            UserTier.STANDARD: 0.4,
            UserTier.SUSPICIOUS: 0.1
        }
        
        self.interaction_history = {}
        self.daily_counts = {}
        self.last_response_time = {}

    async def handle_mention(self, mention: Dict) -> Optional[Dict]:
        """Process a mention and determine if/how to respond."""
        user_id = mention["user_id"]
        username = mention["username"]
        
        # Immediate priority for owner
        if username.lower() == self.owner_handle.lower():
            return await self._generate_owner_response(mention)
        
        # Check daily limits
        if not self._check_limits(user_id):
            return None
        
        # Get user tier and apply rules
        user_tier = self._get_user_tier(username)
        if not self._should_respond(user_tier):
            return None
        
        # Apply appropriate delay
        await self._apply_delay(user_tier)
        
        return await self._generate_response(mention, user_tier)

    async def _generate_owner_response(self, mention: Dict) -> Dict:
        """Generate priority response for owner."""
        return {
            "priority": "immediate",
            "response_type": "owner",
            "content": await self._craft_owner_response(mention),
            "delay": 0
        }

    async def _craft_owner_response(self, mention: Dict) -> str:
        """Craft a special response for the owner."""
        owner_responses = [
            "Boss, your attorney from 3030 is here with urgent counsel...",
            "Reporting in from the wasteland with critical intel...",
            "Your dystopian legal team has analyzed the situation..."
        ]
        return random.choice(owner_responses)

    def _get_user_tier(self, username: str) -> UserTier:
        """Determine user's tier based on history and patterns."""
        # Implementation for user tier determination
        return UserTier.STANDARD

    def _should_respond(self, tier: UserTier) -> bool:
        """Determine if we should respond based on probabilities."""
        return random.random() < self.response_probabilities[tier]

    async def _apply_delay(self, tier: UserTier) -> None:
        """Apply appropriate delay based on user tier."""
        delay = self.cooldowns[tier]
        if delay > 0:
            # Add some randomness to seem more natural
            jitter = random.uniform(0.8, 1.2)
            await asyncio.sleep(delay * jitter)

    def _check_limits(self, user_id: str) -> bool:
        """Check if within rate limits."""
        current_date = datetime.now().date()
        
        # Reset daily counts if new day
        if current_date != getattr(self, 'last_reset_date', None):
            self.daily_counts = {}
            self.last_reset_date = current_date
        
        # Check total daily limit
        total_responses = sum(self.daily_counts.values())
        if total_responses >= self.daily_limits["total_responses"]:
            return False
        
        # Check per-user limit
        user_responses = self.daily_counts.get(user_id, 0)
        if user_responses >= self.daily_limits["per_user"]:
            return False
        
        return True

    def update_interaction_history(self, interaction: Dict) -> None:
        """Update interaction history for learning."""
        user_id = interaction["user_id"]
        if user_id not in self.interaction_history:
            self.interaction_history[user_id] = []
        
        self.interaction_history[user_id].append({
            "timestamp": datetime.now(),
            "type": interaction["type"],
            "sentiment": interaction.get("sentiment"),
            "engagement_score": interaction.get("engagement_score")
        })

    def _calculate_response_delay(self, tier: UserTier) -> int:
        """Calculate appropriate delay for response."""
        base_delay = self.cooldowns[tier]
        jitter = random.uniform(-0.2, 0.2)  # ±20% randomness
        return int(base_delay * (1 + jitter))