import os
import logging
import torch
from typing import List, Dict, Optional, Any
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
openai_api_key = os.getenv('OPENAI_API_KEY')

torch.set_num_threads(1)  # Initialize PyTorch
device = 'cpu'  # I do not have a gpu :(
model = SentenceTransformer("all-MiniLM-L6-v2")


def query_pinecone(
    query: str, 
    index_name: str = "audio-embeddings", 
    top_k: int = 1,
    include_metadata: bool = True,
    filter_dict: Optional[Dict[str, Any]] = None
) -> Any:
    """
    Query Pinecone vector database for similar documents.
    
    Args:
        query (str): The search query string
        index_name (str): Name of the Pinecone index to query
        top_k (int): Number of results to return (default: 1)
        include_metadata (bool): Whether to include metadata in results
        filter_dict (Optional[Dict[str, Any]]): Metadata filter dictionary for Pinecone
    
    Returns:
        Query results from Pinecone
    
    Raises:
        Exception: If Pinecone API key is missing or query fails
    """
    try:
        # Validate inputs
        if not query or not isinstance(query, str):
            raise ValueError("Query must be a non-empty string")
        
        if not PINECONE_API_KEY:
            raise ValueError("PINECONE_API_KEY not set in environment")
        
        logger.info(f"Querying Pinecone with: '{query}' (top_k={top_k})")
        
        # Configure index
        pc = Pinecone(api_key=PINECONE_API_KEY)
        index = pc.Index(index_name)
        
        # Encode query to embedding
        query_embedding = model.encode([query]).tolist()
        
        # Prepare query parameters
        query_params = {
            "vector": query_embedding[0],
            "top_k": top_k,
            "include_metadata": include_metadata
        }
        
        # Add filter if provided
        if filter_dict:
            query_params["filter"] = filter_dict
            logger.info(f"Applying filter: {filter_dict}")
        
        # Execute query
        query_results = index.query(**query_params)
        
        logger.info(f"Found {len(query_results.matches)} results")
        return query_results
        
    except Exception as e:
        logger.error(f"Error querying Pinecone: {str(e)}")
        raise


def format_retrieval_results(query_results: Any) -> List[Dict[str, Any]]:
    """
    Format retrieval results into a more usable structure.
    
    Args:
        query_results: Query results from Pinecone
    
    Returns:
        List of dictionaries containing score, metadata, and id for each result
    """
    formatted_results = []
    
    for match in query_results.matches:
        formatted_results.append({
            'id': match.id,
            'score': match.score,
            'metadata': match.metadata,
            'text': match.metadata.get('text', ''),
            'url': match.metadata.get('url', ''),
            'start_time': match.metadata.get('start_time', ''),
            'end_time': match.metadata.get('end_time', '')
        })
    
    return formatted_results


def get_best_match(query_results: Any) -> Optional[Dict[str, Any]]:
    """
    Extract the best match from query results.
    
    Args:
        query_results: Query results from Pinecone
    
    Returns:
        Dictionary with best match information, or None if no results
    """
    if not query_results or not query_results.matches:
        logger.warning("No matches found in query results")
        return None
    
    return format_retrieval_results(query_results)[0]


def query_multiple_chunks(
    query: str,
    index_name: str = "audio-embeddings",
    top_k: int = 3,
    min_score: float = 0.0
) -> List[Dict[str, Any]]:
    """
    Query for multiple chunks and filter by minimum relevance score.
    
    Args:
        query (str): The search query string
        index_name (str): Name of the Pinecone index
        top_k (int): Number of results to retrieve
        min_score (float): Minimum relevance score threshold
    
    Returns:
        List of formatted results above the minimum score
    """
    query_results = query_pinecone(query, index_name, top_k=top_k)
    
    if not query_results or not query_results.matches:
        logger.warning("No matches found")
        return []
    
    formatted_results = format_retrieval_results(query_results)
    
    # Filter by minimum score
    filtered_results = [r for r in formatted_results if r['score'] >= min_score]
    
    logger.info(f"Returning {len(filtered_results)} results above score threshold {min_score}")
    return filtered_results
