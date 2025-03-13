from pytubefix import YouTube
from pytubefix.cli import on_progress
from src.config.directories import directories
from pydub import AudioSegment
import whisper


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
    all_clips = []

    for i in range(0, total_duration, seconds):
        audio_clip = audio[i:i+seconds]
        all_clips.append(audio_clip)

    return all_clips



if __name__ == "__main__":
    audio = download_audio("https://www.youtube.com/watch?v=CWeSzhJpJ9U")
    clips = clip_audio_file(audio)