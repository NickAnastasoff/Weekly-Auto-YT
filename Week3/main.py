from reddit_scraper import *
from PIL import Image
from constants import *
import os
from io import BytesIO
from edit import make_clip
import moviepy.editor as mp
from edgeTTS import speak
from PIL import Image
from PIL import PngImagePlugin
from io import BytesIO

# first we need to get the meme
data = get_subreddit(subreddit=SUBREDDIT, sort="top", t="week")
memes = download_top(num_images=NUM_ITERATIONS, t="week", data=data)

# then we need to get the comments from the meme
for i in range(NUM_ITERATIONS):
    try:
        comments = get_comments(i, data, num_comments=3)
        comments = [comment.encode("ascii", "ignore").decode() for comment in comments]
        remove_list = [
            "/",
            "\n",
            "\r",
            "\t",
            "\b",
            "\f",
            "\v",
            "~",
            ">",
            "<",
            "@",
            "$",
            "%",
            "^",
            "(",
            ")",
            "_",
            "{",
            "}",
            "[",
            "]",
            "|",
            "\\",
            ":",
            ";",
            "'",
            '"',
            ",",
            ".",
            "<",
            ">",
        ]
        for remove in remove_list:
            comments = [comment.replace(remove, "") for comment in comments]
        comments = [comment.split("Edit:")[0] for comment in comments]
        for _, comment in enumerate(comments):
            # check for bots
            if "I am a bot" not in comment:
                index = _
                break

        image_data = BytesIO(memes[i][index])
        image = Image.open(image_data)

        # Save the comment as metadata in the image file
        metadata = PngImagePlugin.PngInfo()
        metadata.add_text("comment", comments[index])
        image.save(f"{IMAGE_DIR}/{i}.png", pnginfo=metadata)
    except:
        print(f"Error on {i}")
        continue

clips = []

for image in os.listdir(IMAGE_DIR):
    if image.endswith(".png"):
        comment = Image.open(f"{IMAGE_DIR}/{image}").info["comment"]
        print("speaking: ", comment)
        print("============================")
        speak(comment, f"{VIDEO_DIR}/temp.mp3")
        clip = make_clip(f"{IMAGE_DIR}/{image}", f"{VIDEO_DIR}/temp.mp3")
        clips.append(clip)

os.remove(f"{VIDEO_DIR}/temp.mp3")

final_clip = mp.concatenate_videoclips(clips)
final_clip.write_videofile(f"{VIDEO_DIR}/final.mp4", fps=24)
