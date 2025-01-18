# Fitness Data API System

This project implements a simulated fitness data API system with real-time data generation and a client for data collection.

## Components

1. **Simulated API Server**: FastAPI-based server that generates synthetic fitness data (steps and heart rate)
2. **Data Collection Client**: Python script to fetch and store data from the API
3. **Tests**: Unit tests and stress tests for the system

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the API server:
```bash
python src/api_server.py
```

You should see output similar to this:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [66095] using StatReload
INFO:     Started server process [66102]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Once the server is running, you can access:
- API Documentation: http://localhost:8000/docs
- Alternative API Documentation: http://localhost:8000/redoc

## FastAPI Interactive Documentation

The API comes with interactive documentation powered by Swagger UI. Here's what we can see when visit to http://localhost:8000/docs:

![FastAPI Docs](https://i.imgur.com/YVEWBtb.png)

What is possible:
- Explore available endpoints
- Test API calls directly from the browser
- View request/response schemas
- See example responses

2. In a separate terminal, run the data collection client:
```bash
python src/data_client.py
```

The client will start collecting data for test users and you'll see logs similar to this:
```
2025-01-18 02:13:27,966 - INFO - HTTP Request: GET http://127.0.0.1:8000/api/v1/fitness/data/user1 "HTTP/1.1 200 OK"
2025-01-18 02:13:27,967 - INFO - Stored fitness data for user user1
2025-01-18 02:13:27,978 - INFO - HTTP Request: GET http://127.0.0.1:8000/api/v1/fitness/stats/user1 "HTTP/1.1 200 OK"
2025-01-18 02:13:27,979 - INFO - Stored stats for user user1
2025-01-18 02:13:28,094 - INFO - HTTP Request: GET http://127.0.0.1:8000/api/v1/fitness/data/user2 "HTTP/1.1 200 OK"
2025-01-18 02:13:28,096 - INFO - Stored fitness data for user user2
```

The client will continuously:
- Fetch real-time fitness data for each test user
- Store the data in CSV files
- Collect user statistics
- Wait for 5 seconds before the next data collection cycle

## Testing

Run unit tests:
```bash
pytest tests/test_api.py
```

Run stress tests:
```bash
pytest tests/test_stress.py
```

## API Endpoints

- `GET /health`: Health check endpoint
- `GET /api/v1/fitness/data/{user_id}`: Get real-time fitness data for a user
- `GET /api/v1/fitness/stats/{user_id}`: Get aggregated fitness stats for a user

## Data Storage

The collected data is stored in CSV format in the `data` directory with the following structure:
- `fitness_data.csv`: Raw fitness data with timestamps
- `user_stats.csv`: Aggregated user statistics 