"""
Basic usage example for LexiconTrail
"""

from lexicontrail import LexiconTrailClient
import json


def main():
    # Initialize client
    client = LexiconTrailClient(api_key="your-api-key")
    
    # Example 1: Analyze a document
    print("=== Document Analysis Example ===")
    
    document_content = """
    LexiconTrail is an advanced agentic AI system that combines NVIDIA's 
    research on Small Language Models (SLMs) with LlamaIndex's powerful 
    indexing capabilities. The system achieves 10x performance improvements 
    through intelligent agent routing and specialized model deployment.
    """
    
    # Analyze the document
    analysis_result = client.analyze_document(
        content=document_content,
        options={
            "extract_entities": True,
            "generate_summary": True,
            "build_knowledge_graph": True
        }
    )
    
    print(f"Document ID: {analysis_result.document_id}")
    print(f"Processing Time: {analysis_result.processing_time_ms}ms")
    print(f"Entities Found: {', '.join(analysis_result.entities)}")
    print(f"Key Concepts: {', '.join(analysis_result.key_concepts)}")
    print(f"Summary: {analysis_result.summary}")
    print()
    
    # Example 2: Query the system
    print("=== Query Processing Example ===")
    
    queries = [
        "What is LexiconTrail?",
        "How does it achieve 10x performance?",
        "What technologies does it use?"
    ]
    
    for query in queries:
        response = client.query(
            question=query,
            context={"document_ids": [analysis_result.document_id]},
            options={
                "use_cache": True,
                "return_sources": True
            }
        )
        
        print(f"Q: {query}")
        print(f"A: {response.answer}")
        print(f"Confidence: {response.confidence:.2%}")
        print(f"Response Time: {response.processing_time_ms}ms")
        print(f"Agents Used: {', '.join(response.agents_used)}")
        print()
    
    # Example 3: Batch processing
    print("=== Batch Processing Example ===")
    
    documents = [
        "Document about machine learning and AI...",
        "Technical specification for neural networks...",
        "Research paper on language models..."
    ]
    
    batch_result = client.batch_analyze(
        documents=documents,
        options={"parallel_processing": True}
    )
    
    print(f"Batch ID: {batch_result.batch_id}")
    print(f"Documents Queued: {batch_result.documents_queued}")
    
    # Wait for completion
    status = client.get_batch_status(batch_result.batch_id)
    print(f"Status: {status.status}")
    print(f"Progress: {status.progress:.1%}")
    
    # Example 4: Streaming responses
    print("=== Streaming Example ===")
    
    print("Streaming response for complex query...")
    for chunk in client.query_stream(
        question="Explain the architecture of LexiconTrail in detail"
    ):
        print(chunk, end="", flush=True)
    print("\n")
    
    # Example 5: Agent monitoring
    print("=== Agent Status Example ===")
    
    agents = client.get_agents()
    for agent in agents:
        print(f"Agent: {agent.name}")
        print(f"  Type: {agent.type}")
        print(f"  Status: {agent.status}")
        print(f"  Load: {agent.load:.1%}")
    
    # Example 6: Health check
    print("=== System Health ===")
    
    health = client.health_check()
    print(f"Status: {health['status']}")
    print(f"Version: {health['version']}")
    print(f"Agents Available: {health['agents_available']}")
    

if __name__ == "__main__":
    main()