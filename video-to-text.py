from requests import get
import os
import yt_dlp as youtube_dl
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
import speech_recognition as sr
from pydub import AudioSegment


YDL_OPTIONS_VIDEO = {
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "noplaylist": "True",
}

YDL_OPTIONS_AUDIO = {
    "format": "bestaudio/best",
    "postprocessors": [
        {
            "key": "FFmpegExtractAudio",
            "preferredcodec": "wav",
        }
    ],
    "noplaylist": "True",
}


def download_video_and_audio(song, time_length):
    results = YoutubeSearch(song, max_results=15).to_dict()

    for data in results:
        if len(data["duration"].split(":")) < 3:
            time = (int(data["duration"].split(":")[0]) * 60) + int(
                data["duration"].split(":")[1]
            )
            if abs(int(time) - int(time_length)) < 3:
                title = data["title"]
                with YoutubeDL(YDL_OPTIONS_VIDEO) as ydl_video, YoutubeDL(
                    YDL_OPTIONS_AUDIO
                ) as ydl_audio:
                    try:
                        get(title)
                    except:
                        video_info = ydl_video.extract_info(
                            f"ytsearch:{title}", download=True
                        )["entries"][0]
                        audio_info = ydl_audio.extract_info(
                            f"ytsearch:{title}", download=True
                        )["entries"][0]
                    else:
                        video_info = ydl_video.extract_info(title, download=True)
                        audio_info = ydl_audio.extract_info(title, download=True)
                filename_video = os.path.splitext(
                    ydl_video.prepare_filename(video_info)
                )[:-1]
                filename_audio = os.path.splitext(
                    ydl_audio.prepare_filename(audio_info)
                )[:-1]
                break
    return "".join(filename_video) + ".mp4", "".join(filename_audio) + ".wav"


def speech_to_text(audio_file):
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError as e:
            return f"Error: {str(e)}"
        
        
video_file, audio_file = download_video_and_audio("English in a Minute: Grow Like a Weed", 60)

text = speech_to_text(audio_file)
print("Converted Text:")
print(text)
