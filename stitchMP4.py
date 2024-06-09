import os
from moviepy.editor import *
import moviepy.editor as mp
from moviepy.video.fx.all import crop
import moviepy.video.fx.all as vfx

def create_video(path="videos/", video_files="video_list.txt", subtitle_file="subtitles-1.txt", logo_file="images/America-Ferrera.png"):
    f = open(subtitle_file, "r")
    text = f.read()
    list_of_words = text.lower().split(";")

    files = []
    idx = 0

    for i in range(len(list_of_words)):
        files = []
        word = list_of_words[i].split(" ")
        for file in os.listdir(path):
            if file.endswith(".mp4") and file.split(".")[0] in word:
                try:
                    files.append(VideoFileClip(path + file))
                except:
                    print("Error: " + file)
        final = concatenate_videoclips(files)
        final = final.fx(vfx.speedx, 3)
        final.write_videofile("outputs/output" + str(i) + ".mp4", codec="libx264", audio_codec="aac")

    files = []

    for i in range(len(list_of_words)):
        files.append(VideoFileClip("outputs/output" + str(i) + ".mp4"))

    final = concatenate_videoclips(files)
    (w,h) = final.size
    logo = (mp.ImageClip(logo_file)
              .set_duration(final.duration)
              .resize(height=100)
              .margin(right=8, top=8, opacity=0) # (optional) logo-border padding
              .set_pos(("center","top")))
    final = crop(final, width=500, height=1000, x_center=w/2, y_center=h/2)
    final = CompositeVideoClip([final, logo])
    final.write_videofile("outputs/output.mp4", codec="libx264", audio_codec="aac")
