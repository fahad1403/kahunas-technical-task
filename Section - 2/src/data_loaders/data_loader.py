from typing import List, Dict, Any
import pandas as pd
import os
import logging
from PyPDF2 import PdfReader
import psycopg2
from psycopg2.extras import DictCursor
from config.config import postgres_config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DataLoader:
    KAHUNAS_DATA_PATH = "/Users/fahadpatel/Documents/kahunas-assignment/Section - 1/data"
    
    @staticmethod
    def load_csv(file_path: str) -> pd.DataFrame:
        """Load data from a CSV file."""
        logger.info(f"Loading CSV file: {file_path}")
        try:
            df = pd.read_csv(file_path)
            logger.info(f"Successfully loaded CSV with {len(df)} rows")
            return df
        except Exception as e:
            logger.error(f"Error loading CSV file {file_path}: {e}")
            return pd.DataFrame()

    @staticmethod
    def load_kahunas_data() -> Dict[str, pd.DataFrame]:
        """Load Kahunas CSV data files."""
        logger.info("Loading Kahunas data files...")
        data_dict = {}
        try:
            # Load users data
            users_path = os.path.join(DataLoader.KAHUNAS_DATA_PATH, "users.csv")
            if os.path.exists(users_path):
                logger.info("Loading users data...")
                data_dict['users'] = pd.read_csv(users_path)
                logger.info(f"Loaded {len(data_dict['users'])} user records")
            
            # Load workouts data
            workouts_path = os.path.join(DataLoader.KAHUNAS_DATA_PATH, "workouts.csv")
            if os.path.exists(workouts_path):
                logger.info("Loading workouts data...")
                data_dict['workouts'] = pd.read_csv(workouts_path)
                logger.info(f"Loaded {len(data_dict['workouts'])} workout records")
            
            # Load interactions data
            interactions_path = os.path.join(DataLoader.KAHUNAS_DATA_PATH, "interactions.csv")
            if os.path.exists(interactions_path):
                logger.info("Loading interactions data...")
                data_dict['interactions'] = pd.read_csv(interactions_path)
                logger.info(f"Loaded {len(data_dict['interactions'])} interaction records")
            
            logger.info("Successfully loaded all Kahunas data files")
            return data_dict
        except Exception as e:
            logger.error(f"Error loading Kahunas data: {e}")
            return {}

    @staticmethod
    def load_pdf(file_path: str) -> str:
        """Extract text from a PDF file."""
        logger.info(f"Loading PDF file: {file_path}")
        try:
            reader = PdfReader(file_path)
            text = ""
            for i, page in enumerate(reader.pages):
                logger.info(f"Processing page {i+1} of PDF")
                text += page.extract_text() + "\n"
            logger.info("Successfully extracted text from PDF")
            return text
        except Exception as e:
            logger.error(f"Error loading PDF file {file_path}: {e}")
            return ""

    @staticmethod
    def load_postgres_data(query: str) -> List[Dict[str, Any]]:
        """Load data from PostgreSQL database."""
        logger.info(f"Executing PostgreSQL query: {query}")
        try:
            connection = psycopg2.connect(
                host=postgres_config.host,
                user=postgres_config.user,
                password=postgres_config.password,
                port=postgres_config.port,
                dbname=postgres_config.database
            )
            logger.info("Successfully connected to PostgreSQL")
            
            cursor = connection.cursor(cursor_factory=DictCursor)
            cursor.execute(query)
            results = cursor.fetchall()
            logger.info(f"Query returned {len(results)} results")
            
            cursor.close()
            connection.close()
            logger.info("Database connection closed")
            
            return [dict(row) for row in results]
        except psycopg2.Error as e:
            logger.error(f"Error querying PostgreSQL: {e}")
            return []

    @staticmethod
    def create_sample_data():
        """Create sample data files for demonstration."""
        logger.info("Creating sample data files...")
        # Load Kahunas data first
        kahunas_data = DataLoader.load_kahunas_data()
        
        # Create sample CSV if Kahunas data not available
        if not kahunas_data:
            logger.info("No Kahunas data found, creating sample CSV...")
            sample_data = {
                'date': ['2024-01-01', '2024-01-02', '2024-01-03'],
                'exercise': ['Running', 'Weight Training', 'Yoga'],
                'duration': [30, 45, 60],
                'calories_burned': [300, 200, 150]
            }
            df = pd.DataFrame(sample_data)
            
            # Create data directory if it doesn't exist
            os.makedirs('./data', exist_ok=True)
            df.to_csv('./data/sample_data.csv', index=False)
            logger.info("Sample CSV created successfully")

        # Create sample PDF content
        logger.info("Creating sample PDF content...")
        pdf_content = """
        Kahunas Fitness Training Guide

        1. Cardiovascular Exercise
        - Running: 30 minutes, 3 times per week
        - Swimming: 45 minutes, 2 times per week
        - Cycling: 40 minutes, 2 times per week

        2. Strength Training
        - Upper body: 3 sets of 12 reps
        - Lower body: 3 sets of 15 reps
        - Core exercises: 3 sets of 20 reps

        3. Flexibility
        - Daily stretching routine
        - Yoga sessions twice per week
        """
        
        # Save sample PDF content
        os.makedirs('./data/documents', exist_ok=True)
        with open('./data/documents/training_guide.txt', 'w') as f:
            f.write(pdf_content)
        logger.info("Sample training guide created successfully")

    @staticmethod
    def create_postgres_schema():
        """Create PostgreSQL schema and sample data."""
        logger.info("Setting up PostgreSQL schema...")
        try:
            logger.info("Connecting to default PostgreSQL database...")
            connection = psycopg2.connect(
                host=postgres_config.host,
                user=postgres_config.user,
                password=postgres_config.password,
                port=postgres_config.port,
                dbname="postgres"  # Connect to default db first
            )
            connection.autocommit = True  # Enable autocommit for database creation
            cursor = connection.cursor()
            
            # Create database if it doesn't exist
            logger.info(f"Checking if database '{postgres_config.database}' exists...")
            cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = %s", (postgres_config.database,))
            if not cursor.fetchone():
                logger.info(f"Creating database '{postgres_config.database}'...")
                cursor.execute(f"CREATE DATABASE {postgres_config.database}")
            
            # Close connection to default db
            cursor.close()
            connection.close()
            logger.info("Closed connection to default database")
            
            # Connect to our database
            logger.info(f"Connecting to '{postgres_config.database}' database...")
            connection = psycopg2.connect(
                host=postgres_config.host,
                user=postgres_config.user,
                password=postgres_config.password,
                port=postgres_config.port,
                dbname=postgres_config.database
            )
            cursor = connection.cursor()
            
            # Create fitness_metrics table
            logger.info("Creating fitness_metrics table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS fitness_metrics (
                    id SERIAL PRIMARY KEY,
                    date DATE,
                    exercise_type VARCHAR(50),
                    duration_minutes INTEGER,
                    calories_burned INTEGER,
                    heart_rate_avg INTEGER
                )
            """)
            
            # Create user_workouts table
            logger.info("Creating user_workouts table...")
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_workouts (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    workout_date DATE NOT NULL,
                    workout_type VARCHAR(50),
                    duration_minutes INTEGER,
                    calories_burned INTEGER,
                    heart_rate_avg INTEGER,
                    completion_status VARCHAR(20),
                    notes TEXT
                )
            """)
            
            # Insert sample fitness metrics data
            sample_metrics = [
                ('2024-01-01', 'Running', 30, 300, 145),
                ('2024-01-02', 'Weight Training', 45, 200, 130),
                ('2024-01-03', 'Yoga', 60, 150, 110)
            ]
            
            logger.info("Clearing existing data from fitness_metrics...")
            cursor.execute("TRUNCATE fitness_metrics RESTART IDENTITY")
            
            logger.info("Inserting sample data into fitness_metrics...")
            cursor.executemany("""
                INSERT INTO fitness_metrics 
                (date, exercise_type, duration_minutes, calories_burned, heart_rate_avg)
                VALUES (%s, %s, %s, %s, %s)
            """, sample_metrics)
            
            # Insert sample user workout data
            sample_workouts = [
                (26, '2024-01-15', 'Running', 45, 450, 155, 'Completed', 'Great cardio session'),
                (26, '2024-01-16', 'Weight Training', 60, 320, 135, 'Completed', 'Upper body focus'),
                (26, '2024-01-17', 'HIIT', 30, 380, 165, 'Completed', 'Intense workout'),
                (26, '2024-01-18', 'Yoga', 45, 180, 110, 'Completed', 'Recovery session')
            ]
            
            logger.info("Clearing existing data from user_workouts...")
            cursor.execute("TRUNCATE user_workouts RESTART IDENTITY")
            
            logger.info("Inserting sample data into user_workouts...")
            cursor.executemany("""
                INSERT INTO user_workouts 
                (user_id, workout_date, workout_type, duration_minutes, calories_burned, heart_rate_avg, completion_status, notes)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, sample_workouts)
            
            connection.commit()
            cursor.close()
            connection.close()
            logger.info("PostgreSQL schema setup completed successfully")
            
        except psycopg2.Error as e:
            logger.error(f"Error setting up PostgreSQL schema: {e}")

def initialize_data():
    """Initialize all sample data sources."""
    logger.info("Starting data initialization...")
    data_loader = DataLoader()
    data_loader.create_sample_data()
    data_loader.create_postgres_schema()
    logger.info("Data initialization completed") 