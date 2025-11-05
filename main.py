from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import json
from datetime import datetime
import random

app = FastAPI(title="Ecoroute AI API", version="1.0.0")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request/Response models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    sources: List[dict] = []
    conversation_id: str

class AnalyticsData(BaseModel):
    total_queries: int
    active_users: int
    popular_questions: List[dict]
    response_time_avg: float
    satisfaction_score: float

# Mock RAG knowledge base
MOCK_KNOWLEDGE_BASE = {
    "admission": {
        "content": "Admissions are open for Fall 2024. Application deadline is March 15, 2024. Required documents include transcripts, recommendation letters, and a personal statement. Application fee is $50.",
        "source": "Admissions Office - Policy Document 2024"
    },
    "tuition": {
        "content": "Tuition fees vary by program. Undergraduate programs: $15,000 per semester. Graduate programs: $20,000 per semester. Financial aid and scholarships are available. Payment plans can be arranged through the Bursar's Office.",
        "source": "Bursar's Office - Fee Schedule 2024"
    },
    "registration": {
        "content": "Course registration opens two weeks before the start of each semester. Students must meet with their academic advisor before registering. Registration is done through the student portal. Maximum credit hours: 18 per semester.",
        "source": "Registrar's Office - Registration Guide"
    },
    "housing": {
        "content": "On-campus housing applications are accepted starting January 1st for the following academic year. Room options include single, double, and suite-style accommodations. Priority is given to first-year students. Housing cost ranges from $8,000-$12,000 per academic year.",
        "source": "Housing Office - Accommodation Policy"
    },
    "library": {
        "content": "The main library is open Monday-Friday 8 AM - 10 PM, Saturday 9 AM - 6 PM, and Sunday 10 AM - 8 PM. Study rooms can be reserved online. Digital resources are available 24/7 through the library portal. Library card is required for borrowing materials.",
        "source": "University Library - Hours and Services"
    },
    "financial aid": {
        "content": "Financial aid applications are processed through the FAFSA. Priority deadline is February 1st. Available aid includes grants, loans, and work-study programs. Merit scholarships require separate application. Contact the Financial Aid Office for assistance.",
        "source": "Financial Aid Office - Application Guide"
    },
    "academic calendar": {
        "content": "Fall semester runs from late August to mid-December. Spring semester runs from mid-January to early May. Summer sessions are available in June and July. Important dates include: add/drop deadline (first week), midterms (week 7-8), finals (last week of semester).",
        "source": "Academic Affairs - Academic Calendar 2024"
    },
    "campus facilities": {
        "content": "Campus facilities include: Student Recreation Center (6 AM - 11 PM), Dining Hall (7 AM - 9 PM), Health Center (8 AM - 5 PM), Bookstore (9 AM - 6 PM). All facilities are accessible via student ID card.",
        "source": "Campus Services - Facilities Directory"
    }
}

def generate_rag_response(query: str) -> tuple[str, List[dict]]:
    """Generate a mock RAG response based on the query."""
    query_lower = query.lower()
    
    # Simple keyword matching for demo purposes
    matched_topics = []
    for topic, info in MOCK_KNOWLEDGE_BASE.items():
        if topic in query_lower or any(keyword in query_lower for keyword in topic.split()):
            matched_topics.append((topic, info))
    
    if matched_topics:
        # Use the first matching topic
        topic, info = matched_topics[0]
        response = info["content"]
        sources = [{"title": info["source"], "relevance": 0.95}]
        
        # Add a conversational touch
        response = f"Based on our university resources, {response}"
    else:
        # Default response for unmatched queries
        response = "I can help you with information about admissions, tuition, registration, housing, library services, financial aid, academic calendar, and campus facilities. Could you please rephrase your question?"
        sources = [{"title": "General FAQ", "relevance": 0.75}]
    
    return response, sources

@app.get("/")
async def root():
    return {"message": "Ecoroute AI API is running", "version": "1.0.0"}

@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Handle chat requests and return RAG-based responses."""
    try:
        response, sources = generate_rag_response(request.message)
        conversation_id = request.conversation_id or f"conv_{datetime.now().timestamp()}"
        
        return ChatResponse(
            response=response,
            sources=sources,
            conversation_id=conversation_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/analytics", response_model=AnalyticsData)
async def get_analytics():
    """Return mock analytics data for the admin dashboard."""
    return AnalyticsData(
        total_queries=random.randint(1500, 2500),
        active_users=random.randint(120, 200),
        popular_questions=[
            {"question": "How do I apply for admission?", "count": 342},
            {"question": "What are the tuition fees?", "count": 298},
            {"question": "When does registration open?", "count": 267},
            {"question": "How do I apply for financial aid?", "count": 234},
            {"question": "What are the library hours?", "count": 189}
        ],
        response_time_avg=round(random.uniform(0.8, 1.5), 2),
        satisfaction_score=round(random.uniform(4.2, 4.8), 1)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

