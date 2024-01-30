import datetime
from googleapiclient.http import MediaFileUpload
from google_apis import create_service


def upload(Title, videoDescription, video_file, client_file):
    API_NAME = "youtube"
    API_VERSION = "v3"
    SCOPES = ["https://www.googleapis.com/auth/youtube"]
    # SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    service = create_service(client_file, API_NAME, API_VERSION, SCOPES)

    upload_time = (
        datetime.datetime.now() + datetime.timedelta(days=0)
    ).isoformat() + ".000Z"
    request_body = {
        "snippet": {
            "title": Title,
            "description": videoDescription,
            "categoryId": "29",
            "tags": [],
        },
        "status": {
            "privacyStatus": "public",
            "publishedAt": upload_time,
            "selfDeclaredMadeForKids": False,
        },
        "notifySubscribers": False,
    }

    video_file = video_file
    media_file = MediaFileUpload(video_file)
    # print(media_file.size() / pow(1024, 2), 'mb')
    # print(media_file.to_json())
    # print(media_file.mimetype())

    response_video_upload = (
        service.videos()
        .insert(part="snippet,status", body=request_body, media_body=media_file)
        .execute()
    )
    uploaded_video_id = response_video_upload.get("id")

    video_id = uploaded_video_id
