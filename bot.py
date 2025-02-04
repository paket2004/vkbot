# import necessary libraries
import json

from fastapi import FastAPI, Request
import vk_api
from fastapi.responses import PlainTextResponse

import requests

import random

import time

# initialize fastapi app
app = FastAPI()

# my vk api token
TOKEN = "YOUR_VK_TOKEN"

# create vk session
vk_session = vk_api.VkApi(token=TOKEN)
vk = vk_session.get_api()


# files to store users and messages to avoid several replies for one message and resending images
USERS_FILE = "users_greeted.json"
PROCESSED_MESSAGES_FILE = "processed_messages.json"

# upload messages from history and users
try:
    with open(USERS_FILE, "r") as file:
        users_greeted = set(json.load(file))
except (FileNotFoundError, json.JSONDecodeError):
    users_greeted = set()

try:
    with open(PROCESSED_MESSAGES_FILE, "r") as file:
        processed_messages = set(json.load(file))
except (FileNotFoundError, json.JSONDecodeError):
    processed_messages = set()

# function to save users in the json
def save_users():
    with open(USERS_FILE, "w") as file:
        json.dump(list(users_greeted), file)

# function to save messages into the json
def save_processed_messages():
    with open(PROCESSED_MESSAGES_FILE, "w") as file:
        json.dump(list(processed_messages), file)

# function to send message
def send_message(user_id, text):
    vk.messages.send(user_id=user_id, message=text, random_id=random.randint(1, 2**31))

# function to resend image
def send_image(user_id, photo_url):
    upload_url = vk.photos.getMessagesUploadServer()["upload_url"]
    photo = requests.get(photo_url).content
    files = {"photo": ("photo.jpg", photo, "image/jpeg")}
    # print(f"Upload URL: {upload_url}")
    for i in range(3):
        try:
            response = requests.post(upload_url, files=files).json()
            break
        except requests.exceptions.RequestException as e:
            print(f"Ошибка загрузки фото: {e}")
            time.sleep(1)

    photo_data = vk.photos.saveMessagesPhoto(
        photo=response["photo"], server=response["server"], hash=response["hash"]
    )[0]

    attachment = f"photo{photo_data['owner_id']}_{photo_data['id']}"
    vk.messages.send(user_id=user_id, attachment=attachment, random_id=random.randint(1, 2**31))


# vk callback api handler
@app.post("/")
async def vk_callback(request: Request):
    data = await request.json()
    
    # check from vk
    if "type" in data and data["type"] == "confirmation":
        return PlainTextResponse("YOUR_CALLBACK_API_CODE", status_code=200)


    if data["type"] == "message_new":
        message_id = data["object"]["message"]["id"]
        user_id = data["object"]["message"]["from_id"]
        attachments = data["object"]["message"].get("attachments", [])

        # check history
        if message_id in processed_messages:
            return {"status": "ok"}

        # store messages
        processed_messages.add(message_id)
        save_processed_messages()

        # if 1st message - reply
        if user_id not in users_greeted:
            send_message(user_id, "Привет! Отправьте мне изображение.")
            users_greeted.add(user_id)
            save_users()
        # send back photo from message
        if attachments and attachments[0]["type"] == "photo":
            photo_url = attachments[0]["photo"]["sizes"][-1]["url"]
            send_image(user_id, photo_url)

    return {"status": "ok"}
