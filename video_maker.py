from moviepy.editor import *
import os, json

with open("settings.json", "r", encoding='utf-8', errors='ignore') as f:
    settings = json.load(f)["videoSettings"]

bgColor, textColor, fontName, fontSize, textSpacing = tuple(settings["backgroundColor"]), settings["foreColor"], settings["font"], settings["fontSize"], tuple(settings["spacing"])

def generate(audio_file, text_override=None):
    audio = AudioFileClip(audio_file)
    duration = audio.duration

    path_origin = os.path.basename(audio_file).split('/')[-1]
    textContent = text_override or path_origin
    text_clip = TextClip(textContent, font=fontName, color=textColor, fontsize=fontSize)
    screenSize = tuple(map(sum,zip((text_clip.w, text_clip.h),textSpacing))) #tuple(lambda i, j: i + j, tuple((text_clip.w, text_clip.h)), textSpacing) #(text_clip.w + 30, text_clip.h + 5)

    video = ColorClip(screenSize, color=bgColor).set_duration(duration)

    text_clip = text_clip.set_position("center").set_duration(duration)
    video = CompositeVideoClip([video, text_clip])

    video = video.set_audio(audio)
    
    path = f"data/{path_origin}.mp4"
    video.write_videofile(path, codec="mpeg4", fps=1)
    
    return path