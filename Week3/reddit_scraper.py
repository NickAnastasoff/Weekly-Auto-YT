import requests
import re
import os
import json

from colorama import init, Fore, Style

init(autoreset=True)


def get_subreddit(subreddit="programminghumor", sort="top", t="day"):
    print(Fore.YELLOW + "============================")
    print(Fore.GREEN + f"Getting json from {subreddit}...")
    url = f"https://www.reddit.com/r/{subreddit}/{sort}.json?t={t}"
    response = requests.get(url, headers={"User-agent": "<3"})
    if response.status_code == 200:
        print(Fore.GREEN + f"Successfully got json from {subreddit}!")
    else:
        raise Exception(
            Fore.RED + "Error getting json from subreddit!\n" + response.text
        )
    return json.loads(response.text)


def get_post_info(index, data):
    print(Fore.YELLOW + "============================")
    print(Fore.GREEN + f"Getting post info from index {index}...")
    post_data = data["data"]["children"][index]["data"]
    url = post_data["url"]
    title = post_data["title"]
    print(Fore.GREEN + f"Successfully got post info from index {index}!")
    return url, title


def get_comments(index, data, num_comments=1):
    print(Fore.YELLOW + "============================")
    print(Fore.GREEN + f"Getting json for {index}...")
    url = (
        f'https://reddit.com{data["data"]["children"][index]["data"]["permalink"]}.json'
    )
    response = requests.get(url, headers={"User-agent": "<3"})
    if response.status_code == 200:
        print(Fore.GREEN + f"Successfully got json for {index}!")
    else:
        raise Exception(Fore.RED + "Error getting comments!\n" + response.text)
    data = json.loads(response.text)
    comments = []
    for i in range(num_comments):
        comment = data[1]["data"]["children"][i]["data"]["body"]
        comments.append(comment)
    return comments


def download_image(url="", title="", index=None, data=None):
    if index is not None and data is not None:
        url, title = get_post_info(index, data)
    print(Fore.YELLOW + "============================")
    print(Fore.GREEN + f"Downloading {title} from {url}...")
    response = requests.get(url, headers={"User-agent": "your bot 0.1"})
    if response.status_code == 200:
        print(Fore.GREEN + f"Successfully downloaded {title} from {url}!")
    else:
        raise Exception(Fore.RED + "Error downloading image!\n" + response.text)
    # Remove special characters from title
    safe_title = re.sub(r"[^a-zA-Z0-9]+", "_", title)
    return safe_title, response.content


def download_top(subreddit="programminghumor", num_images=1, t="week", data=None):
    print(Fore.YELLOW + "============================")
    print(
        Fore.GREEN
        + f"Downloading {num_images} top images from r/{subreddit} from the past {t}..."
    )
    if data is None:
        data = get_subreddit(subreddit, t=t)
    responses = []
    for i in range(num_images):
        url, title = get_post_info(i, data)
        responses.append(download_image(url, title))
    print(
        Fore.GREEN
        + f"Successfully downloaded {num_images} top images from r/{subreddit} from the past {t}!"
    )
    return responses
