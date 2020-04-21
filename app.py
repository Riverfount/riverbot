import re

from dynaconf import settings
from flask import Flask, request
import requests


app = Flask(__name__)

RE_PATTERN_IN = re.compile(
    r"""\bvagas?\b|\bempregos?\b|\bworks?\b|\bfreelancers?\b|\bfreelas?\b|\bjunior\b|\bsenior\b|\bpleno\b|\boportunidades?\b|
\bdesenvolvedor|\bdevelopers?\b|\bdev\b""",
    re.IGNORECASE,
)

RE_PATTERN_OUT = re.compile(r"\bfake|\bpresencial|\bremot(a|o)?|\bremote", re.IGNORECASE)


@app.route("/event/", methods=["POST"])
def reply_message():

    url = f"https://api.telegram.org/bot{settings.API_TOKEN}/sendMessage"
    msg_telegram = request.get_json()

    if "message" not in msg_telegram.keys():
        return {"message": "not found!"}

    msg = msg_telegram["message"]

    if "text" not in msg.keys():
        return {"message": "not found!"}

    params = {}

    if re.findall(RE_PATTERN_OUT, msg["text"]):
        return {"message": "not found!"}

    if re.findall(RE_PATTERN_IN, msg["text"]):
        params = {
            "chat_id": msg["chat"]["id"],
            "text": "A vaga oferecida aceita trabalho remoto? \n# Msg enviada pelo ࿇RɨʋɛʀBօȶ࿇!",
            "reply_to_message_id": msg["message_id"],
        }

    requests.post(url, params=params)

    return {"message": "complet job!"}
