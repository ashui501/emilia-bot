from pyrogram import filters
from pyromod import Client
from pluginsuserBot.mediastream import app
from decouple import config


OWNER = 1152935968

@app.on_message(filters.command("join"))
async def play_handler(client,message):
    if message.from_user.id == OWNER:
     await client.join_chat(message.command[1])
    else:
       await message.reply_text("• 🎐 you don't have the right to do so !")


   