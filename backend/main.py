from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
from pydantic import BaseModel
from agent.loop import run_agent

load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_id: str
    message: str

test_profile = {
    "major": "Computer Science",
    "catalog_year": "2023",
    "target_graduation": "Winter 2027",
    "completed_courses": [
        {"code": "EECS 280", "name": "Programming and Data Structures", "credits": 4},
        {"code": "MATH 214", "name": "Linear Algebra", "credits": 4},
    ]
}

@app.post("/chat")
def chat(request: ChatRequest):
    response = run_agent(request.message, test_profile, request.user_id)
    return {"response": response.content}