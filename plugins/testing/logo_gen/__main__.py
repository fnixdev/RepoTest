""" logo generator """

from pyrogram import enums

from userge import userge, Message


@userge.on_cmd(
    "logo", about={
        'header': "Logo Gen",
        'usage': "{tr}logo"},
    allow_channels=False, allow_via_bot=False
)
async def logo_gen(message: Message):
    list = []
    search = userge.search_messages("@UltroidLogos", filter=enums.MessagesFilter.PHOTO)
    list.append(search)
    await message.reply(list)