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
        await message.err("<code>Reply audio needed.</code>")
        return
    await message.edit("<code>downloading audio..</code>")
    file = await message.client.download_media(
                message=message.reply_to_message,
                file_name=config.Dynamic.DOWN_PATH
            )
    try:
        await message.edit("<code>identifying music</code>")
        res = await shazam.recognize_song(file)
    except Exception as e:
        await message.reply(e)
        os.remove(file)
        return await message.err("<code>Failed to get sound data.</code>")
    song = res["track"]
    out = f"<b>Song Recognised!\n\n{song['title']}</b>\n<i>- {song['subtitle']}</i>"
    if song["images"]["coverart"]:
        await message.delete()
        await message.reply_photo(photo=song["images"]["coverart"], caption=out)
    else:
        await message.edit(out)
    os.remove(file)