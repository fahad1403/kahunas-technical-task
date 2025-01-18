import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import os

class HealthDataGenerator:
    def __init__(self, num_users=100, days=30):
        self.num_users = num_users
        self.days = days
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        os.makedirs(self.data_dir, exist_ok=True)

    def generate_user_data(self):
        data = []
        start_date = datetime.now() - timedelta(days=self.days)

        for user_id in range(1, self.num_users + 1):
            # Generate base characteristics for each user
            base_steps = np.random.normal(8000, 2000)  # Mean 8000 steps, SD 2000
            base_heart_rate = np.random.normal(70, 5)  # Mean 70 bpm, SD 5
            base_sleep_hours = np.random.normal(7.5, 1)  # Mean 7.5 hours, SD 1

            for day in range(self.days):
                current_date = start_date + timedelta(days=day)
                
                # Add random daily variation
                daily_steps = max(0, int(np.random.normal(base_steps, 1000)))
                heart_rate = max(50, min(100, int(np.random.normal(base_heart_rate, 3))))
                sleep_hours = max(4, min(10, np.random.normal(base_sleep_hours, 0.5)))
                sleep_quality = min(100, max(0, int(np.random.normal(70 + (sleep_hours - 7) * 10, 10))))
                
                # Calculate performance score based on other metrics
                performance_score = min(100, max(0, int(
                    0.3 * (daily_steps / 10000 * 100) +
                    0.3 * (100 - (heart_rate - 60) * 2) +
                    0.4 * sleep_quality
                )))

                data.append({
                    'user_id': user_id,
                    'date': current_date.strftime('%Y-%m-%d'),
                    'steps': daily_steps,
                    'heart_rate': heart_rate,
                    'sleep_hours': round(sleep_hours, 2),
                    'sleep_quality': sleep_quality,
                    'performance_score': performance_score
                })

        return pd.DataFrame(data)

    def save_data(self, df):
        output_file = os.path.join(self.data_dir, 'health_data.csv')
        df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")

def main():
    generator = HealthDataGenerator()
    data = generator.generate_user_data()
    generator.save_data(data)

if __name__ == "__main__":
    main() 