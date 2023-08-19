import googleapiclient
import googleapiclient.discovery
from django.conf import settings
from google.oauth2.credentials import Credentials
from googleapiclient.http import MediaFileUpload


def get_gdrive_folder_id(credentials: Credentials) -> str:
    drive = googleapiclient.discovery.build("drive", "v3", credentials=credentials)

    folders = []
    page_token = None

    while True:
        response = (
            drive.files()
            .list(
                q=f"mimeType='application/vnd.google-apps.folder' and name = '{settings.GOOGLE_DRIVE_FOLDER_NAME}' and trashed=false",
                spaces="drive",
                fields="nextPageToken, files(id, name)",
                pageToken=page_token,
            )
            .execute()
        )

        folders.extend(response.get("files", []))

        page_token = response.get("nextPageToken", None)

        if not page_token:
            break

    if folders:
        folder_id = folders[0]["id"]

    else:
        file_metadata = {"name": settings.GOOGLE_DRIVE_FOLDER_NAME, "mimeType": "application/vnd.google-apps.folder"}

        folder_id = drive.files().create(body=file_metadata, fields="id").execute()["id"]

    return folder_id


def uploadImage(credentials, src_image, save_image_name, mime_type, folder_id):
    drive = googleapiclient.discovery.build("drive", "v3", credentials=credentials)

    file_metadata = {"name": save_image_name, "parents": [folder_id]}
    media = MediaFileUpload(src_image, mimetype=mime_type)

    drive.files().create(body=file_metadata, media_body=media, fields="id").execute()

    return True


if __name__ == "__main__":
    ...
