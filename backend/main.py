import json
import os
import numpy as np
import faiss
import openai
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
openai_client = openai.OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load stories and initialize FAISS index
def initialize_faiss_index():
    with open("stories.json", "r") as f:
        stories = json.load(f)
    
    # Compute embeddings for all stories
    embeddings = []
    for story in stories:
        response = openai_client.embeddings.create(
            model="text-embedding-ada-002",
            input=story["content"]
        )
        embedding = response.data[0].embedding
        embeddings.append(embedding)
    
    # Convert to numpy array
    embeddings_array = np.array(embeddings).astype("float32")
    
    # Create and populate FAISS index
    embedding_dim = len(embeddings[0])
    index = faiss.IndexFlatL2(embedding_dim)
    index.add(embeddings_array)
    
    return stories, index, embeddings_array

stories, faiss_index, stored_embeddings = initialize_faiss_index()

class ChatRequest(BaseModel):
    message: str

def retrieve_relevant_stories(query: str, k: int = 2):
    # Get embedding for the query
    response = openai_client.embeddings.create(
        model="text-embedding-ada-002",
        input=query
    )
    query_embedding = np.array(response.data[0].embedding, dtype="float32")
    query_embedding = np.expand_dims(query_embedding, axis=0)
    
    # Search for similar stories
    distances, indices = faiss_index.search(query_embedding, k)
    relevant_stories = [stories[i] for i in indices[0] if i < len(stories)]
    
    return relevant_stories

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Get relevant stories based on the query
        relevant_stories = retrieve_relevant_stories(request.message)
        
        # Construct the system prompt
        system_prompt = (
            "You are an AI assistant with detailed knowledge of the user's work history. "
            "Your responses should be professional, engaging, and demonstrate strong business acumen. "
            "When answering questions, synthesize information from the provided work experiences "
            "to create coherent, relevant responses. Focus on concrete achievements, skills, "
            "and leadership qualities. Here are the relevant experiences to draw from:\n\n"
        )
        
        for story in relevant_stories:
            system_prompt += f"Experience: {story['title']}\n{story['content']}\n\n"
        
        # Generate response using ChatGPT
        chat_response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": request.message}
            ],
            temperature=0.7,
            max_tokens=500
        )
        
        return {"response": chat_response.choices[0].message.content}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
