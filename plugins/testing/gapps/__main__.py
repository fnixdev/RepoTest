# == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

from bs4 import BeautifulSoup
from requests import get

from pyrogram import filters
from pyrogram.errors import MessageIdInvalid, MessageNotModified
from pyrogram.types import CallbackQuery, InlineQuery, InlineQueryResultPhoto, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup

from userge import Message, userge, config as Config
from userge.utils import get_response
from ...builtin import sudo


async def flame_(version):
    if version == "11.0":
        link = "https://sourceforge.net/projects/flamegapps/files/arm64/android-11/"
    if version == "12.0":
        link = "https://sourceforge.net/projects/flamegapps/files/arm64/android-12/"
    if version == "12.1":
        link = "https://sourceforge.net/projects/flamegapps/files/arm64/android-12.1/"
    url = get(link)
    page = BeautifulSoup(url.content, "lxml")
    content = page.tbody.tr
    date = content["title"]
    date2 = date.replace("-", "")
    flame = "{link}{date}/FlameGApps-{version}-{varient}-arm64-{date2}.zip/download"
    basic = flame.format(link=link, date=date,
                         version=version, varient="basic", date2=date2)
    full = flame.format(link=link, date=date, version=version,
                        varient="full", date2=date2)
    return basic, full


async def nik_(version):
    if version == "11.0":
        link = "https://sourceforge.net/projects/nikgapps/files/Releases/NikGapps-R/"
    if version == "12.0":
        link = "https://sourceforge.net/projects/nikgapps/files/Releases/NikGapps-S/"
    if version == "12.1":
        link = "https://sourceforge.net/projects/nikgapps/files/Releases/NikGapps-SL/"
    url = get(link)
    page = BeautifulSoup(url.content, "lxml")
    content = page.tbody.tr
    date = content["title"]
    url2 = get(link+date)
    page2 = BeautifulSoup(url2.content, "lxml")
    name = page2.tbody.find_all("th", {'headers': 'files_name_h'})
    results = []
    for item in name:
        nam = item.find("a")
        string_ = f"[{nam.span.text}]({nam['href']})"
        results.append(string_)
    return results


@userge.on_cmd(
    "gapps", about={
        'header': "get latest google apps"
    }
)
async def latest_gapps(message: Message):
    buttons = [
        [
            InlineKeyboardButton(
                text="11", callback_data=""),
            InlineKeyboardButton(
                text="12", callback_data=""),
            InlineKeyboardButton(
                text="12L", callback_data=""),
        ]
    ]
    if message.client.is_bot:
        await userge.bot.send_message(message.chat.id, "**Select gapps version**", reply_markup=buttons)
    else:
        await message.delete()
        username = (await userge.bot.get_me()).username
        x = await userge.get_inline_bot_results(username, "gapps")
        await userge.send_inline_bot_result(chat_id=message.chat.id, query_id=x.query_id, result_id=x.results[0].id)


if userge.has_bot:
    def check_owner(func):
        async def wrapper(_, c_q: CallbackQuery):
            if c_q.from_user and c_q.from_user.id in (list(Config.OWNER_ID) + list(sudo.USERS)):
                try:
                    await func(c_q)
                except MessageNotModified:
                    await c_q.answer("Nothing Found to Refresh 🤷‍♂️", show_alert=True)
                except MessageIdInvalid:
                    await c_q.answer("Sorry, I Don't Have Permissions to edit this 😔",
                                     show_alert=True)
            else:
                user_dict = await userge.bot.get_user_dict(Config.OWNER_ID[0])
                await c_q.answer(
                    f"Only {user_dict['flname']} Can Access this...! Build Your Own @fnixsup 🤘",
                    show_alert=True)
        return wrapper

    @userge.bot.on_inline_query(
        filters.create(
            lambda _, __, inline_query: (
                inline_query.query
                and inline_query.query.startswith("gapps")
                and inline_query.from_user
                and inline_query.from_user.id in Config.OWNER_ID
            ),
            name="InlineGapps"
        ),
        group=-2
    )
    async def inline_iydl(_, inline_query: InlineQuery):
        results = []
        buttons = [
            [
                InlineKeyboardButton(
                    text="11", callback_data=""),
                InlineKeyboardButton(
                    text="12", callback_data=""),
                InlineKeyboardButton(
                    text="12L", callback_data=""),
            ]
        ]
        results.append(
            InlineQueryResultArticle(
                title="Gapps",
                input_message_content=InputTextMessageContent(
                    "**Select gapps version**"
                ),
                description="Get latest gapps",
                reply_markup=buttons
            )
        )

    # ==  Sector select gapps\

    @userge.bot.on_callback_query(filters=filters.regex(pattern=r"gapps_v\|(.*)"))
    @check_owner
    async def gapps_filter_cq(cq: CallbackQuery):
        cb = cq.data.split("|")
        version = cb[1]
        buttons = [
            [
                InlineKeyboardButton(
                    text="Flame Gapps", callback_data=f"gapps_flame|{version}"),
                InlineKeyboardButton(
                    text="Nik Gapps", callback_data=f"gapps_nik|{version}"),
            ]
        ]
        await cq.edit_message_text(text="**Select your preferred gapps**", reply_markup=buttons)

    @userge.bot.on_callback_query(filters=filters.regex(pattern=r"gapps_(flame|nik)\|(.*)"))
    @check_owner
    async def gapps_filter_cq(cq: CallbackQuery):
        cb = cq.data.split("|")
        version = cb[1]
        if cb[0] == "gapps_flame":
            aaa = ''
        elif cb[0] == "gapps_nik":
            aaa = ''