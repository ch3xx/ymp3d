import youtube_dl
from modules import database


def download_mp3(url: str, process_id: str) -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '320',
        }],
        'outtmpl': rf'downloads\{url.split("watch?v=")[-1]}.mp3'
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        try:
            a = ydl.download([url])
        except:
            pass

    database.change_status(process_id)
