# AI Research Collaborator Agent

An intelligent research assistance platform that functions as a persistent academic collaborator, combining LLMs, retrieval systems, structured knowledge management, and interactive dashboards to support long-term scholarly research.

## 🎯 Features

- **Intelligent Research Agent** — Persistent AI collaborator with memory across sessions
- **Retrieval-Augmented Generation** — Citation-grounded summaries and document synthesis
- **Knowledge Management** — Citation graphs, topic maps, concept hierarchies, author networks
- **Interactive Dashboard** — Exploratory research navigation and discovery interface
- **Research Analytics** — Literature gap identification, hypothesis generation, future directions
- **Memory Systems** — Long-term memory of research interests, explored topics, ongoing questions
- **Multi-Source Analysis** — Comparative analyses across foundational texts, seminal papers, and emerging research

## 🏗️ Architecture

```
FastAPI Backend (port 8000)
├── Agent Engine (OpenAI integration with configurable models)
├── Retrieval System (Vector search with embeddings)
├── Knowledge Graph (Citation networks, topic hierarchies)
└── Memory System (User context, research history)

Frontend UI (React, port 3000)
├── Chat Interface
├── Research Dashboard
├── Citation Graph Visualizer
└── Knowledge Explorer

Database & Storage
├── PostgreSQL (Metadata, user data)
├── Vector Store (FAISS/Redis)
└── File Storage (Papers, embeddings, cache)
```

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- Node.js 18+ (for UI)
- Docker & Docker Compose
- OpenAI API key

### Setup

1. **Clone & Setup**
```bash
cd /Users/abhijitghosh/projects/academic-research-chat-agent-
git init
```

2. **Install Dependencies**
```bash
uv sync
```

3. **Configure Environment**
```bash
cp .env.example .env
# Edit .env with your OpenAI API key and model preference
```

4. **Run Services**
```bash
# Backend
uv run uvicorn src.api.main:app --reload --port 8000

# Frontend (in another terminal)
cd frontend && npm install && npm start
```

5. **Access Dashboard**
Open browser: **http://localhost:3000**

## 📁 Project Structure

```
src/
├── api/                  # FastAPI routes & endpoints
├── agent/               # LLM agent logic & reasoning
├── retrieval/           # Vector search & RAG implementation
├── memory/              # Persistent memory systems
├── knowledge_graph/     # Citation networks, topic maps
├── config/              # Configuration management
└── utils/               # Shared utilities

frontend/
├── src/
│   ├── components/      # React components
│   ├── pages/          # Page layouts
│   ├── hooks/          # Custom React hooks
│   └── utils/          # Frontend utilities
└── public/

tests/
├── unit/                # Unit tests
├── integration/         # Integration tests
└── fixtures/            # Test data

docs/
├── SETUP.md            # Setup guide
├── API.md              # API documentation
└── ARCHITECTURE.md     # System design
```

## 🛠️ Development

### Run Tests
```bash
uv run pytest tests/ -v
```

### Code Quality
```bash
uv run black src/ tests/
uv run ruff check src/ tests/
```

### Docker
```bash
docker-compose up --build
docker-compose down
```

## 📚 Documentation

- [Setup Guide](docs/SETUP.md)
- [API Documentation](docs/API.md)
- [Architecture Guide](docs/ARCHITECTURE.md)

## 🔧 Configuration

Set environment variables in `.env`:

```env
OPENAI_API_KEY=your_api_key
OPENAI_MODEL=gpt-4
DATABASE_URL=postgresql://user:pass@localhost:5432/research_agent_db
REDIS_URL=redis://localhost:6379
```

## 📝 License

Proprietary - Academic Use Only
