import os
import torch
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from langchain_core.prompts import PromptTemplate
#from langchain_openai import OpenAI

# Initialize PyTorch
torch.set_num_threads(1)  # Limit PyTorch to use only one thread
device = 'cpu'  # Always use CPU

retriever = SentenceTransformer(
    'flax-sentence-embeddings/all_datasets_v3_mpnet-base',
    device=device
)

# initialize connection to pinecone (get API key at app.pinecone.io)
api_key = os.environ.get('PINECONE_API_KEY') or 'PINECONE_API_KEY'

# configure client
pc = Pinecone(api_key=api_key)


def query_pinecone(query: str):
    # configure index
    index_name = "audio-embeddings"
    index = pc.Index(index_name)

    xq = retriever.encode([query]).tolist()
    # now query
    xc = index.query(vector=xq, top_k=5, include_metadata=True)
    return xc

def get_transcriptions(xc: dict):
    return xc["matches"]

def get_rag_response(query: str, model_name: str = "gpt-3.5-turbo") -> str:
    """
    Simple RAG function that:
    1. Retrieves relevant context from Pinecone
    2. Creates a prompt with the context
    3. Gets a response from the LLM
    """
    # Get relevant documents from Pinecone
    results = query_pinecone(query)
    transcriptions = get_transcriptions(results)
    
    # Combine all relevant transcriptions
    context = "\n".join([t["metadata"]["text"] for t in transcriptions])
    
    # Create prompt template
    prompt_template = """
    Answer the question based on the following context from a video transcript.
    If you cannot answer the question based on the context, say "I cannot answer this based on the video content."
    
    Context: {context}
    
    Question: {question}
    
    Answer: """
    
    prompt = PromptTemplate(
        template=prompt_template,
        input_variables=["context", "question"]
    )  
    
    # Get LLM response
    #llm = OpenAI(temperature=0, model_name=model_name)
    #final_prompt = prompt.format(context=context, question=query)
    #response = llm(final_prompt)
    
    return "Hello World"

