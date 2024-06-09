from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.editor import VideoFileClip

def crop_square(video_file):
    clip = VideoFileClip(video_file)
    width, height = clip.size
    min_dimension = min(width, height)

    # Crop to square
    cropped_clip = clip.crop(
        width=min_dimension,
        height=min_dimension,
        x_center=clip.w/2,
        y_center=clip.h/2
    )

    # Save the cropped video
    cropped_clip.write_videofile("cropped_" + video_file)

crop_square("videos/beautiful.mp4")