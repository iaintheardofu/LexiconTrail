# LexiconTrail API Reference

## Overview

The LexiconTrail API provides programmatic access to the advanced agentic AI system. This reference covers all available endpoints, request/response formats, and integration patterns.

## Authentication

All API requests require authentication using an API key.

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" \
     https://api.lexicontrail.com/v1/health
```

## Base URL

```
https://api.lexicontrail.com/v1
```

## Rate Limits

| Plan | Requests/min | Requests/day | Concurrent |
|------|--------------|--------------|------------|
| Free | 10 | 1,000 | 1 |
| Pro | 100 | 50,000 | 10 |
| Enterprise | 1,000 | Unlimited | 100 |

## Endpoints

### Health Check

Check system status and availability.

```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "agents_available": 4,
  "response_time_ms": 12
}
```

### Document Analysis

#### Analyze Document

Process and analyze a document using multi-agent system.

```http
POST /documents/analyze
```

**Request Body:**
```json
{
  "content": "Document text content...",
  "type": "text/plain",
  "metadata": {
    "source": "upload",
    "language": "en"
  },
  "options": {
    "extract_entities": true,
    "build_knowledge_graph": true,
    "generate_summary": true
  }
}
```

**Response:**
```json
{
  "document_id": "doc_12345",
  "status": "completed",
  "processing_time_ms": 342,
  "agents_used": ["DocumentAnalyzer", "EntityExtractor", "Summarizer"],
  "results": {
    "entities": [
      {
        "text": "LlamaIndex",
        "type": "TECHNOLOGY",
        "confidence": 0.98
      }
    ],
    "key_concepts": ["AI", "Machine Learning", "NLP"],
    "summary": "This document discusses...",
    "embeddings_created": 128,
    "knowledge_graph_nodes": 45
  }
}
```

#### Get Document Status

Check the status of document processing.

```http
GET /documents/{document_id}/status
```

**Response:**
```json
{
  "document_id": "doc_12345",
  "status": "processing",
  "progress": 0.75,
  "estimated_completion_ms": 1200
}
```

#### Get Document Results

Retrieve full analysis results for a document.

```http
GET /documents/{document_id}/results
```

### Query Processing

#### Submit Query

Process a natural language query.

```http
POST /query
```

**Request Body:**
```json
{
  "question": "What are the key features of LexiconTrail?",
  "context": {
    "document_ids": ["doc_12345", "doc_67890"],
    "session_id": "sess_abc123"
  },
  "options": {
    "use_cache": true,
    "return_sources": true,
    "max_agents": 3,
    "confidence_threshold": 0.8
  }
}
```

**Response:**
```json
{
  "query_id": "qry_98765",
  "answer": "LexiconTrail's key features include...",
  "confidence": 0.94,
  "processing_time_ms": 186,
  "agents_used": ["QueryProcessor", "ResponseGenerator"],
  "sources": [
    {
      "document_id": "doc_12345",
      "relevance_score": 0.92,
      "excerpt": "The system leverages..."
    }
  ],
  "metadata": {
    "query_type": "explanatory",
    "cache_hit": false,
    "tokens_processed": 512
  }
}
```

#### Stream Query Response

Get streaming responses for real-time applications.

```http
POST /query/stream
```

**Request Body:** Same as `/query`

**Response:** Server-Sent Events (SSE) stream
```
data: {"chunk": "Based on the analysis", "index": 0}
data: {"chunk": " using multiple agents,", "index": 1}
data: {"chunk": " LexiconTrail provides...", "index": 2}
data: {"done": true, "total_chunks": 3}
```

### Agent Management

#### List Available Agents

Get information about available agents.

```http
GET /agents
```

**Response:**
```json
{
  "agents": [
    {
      "id": "agent_doc_analyzer",
      "name": "DocumentAnalyzer",
      "type": "document-slm",
      "specialization": "document_understanding",
      "status": "active",
      "load": 0.23
    },
    {
      "id": "agent_query_proc",
      "name": "QueryProcessor",
      "type": "query-slm",
      "specialization": "query_understanding",
      "status": "active",
      "load": 0.45
    }
  ]
}
```

#### Get Agent Metrics

Retrieve performance metrics for agents.

```http
GET /agents/metrics
```

**Response:**
```json
{
  "metrics": {
    "agent_doc_analyzer": {
      "requests_processed": 10234,
      "avg_response_time_ms": 234,
      "success_rate": 0.98,
      "current_load": 0.23
    }
  },
  "aggregate": {
    "total_requests": 45678,
    "avg_response_time_ms": 198,
    "overall_success_rate": 0.97
  }
}
```

### Batch Operations

#### Batch Document Analysis

Process multiple documents in a single request.

```http
POST /batch/documents/analyze
```

**Request Body:**
```json
{
  "documents": [
    {
      "content": "First document...",
      "metadata": {"id": "1"}
    },
    {
      "content": "Second document...",
      "metadata": {"id": "2"}
    }
  ],
  "options": {
    "parallel_processing": true,
    "priority": "high"
  }
}
```

**Response:**
```json
{
  "batch_id": "batch_123",
  "status": "processing",
  "documents_queued": 2,
  "estimated_completion_ms": 5000
}
```

#### Get Batch Status

Check the status of batch processing.

```http
GET /batch/{batch_id}/status
```

### WebSocket API

For real-time bidirectional communication.

```javascript
const ws = new WebSocket('wss://api.lexicontrail.com/v1/ws');

