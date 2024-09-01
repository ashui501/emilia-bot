from pyrogram.types import Message
from pyrogram.errors import UserNotParticipant
from pyrogram import enums



async def admincheck(message) -> bool:
 client = message._client
 chat_id = message.chat.id
 user_id = message.from_user.id
 user = await client.get_chat_member(chat_id, user_id)
 if user.status == enums.ChatMemberStatus.OWNER or user.status == enums.ChatMemberStatus.ADMINISTRATOR :
    return True
 else:
    return False


async def is_sudoadmin(message: Message) -> bool:
    client = message._client
    check_user = await client.get_chat_member(message.chat.id, message.from_user.id)
    user_type = check_user.status
    if user_type == "member":
        return False
    if user_type == "administrator":
        add_adminperm = check_user.can_promote_members
        if add_adminperm:
            return True
        return False
    return True


async def check_membership(message) -> bool:
    client = message._client
    group_id = message.chat.id # Replace with your group ID
    user_bot_id = 1152935968
    try:
        member = await client.get_chat_member(group_id, user_bot_id)
        if member:
            return True
        else:
            return False
    except UserNotParticipant:
        return False
    except Exception as e:
        await message.reply_text(f"• 🎐 An error occurred: {e}")


