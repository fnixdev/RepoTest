## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" audio tools """

import os

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
    if not replied or not replied.video:
        await message.edit("<code>Reply video needed.</code>")
        return
    await message.edit("<code>downloading video..</code>")
    file = await message.client.download_media(
                message=message.reply_to_message,
                file_name=config.Dynamic.DOWN_PATH
            )
    out_file = file + ".aac"
    try:
        cmd = f"ffmpeg -i {file} -vn -acodec copy {out_file}"
        await runcmd(cmd)
        os.remove(file)
        await message.client.send_audio(message.chat.id, audio=out_file, caption="<b>Audio extracted by @HilzuUB</b>")
    except Exception:
        os.remove(file)
        await message.edit("<code>Fail.</code>")
        return

