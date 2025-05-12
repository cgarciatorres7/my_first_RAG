import whisper
from typing import List, Dict
import os
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from pydub import AudioSegment
from pytubefix import YouTube
from pytubefix.cli import on_progress
from src.config.directories import directories
from pinecone import Pinecone, ServerlessSpec


load_dotenv()
# Reads HF_TOKEN from env
PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")


def download_audio(url: str)-> Dict:
    yt = YouTube(url, on_progress_callback=on_progress)
    print(yt.title)

    ys = yt.streams.get_audio_only()
    ys.download(directories.raw)

    return {"video_name" : yt.title, "id" : yt.video_id}

def clip_audio_file(audio:str, id:str, time:int = 20)-> List[Dict]:
    seconds = time * 1000
    audio = AudioSegment.from_file(directories.raw / str(audio + ".m4a"), "m4a")

    total_duration = len(audio)
    files = []
    for i in range(0, total_duration, seconds):
        file_handle = audio[i : i + seconds].export(directories.processed / f'audio_{i}.wav', format='wav')
        files.append({
            "video_id" : id,
            "start_time" : i / 1000,
            "end_time" : (i + seconds) / 1000,
            "file_path" : file_handle.name,
            "url" : f"https://www.youtube.com/watch?v={id}&t={i/1000}s"

        })

    return files

def transcribe_audio(clips: List[Dict])-> List[Dict]:
    model = whisper.load_model("base")

    for clip in clips:
        text = model.transcribe(clip["file_path"], fp16=False)["text"]
        clip["text"] = text
    return clips


def create_embeddings(transcript_list: List[Dict]) -> List[List[float]]:
    """Generate embeddings locally using sentence-transformers."""

    # Extract text from dictionary
    texts = [d["text"] for d in transcript_list]

    # Generate embeddings
    model = SentenceTransformer("all-MiniLM-L6-v2")
    return model.encode(texts).tolist()


def format_embeddings(embeddings, metadata_list=None):
    """
    Converts a list of embeddings into the required format for Pinecone upsert.

    :param embeddings: List of embedding vectors (each is a list of floats).
    :param ids: List of unique IDs corresponding to each embedding.
    :param metadata_list: (Optional) List of metadata dictionaries, one per embedding.
    :return: List of formatted dictionaries.
    """
    formatted_vectors = []

    for i, embedding in enumerate(embeddings):
        vector_data = {
            "id": f"{i}",
            "values": embedding,
            "metadata": metadata_list[i]
        }

        if metadata_list and i < len(metadata_list):
            vector_data["metadata"] = metadata_list[i]

        formatted_vectors.append(vector_data)

    return formatted_vectors


def create_vector_database(embeddings: List[Dict]):
    #todo finish vector database
    # Initialize Pinecone

    pc = Pinecone(PINECONE_API_KEY)
    index_name = "audio-embeddings"
    if not pc.has_index(index_name):
        pc.create_index(name=index_name, dimension=384, metric="cosine", spec=ServerlessSpec("aws", "us-east-1"))

    # Initialize index client
    index = pc.Index(name=index_name)

    # View index stats
    index.describe_index_stats()
    index.upsert(embeddings)

    print("Creating vector database Successful")   

def process_video(input_video: str) -> None:
    
    audio_dict = download_audio(input_video)
    clips = clip_audio_file(audio_dict["video_name"], audio_dict["id"])
    transcriptions = transcribe_audio(clips)
    embeddings = create_embeddings(transcriptions)
    formated_embeddings = format_embeddings(embeddings, transcriptions)
    create_vector_database(formated_embeddings)
    print("Embeddings Created")
    
    return input_video


if __name__ == "__main__":
    process_video("https://www.youtube.com/watch?v=IELMSD2kdmk")
    