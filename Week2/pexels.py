import requests
import os
import PIL
import io

PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY")


def search_videos(query_string, orientation_landscape=True):
    url = "https://api.pexels.com/videos/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {
        "query": query_string,
        "orientation": "landscape" if orientation_landscape else "portrait",
        "per_page": 15,
    }

    response = requests.get(url, headers=headers, params=params)
    json_data = response.json()
    return json_data


def get_best_video(query_string, orientation_landscape=True, used_vids=[]):
    vids = search_videos(query_string, orientation_landscape)
    videos = vids["videos"]  # Extract the videos list from JSON

    # Filter and extract videos with width and height as 1920x1080 for landscape or 1080x1920 for portrait
    if orientation_landscape:
        filtered_videos = [
            video
            for video in videos
            if video["width"] >= 1920
            and video["height"] >= 1080
            and video["width"] / video["height"] == 16 / 9
        ]
    else:
        filtered_videos = [
            video
            for video in videos
            if video["width"] >= 1080
            and video["height"] >= 1920
            and video["height"] / video["width"] == 16 / 9
        ]

    # Sort the filtered videos by duration in ascending order
    sorted_videos = sorted(filtered_videos, key=lambda x: abs(15 - int(x["duration"])))

    # Extract the top 3 videos' URLs
    for video in sorted_videos:
        for video_file in video["video_files"]:
            if orientation_landscape:
                if video_file["width"] == 1920 and video_file["height"] == 1080:
                    if not (video_file["link"].split(".hd")[0] in used_vids):
                        return video_file["link"]
            else:
                if video_file["width"] == 1080 and video_file["height"] == 1920:
                    if not (video_file["link"].split(".hd")[0] in used_vids):
                        return video_file["link"]
    print("NO LINKS found for this round of search with query :", query_string)
    return None


def search_images(query_string):
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query_string, "per_page": 1}

    response = requests.get(url, headers=headers, params=params)
    json_data = response.json()
    return json_data


def get_best_images(query_strings):
    if not os.path.exists("Week2/images"):
        os.mkdir("Week2/images")
    for i, query in enumerate(query_strings):
        for _ in query:
            try:
                imgs = search_images(query)
                image = imgs["photos"][0]["src"]["original"]
                image = requests.get(image).content
                break
            except:
                print("NO LINKS found for this round of search with query :", query)
                continue
        # resize to 384 height
        image = PIL.Image.open(io.BytesIO(image))
        w, h = image.size
        new_h = 384
        new_w = int(new_h * w / h)
        image = image.resize((new_w, new_h))

        # put in Week2/images
        image.save(f"Week2/images/{i}.jpg")


#     image_urls = []
# json_data = search_images("c")
# for photo in json_data['photos']:
#     image_urls.append(photo['src']['large'])

# if not os.path.exists("Week2/images"):
#     os.mkdir("Week2/images")
# # download to Week2/images
# response = requests.get(image_urls[0])
# with open(f"Week2/images/0.jpg", "wb") as f:
#     f.write(response.content)
