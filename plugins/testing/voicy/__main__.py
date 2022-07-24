# == Modules Userge by fnix
#
# = All copyrights to UsergeTeam
#
# ==

from pyrogram.errors import YouBlockedUser

from userge import Message, userge
from userge.utils.exceptions import StopConversation


@userge.on_cmd(
    "fstat",
    about={
        "header": "Fstat of user",
        "description": "fetch fstat of user using @missrose_bot",
        "usage": "{tr}fstat [UserID/username] or [reply to user]",
    },
)
async def f_stat(message: Message):
    """Fstat of user"""
    reply = message.reply_to_message
    user_ = message.input_str if not reply else reply.from_user.id
    if not user_:
        user_ = message.from_user.id
    try:
        get_u = await userge.get_users(user_)
        user_name = get_u.first_name
        user_id = get_u.id
        await message.edit(
            f"Fetching fstat of user <a href='tg://user?id={user_id}'><b>{user_name}</b></a>..."
        )
    except BaseException:
        user_name = user_
        user_id = user_
    msgs = []
    try:
        async with userge.conversation("MissRose_bot") as conv:
            try:
                await conv.send_message(f"!fstat {user_id}")
            except YouBlockedUser:
                await message.err(f"**You blocked @missrose_bot, Unblock it**", del_in=5)
                return
            msgs.append(await conv.get_response(mark_read=True))
            msgs.append(await conv.get_response(mark_read=True))
            msgs.append(await conv.get_response(timeout=3, mark_read=True))
    except StopConversation:
        pass
    for msg in msgs:
        if msg.text.startswith("Could not find a user"):
            await message.edit(f"User <b>{user_name}</b> (<code>{user_id}</code>) could not be found in @MissRose_bot's database.")
        else:
            await message.edit(f"{msg.text}")
