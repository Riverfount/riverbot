import logging
import re

import requests
from dynaconf import settings
from flask import Flask, request


app = Flask(__name__)

RE_PATTERN_IN = r"""[v|V]aga$|[f|F]ree[la|lancer]|[j|J]ob$|[w|W]ork$|[d|D]ev|[d|D]eveloper$|[d|D]esenvolvedor$
|[j|J]unior$|[p|P]leno$|[s|S]enior$"""

RE_PATTERN_OUT = r"""[f|F]ake|[p|P]resnecial|[r|R]emoto"""

logging.basicConfig(format="%(asctime)s - %(message)s", level=logging.INFO)


@app.route("/event/", methods=["POST"])
def reply_message():

    # Set Up
    url = f"https://api.telegram.org/bot{settings.API_TOKEN}/sendMessage"  # noqa
    msg_telegram = request.get_json()
    msg = msg_telegram.get("message", False)

    if msg and not msg.get("animation", False) and not msg.get("photo", False):
        if re.search(RE_PATTERN_OUT, msg["text"]):
            return {"message": "out"}
        if re.search(RE_PATTERN_IN, msg["text"]):
            params = {
                "chat_id": msg["chat"]["id"],
                "text": "A vaga oferecida aceita trabalho remoto? \n# Msg enviada pelo ࿇RɨʋɛʀBօȶ࿇!",
                "reply_to_message_id": msg["message_id"],
            }

            requests.post(url, params=params)

    return {"message": "complet job!"}
