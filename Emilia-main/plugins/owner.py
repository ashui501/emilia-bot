from pyrogram import Client, filters,enums
from pyrogram.types import InlineKeyboardMarkup , InlineKeyboardButton

@Client.on_message(filters.command("owner"))
async def owner(client, message):
    keybord=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Git-Hub", url="https://github.com/Debayan08"),
             InlineKeyboardButton("Instagram", url="https://www.instagram.com/das_abae?igsh=MTlpNml5bm9qOTdxbg==")],
            [InlineKeyboardButton("Support", url="https://t.me/+77-e0j4mdhRjOTdl")]

        ])
    await client.send_chat_action(message.chat.id, enums.ChatAction.TYPING)
    await client.send_message(message.chat.id,"• 🎐 NAME: DAS KUN\n• 🎐 AGE: 19\n• 🎐 GENDER: MALE\n• 🎐 CONTACT: @Das_2005_08\n• 🎐 EMAIL: debayanabae2005@gmail.com",reply_markup = keybord)

