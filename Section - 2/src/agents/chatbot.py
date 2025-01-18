from typing import List, Dict, Any
from langchain_openai import ChatOpenAI
from langchain.chains.conversational_retrieval.base import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import psycopg2
from psycopg2.extras import DictCursor
from config.config import postgres_config, openai_config, app_config
import os
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class FitnessChatbot:
    def __init__(self):
        """Initialize the Fitness Chatbot with necessary components."""
        logger.info("Initializing Fitness Chatbot...")
        self.default_user_id = 26
        self.default_user_name = "Fahad"
        
        # Database schema for SQL generation
        self.schema = """
        Table: user_workouts
        Columns:
        - id (serial): Primary key
        - user_id (integer): User identifier
        - workout_date (date): Date of workout
        - workout_type (varchar): Type of workout
        - duration_minutes (integer): Duration in minutes
        - calories_burned (integer): Calories burned
        - heart_rate_avg (integer): Average heart rate
        - completion_status (varchar): Status of workout
        - notes (text): Additional notes

        Table: fitness_metrics
        Columns:
        - id (serial): Primary key
        - date (date): Date of metrics
        - exercise_type (varchar): Type of exercise
        - duration_minutes (integer): Duration in minutes
        - calories_burned (integer): Calories burned
        - heart_rate_avg (integer): Average heart rate
        """
        
        # Initialize OpenAI components
        logger.info("Setting up OpenAI components...")
        self.llm = ChatOpenAI(
            temperature=openai_config.temperature,
            model_name=openai_config.model_name
        )
        self.embeddings = OpenAIEmbeddings()
        self.vector_store = self._initialize_vector_store()
        self.memory = ConversationBufferMemory(
            memory_key="chat_history",
            output_key="answer",
            return_messages=True
        )
        self.qa_chain = self._create_qa_chain()
        self.postgres_connection = self._setup_postgres_connection()

    def _initialize_vector_store(self) -> FAISS:
        """Initialize or load the vector store with document embeddings."""
        logger.info("Initializing vector store...")
        if os.path.exists(app_config.vector_store_path):
            try:
                logger.info("Loading existing vector store from disk...")
                return FAISS.load_local(
                    app_config.vector_store_path,
                    self.embeddings,
                    allow_dangerous_deserialization=True
                )
            except Exception as e:
                logger.warning(f"Error loading existing vector store: {e}. Creating new one...")
                if os.path.exists(app_config.vector_store_path):
                    os.remove(app_config.vector_store_path)
        
        # Create default document if no vector store exists
        default_text = """
        Welcome to Kahunas Fitness! Here's some general fitness information:
        
        1. Workout Types and Benefits:
        - Cardio: Improves heart health, burns calories, increases endurance
        - Strength Training: Builds muscle, boosts metabolism, improves bone density
        - HIIT: Efficient calorie burning, improves cardiovascular fitness
        - Yoga: Enhances flexibility, reduces stress, improves balance
        
        2. Exercise Guidelines:
        - Warm up properly before exercising
        - Stay hydrated during workouts
        - Listen to your body and avoid overtraining
        - Mix different types of exercises for balanced fitness
        
        3. Nutrition Tips:
        - Eat balanced meals with protein, carbs, and healthy fats
        - Stay hydrated throughout the day
        - Time your meals around workouts
        - Consider post-workout nutrition for recovery
        
        4. Recovery and Rest:
        - Get adequate sleep for muscle recovery
        - Take rest days between intense workouts
        - Use proper form to prevent injuries
        - Stretch regularly for flexibility
        """
        
        documents = [Document(page_content=default_text, metadata={"source": "fitness_guide"})]
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_documents(documents)
        
        # Create and save vector store
        logger.info("Creating new vector store...")
        vector_store = FAISS.from_documents(texts, self.embeddings)
        os.makedirs(os.path.dirname(app_config.vector_store_path), exist_ok=True)
        vector_store.save_local(app_config.vector_store_path)
        logger.info("Vector store saved successfully")
        return vector_store

    def _setup_postgres_connection(self):
        """Set up PostgreSQL database connection."""
        logger.info("Setting up PostgreSQL connection...")
        try:
            conn = psycopg2.connect(
                host=postgres_config.host,
                user=postgres_config.user,
                password=postgres_config.password,
                dbname=postgres_config.database,
                port=postgres_config.port
            )
            logger.info("Successfully connected to PostgreSQL database")
            return conn
        except psycopg2.Error as err:
            logger.error(f"Error connecting to PostgreSQL: {err}")
            return None

    def _query_postgres(self, query: str, params: tuple = None) -> List[Dict]:
        """Query PostgreSQL database for relevant information."""
        logger.info(f"Executing PostgreSQL query: {query}")
        if not self.postgres_connection:
            logger.info("Reconnecting to PostgreSQL...")
            self.postgres_connection = self._setup_postgres_connection()
            
        if not self.postgres_connection:
            logger.error("No PostgreSQL connection available")
            return []
        
        try:
            cursor = self.postgres_connection.cursor(cursor_factory=DictCursor)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            logger.info(f"Query returned {len(results)} results")
            return [dict(row) for row in results]
        except psycopg2.Error as err:
            logger.error(f"Error querying PostgreSQL: {err}")
            return []

    def _create_qa_chain(self) -> ConversationalRetrievalChain:
        """Create the question-answering chain."""
        return ConversationalRetrievalChain.from_llm(
            llm=self.llm,
            retriever=self.vector_store.as_retriever(
                search_kwargs={"k": 3}
            ),
            memory=self.memory,
            return_source_documents=True,
            output_key="answer",
            return_generated_question=True
        )

    def _generate_sql_query(self, user_question: str) -> str:
        """Generate SQL query based on user's question."""
        prompt = f"""
        You are an expert SQL query generator. Given a natural language question, generate a PostgreSQL query to fetch the required data.
        
        Database Schema:
        {self.schema}
        
        Important Rules:
        1. Always use proper SQL syntax and best practices
        2. Include proper WHERE clauses to filter data
        3. Return only the SQL query, no explanations
        4. Always handle NULL values appropriately
        5. Use proper date formatting for date comparisons
        6. For workout-related queries, primarily use the user_workouts table
        7. For general fitness metrics, use the fitness_metrics table
        8. Always include user_id = {self.default_user_id} in WHERE clause when querying user_workouts
        9. For time-based queries, use appropriate date functions
        10. For aggregations, use appropriate GROUP BY clauses
        
        Return only the raw SQL query without any formatting or explanations.
        
        User Question: {user_question}
        
        SQL Query:"""

        try:
            logger.info("Generating SQL query...")
            response = self.llm.invoke(prompt)
            sql_query = response.content.strip()
            logger.info(f"Generated SQL query: {sql_query}")
            return sql_query
        except Exception as e:
            logger.error(f"Error generating SQL query: {e}")
            return ""

    def _should_use_vector_store(self, user_input: str) -> bool:
        """Determine if the question requires vector store lookup."""
        general_keywords = [
            "guide", "how to", "technique", "form", "explain",
            "what is", "I want to", "How do I", "benefits", "recommend", "advice", "tips",
            "best practices", "nutrition", "diet", "meal", "food"
        ]
        return any(keyword in user_input.lower() for keyword in general_keywords)

    def get_response(self, user_input: str) -> str:
        """Generate a response to the user's input."""
        try:
            logger.info(f"Processing user input: {user_input}")
            
            context_data = ""
            use_vector_store = self._should_use_vector_store(user_input)
            
            # For personal data queries, get data from database
            if not use_vector_store:
                sql_query = self._generate_sql_query(user_input)
                if sql_query:
                    results = self._query_postgres(sql_query)
                    if results:
                        context_data = "Your Fitness Data:\n" + str(results)

            # Prepare prompt for GPT-4
            prompt = f"""You are a knowledgeable and engaging fitness coach for Kahunas. 
            
                    User Question: {user_input}

                    {"Here is the relevant data from your workout history:" if context_data else ""}
                    {context_data}

                    Please provide a helpful, encouraging, and specific response. If workout data is available, analyze it and provide insights. 
                    Keep the tone conversational and friendly while maintaining professionalism. Note: You are talking to {self.default_user_name} (user_id: {self.default_user_id}). 
                    Keep your responses concise, do not give too wordy responses. Please do provide insights and suggestions of what data you've fetched if you have the data. If you have the data of user, don't assume that they've provided the data, rather frame it as that you've fetched the data and analyzed it or whatever makes sense based on the conversation and user input.
                """

            # Use vector store for general fitness knowledge
            if use_vector_store:
                logger.info("Using vector store for general fitness knowledge")
                docs = self.vector_store.similarity_search(user_input)
                if docs:
                    prompt += "\n\nAdditional fitness information:\n"
                    prompt += "\n".join(doc.page_content for doc in docs)

            # Generate response
            logger.info("Generating final response...")
            response = self.llm.invoke(prompt)
            return response.content.strip()

        except Exception as e:
            logger.error(f"Error generating response: {e}", exc_info=True)
            return "I apologize, but I encountered an error while processing your request. Please try again."

    def __del__(self):
        """Cleanup when the chatbot is destroyed."""
        logger.info("Cleaning up chatbot resources...")
        if hasattr(self, 'postgres_connection') and self.postgres_connection:
            self.postgres_connection.close()
            logger.info("PostgreSQL connection closed") 