from pytubefix import YouTube
from pytubefix.cli import on_progress
from src.config.directories import directories
from pydub import AudioSegment
import whisper
from typing import List
import numpy as np


def download_audio(url: str)-> dict:
    yt = YouTube(url, on_progress_callback=on_progress)
    print(yt.title)

    ys = yt.streams.get_audio_only()
    ys.download(directories.raw)

    return {"video_name" : yt.title, "id" : yt.video_id}

def clip_audio_file(audio:str, id:str, time:int = 20)-> List[dict]:
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

def transcribe_audio(clips: List[dict])-> List[dict]:
    model = whisper.load_model("base")
    texts = []

    for clip in clips:
        text = model.transcribe(clip["file_path"])["text"]
        clip["text"] = text
    return clips


if __name__ == "__main__":
    audio_dict = download_audio("https://www.youtube.com/watch?v=IELMSD2kdmk")
    clips = clip_audio_file(audio_dict["video_name"], audio_dict["id"])
    transcriptions = transcribe_audio(clips)

    for idx, text in enumerate(transcriptions):
        print(f"Clip {idx+1}: {text}")