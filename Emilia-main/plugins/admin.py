from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
    ChatPermissions,
)
from pyrogram import Client, filters
from pyrogram.types import ChatPrivileges
from Helpers.admincheck import admincheck,is_sudoadmin
from Helpers.mongodb import captcha, event, ban, unban
from pyrogram.raw import types
import os,time

OWNER = 1152935968


@Client.on_message(filters.command("admin"))
async def promtie(client, message):
    chat_id = message.chat.id
    user_id = 1557927212
    await Client.promote_chat_member(
        chat_id, user_id, ChatPrivileges(can_manage_chat=False, can_post_messages=False)
    )


@Client.on_message(filters.command("captcha") & ~filters.private)
async def captcha_(client, message):
    ms_g = "• 🎐 Do you want to turn the captcha:"
    keybord = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("OFF 📴", callback_data="captcha_FALSE")],
            [InlineKeyboardButton("ON 🔛", callback_data="captcha_TRUE")],
        ]
    )
    await client.send_message(message.chat.id, ms_g, reply_markup=keybord)


@Client.on_callback_query(filters.regex("captcha_(.*)"))
async def captcha_switch(client, callback_query: CallbackQuery):

    chat_id = callback_query.message.chat.id
    chat_titel = callback_query.message.chat.title
    input = callback_query.data.split("_", 1)[1]
    if await admincheck(callback_query.message):
        if input == "TRUE":
            captcha(chat_id, input)
            await client.answer_callback_query(
                callback_query_id=callback_query.id,
                text=f"• 🎐 Captcha has been turned 🔛 **on** in {chat_titel}",
                show_alert=True,
            )
        elif input == "FALSE":
            captcha(chat_id, input)
            await client.answer_callback_query(
                callback_query_id=callback_query.id,
                text=f"• 🎐 Captcha has been turned 📴 **off** in {chat_titel}",
                show_alert=True,
            )
    else:
        await client.answer_callback_query(
            callback_query_id=callback_query.id,
            text="• 🎐 You don't have admin permitions!",
            show_alert=True,
        )


@Client.on_message(filters.command("event") & ~filters.private)
async def event(client, message):
    ms_g = "• 🎐 Do you want to turn the event:"
    keybord = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("OFF 📴", callback_data="event_FALSE")],
            [InlineKeyboardButton("ON 🔛", callback_data="event_TRUE")],
        ]
    )
    reply = await message.reply(text=ms_g, reply_markup=keybord)
    global message_id
    message_id = reply.id


@Client.on_callback_query(filters.regex("event_(.*)"))
async def event_switch(client, callback_query: CallbackQuery):

    chat_id = callback_query.message.chat.id
    chat_titel = callback_query.message.chat.title
    input = callback_query.data.split("_", 1)[1]
    if await admincheck(callback_query.message):
        if input == "TRUE":
            event(chat_id, input)
            await client.edit_message_text(
                callback_query.message.chat.id,
                callback_query.message.id,
                text=f"• 🎐 Event has been turned 🔛 **on** in {chat_titel}",
            )
        elif input == "FALSE":
            event(chat_id, input)
            await client.edit_message_text(
                callback_query.message.chat.id,
                callback_query.message.id,
                text=f"• 🎐 Event has been turned 📴 **off** in {chat_titel}",
            )
    else:
        await client.answer_callback_query(
            callback_query_id=callback_query.id,
            text="• 🎐 You don't have admin permitions!",
            show_alert=True,
        )


@Client.on_message(filters.command("del") & ~filters.private)
async def deleteFunc(client, message):
    chat_member = await client.get_chat_member(message.chat.id, message.from_user.id)
    privileges = chat_member.privileges
    try:
        if privileges.can_delete_messages:
            if not message.reply_to_message:
                return await message.reply_text("• 🎐 Reply To A Message To Delete It")
            await message.reply_to_message.delete()
            await message.delete()
    except:
        await message.reply_text("• 🎐 You don't have permission !")


@Client.on_message(filters.command("ban") & filters.group)
async def ban_chat_user(client, message):
    peer = await client.resolve_peer("paura")
    if isinstance(peer, types.InputPeerUser):
        username_id = int(peer.user_id)
    if not await admincheck(message):
        return await message.reply_text("• 🎐 You not admin in this group.")
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = message.reply_to_message.from_user.id or username_id
    else:
        try:
            user_id = message.text.split(" ", 1)[1]
        except IndexError:
            return await message.reply_text(
                "• 🎐 Reply to any user message or give user id, username"
            )
    try:
        user_id = int(user_id)
    except ValueError:
        pass
    try:
        user = (await client.get_chat_member(message.chat.id, user_id)).user
    except:
        return await message.reply_text("• 🎐 Can't find you given user in this group")
    try:
        ban(message.chat.id, user_id)
        await client.ban_chat_member(message.chat.id, user_id)
    except:
        return await message.reply_text("• 🎐 I don't have access to ban user")
    await message.reply_text(
        f"• 🎐 Successfully banned {user.mention} from {message.chat.title}"
    )


