from pyrogram import filters
from Helpers.admincheck import is_sudoadmin,check_membership
from pluginsuserBot.mediastream import app

@app.on_message(filters.command("slowmode") & ~filters.private)
async def slowmode(client, message):
    if await check_membership(message):
     chat_id = message.chat.id
     if len(message.command) < 2:
        await message.reply_text("• 🎐 /slowmode <time>")
     elif int(message.command[1]) not in [10,20,30]:
        await message.reply("• 🎐 More then 30 seconds can't be set")
     else:
      try:
       if not await is_sudoadmin(message):
           await message.repl_text("• 🎐 Sir, you don't have permissions do so.")
       else:
           sleep = int(message.command[1])
           await app.set_slow_mode(chat_id, sleep)
           await message.reply(f"• 🎐 Slow mode of has been set in **{message.chat.title}**")
      except:
         await message.reply(f"• 🎐 Slow mode is already turned on in **{message.chat.title}**")
    else:
     await message.reply_text("• 🎐 Sir, you haven't added the user bot.")
       
        

@app.on_message(filters.command("slowmode_off") & ~filters.private)
async def slowmode_off(client, message):
    if await check_membership(message):
     chat_id = message.chat.id
     try:
      if not await is_sudoadmin(message):
          await message.reply_text("• 🎐 Sir, you don't have permissions do so.")
      else:
          await app.set_slow_mode(chat_id, None)
          await message.reply(f"• 🎐 Slow mode has been set to off in **{message.chat.title}**")
     except:
         await message.reply(f"• 🎐 Slow mode is already turned off in **{message.chat.title}**")
    else:
     await message.reply_text("• 🎐 Sir, you haven't added the user bot.")
 
         
 
 
 
