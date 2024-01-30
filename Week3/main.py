from reddit_scraper import *
from PIL import Image
from constants import *
import os
from io import BytesIO

# so the plan is to have minecraft parkor maps as the background
# then have the meme on top of it
# then have the comments on the meme read out loud

# we need to get the parkor map video as mp4
if not os.path.exists(VIDEO_DIR):
    os.makedirs(VIDEO_DIR)
    raise Exception("ADD VIDEOS!")

# first we need to get the meme
data = get_subreddit(sort="top", t="week")
memes = download_top(num_images=1, t="week", data=data)

# then we need to get the comments from the meme
for i in range(NUM_ITERATIONS):
    comment = get_comments(i, data, num_comments=1)
    image_data = BytesIO(memes[i][1])
    image = Image.open(image_data)
    image.show()
    print(comment)
