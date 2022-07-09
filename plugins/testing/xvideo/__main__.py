""" xvideo plugin """

import requests
import bs4

from userge import userge, Message


@userge.on_cmd(
    "xvideo", about={
        'header': "xvideo link direct",
        'usage': "{tr}xvideo <url>"},
    allow_channels=False
)
async def xvideo_direct(message: Message):
    await message.edit("`Please Wait.....`")
    url = message.input_or_reply_str
    if not url:
        await message.err("`Please Enter Valid Input`")
        return
    try:
        req = requests.get(url)
        soup = bs4.BeautifulSoup(req.content, 'html.parser')

        soups = soup.find("div",{"id":"video-player-bg"})
        link =""
        for a in soups.find_all('a', href=True):
            link = a["href"]
        await message.edit(f"HERE IS YOUR LINK:\n`{link}`")
    except:
        await message.err("something went right, if you entered correct link")