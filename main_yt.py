import os
import sys
from .video2text import download_video_and_audio, generate_subtitles

video_file, audio_file = download_video_and_audio("America Ferrera's Iconic Barbie Speech", 152)

text = generate_subtitles(audio_file)

print("Converted Text:")
print(text)

with open('subtitles.txt', 'w') as file:
    # Write the content of 'text' to the file
    file.write(text)
    
    