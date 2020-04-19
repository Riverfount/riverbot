from typing import Any, Dict

from dynaconf import settings
from pprint import pprint  # noqa

import requests

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Message(BaseModel):
    message: Dict[str, Any]


@app.post("/event/")
async def read_root(message_to_read: Message):
    url = f"https://api.telegram.org/bot{settings.API_TOKEN}/sendMessage"
    message_to_read = message_to_read.dict()
    animation = message_to_read["message"].get("animation", False)

    if not animation:
        msg_txt = message_to_read["message"]["text"]  # noqa
        msg_id = message_to_read["message"]["message_id"]
        chat_id = message_to_read["message"]["chat"]["id"]

        params = {
            "chat_id": chat_id,
            "text": "A vaga oferecida aceita trabalho remoto? \n# Msg enviada pelo Riverbot!",
            "reply_to_message": msg_id,
        }

        requests.post(url, params=params)