@Client.on_message(filters.command("mute") & filters.group)
async def mute_chat_user(client, message):
    if not await admincheck(message):
        return await message.reply_text("• 🎐 You not admin in this group.")
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = (
            message.reply_to_message.from_user.username
            or message.reply_to_message.from_user.id
        )
    else:
        try:
            user_id = message.text.split(" ", 1)[1]
        except IndexError:
            return await message.reply_text(
                "• 🎐 Reply to any user message or give user id, username"
            )
    try:
        user_id = int(user_id)
    except ValueError:
        pass
    try:
        user = (await client.get_chat_member(message.chat.id, user_id)).user
    except:
        return await message.reply_text("• 🎐 Can't find you given user in this group")
    try:
        await client.restrict_chat_member(message.chat.id, user_id, ChatPermissions())
    except:
        return await message.reply_text("• 🎐 I don't have access to mute user")
    await message.reply_text(
        f"• 🎐 Successfully muted {user.mention} from {message.chat.title}"
    )


@Client.on_message(filters.command(["unban", "unmute"]) & filters.group)
async def unban_chat_user(client, message):
    if not await admincheck(message):
        return await message.reply_text("You not admin in this group.")
    if message.reply_to_message and message.reply_to_message.from_user:
        user_id = (
            message.reply_to_message.from_user.username
            or message.reply_to_message.from_user.id
        )
    else:
        try:
            user_id = message.text.split(" ", 1)[1]
        except IndexError:
            return await message.reply_text(
                "• 🎐 Reply to any user message or give user id, username"
            )
    try:
        user_id = int(user_id)
    except ValueError:
        pass
    try:
        user = (await client.get_chat_member(message.chat.id, user_id)).user
    except:
        return await message.reply_text("• 🎐 Can't find you given user in this group")
    try:
        unban(message.chat.id, user_id)
        await client.unban_chat_member(message.chat.id, user_id)
    except:
        return await message.reply_text(
            f"• 🎐 I don't have access to {message.command[0]} user"
        )
    await message.reply_text(
        f"• 🎐 Successfully {message.command[0]} {user.mention} from {message.chat.title}"
    )


@Client.on_message(filters.command("ban_ghosts") & ~filters.private)
async def ban_deleted_accounts(client, message):
    chat_id = message.chat.id
    deleted_users = []
    async for i in client.get_chat_members(chat_id):
        if i.user.is_deleted:
            deleted_users.append(i.user.id)
    if deleted_users:
        banned_users = 0
        for deleted_user in deleted_users:
            try:
                await message.chat.ban_member(deleted_user)
            except Exception:
                pass
            banned_users += 1
        await message.reply_text(f"• 🎐 Banned {banned_users} Deleted Accounts")
        time.sleep(1.9)
        await message.delete()
    else:
        await message.reply_text("• 🎐 There are no deleted accounts in this chat")
        time.sleep(1.9)
        await message.delete()


@Client.on_message(filters.user(OWNER) & filters.command("leave") & ~filters.private)
async def leave(client, message):
    if len(message.command) < 2:
        await message.reply_text("• 🎐 Sir, you haven't provied the chat_id.")
        time.sleep(1.9)
        await message.delete()
    else:
        message.command.pop(0)
        keybord = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Leave Chat", callback_data="leave_chat")],
                [
                    InlineKeyboardButton(
                        "Leave Chat Delete", callback_data="leave_chatdelete"
                    )
                ],
            ]
        )
        await message.reply(
            text="• 🎐 • Leave Chat\nDes- Only leave the chat\n\n• Leave Chat Delete\nDes- Leave the chat and delete",
            reply_markup=keybord,
        )
        global chat_id
        chat_id = " ".join(message.command)


@Client.on_callback_query(filters.regex("leave_(.*)"))
async def leave_chat(client, callback_query: CallbackQuery):
    global chat_id
    if OWNER == callback_query.from_user.id:
        if callback_query.data.split("_", 1)[1] == "chat":
            await client.send_photo(
                chat_id,
                "plugins/images/photo_2024-03-18_13-08-29.jpg",
                caption="• 🎐 I have to go, my owner ordered  me !\nSE YA 👋, contact my owner if your have any question.",
            )
            await client.leave_chat(chat_id)
        else:
            await client.send_photo(
                chat_id,
                "plugins/images/photo_2024-03-18_13-08-29.jpg",
                caption="• 🎐 I have to go, my owner ordered  me !\nSE YA 👋, contact my owner if your have any question.\nAll the bot messages will be deleted",
            )
            await client.leave_chat(chat_id, delete=True)
    else:
        await client.answer_callback_query(
            callback_query.id, text="Hello, You are not the owner !", show_alert=True
        )


