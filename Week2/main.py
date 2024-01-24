from constants import *

import moviepy.editor as mp
import csv
import random

def get_random_choices():
    with open(f'{path}/would-you-rather.csv', newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter='*', quotechar='|')
        choices = random.sample(list(reader), 2)
    csvfile.close()
    return choices


def textBox(text="text", fontsize=40, backOpacity=.5, y=0, width=0, height=0, duration=5, startTime=0, w=1080, h=1920):
        """
        Creates a text clip with a background color and a black outline
        params:
                text: the text to be displayed
                fontsize: the size of the text
                backOpacity: the opacity of the background
                y: the y position of the text
                width: the width of the background
                height: the height of the background
                duration: the duration of the clip
                startTime: the start time of the clip
                w: the width of the video
                h: the height of the video
        """
        Ratio = int(w / videowidth)
        text_clip = mp.TextClip(text, 
                                font='Amiri-regular', 
                                color='white', 
                                fontsize=fontsize * Ratio, 
                                size=((videowidth-width) * Ratio, (height) * Ratio), 
                                method='caption')
        text_clip = text_clip.on_color(size=(text_clip.w, text_clip.h+20), 
                                color=(0,0,0), 
                                pos=(0,'center'), 
                                col_opacity=backOpacity)
        text_clip = text_clip.set_pos(lambda t: ((w-text_clip.w)/2, (h-text_clip.h)/y))
        text_clip = text_clip.set_duration(duration)
        text_clip = text_clip.set_start(startTime)

        return text_clip

def main():
        # make default background video with the top red, and bottom blue using videowidth, videoheight
        # make a text clip with the text "Would you rather?" in the middle of the screen

        background = mp.ColorClip((videowidth, videoheight), color=(255,0,0))
        half_mask = mp.ColorClip((videowidth, int(videoheight/2)), color=(0,0,255))
        background = mp.CompositeVideoClip([background, half_mask.set_pos((0, videoheight/2))])
        background = background.set_duration(iterations*videoLength)

        text_clips = []
        for iter in range(iterations):
                choices = get_random_choices()

                for i, choice in enumerate(choices):
                        text_clip = textBox(choice[0], 
                                                  fontsize=80, 
                                                  backOpacity=0.0, 
                                                  y=(i*40)+1.5,
                                                  width=0, 
                                                  height=500, 
                                                  duration=3, 
                                                  startTime=iter*videoLength)
                        text_clips.append(text_clip)

        final_clip = mp.CompositeVideoClip([background, *text_clips])
        final_clip.write_videofile(f'{path}/would-you-rather.mp4', fps=24, codec='libx264')

if __name__ == "__main__":
    main()