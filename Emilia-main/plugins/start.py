from pyrogram import Client, filters

@Client.on_message(filters.command("start"))
async def start(client, message):
    await client.send_video(message.chat.id,"Images/photo_2024-05-29_14-16-44.jpg",caption='• 🎐 Hello, I am Limbo Bot. Nice meet you.\nKindly type your name below and age!')