#!/usr/bin/python3
import json

import cv2
import random
import moviepy.editor as mp
import os
from youtube import upload
from constants import *
from gemini import prompt
from pexels import get_best_video
import requests

music = mp.AudioFileClip(f"{pathToMusic}/{(random.choice([f for f in os.listdir(pathToMusic) if not f.endswith('.DS_Store')]))}")

def textBox(text, fontsize, backOpacity, y, width, height, duration, startTime, w, h, Ratio):
		# Create a text clip
		text_clip = mp.TextClip(text, font='Amiri-regular', color='white', fontsize=fontsize * Ratio, size=((phonewidth-width) * Ratio, (height) * Ratio), method='caption')

		# Add a background color to the text clip
		text_clip = text_clip.on_color(size=(text_clip.w, text_clip.h+20), color=(0,0,0), pos=(0,'center'), col_opacity=backOpacity)

		# Move the text clip to the desired position
		text_clip = text_clip.set_pos(lambda t: ((w-text_clip.w)/2, (h-text_clip.h)/y))

		# Set the duration of the text clip
		text_clip = text_clip.set_duration(duration)

		# Set the start time of the text clip
		text_clip = text_clip.set_start(startTime)

		return text_clip

def main():
	if not os.path.exists(pathToRun):
		os.makedirs(pathToRun)

	musicDuration = music.duration
	start_time = random.uniform(0, musicDuration - videoLength)
	clip = music.subclip(start_time, start_time + videoLength)
	clip.write_audiofile(f"{pathToRun}/random_clip.wav")

	response = prompt(prompt_text)
	print(response)
	response = json.loads(response)
	title = response['Title']
	openingText = response['Start']
	endingText = response['End']
	background = response['Background']
	print("video title: " + title)
	print("opening text: " + openingText)
	print("ending text: " + endingText)
	print("background: " + background)

	# Get the video
	video_url = get_best_video(background, False)
	with open(f"{pathToRun}/background.mp4", 'wb') as f:
		f.write(requests.get(video_url).content)
				
	clip = mp.VideoFileClip(f"{pathToRun}/background.mp4")
	videoDuration = clip.duration
	start_time = random.uniform(0, videoDuration - videoLength)
	subclip = clip.subclip(start_time, start_time + videoLength)
	subclip.write_videofile(f"{pathToRun}/clip.mp4", fps=clip.fps)
	cap = cv2.VideoCapture(f"{pathToRun}/clip.mp4")
	frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
	my_video = mp.VideoFileClip(subclip.filename, audio=True)
	w,h = my_video.size

	Ratio = int(w / phonewidth)

	print("screen ratio: "+str(Ratio))
	
	# Add the ending text
	end_txt_mov = textBox(endingText, 60, 0.5, 2, 100, 500, 5, 4, w, h, Ratio)

	# Add the opening text
	start_txt_mov = textBox(openingText, 60, 0.5, 2, 100, 500, 4, 0, w, h, Ratio)

	# Add the title
	title_mov = textBox(title, 70, 1, 4, 150, 100, 10, 0, w, h, Ratio)

	final = mp.CompositeVideoClip([my_video, start_txt_mov, end_txt_mov, title_mov])
	final_clip = final.set_audio(music)
	final_clip.subclip(0,6).write_videofile(f"{pathToRun}/Short.mov",codec='libx264')

	os.remove(f"{pathToRun}/clip.mp4")
	os.remove(f"{pathToRun}/random_clip.wav")
	os.remove(f"{pathToRun}/background.mp4")

	upload(title, videoDescription, f"{pathToRun}/Short.mov", pathToClient)

if __name__ == "__main__":
	main()