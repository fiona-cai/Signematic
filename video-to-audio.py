from moviepy.editor import *

# Function to convert MP4 to MP3
def convert_mp4_to_mp3(mp4_file_path, mp3_file_path):
    video = VideoFileClip(mp4_file_path)
    video.audio.write_audiofile(mp3_file_path)
    video.close()

# Paths to your mp4 and mp3 files
video_file_path = "video.mp4"  # The video file is always named 'video.mp4'
audio_file_path = "audio.mp3"  # The audio file will be saved as 'audio.mp3'

# Convert the video and save as audio
convert_mp4_to_mp3(video_file_path, audio_file_path)
