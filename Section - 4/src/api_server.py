from fastapi import FastAPI, HTTPException
from datetime import datetime
import random
import uvicorn
from typing import Dict
from pydantic import BaseModel
import time

app = FastAPI(title="Fitness Data API")

# In-memory store for demo purposes
user_data_store: Dict[str, Dict] = {}

class FitnessData(BaseModel):
    user_id: str
    timestamp: str
    steps: int
    heart_rate: int

def generate_fitness_data(user_id: str) -> FitnessData:
    """Generate synthetic fitness data for a user."""
    current_time = datetime.now().isoformat()
    
    # Generate realistic-looking data
    steps = random.randint(0, 500)  # Steps in last interval
    heart_rate = random.randint(60, 150)  # Normal heart rate range
    
    return FitnessData(
        user_id=user_id,
        timestamp=current_time,
        steps=steps,
        heart_rate=heart_rate
    )

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.get("/api/v1/fitness/data/{user_id}")
async def get_fitness_data(user_id: str):
    """Get real-time fitness data for a user."""
    # Simulate processing time
    time.sleep(0.1)
    
    if not user_id.strip():
        raise HTTPException(status_code=400, detail="Invalid user ID")
    
    # Generate and store new data
    data = generate_fitness_data(user_id)
    user_data_store[user_id] = data.dict()
    
    return data

@app.get("/api/v1/fitness/stats/{user_id}")
async def get_user_stats(user_id: str):
    """Get aggregated fitness stats for a user."""
    if user_id not in user_data_store:
        raise HTTPException(status_code=404, detail="User not found")
    
    # In a real implementation, this would aggregate from a database
    return {
        "user_id": user_id,
        "total_steps": random.randint(5000, 15000),
        "average_heart_rate": random.randint(70, 90),
        "active_minutes": random.randint(30, 180)
    }

if __name__ == "__main__":
    uvicorn.run("api_server:app", host="127.0.0.1", port=8000, reload=True) 