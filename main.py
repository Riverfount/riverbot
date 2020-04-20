import logging
import re
from typing import Any, Dict

from dynaconf import settings

import requests

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

logging.basicConfig(level=logging.DEBUG)

RE_PATTERN = r"""[v|V]aga|[f|F]ree[la|lancer]|[j|J]ob|[w|W]ork|[d|D]ev|[d|D]eveloper|[d|D]esenvolvedor
|[j|J]unior|[p|p]leno|[s|S]enior"""


class Message(BaseModel):
    message: Dict[str, Any]


@app.post("/event/")
async def read_root(message_to_read: Message) -> None:

    # Set Up
    url = f"https://api.telegram.org/bot{settings.API_TOKEN}/sendMessage"
    message_to_read = message_to_read.dict()
    animation = message_to_read["message"].get("animation", False)

    # Data Processing
    if not animation:
        msg_txt = message_to_read["message"].get("text", "No text")
        msg_id = message_to_read["message"]["message_id"]
        chat_id = message_to_read["message"]["chat"]["id"]
        if re.search(RE_PATTERN, msg_txt):
            params = {
                "chat_id": chat_id,
                "text": "A vaga oferecida aceita trabalho remoto? \n# Msg enviada pelo Riverbot!",
                "reply_to_message": msg_id,
            }

            requests.post(url, params=params)
