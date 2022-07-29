## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" nekos module """

import random

from userge import userge, Message
from userge.utils import get_response

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
    try:
        resp = await get_response.json(API+choice)
    except Exception:
        return await message.edit("request error")
    link = resp["results"][0]["url"]
    capt = f'Source: <a href=\"{resp["results"][0]["source_url"]}\"> Here</a>\nArtst: <a href=\"{resp["results"][0]["artist_href"]}\">{resp["results"][0]["artist_name"]}</a>'
    await message.reply(link, capt)