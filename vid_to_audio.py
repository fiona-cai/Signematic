import os
from moviepy.editor import *


def vid2audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)
    video.close()


vid2audio("videos/soheil_test.mp4", "audios/soheil_test.mp3")
