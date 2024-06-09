import os
import subprocess
import time
from moviepy.editor import *
import moviepy.video.fx.all as vfx

path = "videos/"
video_files = "video_list.txt"

f = open("subtitles-1.txt", "r")
text = f.read()
list_of_words = text.lower().split(";")

files = []
idx = 0

for i in range(len(list_of_words)):
    word = list_of_words[i].split(" ")
    for file in os.listdir(path):
        if file.endswith(".mp4") and file.split(".")[0] in word:
            try:
                files.append(VideoFileClip(path + file))
            except:
                print("Error: " + file)
    final = concatenate_videoclips(files)
    final = final.fx(vfx.speedx, 3)
    final.write_videofile("output" + str(i) + ".mp4", codec="libx264", audio_codec="aac")

files = []

for i in range(len(list_of_words)):
    files.append(VideoFileClip("output" + str(i) + ".mp4"))

final = concatenate_videoclips(files)
final.write_videofile("output.mp4", codec="libx264", audio_codec="aac")