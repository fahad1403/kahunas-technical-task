import pytest
import asyncio
import time
import httpx
import statistics
from concurrent.futures import ThreadPoolExecutor
import sys
import os

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

BASE_URL = "http://127.0.0.1:8000"
NUM_REQUESTS = 100
NUM_CONCURRENT = 10

async def make_request(client: httpx.AsyncClient, endpoint: str) -> float:
    """Make a request and return the response time in seconds."""
    start_time = time.time()
    await client.get(f"{BASE_URL}{endpoint}")
    return time.time() - start_time

async def stress_test_endpoint(endpoint: str, num_requests: int, concurrent_requests: int):
    """Run stress test on an endpoint."""
    async with httpx.AsyncClient() as client:
        tasks = []
        for _ in range(num_requests):
            tasks.append(make_request(client, endpoint))
            
            if len(tasks) >= concurrent_requests:
                # Wait for the batch to complete
                response_times = await asyncio.gather(*tasks)
                tasks = []
                
        # Handle any remaining tasks
        if tasks:
            response_times = await asyncio.gather(*tasks)
            
    return response_times

def calculate_stats(response_times):
    """Calculate statistics from response times."""
    return {
        "min": min(response_times),
        "max": max(response_times),
        "mean": statistics.mean(response_times),
        "median": statistics.median(response_times),
        "p95": statistics.quantiles(response_times, n=20)[-1],  # 95th percentile
        "requests_per_second": len(response_times) / sum(response_times)
    }

@pytest.mark.asyncio
async def test_stress_health_endpoint():
    """Stress test the health check endpoint."""
    print("\nStress testing health endpoint...")
    response_times = await stress_test_endpoint(
        "/health",
        NUM_REQUESTS,
        NUM_CONCURRENT
    )
    stats = calculate_stats(response_times)
    
    print(f"Results for {NUM_REQUESTS} requests ({NUM_CONCURRENT} concurrent):")
    print(f"Min response time: {stats['min']:.3f}s")
    print(f"Max response time: {stats['max']:.3f}s")
    print(f"Mean response time: {stats['mean']:.3f}s")
    print(f"Median response time: {stats['median']:.3f}s")
    print(f"95th percentile: {stats['p95']:.3f}s")
    print(f"Requests per second: {stats['requests_per_second']:.2f}")
    
    # Assert reasonable performance
    assert stats["p95"] < 1.0, "95th percentile response time too high"
    assert stats["requests_per_second"] > 10, "Throughput too low"

@pytest.mark.asyncio
async def test_stress_fitness_data_endpoint():
    """Stress test the fitness data endpoint."""
    print("\nStress testing fitness data endpoint...")
    response_times = await stress_test_endpoint(
        "/api/v1/fitness/data/stress_test_user",
        NUM_REQUESTS,
        NUM_CONCURRENT
    )
    stats = calculate_stats(response_times)
    
    print(f"Results for {NUM_REQUESTS} requests ({NUM_CONCURRENT} concurrent):")
    print(f"Min response time: {stats['min']:.3f}s")
    print(f"Max response time: {stats['max']:.3f}s")
    print(f"Mean response time: {stats['mean']:.3f}s")
    print(f"Median response time: {stats['median']:.3f}s")
    print(f"95th percentile: {stats['p95']:.3f}s")
    print(f"Requests per second: {stats['requests_per_second']:.2f}")
    
    # Assert reasonable performance
    assert stats["p95"] < 1.0, "95th percentile response time too high"
    assert stats["requests_per_second"] > 5, "Throughput too low"

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 