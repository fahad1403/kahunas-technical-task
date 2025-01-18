import os
from dotenv import load_dotenv
from dataclasses import dataclass

# Load environment variables
load_dotenv()

@dataclass
class PostgresConfig:
    host: str = os.getenv("DB_HOST", "localhost")
    user: str = os.getenv("DB_USER", "postgres")
    password: str = os.getenv("DB_PWD", "")
    database: str = os.getenv("DB_NAME", "fitness_db")
    port: int = int(os.getenv("DB_PORT", "5432"))

@dataclass
class OpenAIConfig:
    api_key: str = os.getenv("OPENAI_API_KEY")
    model_name: str = os.getenv("MODEL_NAME", "gpt-4o-mini")
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))

@dataclass
class AppConfig:
    debug: bool = os.getenv("DEBUG", "False").lower() == "true"
    vector_store_path: str = os.getenv("VECTOR_STORE_PATH", "./data/vector_store")

# Create config instances
postgres_config = PostgresConfig()
openai_config = OpenAIConfig()
app_config = AppConfig() 