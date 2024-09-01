from pyrogram import filters,Client
from Helpers.uptime import uptime
from datetime import datetime
import psutil



OWNER = 1152935968
now = datetime.now().time().strftime("%H:%M:%S")
date = datetime.now().strftime("%Y-%m-%d")





@Client.on_message(filters.command('stats'))
async def stat(client,message):
 cpu_usage = psutil.cpu_percent()
 memory_info = psutil.virtual_memory()
 memory_usage = memory_info.percent
 if str(message.from_user.id)== OWNER:
  await client.send_animation(message.chat.id,"Images/animation.gif.mp4",f"`―――――――[STATS]―――――――`\n• 🎐 Status: Working\n• 🎐 Data: {date}\n• 🎐 Time: {now}\n• 🎐 Uptime: {uptime()}\n• 🎐 CPU: {cpu_usage}%\n• 🎐 Memory: {memory_usage}%\n `―――――――――――――――――`")