@Client.on_message(filters.command(["rc", "restrict_chat"]) & ~filters.private)
async def rc(client, message):
    keybord = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Restrict chat", callback_data="restrict_chat")],
            [InlineKeyboardButton("Only Text", callback_data="restrict_text")],
        ]
    )
    await client.send_message(
        message.chat.id,
        f"• 🎐 Restrict chat: Completely restrict chat\n• Only Text: Chat members can only send text messages and media messages.",
        reply_markup=keybord,
    )


@Client.on_callback_query(filters.regex("restrict_(.*)"))
async def leave_chat(client, callback_query: CallbackQuery):
    if not await admincheck(callback_query.message):
        if callback_query.data.split("_", 1)[1] == "chat":
            await client.send_message(
                callback_query.message.chat.id,
                "• 🎐 This chat has been completely restricted.",
            )
            await client.set_chat_permissions(
                callback_query.from_user.id, ChatPermissions()
            )
        else:
            await client.send_message(
                callback_query.message.chat.id,
                "• 🎐 Chat members can only send text messages and media messages.",
            )
            await client.set_chat_permissions(
                callback_query.from_user.id,
                ChatPermissions(can_send_messages=True, can_send_media_messages=True),
            )
    else:
        await client.answer_callback_query(
            callback_query.id,
            text="Sir, you don't have permissions do so !",
            show_alert=True,
        )
        time.sleep(1.9)
        await callback_query.message.delete()


@Client.on_message(filters.command(["scp", "set_chat_profile"]))
async def set_profile(client, message):
    if not await admincheck(message):
        await message.repl_text("• 🎐 Sir, you don't have permissions do so.")
        time.sleep(1.9)
        await message.delete()
    else:
        reply_message = message.reply_to_message
        if reply_message and reply_message.photo:
            file_id = reply_message.photo.file_id
            try:
                await client.download_media(file_id, file_name="downloaded_image.jpg")
                await client.set_chat_photo(
                    message.chat.id, photo="downloads/downloaded_image.jpg"
                )
                os.remove(f"downloads/downloaded_image.jpg")
            except:
                await message.reply_text(
                    "• 🎐 Sir, Bot don't have the permission to do so."
                )
                time.sleep(1.9)
                await message.delete()
        else:
            await message.repl_text("• 🎐 Sir, you haven't replied to a pic.")
            time.sleep(1.9)
            await message.delete()


@Client.on_message(filters.command("promote") & filters.group)
async def promote_user(client, message):
    if is_sudoadmin:
     try:
         if message.reply_to_message:
             # Promote the user in the replied message
             user_id = message.reply_to_message.from_user.id
             print(user_id)
         elif message.entities:
             for entity in message.entities:
                 if entity.type.MENTION:
                     # Username mention (e.g., @username)
                     username = message.command[1]
                     user = await client.get_users(username)
                     user_id = user.id
                     break
         else:
             await message.reply_text("• 🎐 Please reply to a user or mention a user to promote.")
             return
 
         chat_id = message.chat.id
         
         # Promote the user
         await client.promote_chat_member(
             chat_id,
             user_id,
             ChatPrivileges(
                 can_change_info=True,
                 can_invite_users=True,
                 can_restrict_members=True,
                 can_pin_messages=True,
                 can_promote_members=True,
                 can_manage_video_chats=True,
                 is_anonymous=False
             )
         )
 
         await message.reply_text("• 🎐 User promoted successfully.")
 
     except Exception as e:
         await message.reply_text(f"• 🎐 An error occurred: {e}")
    else:
        await message.reply_text("• 🎐 Sir you don't have the rights to do so!")


@Client.on_message(filters.command("demote") & filters.group)
async def demote_user(client, message):
    if is_sudoadmin:
     try:
         if message.reply_to_message:
             # demote the user in the replied message
             user_id = message.reply_to_message.from_user.id
             print(user_id)
         elif message.entities:
             for entity in message.entities:
                 if entity.type.MENTION:
                     # Username mention (e.g., @username)
                     username = message.command[1]
                     user = await client.get_users(username)
                     user_id = user.id
                     break
         else:
             await message.reply_text("• 🎐 Please reply to a user or mention a user to demote.")
             return
 
         chat_id = message.chat.id
         
         # demotes the user
         await client.promote_chat_member(
             chat_id,
             user_id,
             ChatPrivileges(
                 can_change_info=False,
                 can_invite_users=False,
                 can_restrict_members=False,
                 can_pin_messages=False,
                 can_promote_members=False,
                 can_manage_video_chats=False,
                 is_anonymous=False
             )
         )
 
         await message.reply_text("• 🎐 User demote successfully.")
 
     except Exception as e:
         await message.reply_text(f"• 🎐 An error occurred: {e}")
    else:
        await message.reply_text("• 🎐 Sir you don't have the rights to do so!")