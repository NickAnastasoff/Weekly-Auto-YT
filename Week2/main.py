import csv
import random
import moviepy.editor as mp
from constants import *
from moviepy.editor import concatenate_videoclips
from pexels import get_best_images
import os

def get_random_choices():
    """
    Gets two random choices from the would-you-rather.csv file.
    """
    
    with open(f"{path}/would-you-rather.csv", newline="") as csvfile:
        reader = csv.reader(csvfile, delimiter="*", quotechar="|")
        choices = random.sample(list(reader), 2)
    return choices

def text_box(
    text="text",
    fontsize=40,
    opac=0.5,
    y=0,
    width=0,
    height=0,
    duration=5,
    start_time=0,
    w=1080,
    h=1920,
):

    """
    Creates a text clip with a background color and a black outline.

    Args:
        text: The text to be displayed.
        fontsize: The size of the text.
        opac: The opacity of the background.
        y: The y position of the text.
        width: The width of the background.
        height: The height of the background.
        duration: The duration of the clip.
        start_time: The start time of the clip.
        w: The width of the video.
        h: The height of the video.

    Returns:
        A text clip with the specified properties.
    """
    ratio = int(w / video_width)
    text_clip = mp.TextClip(
        text,
        font="Amiri-regular",
        color="white",
        fontsize=fontsize * ratio,
        size=((video_width - width) * ratio, (height) * ratio),
        method="caption",
    )
    text_clip = text_clip.on_color(
        size=(text_clip.w, text_clip.h + 20),
        color=(0, 0, 0),
        pos=(0, "center"),
        col_opacity=opac,
    )
    text_clip = text_clip.set_pos(
        lambda t: ((w - text_clip.w) / 2, (h - text_clip.h) / y)
    )
    text_clip = text_clip.set_duration(duration)
    text_clip = text_clip.set_start(start_time)

    return text_clip


def text_clip_from_choices(choices):
    """
    Creates a list of text clips from a list of choices.
    Args:
        choices: A list of choices.
    """
    text_clips = []
    for i, choice in enumerate(choices):
        text_clip = text_box(
            choice[0],
            fontsize=80,
            opac=0.0,
            y=(i * 40) + 1.5,
            width=0,
            height=500,
            duration=video_length,
            start_time=0,
        )
        text_clips.append(text_clip)
    return text_clips
  
def resized_image_clip(image, duration=5, start_time=0, h=384, y=0):
    """
    Creates a resized image clip with a black outline.

    Args:
        image: The image to be displayed.
        duration: The duration of the clip.
        start_time: The start time of the clip.
        h: The height of the video.
        y: The y position of the image.

    Returns:
        A resized image clip with the specified properties.
    """
    image_clip = mp.ImageClip(image).set_duration(duration)
    image_clip = image_clip.set_start(start_time)
    image_clip = image_clip.set_pos(lambda _: ((video_width - image_clip.w) / 2, y))
    return image_clip


def make_background(top):
    """
    Creates a background clip with a red top, blue bottom and switch a side to green at the end.
    """
    green_back = mp.ColorClip(
        (video_width, video_height), color=(0, 255, 0)
    ).set_duration(video_length)
    red_mask = mp.ColorClip(
        (video_width, int(video_height / 2)), color=(255, 0, 0)
    ).set_duration(video_length - green_length * top)
    blue_mask = mp.ColorClip(
        (video_width, int(video_height / 2)), color=(0, 0, 255)
    ).set_duration(video_length - green_length * (1 - top))
    background = mp.CompositeVideoClip(
        [green_back, blue_mask.set_pos((0, video_height / 2)), red_mask.set_pos((0, 0))]
    )
    return background


def main():
    final_clips = []
    for iteration in range(iterations):
        choices = get_random_choices()
        # find longest words in sentence
        longest_words = [
            sorted(choice[0].split(), key=len, reverse=True) for choice in choices
        ]
        get_best_images(longest_words)
        image_clips = resized_image_clip(
            "Week2/images/0.jpg", y=384 * 1.5
        ), resized_image_clip("Week2/images/1.jpg", y=384 * 3.5)
        text_clips = text_clip_from_choices(choices)
        background = make_background(random.randint(0, 1))

        # play tick.mp3 until the start of green_length
        tick = (
            mp.AudioFileClip(f"{sfx}/tick.mp3")
            .set_start(0)
            .set_end(video_length - green_length)
        )
        correct = mp.AudioFileClip(f"{sfx}/correct.mp3").set_start(
            video_length - green_length
        )
        audio_clip = mp.concatenate_audioclips([tick, correct])

        background = background.set_audio(audio_clip)

        final_clip = mp.CompositeVideoClip([background, *image_clips, *text_clips])
        final_clips.append(final_clip)

    combined_clip = concatenate_videoclips(final_clips)
    combined_clip.write_videofile(
        f"{path}/would-you-rather.mp4", fps=24, codec="libx264"
    )
    # delete images folder
    os.system("rm -rf Week2/images")

if __name__ == "__main__":
    main()
