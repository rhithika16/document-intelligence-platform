from fastapi import FastAPI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="AI-Based Document Intelligence Platform"
)

# Include routers
from api.document_api import router as document_router

app.include_router(document_router)


@app.get("/")
def home():
    return {
        "message": "AI-Based Document Intelligence Platform API is running successfully!"
    }