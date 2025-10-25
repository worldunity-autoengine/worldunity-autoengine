import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def main():
    print("\U0001f680 Starting real upload script.")
    secret_json = os.getenv("GOOGLE_CLIENT_SECRET")
    if not secret_json:
        print("\u274c Missing GOOGLE_CLIENT_SECRET environment variable.")
        return
    video_path = os.getenv("VIDEO_PATH")
    if not video_path or not os.path.exists(video_path):
        print(f"\u274c VIDEO_PATH not set or file not found: {video_path}")
        return
    video_title = os.getenv("VIDEO_TITLE", "Auto uploaded video")
    video_description = os.getenv("VIDEO_DESCRIPTION", "")
    video_privacy = os.getenv("VIDEO_PRIVACY_STATUS", "public")
    video_tags = os.getenv("VIDEO_TAGS", "")
    tags_list = [tag.strip() for tag in video_tags.split(",") if tag.strip()] if video_tags else None
    # load service account credentials from JSON
    try:
        info = json.loads(secret_json)
    except Exception as e:
        print("\u274c Failed to parse GOOGLE_CLIENT_SECRET:", e)
        return
    scopes = ["https://www.googleapis.com/auth/youtube.upload"]
    credentials = service_account.Credentials.from_service_account_info(info, scopes=scopes)
    youtube = build("youtube", "v3", credentials=credentials)
    body = {
        "snippet": {
            "title": video_title,
            "description": video_description,
        },
        "status": {
            "privacyStatus": video_privacy
        }
    }
    if tags_list:
        body["snippet"]["tags"] = tags_list
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")
    print(f"\u2705 Upload complete. Video ID: {response['id']}")


if __name__ == "__main__":
    main()
