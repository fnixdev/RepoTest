## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" nekos module """

import random
import requests

from userge import userge, Message

API = "https://nekos.best/api/v2/"
CATEGORIES = [
    "baka",
    "bite",
    "blush",
    "bored",
    "cry",
    "cuddle",
    "dance",
    "facepalm",
    "feed",
    "happy",
    "highfive",
    "hug",
    "kiss",
    "laugh",
    "neko",
    "pat",
    "poke",
    "pout",
    "shrug",
    "slap",
    "sleep",
    "smile",
    "smug",
    "stare",
    "think",
    "thumbsup",
    "tickle",
    "wave",
    "wink",
    "kitsune",
    "waifu",
    "handhold",
    "kick",
    "punch",
    "shoot",
    "husbando",
    "yeet",
]


@userge.on_cmd(
    "neko",
    about={
        "header": "Get SFW stuff from nekos.best",
        "usage": "{tr}neko\n{tr}neko [Choice]",
        "choice": CATEGORIES,
    },
)
async def nekos_best(message: Message):
    """ get sfw nekos """
    choice = message.input_str
    if choice:
        lower_choice = str(choice).lower()
        if lower_choice in CATEGORIES:
            await send_neko(message, lower_choice)
        else:
            await message.err("<code>Invalid input..</code>")
    else:
        await send_neko(message, random.choice(CATEGORIES))


async def send_neko(message: Message, choice: str):
    resp = requests.get(API+choice).json()
    reply = message.reply_to_message
    reply_id = reply.id if reply else None
    x = resp["results"][0]
    link = x["url"]
    art = x["artist_name"]
    hart = x["artist_href"]
    source = x["source_url"]
    capt = f'**Artist:** [{art}]({hart})\n**Source** [Here]({source})'
    if link.endswith(".gif"):
        bool_unsave = not message.client.is_bot
        await message.client.send_animation(
            chat_id=message.chat.id,
            animation=link,
            caption=capt,
            unsave=bool_unsave,
            reply_to_message_id=reply_id,
        )
    else:
        await message.client.send_photo(
            chat_id=message.chat.id, photo=link, caption=capt, reply_to_message_id=reply_id
        )
    