from pytubefix import YouTube
from pytubefix.cli import on_progress
from src.config.directories import directories
from pydub import AudioSegment
import whisper
from typing import List, Dict
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer

import os
import requests

model = SentenceTransformer("all-MiniLM-L6-v2") # Reads HF_TOKEN from env


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
            "url" : f"https://www.youtube.com/watch?v={id}&t={i/1000}"

        })

    return files

def transcribe_audio(clips: List[Dict])-> List[Dict]:
    model = whisper.load_model("base")

    for clip in clips:
        text = model.transcribe(clip["file_path"])["text"]
        clip["text"] = text
    return clips


def create_embeddings(transcript_list: List[Dict]) -> List[List[float]]:
    """Generate embeddings locally using sentence-transformers."""

    # Extract text from dictionary
    texts = [d["text"] for d in transcript_list]

    # Generate embeddings
    return model.encode(texts).tolist()

if __name__ == "__main__":
    audio_dict = download_audio("https://www.youtube.com/watch?v=IELMSD2kdmk")
    clips = clip_audio_file(audio_dict["video_name"], audio_dict["id"])
    transcriptions = transcribe_audio(clips)
    embeddings = create_embeddings(transcriptions)

    print("Embeddings Created")

