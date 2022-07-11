## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" website screenshot """

import os
import aiohttp
import aiofiles
import validators

from wget import download
from hashlib import md5
from bs4 import BeautifulSoup

from userge import userge, Message, config


@userge.on_cmd(
    "ssweb", about={
        'header': "get a screenshot from website",
        'usage': "{tr}ssweb url"}
)
async def web_ss(message: Message):
    reply = message.reply_to_message
    query = None
    if message.input_str:
        query = message.input_str
    elif reply:
        if reply.text:
            query = reply.text
        elif reply.caption:
            query = reply.caption
    if not query:
        return await message.err("Input or reply to a valid URL", del_in=5)
    await message.edit("`Checking URL..`")
    valid = validators.url(query)
    if not valid == True:
        return await message.err("Insert a valid URL")
    await message.edit("`Getting access key..`")
    async with aiohttp.ClientSession() as ses, ses.get("https://screenshotlayer.com") as resp:
        soup = BeautifulSoup(await resp.text(), features="html.parser")
    scl_secret = soup.findAll("input")[1]["value"]
    key = md5((str(query) + scl_secret).encode()).hexdigest()
    url = f"https://screenshotlayer.com/php_helper_scripts/scl_api.php?secret_key={key}&url={query}"
    await message.edit("`generating image..`")
    file_ = None
    try:
        file_ = download(url, config.Dynamic.DOWN_PATH)
    except Exception:
        return await message.err("Fail to generate image.")
    if message.client.is_bot:
        await userge.bot.send_photo(message.chat.id, photo=file_, caption="`Powered By @HilzuUB`")
    else:
        await message.delete()
        await userge.send_photo(message.chat.id, photo=file_, caption="`Powered By @HilzuUB`")
    if os.path.exists(file_):
        os.remove(file_)