import os
import sys
from video2text import download_video_and_audio, generate_subtitles
from word2signvid import save_signed_video
from .stitchMP4 import create_video

video_file, audio_file = download_video_and_audio("America Ferrera's Iconic Barbie Speech", 152)

text = generate_subtitles(audio_file)

print("Converted Text:")
print(text)

with open('subtitles.txt', 'w') as file:
    # Write the content of 'text' to the file
    file.write(text)
    
    
f = open("subtitles-1.txt", "r")
text = f.read()
text = text.replace(";", " ")
list_of_words = text.lower().split(" ")

for word in list_of_words:
    save_signed_video(word)
    
create_video(path="videos/", video_files="video_list.txt", subtitle_file="subtitles-1.txt", logo_file="images/America-Ferrera.png")

