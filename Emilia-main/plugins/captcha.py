from pyrogram.types import InlineKeyboardMarkup,CallbackQuery,InlineKeyboardButton,Message,ChatPermissions
from pyrogram import Client, filters,enums
from Helpers.admincheck import admincheck
from captcha.image import ImageCaptcha
import random
import os,time
import sqlite3


def cpa(id):
    conn = sqlite3.connect('Limbo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT CAPTCHA FROM chat_data WHERE ID =?', (id,))
    row = cursor.fetchone()
    return row[0]

def eve(id):
    conn = sqlite3.connect('Limbo.db')
    cursor = conn.cursor()
    cursor.execute('SELECT EVENT FROM chat_data WHERE ID =?', (id,))
    row = cursor.fetchone()
    print(row[0])


def captcha():
  image = ImageCaptcha(fonts=['captcha/Roboto-BlackItalic.ttf','captcha/Roboto-Bold.ttf','captcha/Roboto-Bold.ttf','captcha/Roboto-Italic.ttf','captcha/Roboto-Light.ttf','captcha/Roboto-LightItalic.ttf','captcha/Roboto-Medium.ttf','captcha/Roboto-MediumItalic.ttf','captcha/Roboto-Regular.ttf','captcha/Roboto-Thin.ttf'])
  letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'M',
               'N', 'P', 'R', 'T', 'U', 'V', 'W', 'X', 'Y']
  captcha = random.sample(letters, 4)
  str = "".join(captcha)
  image.write(str, 'out.png')
  return str
  
 
#Pillow-9.5.0
@Client.on_message(filters.new_chat_members)
async def new_member(client: Client, message: Message):
  chat_titel = message.chat.title
  if cpa(message.chat.id) == "TRUE":
   global member
   new_members = message.new_chat_members
   for member in new_members:
    await client.restrict_chat_member(message.chat.id, member.id,ChatPermissions())
   global captcha_str
   captcha_str = captcha()
   # Define the three variables
   var1 = None
   var2 = None
   var3 = None
   
   # Assign 'das' to one of the three variables randomly
   selected_var = random.choice(['var1', 'var2', 'var3'])
   
   if selected_var == 'var1':
       var1 = captcha_str
   elif selected_var == 'var2':
       var2 = captcha_str
   else:
       var3 = captcha_str
   
   if not var1:
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'M',
                  'N', 'P', 'R', 'T', 'U', 'V', 'W', 'X', 'Y']
    randrom_str = random.sample(letters, 4)
    var1 = "".join(randrom_str)
   if not var2:
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'M',
                  'N', 'P', 'R', 'T', 'U', 'V', 'W', 'X', 'Y']
    randrom_str = random.sample(letters, 4)
    var2 = "".join(randrom_str)
   if not var3:
    letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'K', 'M',
                  'N', 'P', 'R', 'T', 'U', 'V', 'W', 'X', 'Y']
    randrom_str = random.sample(letters, 4)
    var3 = "".join(randrom_str)
   keybord=InlineKeyboardMarkup(
        [
            [InlineKeyboardButton(var1, callback_data =f"ver_{var1}"),
             InlineKeyboardButton(var2 , callback_data =f"ver_{var2}") ,
             InlineKeyboardButton(var3, callback_data =f"ver_{var3}")],

        ])
   global reply
   reply = await client.send_photo(message.chat.id,"out.png",caption=f"• 🎐 Welcome @{member.username} to {chat_titel} 🎉\nKindly solve this captcha to join the chat!",reply_markup = keybord)
   os.remove("out.png")
  else:
    return
  time.sleep(3*60)
  await client.delete_messages(message.chat.id, reply.id)


@Client.on_callback_query(filters.regex("ver_(.*)"))
async def switch(client, callback_query: CallbackQuery):
 if member.id == callback_query.from_user.id:
   if callback_query.data.split("_", 1)[1] == captcha_str:
    await client.restrict_chat_member(callback_query.message.chat.id, member.id,
    ChatPermissions(can_send_messages=True,can_send_media_messages=True))
    await client.delete_messages(callback_query.message.chat.idt_id, reply.id)
   elif callback_query.data.split("_", 1)[1] != captcha_str:
      await client.ban_chat_member(callback_query.message.chat.id, member.id)
      await client.delete_messages(callback_query.message.chat.idt_id, reply.id)
 else:
   await client.answer_callback_query(callback_query_id= callback_query.id ,text="• 🎐 This Captcha is not you!", show_alert=True)


  
   
   

   