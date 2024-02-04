from moviepy.editor import *
from constants import PHONE_WIDTH, PHONE_HEIGHT
import numpy as np


def make_clip(image_path, audio_path=None):
    # Create a cream-colored background clip
    background = ColorClip(size=(PHONE_WIDTH, PHONE_HEIGHT), color=(255, 253, 208))

    # Create ImageClip from the numpy array
    image = ImageClip(image_path)

    # Resize image to match background size
    image = image.resize(width=PHONE_WIDTH).set_pos("center")

    # Overlay image on the background
    final_clip = CompositeVideoClip([background, image])

    if audio_path is not None:
        audio = AudioFileClip(audio_path)
        final_clip = final_clip.set_duration(audio.duration + 0.5)
        final_clip = final_clip.set_audio(audio)
    else:
        final_clip = final_clip.set_duration(2)

    return final_clip
