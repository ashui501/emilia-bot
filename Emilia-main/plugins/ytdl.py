from pyrogram import Client,filters,enums
from pyrogram.types import InlineKeyboardMarkup , InlineKeyboardButton
from pyrogram.types import CallbackQuery
from pytube import YouTube
import os

def delete_mp4_files():
  # Get list of all files in the current directory
  files = os.listdir(".")

  # Loop through all files
  for file in files:
      # Check if the file ends with '.mp4'
      if file.endswith('.mp4'):
          # Construct the full file path
          file_path = os.path.join(".", file)

          # Delete the file
          os.remove(file_path)
          print(f"Deleted {file_path}")



@Client.on_message(filters.command("ytdl"))
async def anime(client, message):
    if len(message.command) < 2:
        return await message.reply_text(f"• 🎐 ERROR: Provide the youtube video link🔗 to download.")
    message.command.pop(0)
    keybord=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("YouTube video 📼", callback_data="YouTube_video")],
            [InlineKeyboardButton("YouTube Music 🎶", callback_data="YouTube_Audio")]
        ])
    await message.reply(text =f"• 🎐 What you want to download ⬇️:", reply_markup = keybord)
    global link
    link = " ".join(message.command)


@Client.on_callback_query(filters.regex("YouTube_(.*)"))
async def switch(client, callback_query: CallbackQuery):
    global link
    video = YouTube(link)
    if callback_query.data.split("_", 1)[1] == "video":
       video = video.streams.get_highest_resolution()
       try:
         ml = video.download()
       except:
        await client.send_message(callback_query.message.chat.id,"• 🎐 An error has occurred.")
       await client.send_message(callback_query.message.chat.id,f"• 🎐 Download is completed successfully✅")
       await client.send_chat_action(callback_query.message.chat.id, enums.ChatAction.UPLOAD_VIDEO)
       await client.send_video(callback_query.message.chat.id, video = ml, caption=f"• 🎐 Title: {video.title}")
       delete_mp4_files()
    elif callback_query.data.split("_", 1)[1] == "Audio":
         try:
            video = YouTube(link)
            stream = video.streams.filter(only_audio=True).first()
            stream.download(filename=f"{video.title}.mp3")
            await client.send_message(callback_query.message.chat.id,f"• 🎐 Download is completed successfully✅")
         except KeyError:
           await client.send_message(callback_query.message.chat.id,"• 🎐 ERROR: Unable to fetch video information. Please check the video URL or your network connection.")
         await client.send_audio(callback_query.message.chat.id,f"{video.title}.mp3", caption=f"Title: {video.title}")
         os.remove(f"{video.title}.mp3")

