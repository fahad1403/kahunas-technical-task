# Health Data Insights

This project analyzes simulated health data for 100 users and provides actionable insights about their health patterns and correlations between different health metrics. Following the restriction of not using third-party analytics libraries, all calculations and visualizations are implemented from scratch.

## Project Structure

```
health-data-insights/
├── data/                  # Directory for generated data
│   └── health_data.csv    # Generated health data for 100 users
├── src/                   # Source code
│   ├── data_generator.py  # Script to generate synthetic health data
│   └── analyzer.py        # Analysis and insights generation
└── requirements.txt      # Project dependencies
```

## Features

- Generates synthetic health data for 100 users including:
  - Daily step count
  - Heart rate (resting)
  - Sleep quality (hours and quality score)
  - Physical performance score
- Analyzes correlations between different health metrics
- Provides personalized insights based on user data
- Generates text-based visualizations and reports for 5 sample users

## How to Run

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Generate synthetic data:
```bash
python src/data_generator.py
```

3. Run analysis and generate insights:
```bash
python src/analyzer.py
```

## Sample Output

The analysis generates a detailed report for 10 users, including:

### Text Insights
```
User 1 Analysis
--------------------------------------------------
Key Insights:
- Strong positive correlation between sleep quality and performance.
- Excellent daily step count, maintaining above 10000 steps!

Average Metrics:
avg_steps: 10234.5
avg_heart_rate: 68.3
avg_sleep_hours: 7.8
avg_sleep_quality: 82.4
avg_performance: 85.6

Correlations:
sleep_quality_vs_performance: 0.72
steps_vs_performance: 0.65
heart_rate_vs_performance: -0.23

Weekly Performance Trend:
85.6 | ████████████████████
87.2 | ██████████████████████
82.4 | ███████████████
86.8 | █████████████████████
84.5 | ███████████████████
```

## Implementation Details

- Data Generation: Uses statistical distributions to create realistic health data
- Analysis: 
  - Custom correlation calculations (implemented from scratch)
  - Weekly trend analysis using basic statistics
  - Performance scoring based on multiple metrics
- Visualizations:
  - ASCII-based charts for trends
  - Text-based reporting format
  - Simple and clean output design

## Restrictions Followed

- No third-party analytics libraries used
- All statistical calculations implemented from scratch
- Pure Python implementation for data analysis
- Basic data storage using pandas only 