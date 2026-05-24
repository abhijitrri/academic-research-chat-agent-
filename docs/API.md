# API Documentation

## Overview

The AI Research Collaborator Agent API provides endpoints for research collaboration, document retrieval, and knowledge management.

## Base URL
```
http://localhost:8000
```

## Authentication
(To be implemented)

## Endpoints

### Health Check
```
GET /health
```

Returns service health status.

**Response:**
```json
{
  "status": "healthy",
  "service": "research-agent-api"
}
```

### Root
```
GET /
```

Root endpoint with service information.

**Response:**
```json
{
  "message": "AI Research Collaborator Agent API"
}
```

### Chat Interface (To be implemented)
```
POST /api/chat
```

Send message to research agent.

**Request:**
```json
{
  "user_id": "user123",
  "message": "What are the latest advances in machine learning?",
  "model": "gpt-4"
}
```

**Response:**
```json
{
  "message_id": "msg_123",
  "response": "...",
  "sources": ["paper1", "paper2"]
}
```

### Document Search (To be implemented)
```
GET /api/search
```

Search for relevant papers.

**Query Parameters:**
- `query` (string): Search query
- `limit` (int): Number of results (default: 10)
- `offset` (int): Results offset (default: 0)

**Response:**
```json
{
  "results": [
    {
      "paper_id": "arxiv_123",
      "title": "...",
      "authors": ["..."],
      "relevance": 0.95
    }
  ],
  "total": 42
}
```

### Knowledge Graph (To be implemented)
```
GET /api/knowledge-graph/{topic}
```

Get knowledge graph for a topic.

**Response:**
```json
{
  "nodes": [...],
  "edges": [...]
}
```

### User Memory (To be implemented)
```
GET /api/memory/{user_id}
```

Get user research memory and context.

**Response:**
```json
{
  "user_id": "user123",
  "research_interests": ["ML", "NLP"],
  "explored_topics": {},
  "ongoing_questions": []
}
```

## Response Codes

- `200`: Success
- `400`: Bad request
- `401`: Unauthorized
- `404`: Not found
- `500`: Server error

## Error Response Format

```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {}
}
```

## Rate Limiting
(To be implemented)

## WebSocket (To be implemented)

```
WS /api/ws/{user_id}
```

Real-time chat connection for streaming responses.

## Interactive API Documentation

Once the backend is running, access interactive API docs at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
