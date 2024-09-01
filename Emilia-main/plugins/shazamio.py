#pip install shazamio
import os
from pyrogram import filters,Client
from aiohttp_retry import ExponentialRetry
from shazamio import Shazam, Serialize, HTTPClient
from pyrogram.types import InlineKeyboardMarkup , InlineKeyboardButton

shazam = Shazam(
    http_client=HTTPClient(
        retry_options=ExponentialRetry(
            attempts=12, max_timeout=204.8, statuses={500, 502, 503, 504, 429}
        ),
    ),
)

async def recognize(message,path):
 try:
  voice_path = await shazam.recognize(path)
  voice = Serialize.full_track(voice_path)
  return voice.track.ringtone,voice.track.sections[0].meta_pages[1].image,voice.track.title,voice.track.sections[0].metadata[2].text
 except:
   os.remove(path)
   await message.reply(f"• 🎐  Unable to recognize try differtent clip!")



@Client.on_message(filters.command('szm'))
async def shazamio(client,message):
 original_message = message.reply_to_message
 if not message.reply_to_message:
    await message.reply_text("• 🎐 Reply to a song to get the name!\n")
 else: 
  if str(original_message.media) == "MessageMediaType.AUDIO" :
    await client.download_media(original_message.audio.file_id,file_name=f"{original_message.id}.mp3")
    ringtone,image,tiltle,Released=await recognize(message,f"downloads/{original_message.id}.mp3")
    btn=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Ringtone 🎵",url = ringtone)] 
        ])
    await client.send_photo(message.chat.id,image,caption=f"• 🎐 Song - {tiltle}\n• 🎐 Released - {Released}",reply_markup = btn)
    os.remove(f"downloads/{original_message.id}.mp3")
  elif str(original_message.media) == "MessageMediaType.VOICE" :
    await client.download_media(original_message.voice.file_id,file_name=f"{original_message.id}.ogg")
    ringtone,image,tiltle,Released=await recognize(message, f"downloads/{original_message.id}.ogg")
    btn=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Ringtone 🎵",url = ringtone)] 
        ])
    await client.send_photo(message.chat.id,image,caption=f"• 🎐 Song - {tiltle}\n• 🎐 Released - {Released}",reply_markup = btn)
    os.remove(f"downloads/{original_message.id}.ogg")


