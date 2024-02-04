import os

DEBUG = True

PATH = "Week3"

VIDEO_DIR = f"{PATH}/Videos"
if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)

IMAGE_DIR = f"{PATH}/Images"
if not os.path.exists(IMAGE_DIR):
    os.makedirs(IMAGE_DIR)

###############################
####### VIDEO CONSTANTS #######
###############################
NUM_ITERATIONS = 0

# Set the dimensions of the phone screen
PHONE_WIDTH = 1080
PHONE_HEIGHT = 1920
