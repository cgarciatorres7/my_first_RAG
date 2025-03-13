from pytubefix import YouTube
from pytubefix.cli import on_progress
from src.config.directories import directories



def download_audio(url):
    yt = YouTube(url, on_progress_callback=on_progress)
    print(yt.title)

    ys = yt.streams.get_audio_only()
    ys.download(directories.raw)



if __name__ == "__main__":
    download_audio("https://www.youtube.com/watch?v=PQ2WjtaPfXU")