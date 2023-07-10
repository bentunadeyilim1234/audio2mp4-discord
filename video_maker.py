from moviepy.editor import *
import os
import random

def generate(audio_file, text_override=None):
    audio = AudioFileClip(audio_file)
    duration = audio.duration

    textContent = text_override or os.path.basename(audio_file).split('/')[-1]
    text_clip = TextClip(textContent, font="Arial-Medium", color="white", fontsize=30)
    screenSize = (text_clip.w + 30, text_clip.h + 5)

    video = ColorClip(screenSize, color=(0, 0, 0)).set_duration(duration)

    text_clip = text_clip.set_position("center").set_duration(duration)
    video = CompositeVideoClip([video, text_clip])

    video = video.set_audio(audio)
    
    path = f"data/{random.randint(000000, 999999)}.mp4"
    video.write_videofile(path, codec="libx264", audio_codec="aac", fps=1)
    
    return path