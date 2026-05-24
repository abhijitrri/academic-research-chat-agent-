"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import settings

app = FastAPI(
    title="AI Research Collaborator Agent",
    description="Intelligent research assistance platform with LLM, retrieval, memory, and knowledge graphs",
    version="0.1.0"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_url],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "research-agent-api"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {"message": "AI Research Collaborator Agent API"}


# TODO: Import and include routers
# from src.api.routes import chat, research, knowledge_graph


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=settings.api_host, port=settings.api_port)
