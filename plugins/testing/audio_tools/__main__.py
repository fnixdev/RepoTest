# == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" audio tools """

import os

from pyrogram.enums import MessageMediaType

from userge import userge, Message, config
from userge.utils import runcmd


@userge.on_cmd(
    "extractaudio", about={
        'header': "extract audio from video",
        'usage': "{tr}extractaud [reply video]"},
    allow_channels=False
)
async def extract_audio(message: Message):
    replied = message.reply_to_message
    if not replied:
        await message.edit("<code>Reply video needed.</code>")
        return
    if replied.media == MessageMediaType.VIDEO:
        await message.edit("<code>downloading video..</code>")
        file = await message.client.download_media(
            message=replied,
            file_name=config.Dynamic.DOWN_PATH
        )
        dur = replied.video.duration
        out_file = file + ".aac"
        try:
            await message.edit("<code>trying extract audio</code>")
            cmd = f"ffmpeg -i {file} -vn -acodec copy {out_file}"
            await runcmd(cmd)
            await message.edit("<code>uploading audio...</code>")
            await message.delete()
            await message.client.send_audio(
                message.chat.id,
                audio=out_file,
                caption="<b>Audio extracted by @HilzuUB</b>",
                duration=dur
            ) 
        except Exception:
            await message.edit("<code>Fail.</code>")
        os.remove(out_file)
        os.remove(file)
    else:
        await message.edit("<code>Reply video needed.</code>")
        return