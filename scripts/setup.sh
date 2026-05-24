#!/bin/bash
set -e

echo "🚀 Setting up AI Research Collaborator Agent..."

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $PYTHON_VERSION"

# Check UV
if ! command -v uv &> /dev/null; then
    echo "Installing uv..."
    pip install uv
fi

# Create .env if not exists
if [ ! -f .env ]; then
    echo "Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please update .env with your OpenAI API key"
fi

# Install dependencies
echo "Installing Python dependencies..."
uv sync

# Create data directories
echo "Creating data directories..."
mkdir -p data/{papers,embeddings,cache}

# Optional: Start Docker services
read -p "Do you want to start Docker services (PostgreSQL, Redis)? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting Docker services..."
    docker-compose up -d postgres redis
    echo "⏳ Waiting for services to be ready..."
    sleep 10
    echo "✓ Services started"
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "  1. Update .env with your OpenAI API key"
echo "  2. Start backend: uv run uvicorn src.api.main:app --reload --port 8000"
echo "  3. Start frontend: cd frontend && npm install && npm start"
echo ""
echo "📖 For more information, see docs/SETUP.md"
