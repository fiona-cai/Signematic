from moviepy.editor import *
import youtube_dl

# Download video from YouTube
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': 'video.mp4',
    'postprocessors': [{
        'key': 'FFmpegVideoConvertor',
        'preferedformat': 'mp4',
    }],
}

with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download(['Your YouTube video URL here'])

# Convert mp4 to mp3
video_clip = VideoFileClip('video.mp4')
audio_clip = video_clip.audio
audio_clip.write_audiofile('audio.mp3')

# Close the clips
video_clip.close()
audio_clip.close()
