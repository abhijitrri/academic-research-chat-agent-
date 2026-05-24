# Setup Guide

## Prerequisites

- Python 3.10+
- Node.js 18+
- Docker & Docker Compose (optional)
- OpenAI API key

## Local Development Setup

### 1. Clone Repository
```bash
git clone <repo-url>
cd academic-research-chat-agent-
```

### 2. Install Python Dependencies
```bash
# Install UV if not already installed
pip install uv

# Install project dependencies
uv sync
uv pip install -e .
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings:
# - OPENAI_API_KEY: Your OpenAI API key
# - OPENAI_MODEL: Your preferred model (gpt-4, gpt-3.5-turbo, etc.)
```

### 4. Setup Database
```bash
# Start PostgreSQL locally or use Docker
docker run -d \
  --name research_db \
  -e POSTGRES_USER=research_user \
  -e POSTGRES_PASSWORD=research_pass \
  -e POSTGRES_DB=research_agent_db \
  -p 5432:5432 \
  postgres:16-alpine

# Run migrations (if applicable)
uv run alembic upgrade head
```

### 5. Setup Redis
```bash
# Start Redis locally or use Docker
docker run -d \
  --name research_redis \
  -p 6379:6379 \
  redis:7-alpine
```

### 6. Start Backend Server
```bash
uv run uvicorn src.api.main:app --reload --port 8000
```

### 7. Setup Frontend
```bash
cd frontend
npm install
npm start
```

The frontend will be available at `http://localhost:3000`

## Docker Setup

### Run All Services
```bash
docker-compose up --build
```

### Stop Services
```bash
docker-compose down
```

### View Logs
```bash
docker-compose logs -f backend
docker-compose logs -f frontend
```

## Testing

### Run Tests
```bash
uv run pytest tests/ -v
```

### Run Tests with Coverage
```bash
uv run pytest tests/ --cov=src --cov-report=html
```

### Run Specific Test
```bash
uv run pytest tests/unit/agent/test_engine.py -v
```

## Troubleshooting

### Database Connection Error
- Ensure PostgreSQL is running: `docker ps | grep research_db`
- Check DATABASE_URL in .env matches your setup

### Redis Connection Error
- Ensure Redis is running: `docker ps | grep research_redis`
- Check REDIS_URL in .env

### OpenAI API Error
- Verify OPENAI_API_KEY is set correctly
- Check that the API key has sufficient quota

### Port Already in Use
- Change ports in docker-compose.yml or .env
- Kill existing process: `lsof -i :8000` and `kill -9 <PID>`

## Development Tools

### Code Formatting
```bash
uv run black src/ tests/
```

### Linting
```bash
uv run ruff check src/ tests/
```

### Type Checking
```bash
uv run mypy src/
```

### Interactive Shell
```bash
uv run ipython
```

## Environment Variables Reference

| Variable | Default | Description |
|----------|---------|-------------|
| OPENAI_API_KEY | - | OpenAI API key (required) |
| OPENAI_MODEL | gpt-4 | OpenAI model to use |
| DATABASE_URL | localhost | PostgreSQL connection string |
| REDIS_URL | localhost:6379 | Redis connection string |
| DATA_DIR | ./data | Data storage directory |
| LOG_LEVEL | INFO | Logging level |
