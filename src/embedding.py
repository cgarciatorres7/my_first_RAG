from pytubefix import YouTube
from pytubefix.cli import on_progress
from src.config.directories import directories
from pydub import AudioSegment
import whisper
from typing import List
import numpy as np


def download_audio(url: str)-> str:
    yt = YouTube(url, on_progress_callback=on_progress)
    print(yt.title)

    ys = yt.streams.get_audio_only()
    ys.download(directories.raw)

    return yt.title

def clip_audio_file(audio:str, time:int = 20):
    seconds = time * 1000
    audio = AudioSegment.from_file(directories.raw / str(audio + ".m4a"), "m4a")

    total_duration = len(audio)
    files = []
    for i in range(0, total_duration, seconds):
        file_handle = audio[i : i + seconds].export(directories.processed / f'audio_{i}.wav', format='wav')
        files.append(file_handle.name)

    return files

def transcribe_audio(clips: List[str])-> List[str]:
    model = whisper.load_model("base")
    texts = []

    for clip in clips:
        text = model.transcribe(clip)["text"]
        texts.append(text)
    return texts


if __name__ == "__main__":
    audio = download_audio("https://www.youtube.com/watch?v=IELMSD2kdmk")
    clips = clip_audio_file(audio)
    transcriptions = transcribe_audio(clips)

    for idx, text in enumerate(transcriptions):
        print(f"Clip {idx+1}: {text}")