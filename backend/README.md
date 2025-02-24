# Work History Chatbot Backend

This is the backend service for the Work History Chatbot. It uses FastAPI to provide a REST API that processes chat messages using OpenAI's GPT-3.5-turbo and embeddings API.

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set up your environment:
   - Copy `.env.example` to `.env`
   - Add your OpenAI API key to `.env`

3. Update your work history:
   - Edit `stories.json` with your actual work experiences
   - Follow the existing format for each story

## Running the Server

Start the development server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- POST `/chat`: Send a message to the chatbot
- GET `/health`: Check if the service is running

## Development

The server uses FAISS for efficient similarity search of work experiences based on the user's query. When a message is received:

1. The query is converted to an embedding
2. Similar work experiences are retrieved
3. A response is generated using GPT-3.5-turbo
4. The response is returned to the client

To modify the behavior, you can adjust:
- The number of relevant stories retrieved (k parameter)
- The system prompt
- The temperature and max_tokens parameters for GPT-3.5-turbo