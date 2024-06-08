from pytube import YouTube
from moviepy.editor import *

# Function to download YouTube video and convert it to MP3
def download_youtube_video_as_mp3(youtube_link, mp3_file_path):
    # Download video from YouTube
    yt = YouTube(youtube_link)
    video = yt.streams.filter(only_audio=True).first().download()

    # Load the downloaded video
    video_clip = VideoFileClip(video)
    
    # Save the audio from the video as an MP3
    video_clip.audio.write_audiofile(mp3_file_path)
    video_clip.close()

# YouTube video URL
youtube_link = 'Your YouTube video link here'

# Path to save the MP3 file
mp3_file_path = "audio.mp3"

# Download the video and save as MP3
download_youtube_video_as_mp3(youtube_link, mp3_file_path)
