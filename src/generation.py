import os
import logging
from typing import Any
from openai import OpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get OpenAI API key from environment
openai_api_key = os.getenv('OPENAI_API_KEY')
if not openai_api_key:
    logger.warning("OPENAI_API_KEY not found in environment")


def rag_prompt(query: str, query_results: Any) -> str:
    """
    Create a RAG prompt from query and Pinecone query results.
    
    Args:
        query (str): The user's question
        query_results (Any): Query results from Pinecone
    
    Returns:
        str: Formatted prompt string for the LLM
    """
    try:
        # Get relevant documents from Pinecone
        context = [
            x.metadata.get('text', '') for x in query_results.matches
        ]
        
        # Join context into a single string
        context_str = "\n".join(context)
        
        # Create prompt template
        prompt_template = """
Answer the question based on the following context from a video transcript.
If you cannot answer the question based on the context, say "I cannot answer this based on the video content."

Context: {context}

Question: {query}

Answer: """
        
        return prompt_template.format(context=context_str, query=query)
    
    except Exception as e:
        logger.error(f"Error creating RAG prompt: {str(e)}")
        raise


def rag_promt(query: str, query_results: Any) -> str:
    """
    Alias for rag_prompt (keeping for backward compatibility).
    """
    return rag_prompt(query, query_results)


def chat_completion(prompt: str, model: str = 'gpt-3.5-turbo-0125') -> str:
    """
    Get a completion from OpenAI's chat API.
    
    Args:
        prompt (str): The user prompt to send
        model (str): The OpenAI model to use (default: gpt-3.5-turbo-0125)
    
    Returns:
        str: The generated response
    
    Raises:
        ValueError: If OpenAI API key is not set
        Exception: If API call fails
    """
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not set in environment")
    
    try:
        logger.info(f"Sending prompt to OpenAI ({model})")
        
        # Instantiate the OpenAI client
        client = OpenAI(api_key=openai_api_key)
        
        # Instructions
        sys_prompt = "You are a helpful assistant that answers questions based on the provided context."
        
        res = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": sys_prompt},
                {"role": "user", "content": prompt}
            ],
            temperature=0
        )
        
        response = res.choices[0].message.content.strip()
        logger.info("Successfully received response from OpenAI")
        return response
    
    except Exception as e:
        logger.error(f"Error in chat completion: {str(e)}")
        raise


def complete_rag(query: str, query_results: Any, model: str = 'gpt-3.5-turbo-0125') -> str:
    """
    Complete RAG pipeline: creates prompt from query results and gets LLM response.
    
    Args:
        query (str): The user's question
        query_results (Any): Query results from Pinecone
        model (str): The OpenAI model to use (default: gpt-3.5-turbo-0125)
    
    Returns:
        str: The generated response
    """
    try:
        logger.info(f"Running complete RAG pipeline for query: '{query}'")
        
        # Create prompt
        prompt = rag_prompt(query, query_results)
        
        # Get completion
        response = chat_completion(prompt, model)
        
        return response
    
    except Exception as e:
        logger.error(f"Error in complete RAG: {str(e)}")
        raise

