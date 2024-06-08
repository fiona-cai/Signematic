from requests import get
import os
import yt_dlp as youtube_dl
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch

YDL_OPTIONS = {'format': 'bestvideo+bestaudio', 'noplaylist': 'True'}

def download_video(song, time_length):
    results = YoutubeSearch(song, max_results=10).to_dict()

    for data in results:
        if len(data['duration'].split(":")) < 3:
            time = (int(data["duration"].split(":")[0]) * 60) + int(data["duration"].split(":")[1])
            if abs(int(time) - int(time_length)) < 3:
                title = data["title"]
                with YoutubeDL(YDL_OPTIONS) as ydl:
                    try:
                        get(title)
                    except:
                        video = ydl.extract_info(f"ytsearch:{title}", download=True)['entries'][0]
                    else:
                        video = ydl.extract_info(title, download=True)
                filename = os.path.splitext(ydl.prepare_filename(video))[:-1]
                break
    return ''.join(filename) + ".mp4"


video_file = download_video("Comparing WATERLOO Housing Prices | Village1/UWP", 378)
