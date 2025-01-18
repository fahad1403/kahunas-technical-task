# Kahunas Fitness Coach Chatbot

A sophisticated AI-powered fitness coach designed to provide personalized fitness advice and insights, powered by Kahunas - your trusted health and fitness partner.

## Features

- Multi-source data retrieval (MySQL, PDFs, CSVs)
- Natural language query processing for fitness-related questions
- Actionable insights generation
- GPT-powered conversational abilities
- Data source integration capabilities
- Access to Kahunas' comprehensive fitness database

## Tech Stack

- Python 3.9+
- LangChain
- OpenAI GPT
- PyPDF2 (PDF processing)
- pandas (CSV handling)
- MySQL Connector
- python-dotenv (environment management)
- streamlit (UI interface)

## Setup

1. Clone the repository
2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
- Copy `.env.example` to `.env`
- Add your OpenAI API key and MySQL credentials

5. Run the application:
```bash
streamlit run app.py
```

Expected output:
2025-01-18 03:29:41,049 - __main__ - INFO - Loading environment variables...
2025-01-18 03:29:41,050 - __main__ - INFO - Starting Kahunas Fitness Coach application...
2025-01-18 03:29:41,757 - __main__ - INFO - Initializing data sources...
2025-01-18 03:29:41,757 - src.data_loaders.data_loader - INFO - Starting data initialization...
2025-01-18 03:29:41,757 - src.data_loaders.data_loader - INFO - Creating sample data files...
2025-01-18 03:29:41,757 - src.data_loaders.data_loader - INFO - Loading Kahunas data files...
2025-01-18 03:29:41,757 - src.data_loaders.data_loader - INFO - Loading users data...
2025-01-18 03:29:41,761 - src.data_loaders.data_loader - INFO - Loaded 1000 user records
2025-01-18 03:29:41,761 - src.data_loaders.data_loader - INFO - Loading workouts data...
2025-01-18 03:29:41,762 - src.data_loaders.data_loader - INFO - Loaded 200 workout records
2025-01-18 03:29:41,762 - src.data_loaders.data_loader - INFO - Loading interactions data...
2025-01-18 03:29:41,771 - src.data_loaders.data_loader - INFO - Loaded 9733 interaction records
2025-01-18 03:29:41,771 - src.data_loaders.data_loader - INFO - Successfully loaded all Kahunas data files
2025-01-18 03:29:41,771 - src.data_loaders.data_loader - INFO - Creating sample PDF content...
2025-01-18 03:29:41,772 - src.data_loaders.data_loader - INFO - Sample training guide created successfully
2025-01-18 03:29:41,772 - src.data_loaders.data_loader - INFO - Setting up PostgreSQL schema...
2025-01-18 03:29:46,241 - src.data_loaders.data_loader - INFO - Creating fitness_metrics table...
2025-01-18 03:29:46,882 - src.data_loaders.data_loader - INFO - Clearing existing data from fitness_metrics...
2025-01-18 03:29:47,204 - src.data_loaders.data_loader - INFO - Inserting sample data into fitness_metrics...
2025-01-18 03:29:48,444 - src.data_loaders.data_loader - INFO - PostgreSQL schema setup completed successfully
2025-01-18 03:29:48,444 - src.data_loaders.data_loader - INFO - Data initialization completed
2025-01-18 03:29:48,444 - __main__ - INFO - Initializing session state...
2025-01-18 03:29:48,444 - __main__ - INFO - Creating new chat history
2025-01-18 03:29:48,444 - __main__ - INFO - Initializing chatbot...
2025-01-18 03:29:48,444 - src.agents.chatbot - INFO - Initializing Fitness Chatbot...

## Project Structure

```
fitness_chatbot/
├── app.py                 # Main Streamlit application
├── config/
│   └── config.py         # Configuration management
├── data/
│   ├── sample_data.csv   # Sample fitness data
│   └── documents/        # PDF documents
├── src/
│   ├── agents/          # Chatbot agent implementation
│   ├── data_loaders/    # Data source connectors
│   └── utils/           # Utility functions
├── requirements.txt      # Project dependencies
└── .env                 # Environment variables
```

## Sample Prompts

Try these example prompts to interact with the Kahunas Fitness Coach:

### Workout Recommendations
- "Can you suggest a beginner-friendly workout routine for weight loss?"
- "What's the best workout plan for building muscle mass in 12 weeks?"
- "I have lower back pain. What exercises should I avoid?"

### Progress Analysis
- "Show me the workout statistics for user ID 123"
- "What are the most popular workout types among users aged 25-35?"
- "Analyze the interaction patterns for highly engaged users"

### Personalized Advice
- "Based on my recent workouts, what areas should I focus on?"
- "How can I improve my workout consistency?"
- "What's the optimal rest period between my strength training sessions?"

### Nutrition & Recovery
- "What should I eat before and after my HIIT workout?"
- "How can I prevent muscle soreness after intense workouts?"
- "Suggest a meal plan that complements my current workout routine"

### Technical Guidance
- "What's the proper form for deadlifts?"
- "How do I adjust my squat technique to prevent knee pain?"
- "Explain the difference between compound and isolation exercises"

## Frontend - with a simple conversation

<img width="1127" alt="chat-greetings" src="https://github.com/user-attachments/assets/2ba8b63d-acdb-45f4-b638-a278f07582f7" />


## Chatbot Persona

The Kahunas Fitness Coach is designed to be:
- Professional yet approachable
- Evidence-based in its recommendations
- Focused on personalized fitness journeys
- Safety-conscious and mindful of individual limitations
- Encouraging and motivational
- Data-driven while maintaining a human touch

## Data Sources

The chatbot processes data from:
- Kahunas' user database (users.csv)
- Workout history and patterns (workouts.csv)
- User interactions and engagement (interactions.csv)
- MySQL databases containing fitness metrics
- PDF documents (workout plans, nutrition guides)
- Additional CSV files (exercise logs, progress tracking)
