# AI Research Collaborator Agent - Project Guide

## Project Overview
An intelligent research assistance platform combining LLMs, retrieval systems, knowledge graphs, and interactive dashboards to support long-term scholarly research. The system maintains persistent memory, offers exploratory navigation, and supports advanced research tasks like literature gap identification and hypothesis generation.

## Tech Stack
- **Backend**: FastAPI + Python 3.10+
- **Frontend**: React (to be scaffolded)
- **LLM**: OpenAI (configurable model via environment)
- **Vector Search**: FAISS + Sentence-Transformers
- **Knowledge Graph**: NetworkX
- **Database**: PostgreSQL + Redis
- **Containerization**: Docker & Docker Compose
- **Package Manager**: UV (not pip)

## Code Style & Standards

### Mandatory Requirements
- **Always use `uv`** for package management: `uv run xxx` (never `python3 xxx`), `uv add xxx` (never pip)
- **Simple, incremental approach**: Work in small steps, validate each increment
- **Use latest APIs**: Reference current library versions (as of May 2026)
- **Avoid over-engineering**: No defensive programming, exception managers only when needed
- **Clear docstrings**: Concise docstring comments, be sparing with other comments
- **No workarounds**: Identify root causes before fixing
- **Consistent formatting**: Black + Ruff for code quality

### Code Organization
- **Modules should be short**: Keep individual files focused
- **Clear naming**: Function and variable names should be self-documenting
- **Logging > print**: Use structured logging for visibility
- **Configuration management**: All env vars in `src/config/settings.py`

### Documentation
- README should be concise but complete
- Architecture decisions documented in `/docs`
- API endpoints documented in `/docs/API.md`
- Setup instructions in `/docs/SETUP.md`

## Project Structure

```
academic-research-chat-agent-/
├── src/                           # Source code
│   ├── api/                       # FastAPI routes
│   │   └── main.py               # Entry point
│   ├── agent/                     # LLM agent logic
│   │   └── engine.py             # ResearchAgent class
│   ├── retrieval/                 # RAG system
│   │   └── rag.py                # RAGSystem class
│   ├── memory/                    # User context memory
│   │   └── manager.py            # MemoryManager class
│   ├── knowledge_graph/           # Citation & topic graphs
│   │   └── graph.py              # ResearchKnowledgeGraph class
│   ├── config/                    # Configuration
│   │   └── settings.py           # Settings class
│   └── utils/                     # Shared utilities
│
├── frontend/                      # React UI (to be scaffolded)
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── hooks/
│   │   └── utils/
│   └── package.json
│
├── tests/                         # Test suite
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── data/                          # Data storage
│   ├── papers/                    # Research papers (PDFs)
│   ├── embeddings/                # Vector embeddings
│   └── cache/                     # Cached data
│
├── docs/                          # Documentation
│   ├── SETUP.md
│   ├── API.md
│   └── ARCHITECTURE.md
│
├── docker/                        # Docker configs
│   └── Dockerfile.backend
│
├── scripts/                       # Utility scripts
│   └── setup.sh
│
├── pyproject.toml                 # Python project config
├── docker-compose.yml             # Service orchestration
├── .env.example                   # Environment template
├── .gitignore                     # Git ignore rules
└── README.md                      # Project overview
```

## Key Modules

### Agent Engine (`src/agent/engine.py`)
- Interfaces with OpenAI API using configurable model
- Maintains conversation history
- Handles context management

### Retrieval System (`src/retrieval/rag.py`)
- Embeds documents using Sentence-Transformers
- Performs semantic search with FAISS
- Returns ranked results with similarity scores

### Memory Manager (`src/memory/manager.py`)
- Tracks user research interests
- Records explored topics with timestamps
- Maintains ongoing questions and context

### Knowledge Graph (`src/knowledge_graph/graph.py`)
- Manages paper, topic, and author nodes
- Tracks citation relationships
- Builds topic hierarchies and author networks

## Development Workflow

### Initial Setup
```bash
cd /Users/abhijitghosh/projects/academic-research-chat-agent-
bash scripts/setup.sh
```

### Running Locally
```bash
# Terminal 1: Backend
uv run uvicorn src.api.main:app --reload --port 8000

# Terminal 2: Frontend (after scaffolding)
cd frontend && npm start

# Terminal 3: Docker services (if using)
docker-compose up postgres redis
```

### Running with Docker
```bash
docker-compose up --build
```

### Testing
```bash
uv run pytest tests/ -v
uv run pytest tests/ --cov=src
```

### Code Quality
```bash
uv run black src/ tests/
uv run ruff check src/ tests/
```

## Configuration

All configuration via environment variables in `.env`:

```env
OPENAI_API_KEY=sk-...              # Your OpenAI API key (required)
OPENAI_MODEL=gpt-4                 # Model: gpt-4, gpt-3.5-turbo, gpt-4-turbo, etc.
DATABASE_URL=postgresql://...      # PostgreSQL connection
REDIS_URL=redis://localhost:6379   # Redis connection
DATA_DIR=./data                     # Data storage path
LOG_LEVEL=INFO                      # Logging level
```

## Debugging & Root Cause Analysis

When troubleshooting:
1. **Reproduce consistently** — test with minimal reproducible case
2. **Identify root cause** — gather evidence before applying fixes
3. **One test at a time** — be methodical, don't jump to conclusions
4. **No workarounds** — fix the actual problem, not symptoms

## Git Workflow
- Keep commits focused and atomic
- Write clear commit messages
- One feature per branch
- Reference issues in commits

## Next Steps
1. Scaffold React frontend structure
2. Implement API endpoints for chat, search, knowledge graph
3. Build user authentication system
4. Set up database models with SQLAlchemy
5. Implement vector store initialization
6. Create integration tests
7. Deploy configuration (CI/CD)
