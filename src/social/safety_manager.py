import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class SafetyManager:
    def __init__(self):
        logging.basicConfig(
            filename='gonzo_x.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
        self.post_history = []
        self.max_posts_per_hour = 5
        self.max_posts_per_day = 20
        self.emergency_shutdown = False
        
        self.daily_stats = {
            'posts': 0,
            'threads': 0,
            'replies': 0,
            'api_errors': 0,
            'rate_limits_hit': 0
        }
    
    def check_rate_limit(self) -> bool:
        """Check if we're within API rate limits"""
        now = datetime.now()
        self.post_history = [ts for ts in self.post_history 
                           if now - ts < timedelta(days=1)]
        
        hour_ago = now - timedelta(hours=1)
        posts_last_hour = sum(1 for ts in self.post_history 
                            if ts > hour_ago)
        posts_today = len(self.post_history)
        
        within_limits = (posts_last_hour < self.max_posts_per_hour and
                        posts_today < self.max_posts_per_day)
        
        if not within_limits:
            logging.warning(f'Rate limit exceeded: {posts_last_hour}/hr, {posts_today}/day')
            self.daily_stats['rate_limits_hit'] += 1
        
        return within_limits
    
    def record_post(self, post_type: str = 'post'):
        self.post_history.append(datetime.now())
        self.daily_stats['posts'] += 1
        
        if post_type == 'thread':
            self.daily_stats['threads'] += 1
        elif post_type == 'reply':
            self.daily_stats['replies'] += 1
    
    def log_api_error(self, error_type: str, details: str):
        logging.error(f'API ERROR - {error_type}: {details}')
        self.daily_stats['api_errors'] += 1
        
        if error_type in ['AUTHENTICATION_FAILED', 'RATE_LIMIT_EXCEEDED', 'API_UNAVAILABLE']:
            self.trigger_emergency_shutdown()
    
    def trigger_emergency_shutdown(self):
        self.emergency_shutdown = True
        logging.critical('EMERGENCY SHUTDOWN ACTIVATED: Technical issue detected')
    
    def resume_operations(self):
        if self.emergency_shutdown:
            self.emergency_shutdown = False
            logging.info('Technical issues resolved - Operations resumed')
    
    def get_technical_stats(self) -> Dict:
        return self.daily_stats.copy()
    
    def is_operational(self) -> bool:
        return not self.emergency_shutdown