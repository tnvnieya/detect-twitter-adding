#!/usr/bin/env python3
import sys
from time import sleep
import json
from functools import partial
from pyrogram import Client
from pyrogram.client.types.message import Message
from pyrogram import Filters
from pyrogram import ParseMode
import secrets
from string import ascii_letters, digits  

eprint = partial(print, file=sys.stderr)

def random_string(n=16):
    return "".join([secrets.choice(ascii_letters)] + [secrets.choice(ascii_letters + digits) for _ in range(n - 1)])

app = Client("baugd", workers=1)

def print_running_info(app):
    me = app.get_me()
    name = me.first_name + " " + me.last_name
    username = me.username
    print("BAUGD is up and running...",
          f"for {name} (@{username})", sep="\n")

@app.on_message(Filters.new_chat_members)
def baug_detector(client, message: Message):
    if client.get_me() in message.new_chat_members:
        suspect = message.from_user
        if hasattr(suspect, "username") and suspect.username != None and suspect.username.strip() != "":
            name = f"@{suspect.username}"
        else:
            name = f"{suspect.first_name} {suspect.last_name}"
        try:
            chat_title = message.chat.title
        except AttributeError:
            chat_title = "UNKNOWN_CHAT"
        tag = "#" + random_string()
        msg = f"Being added into [{chat_title}]({message.chat.id}) by [{name}](tg://user?id={suspect.id}). {tag}"
        client.send_message("me", msg, parse_mode=ParseMode.MARKDOWN)
        client.send_message(message.chat.id, tag, reply_to_message_id=message.message_id)

def main():
    app.start()
    print_running_info(app)

if __name__ == "__main__":
    main()
