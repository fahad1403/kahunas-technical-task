import httpx
import pandas as pd
from datetime import datetime
import time
import os
from typing import Dict, List
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FitnessDataClient:
    def __init__(self, base_url: str = "http://127.0.0.1:8000"):
        self.base_url = base_url
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
        os.makedirs(self.data_dir, exist_ok=True)
        
        # Initialize data files if they don't exist
        self.fitness_data_file = os.path.join(self.data_dir, "fitness_data.csv")
        self.stats_file = os.path.join(self.data_dir, "user_stats.csv")
        self._initialize_files()

    def _initialize_files(self):
        """Initialize CSV files with headers if they don't exist."""
        if not os.path.exists(self.fitness_data_file):
            pd.DataFrame(columns=[
                'user_id', 'timestamp', 'steps', 'heart_rate'
            ]).to_csv(self.fitness_data_file, index=False)
        
        if not os.path.exists(self.stats_file):
            pd.DataFrame(columns=[
                'user_id', 'total_steps', 'average_heart_rate', 'active_minutes'
            ]).to_csv(self.stats_file, index=False)

    async def fetch_fitness_data(self, user_id: str) -> Dict:
        """Fetch real-time fitness data for a user."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/v1/fitness/data/{user_id}"
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Error fetching fitness data: {e}")
                return None

    async def fetch_user_stats(self, user_id: str) -> Dict:
        """Fetch aggregated stats for a user."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(
                    f"{self.base_url}/api/v1/fitness/stats/{user_id}"
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                logger.error(f"Error fetching user stats: {e}")
                return None

    def store_fitness_data(self, data: Dict):
        """Store fitness data in CSV format."""
        try:
            df = pd.DataFrame([data])
            df.to_csv(self.fitness_data_file, mode='a', header=False, index=False)
            logger.info(f"Stored fitness data for user {data['user_id']}")
        except Exception as e:
            logger.error(f"Error storing fitness data: {e}")

    def store_user_stats(self, stats: Dict):
        """Store user stats in CSV format."""
        try:
            df = pd.DataFrame([stats])
            df.to_csv(self.stats_file, mode='a', header=False, index=False)
            logger.info(f"Stored stats for user {stats['user_id']}")
        except Exception as e:
            logger.error(f"Error storing user stats: {e}")

async def main():
    client = FitnessDataClient()
    test_users = ["user1", "user2", "user3"]
    
    while True:
        for user_id in test_users:
            # Fetch and store fitness data
            data = await client.fetch_fitness_data(user_id)
            if data:
                client.store_fitness_data(data)
            
            # Fetch and store user stats
            stats = await client.fetch_user_stats(user_id)
            if stats:
                client.store_user_stats(stats)
        
        # Wait for 5 seconds before next fetch
        time.sleep(5)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 