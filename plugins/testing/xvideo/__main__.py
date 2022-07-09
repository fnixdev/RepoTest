## == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

""" xvideo plugin """

import requests
import bs4

from pyrogram.enums import ParseMode

from userge import userge, Message


@userge.on_cmd(
    "xvideo", about={
        'header': "xvideo link direct",
        'usage': "{tr}xvideo <url>"},
    allow_channels=False
)
async def xvideo_direct(message: Message):
    """ xvideo get direct link """
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
        await message.edit(f"<a href='{link}'>• HERE IS YOUR LINK</a>", parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    except:
        await message.err("`something went right, if you entered correct link`")


@userge.on_cmd(
    "xsearch", about={
        'header': "search videos in xvideos",
        'usage': "{tr}search <query>"},
    allow_channels=False
)
async def xvideo_search(message: Message):
    """ search videos in xvideos """
    await message.edit("`Please Wait.....`")
    query = message.input_or_reply_str
    if not query:
        await message.err("`Please Enter Valid Input`")
        return
    try:
        qu = query.replace(" ","+")
        page= requests.get(f"https://www.xvideos.com/?k={qu}").content
        soup = bs4.BeautifulSoup(page, 'html.parser')
        search = soup.findAll("div",{"class":"thumb"})
        links= ""
        for i in search:
            kek = i.find("a")
            link = kek.get('href')
            semd = link.split("/")[2]
            links += f"<a href='https://www.xvideos.com{link}'>• {semd.upper()}</a>\n"
        await message.edit(links, parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    except:
        await message.err("`Something Went Wrong`")