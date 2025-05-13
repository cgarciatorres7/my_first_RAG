import os
import torch
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from openai import OpenAI

# Initialize PyTorch
torch.set_num_threads(1)  # Limit PyTorch to use only one thread
device = 'cpu'  # Always use CPU

model = SentenceTransformer("all-MiniLM-L6-v2")
# initialize connection to pinecone (get API key at app.pinecone.io)
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
openai_api_key = os.getenv('OPENAI_API_KEY')

# configure client
pc = Pinecone(api_key=PINECONE_API_KEY)


def query_pinecone(query: str):
    # configure index
    index_name = "audio-embeddings"
    index = pc.Index(index_name)

    xq = model.encode([query]).tolist()
    # now query
    query_results = index.query(vector=xq, top_k=1, include_metadata=True)
    return query_results


def rag_promt(query: str, query_results: str) -> str:
    """
    Simple RAG function that:
    1. Retrieves relevant context from Pinecone
    2. Creates a prompt with the context
    3. Gets a response from the LLM
    """
    # Get relevant documents from Pinecone
    context = [
        x.metadata['text'] for x in query_results.matches
    ]
    # Create prompt template
    prompt_template = """
    Answer the question based on the following context from a video transcript.
    If you cannot answer the question based on the context, say "I cannot answer this based on the video content."
    
    Context: {context}
    
    Question: {query}
    
    Answer: """
    
    return prompt_template.format(context=context, query=query)


def chat_completion(prompt):

    # Instantiate the OpenAI client
    client = OpenAI(api_key=openai_api_key)
    
    # Instructions
    sys_prompt = "You are a helpful assistant that always answers questions."
    res = client.chat.completions.create(
        model='gpt-3.5-turbo-0125',
        messages=[
            {"role": "system", "content": sys_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return res.choices[0].message.content.strip()

