## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" shazan plugin """

import os

from shazamio import Shazam

from userge import userge, Message, config
from userge.utils import progress


shazam = Shazam()


@userge.on_cmd(
    "whichisong", about={
        'header': "discover song name",
        'usage': "{tr}whichisong [reply song]"},
    allow_channels=False
)
async def whichi_song(message: Message):
    reply = message.reply_to_message
    if not reply.audio:
        await message.err("Reply audio needed.")
        return
    await message.edit("Downloading audio..")
    file = await message.client.download_media(
                message=message.reply_to_message,
                file_name=config.Dynamic.DOWN_PATH
            )
    try:
        res = await shazam.recognize_song(file)
        await message.edit(res)
    except Exception as e:
        await message.reply(e)
        os.remove(file)
        return await message.err("Failed to get sound data.")