# VERA - Task Manager Chatbot

VERA is a task manager chatbot designed to help users schedule and manage their tasks efficiently. It provides functionalities such as creating tasks, viewing tasks, and deleting tasks.

## Features

- **Create Task:**
  - Add new tasks to your schedule easily.

- **View Tasks:**
  - View your tasks with details like task name, date, and time.

- **Delete Task:**
  - Remove tasks that are no longer relevant or completed.

## Getting Started

### Prerequisites

- Python (>=3.7)
- FastAPI
- MySQL (or any other preferred database)
- ngrok (for local development and testing)

## Getting Started

1. Clone the repository:

```bash
git clone https://github.com/your-username/vera-chatbot.git
cd vera-chatbot
```

2. Install the required Python packages:
```bash
pip install -r requirements.txt
```

3. Configure Dialogflow:

   - Create a new Dialogflow agent.
   - Set up the necessary intents, entities, and fulfillment for your chatbot.
  
4. Configure MySQL Database:

   - Create a MySQL database.
   - Update db_handler.py with your database credentials.

5. Start the FastAPI server:

   ```bash
   uvicorn main:app --reload
   ```

6. Access the chatbot interface:

   - Open `index.html` in your web browser or host it on a web server.
  
