

import os
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
import torch

device = 'cuda' if torch.cuda.is_available() else 'cpu'

retriever = SentenceTransformer(
    'flax-sentence-embeddings/all_datasets_v3_mpnet-base'
)
retriever.to(device)

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

def get_audio_url(xc: dict):
    return xc["matches"][0]["metadata"]["audio_url"]

def get_audio_id(xc: dict):
    return xc["matches"][0]["metadata"]["audio_id"]

def get_audio_time(xc: dict):
    return xc["matches"][0]["metadata"]["audio_time"]

def get_audio_transcription(xc: dict):
    return xc["matches"][0]["metadata"]["audio_transcription"]

def get_audio_transcription_time(xc: dict):
    return xc["matches"][0]["metadata"]["audio_transcription_time"]
