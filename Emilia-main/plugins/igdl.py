from pyrogram import Client,filters
import requests

@Client.on_message(filters.command("ig_dl"))
async def ig_dl(client, message):
    user_name = message.from_user.username
    if len(message.command) < 2:
        return await message.reply_text("• 🎐 ERROR: Send **/ig_dl url** to download the Instagram Reels, Post, Videos ℹ️.")
    message.command.pop(0)
    url = " ".join(message.command)
    res = requests.get(f"https://weeb-api.vercel.app/insta?url={url}")
    data = res.json()
    vedio = data['urls'][0]['url']
    await client.send_video(message.chat.id,vedio,caption = f"• 🎐  Username: @{user_name}")