ws.on('open', () => {
  ws.send(JSON.stringify({
    type: 'auth',
    api_key: 'YOUR_API_KEY'
  }));
});

ws.on('message', (data) => {
  const message = JSON.parse(data);
  console.log('Received:', message);
});

// Send query
ws.send(JSON.stringify({
  type: 'query',
  payload: {
    question: 'What is LexiconTrail?'
  }
}));
```

## Error Handling

### Error Response Format

```json
{
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Rate limit exceeded. Please retry after 60 seconds.",
    "details": {
      "limit": 100,
      "remaining": 0,
      "reset_at": "2024-01-15T12:00:00Z"
    }
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| INVALID_API_KEY | 401 | Invalid or missing API key |
| RATE_LIMIT_EXCEEDED | 429 | Rate limit exceeded |
| INVALID_REQUEST | 400 | Malformed request |
| DOCUMENT_NOT_FOUND | 404 | Document ID not found |
| PROCESSING_ERROR | 500 | Internal processing error |
| TIMEOUT | 504 | Request timeout |
| INSUFFICIENT_QUOTA | 402 | Quota exceeded |

## SDKs and Client Libraries

### Python SDK

```python
from lexicontrail import LexiconTrailClient

client = LexiconTrailClient(api_key="YOUR_API_KEY")

# Analyze document
result = client.analyze_document(
    content="Your document content here...",
    options={"extract_entities": True}
)

# Query
response = client.query(
    question="What are the main topics?",
    context={"document_ids": [result.document_id]}
)
print(response.answer)
```

### JavaScript/TypeScript SDK

```typescript
import { LexiconTrailClient } from 'lexicontrail-js';

const client = new LexiconTrailClient({
  apiKey: 'YOUR_API_KEY'
});

// Analyze document
const result = await client.analyzeDocument({
  content: 'Your document content here...',
  options: { extractEntities: true }
});

// Query
const response = await client.query({
  question: 'What are the main topics?',
  context: { documentIds: [result.documentId] }
});
console.log(response.answer);
```

### Go SDK

```go
package main

import (
    "github.com/lexicontrail/lexicontrail-go"
)

func main() {
    client := lexicontrail.NewClient("YOUR_API_KEY")
    
    // Analyze document
    result, err := client.AnalyzeDocument(
        "Your document content here...",
        lexicontrail.AnalyzeOptions{
            ExtractEntities: true,
        },
    )
    
    // Query
    response, err := client.Query(
        "What are the main topics?",
        lexicontrail.QueryOptions{
            DocumentIDs: []string{result.DocumentID},
        },
    )
}
```

## Webhooks

Configure webhooks to receive notifications about processing events.

### Webhook Configuration

```http
POST /webhooks
```

**Request Body:**
```json
{
  "url": "https://your-server.com/webhook",
  "events": ["document.processed", "query.completed"],
  "secret": "your-webhook-secret"
}
```

### Webhook Payload

```json
{
  "event": "document.processed",
  "timestamp": "2024-01-15T10:30:00Z",
  "data": {
    "document_id": "doc_12345",
    "status": "completed",
    "processing_time_ms": 342
  }
}
```

## Best Practices

### 1. **Efficient Batching**
```python
# Good: Batch multiple documents
results = client.batch_analyze(documents)

# Avoid: Sequential processing
for doc in documents:
    result = client.analyze_document(doc)  # Inefficient
```

### 2. **Use Caching**
```python
# Enable caching for repeated queries
response = client.query(
    question="...",
    options={"use_cache": True}
)
```

### 3. **Handle Rate Limits**
```python
import time

def query_with_retry(client, question):
    max_retries = 3
    for i in range(max_retries):
        try:
            return client.query(question)
        except RateLimitError as e:
            if i < max_retries - 1:
                time.sleep(e.retry_after)
            else:
                raise
```

### 4. **Stream Large Responses**
```python
# For large responses, use streaming
for chunk in client.query_stream(question):
    process_chunk(chunk)
```

## API Changelog

### v1.0.0 (2024-01-15)
- Initial API release
- Document analysis endpoints
- Query processing
- Agent management
- Batch operations

### Coming Soon
- GraphQL API
- Advanced analytics endpoints
- Custom model fine-tuning API
- Export functionality

---

For API support, contact:
- Email: api-support@theaicowboys.com
- Documentation: https://docs.lexicontrail.com
- Status Page: https://status.lexicontrail.com