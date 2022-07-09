""" logo generator """

from random import choice

from pyrogram import enums

from userge import userge, Message


@userge.on_cmd(
    "logo", about={
        'header': "Logo Gen",
        'usage': "{tr}logo"},
    allow_channels=False, allow_via_bot=False
)
async def logo_gen(message: Message):
    lists = []
    async for search in userge.search_messages("@UltroidLogos", filter=enums.MessagesFilter.PHOTO):
        lists.append(search.photo.file_id)
    await message.reply_photo(choice(lists))