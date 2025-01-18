import pandas as pd
import os
from typing import List, Tuple, Dict
from datetime import datetime

class HealthDataAnalyzer:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        self.output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
        os.makedirs(self.output_dir, exist_ok=True)

    def load_data(self) -> pd.DataFrame:
        return pd.read_csv(os.path.join(self.data_dir, 'health_data.csv'))

    def custom_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient without using libraries."""
        n = len(x)
        if n != len(y) or n == 0:
            return 0.0

        # Calculate means
        mean_x = sum(x) / n
        mean_y = sum(y) / n

        # Calculate covariance and standard deviations
        covariance = sum((x[i] - mean_x) * (y[i] - mean_y) for i in range(n))
        std_x = (sum((val - mean_x) ** 2 for val in x)) ** 0.5
        std_y = (sum((val - mean_y) ** 2 for val in y)) ** 0.5

        if std_x == 0 or std_y == 0:
            return 0.0

        return covariance / (std_x * std_y)

    def create_ascii_chart(self, values: List[float], width: int = 50) -> str:
        """Create a simple ASCII bar chart."""
        if not values:
            return ""
        
        max_val = max(values)
        min_val = min(values)
        range_val = max_val - min_val if max_val != min_val else 1
        
        chart = []
        for val in values:
            bar_length = int((val - min_val) / range_val * width)
            chart.append(f"{val:8.1f} | {'█' * bar_length}")
        
        return "\n".join(chart)

    def analyze_user_trends(self, df: pd.DataFrame, user_id: int) -> Dict:
        user_data = df[df['user_id'] == user_id]
        
        # Calculate correlations
        correlations = {
            'sleep_quality_vs_performance': self.custom_correlation(
                user_data['sleep_quality'].tolist(),
                user_data['performance_score'].tolist()
            ),
            'steps_vs_performance': self.custom_correlation(
                user_data['steps'].tolist(),
                user_data['performance_score'].tolist()
            ),
            'heart_rate_vs_performance': self.custom_correlation(
                user_data['heart_rate'].tolist(),
                user_data['performance_score'].tolist()
            )
        }

        # Calculate averages
        averages = {
            'avg_steps': user_data['steps'].mean(),
            'avg_heart_rate': user_data['heart_rate'].mean(),
            'avg_sleep_hours': user_data['sleep_hours'].mean(),
            'avg_sleep_quality': user_data['sleep_quality'].mean(),
            'avg_performance': user_data['performance_score'].mean()
        }

        # Calculate weekly averages for trend visualization
        weekly_stats = user_data.set_index('date').resample('W').mean()
        weekly_trends = {
            'steps': weekly_stats['steps'].tolist(),
            'sleep_quality': weekly_stats['sleep_quality'].tolist(),
            'performance': weekly_stats['performance_score'].tolist()
        }

        return {
            'correlations': correlations,
            'averages': averages,
            'weekly_trends': weekly_trends
        }

    def generate_insights(self, analysis: Dict) -> List[str]:
        insights = []
        
        # Sleep quality insights
        if analysis['correlations']['sleep_quality_vs_performance'] > 0.5:
            insights.append("Strong positive correlation between sleep quality and performance.")
        
        # Steps insights
        avg_steps = analysis['averages']['avg_steps']
        if avg_steps < 7000:
            insights.append("Daily step count is below recommended level (7000 steps).")
        elif avg_steps > 10000:
            insights.append("Excellent daily step count, maintaining above 10000 steps!")

        # Sleep hours insights
        avg_sleep = analysis['averages']['avg_sleep_hours']
        if avg_sleep < 7:
            insights.append("Average sleep duration is below recommended 7-9 hours.")
        
        return insights

    def save_insights(self, insights: Dict, num_users: int = 5):
        """Save insights for the specified number of users."""
        output_file = os.path.join(self.output_dir, 'health_insights.txt')
        with open(output_file, 'w') as f:
            f.write("Health Data Analysis Report\n")
            f.write("=" * 50 + "\n\n")
            
            for user_id in list(insights.keys())[:num_users]:  # Only process first 5 users
                user_insights = insights[user_id]
                f.write(f"\nUser {user_id} Analysis\n")
                f.write("-" * 50 + "\n")
                
                # Write insights
                f.write("\nKey Insights:\n")
                for insight in user_insights['insights']:
                    f.write(f"- {insight}\n")
                
                # Write averages
                f.write("\nAverage Metrics:\n")
                for metric, value in user_insights['analysis']['averages'].items():
                    f.write(f"{metric}: {value:.1f}\n")
                
                # Write correlations
                f.write("\nCorrelations:\n")
                for metric, value in user_insights['analysis']['correlations'].items():
                    f.write(f"{metric}: {value:.2f}\n")
                
                # Add simple ASCII visualization of weekly trends
                f.write("\nWeekly Performance Trend (ASCII Chart):\n")
                weekly_perf = user_insights['analysis']['weekly_trends']['performance']
                f.write(self.create_ascii_chart(weekly_perf))
                f.write("\n" + "-" * 50 + "\n")

    def analyze_all_users(self, df: pd.DataFrame):
        unique_users = df['user_id'].unique()
        all_insights = {}

        for user_id in unique_users:
            analysis = self.analyze_user_trends(df, user_id)
            insights = self.generate_insights(analysis)
            all_insights[user_id] = {
                'analysis': analysis,
                'insights': insights
            }

        return all_insights

def main():
    analyzer = HealthDataAnalyzer()
    df = analyzer.load_data()
    
    # Convert date column to datetime
    df['date'] = pd.to_datetime(df['date'])
    
    # Generate insights for all users but save only 10 to avoid large file size
    insights = analyzer.analyze_all_users(df)
    analyzer.save_insights(insights, num_users=10)
    
    print("Analysis complete. Check the output directory for results.")

if __name__ == "__main__":
    main() 