from dotenv import load_dotenv
import os
from notion_client import Client
from notion_client.helpers import iterate_paginated_api
from coverformat import *
import json
import requests

load_dotenv()
notion = Client(auth=os.environ["NOTION_KEY"])

def create_file_upload():
    """
    Creates Notion File Upload object.
    
    Returns:
        file_upload_id (string): file upload id
    """

    file_create_response = requests.post("https://api.notion.com/v1/file_uploads", headers={
        "Authorization": f"Bearer {os.environ["NOTION_KEY"]}",
        "accept": "application/json",
        "content-type": "application/json",
        "Notion-Version": "2022-06-28"
    })

    if file_create_response.status_code != 200:
        raise Exception(
            f"File creation failed with status code {file_create_response.status_code}: {file_create_response.text}"
        )

    file_upload_id = json.loads(file_create_response.text)['id']
    return file_upload_id


def send_file_upload(upload_id, cover_file):
    """
    Uploads file contents to Notion.
    
    Parameters: 
        upload_id (string): file upload id
        cover_file (bytes): binary file contents
    """

    files = {
        "file": ("cover.png", cover_file, "image/png")
    }

    response = requests.post(
        f"https://api.notion.com/v1/file_uploads/{upload_id}/send",
        headers={
            "Authorization": f"Bearer {os.environ["NOTION_KEY"]}",
            "Notion-Version": "2022-06-28"
        },
        files=files
    )

    if response.status_code != 200:
        raise Exception(
            f"File upload failed with status code {response.status_code}: {response.text}")


def update_cover(file_upload_id, page_id):
    """
    Updates Notion page cover.
    
    Parameters: 
        file_upload_id (string): file upload id
        page_id (string): Notion page id
    """

    update_response = notion.pages.update(
        **{
            "page_id": page_id,
            "cover": {
                "type": "file_upload",
                "file_upload": {
                    "id": f"{file_upload_id}"
                }
            }
        }
    )
    return update_response


def update_notion_books(page):
    """
    Updates Notion book page.
    
    Parameters: 
        page: Notion block
    """

    if page['cover']['type'] == 'external':
        page_id = page['id']
        url = page['cover']['external']['url']
        cover = create_cover(url)

        file_upload_id = create_file_upload()
        send_file_upload(file_upload_id, cover)
        update_cover(file_upload_id, page_id)


# # Iterate through all pages in book database
# for block in iterate_paginated_api(
#     notion.databases.query, database_id=os.environ["NOTION_DATABASE_ID"]
# ):
#     update_notion_books(block)


# Update book pages created after date
response = notion.databases.query(
    **{
        "database_id": os.environ["NOTION_DATABASE_ID"],
        "filter": {
            "timestamp": "created_time",
            "created_time": {
                "on_or_after": "2025-06-13" # change date on each run
            }
        }
    }
)

for block in response['results']:   
    update_notion_books(block)