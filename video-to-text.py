from requests import get
import os
import yt_dlp as youtube_dl
from yt_dlp import YoutubeDL
from youtube_search import YoutubeSearch
import speech_recognition as sr
from pydub import AudioSegment
import io


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
        
def transcribe_audio_to_text(audio_data):
    r = sr.Recognizer()

    # Use the audio data as the audio source
    with sr.AudioFile(audio_data) as source:
        audio = r.record(source)  # Read the entire audio file

    # Recognize speech using Google Speech Recognition
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

def split_audio_into_chunks(audio_file, chunk_length=3000):
    audio = AudioSegment.from_wav(audio_file)

    chunks = [audio[i:i + chunk_length] for i in range(0, len(audio), chunk_length)]
    chunk_data = []

    for chunk in chunks:
        chunk_file = io.BytesIO()
        chunk.export(chunk_file, format="wav")
        chunk_data.append(chunk_file.getvalue())

    return chunk_data

def generate_subtitles(audio_file):
    chunk_data = split_audio_into_chunks(audio_file)

    subtitles = ""
    for chunk in chunk_data:
        text = transcribe_audio_to_text(io.BytesIO(chunk))
        subtitles += "{0}\n".format(text)

    return subtitles


video_file, audio_file = download_video_and_audio("English in a Minute: Grow Like a Weed", 60)

text = generate_subtitles(audio_file)
print("Converted Text:")
print(text)
