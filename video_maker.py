from moviepy.editor import *
import os
import random

def generate(audio_file, text_override=None):
    audio = AudioFileClip(audio_file)
    duration = audio.duration

    path_origin = os.path.basename(audio_file).split('/')[-1]
    textContent = text_override or path_origin
    text_clip = TextClip(textContent, font="Arial-Medium", color="white", fontsize=30)
    screenSize = (text_clip.w + 30, text_clip.h + 5)

    video = ColorClip(screenSize, color=(0, 0, 0)).set_duration(duration)

    text_clip = text_clip.set_position("center").set_duration(duration)
    video = CompositeVideoClip([video, text_clip])

    video = video.set_audio(audio)
    
    path = f"data/{path_origin}.mp4"
    video.write_videofile(path, codec="mpeg4", fps=1)
    
    return path