import os
import subprocess
import time

base_dir = "videos/"
video_files = "video_list.txt"
output_file = "output.avi"

file_list = open(video_files, "w")

try:
    os.remove(output_file)
except OSError:
    pass

f = open("subtitles-1.txt", "r")
text = f.read()
list_of_words = text.lower().split(";")
files = list_of_words[0].split(" ")

start = time.time()
for root, dirs in os.walk(base_dir):
    for video in files:
        if video.endswith(".mp4"):
            file_list.write("file './%s'\n" % video)
file_list.close()

# merge the video files
cmd = ["ffmpeg",
       "-f",
       "concat",
       "-safe",
       "0",
       "-loglevel",
       "quiet",
       "-i",
       "%s" % video_files,
       "-c",
       "copy",
       "%s" % output_file
       ]

p = subprocess.Popen(cmd, stdin=subprocess.PIPE)

fout = p.stdin
fout.close()
p.wait()

print(p.returncode)
if p.returncode != 0:
    raise subprocess.CalledProcessError(p.returncode, cmd)

end = time.time()
print("Merging the files took", end - start, "seconds.")