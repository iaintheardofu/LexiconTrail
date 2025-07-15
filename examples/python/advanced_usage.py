"""
Advanced usage examples for LexiconTrail
"""

import asyncio
from typing import List, Dict
from lexicontrail import LexiconTrailClient, AsyncLexiconTrailClient
import time


class LexiconTrailAdvancedExample:
    """Advanced usage patterns for LexiconTrail"""
    
    def __init__(self, api_key: str):
        self.client = LexiconTrailClient(api_key=api_key)
        self.async_client = AsyncLexiconTrailClient(api_key=api_key)
    
    def custom_agent_routing_example(self):
        """Example of custom agent routing"""
        print("=== Custom Agent Routing ===")
        
        # Configure specific agents for different query types
        specialized_queries = [
            {
                "question": "Analyze the legal implications of this contract",
                "preferred_agents": ["LegalAnalyzer", "ContractReviewer"],
                "confidence_threshold": 0.95
            },
            {
                "question": "Extract technical specifications from this document",
                "preferred_agents": ["TechnicalExtractor", "SpecificationParser"],
                "confidence_threshold": 0.90
            }
        ]
        
        for query_config in specialized_queries:
            response = self.client.query(
                question=query_config["question"],
                options={
                    "preferred_agents": query_config["preferred_agents"],
                    "confidence_threshold": query_config["confidence_threshold"],
                    "fallback_enabled": True
                }
            )
            
            print(f"Query: {query_config['question']}")
            print(f"Agents Used: {response.agents_used}")
            print(f"Met Threshold: {response.confidence >= query_config['confidence_threshold']}")
            print()
    
    async def parallel_document_processing(self, documents: List[str]):
        """Process multiple documents in parallel"""
        print("=== Parallel Document Processing ===")
        
        start_time = time.time()
        
        # Create tasks for parallel processing
        tasks = []
        for i, doc in enumerate(documents):
            task = self.async_client.analyze_document_async(
                content=doc,
                metadata={"batch_id": f"batch_{i}"},
                options={"priority": "high"}
            )
            tasks.append(task)
        
        # Wait for all documents to be processed
        results = await asyncio.gather(*tasks)
        
        end_time = time.time()
        
        print(f"Processed {len(documents)} documents in {end_time - start_time:.2f} seconds")
        print(f"Average time per document: {(end_time - start_time) / len(documents):.2f} seconds")
        
        return results
    
    def multi_modal_processing_example(self):
        """Example of multi-modal document processing"""
        print("=== Multi-Modal Processing ===")
        
        # Process document with mixed content
        result = self.client.analyze_document(
            content="Document content with references to images",
            attachments=[
                {"type": "image", "url": "https://example.com/diagram.png"},
                {"type": "table", "data": [["A", "B"], ["1", "2"]]}
            ],
            options={
                "process_images": True,
                "extract_tables": True,
                "cross_reference": True
            }
        )
        
        print(f"Multi-modal elements processed: {result.metadata['elements_processed']}")
        print(f"Cross-references found: {result.metadata['cross_references']}")
    
    def knowledge_graph_integration(self):
        """Example of knowledge graph queries"""
        print("=== Knowledge Graph Integration ===")
        
        # Build knowledge graph from documents
        kg_result = self.client.build_knowledge_graph(
            document_ids=["doc_1", "doc_2", "doc_3"],
            options={
                "relationship_types": ["references", "contradicts", "supports"],
                "entity_resolution": True,
                "merge_similar": True
            }
        )
        
        print(f"Knowledge Graph ID: {kg_result.graph_id}")
        print(f"Nodes created: {kg_result.node_count}")
        print(f"Relationships: {kg_result.relationship_count}")
        
        # Query the knowledge graph
        graph_query = """
        MATCH (n:Entity)-[r:REFERENCES]->(m:Entity)
        WHERE n.type = 'Technology'
        RETURN n.name, m.name, r.weight
        """
        
        graph_results = self.client.query_knowledge_graph(
            graph_id=kg_result.graph_id,
            query=graph_query
        )
        
        for result in graph_results:
            print(f"{result['n.name']} -> {result['m.name']} (weight: {result['r.weight']})")
    
    def semantic_search_with_reranking(self):
        """Advanced semantic search with custom reranking"""
        print("=== Semantic Search with Reranking ===")
        
        # Perform semantic search with custom scoring
        search_results = self.client.semantic_search(
            query="innovative AI architectures for document processing",
            options={
                "search_depth": 100,  # Retrieve more candidates
                "rerank": True,
                "rerank_model": "cross-encoder",
                "boost_recent": True,
                "boost_factor": 1.2,
                "filters": {
                    "date_range": "2023-01-01:2024-12-31",
                    "categories": ["AI", "NLP", "Architecture"]
                }
            }
        )
        
        print(f"Results found: {len(search_results.results)}")
        for i, result in enumerate(search_results.results[:5]):
            print(f"{i+1}. Score: {result.score:.3f} - {result.title}")
            print(f"   Relevance: {result.relevance_explanation}")
    
    def streaming_with_callbacks(self):
        """Example of streaming with callback handlers"""
        print("=== Streaming with Callbacks ===")
        
        tokens_received = 0
        
        def on_token(token):
            nonlocal tokens_received
            tokens_received += 1
            print(token, end="", flush=True)
        
        def on_complete(stats):
            print(f"\n\nStreaming complete!")
            print(f"Total tokens: {stats['total_tokens']}")
            print(f"Time taken: {stats['duration_ms']}ms")
            print(f"Agents involved: {stats['agents']}")
        
        self.client.query_stream(
            question="Explain how LexiconTrail achieves superior performance",
            callbacks={
                "on_token": on_token,
                "on_complete": on_complete,
                "on_error": lambda e: print(f"Error: {e}")
            }
        )
    
    def caching_strategies(self):
        """Advanced caching strategies"""
        print("=== Caching Strategies ===")
        
        # Warm up cache with common queries
        common_queries = [
            "What is LexiconTrail?",
            "How does it work?",
            "What are the benefits?"
        ]
        
        print("Warming up cache...")
        for query in common_queries:
            self.client.query(
                question=query,
                options={
                    "cache_ttl": 3600,  # 1 hour
                    "cache_key": f"common_{hash(query)}"
                }
            )
        
        # Test cache performance
        print("\nTesting cache performance...")
        
        # First call (cache miss)
        start = time.time()
        result1 = self.client.query(common_queries[0])
        time1 = time.time() - start
        
        # Second call (cache hit)
        start = time.time()
        result2 = self.client.query(common_queries[0])
        time2 = time.time() - start
        
        print(f"Cache miss time: {time1*1000:.2f}ms")
        print(f"Cache hit time: {time2*1000:.2f}ms")
        print(f"Speed improvement: {time1/time2:.1f}x")
    
    def error_handling_and_retries(self):
        """Robust error handling with retries"""
        print("=== Error Handling ===")
        
        from lexicontrail.exceptions import (
            RateLimitError, 
            TimeoutError,
            AgentUnavailableError
        )
        
        def robust_query(question: str, max_retries: int = 3):
            for attempt in range(max_retries):
                try:
                    return self.client.query(
                        question=question,
                        options={"timeout": 5000}  # 5 second timeout
                    )
                except RateLimitError as e:
                    wait_time = e.retry_after or 60
                    print(f"Rate limited. Waiting {wait_time}s...")
                    time.sleep(wait_time)
                except TimeoutError:
                    print(f"Timeout on attempt {attempt + 1}. Retrying...")
                    continue
                except AgentUnavailableError as e:
                    print(f"Agent unavailable: {e.agent_name}. Using fallback...")
                    return self.client.query(
                        question=question,
                        options={"exclude_agents": [e.agent_name]}
                    )
                except Exception as e:
                    print(f"Unexpected error: {e}")
                    if attempt == max_retries - 1:
                        raise
            
            return None
        
        # Test robust querying
        result = robust_query("Complex query that might fail")
        if result:
            print(f"Success: {result.answer[:100]}...")


async def main():
    """Run advanced examples"""
    example = LexiconTrailAdvancedExample(api_key="your-api-key")
    
    # Run synchronous examples
    example.custom_agent_routing_example()
    example.multi_modal_processing_example()
    example.knowledge_graph_integration()
    example.semantic_search_with_reranking()
    example.streaming_with_callbacks()
    example.caching_strategies()
    example.error_handling_and_retries()
    
    # Run async examples
    documents = [
        "Document 1 content...",
        "Document 2 content...",
        "Document 3 content..."
    ]
    await example.parallel_document_processing(documents)


if __name__ == "__main__":
    asyncio.run(main())