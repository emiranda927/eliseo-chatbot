# Work History Chatbot

A personalized AI chatbot that answers questions about my professional experience by drawing from my work history.

## Project Structure

- `/backend` - Python FastAPI server that handles chat interactions
- `/src` - React frontend application

## Setup

1. Install frontend dependencies:
```bash
npm install
```

2. Install backend dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Configure environment:
- Copy `backend/.env.example` to `backend/.env`
- Add your OpenAI API key to `backend/.env`

4. Start the services:

Backend:
```bash
cd backend
uvicorn main:app --reload
```

Frontend:
```bash
npm run dev
```

## Development

1. Update your work history:
- Edit `backend/stories.json` with your actual work experiences
- Follow the existing format for each story

2. Customize the chatbot:
- Adjust the system prompt in `backend/main.py`
- Modify the UI in `src/App.tsx`

## Deployment

### Frontend
The frontend can be deployed to any static hosting service (Netlify, Vercel, etc.)

### Backend
The backend requires a Python hosting environment with the following:
- Python 3.8+
- Access to OpenAI API
- Ability to install dependencies from requirements.txt