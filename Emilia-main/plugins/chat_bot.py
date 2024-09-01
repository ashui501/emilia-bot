from pyrogram import Client,filters
import requests


def emilia(msg,user_id) -> str:
 url = requests.get(f"https://oni-chan-unique-api.vercel.app/forge?user={user_id}&text={msg}")
 response = url.json()['response']
 return response

@Client.on_message(filters.all,group=-1)
async def chatbot(client, message):
    try:
     my_list = []
     sentence = message.text
     words = sentence.split()
     my_list.extend(words)
     if not message.from_user.is_bot:
       if my_list[0] in ['emilia','Emilia'] :
        msg = ' '.join(words[1:])
        res = emilia(msg, message.from_user.id)
        await message.reply_text(res)
        my_list.clear()
       elif message.reply_to_message:
         if message.reply_to_message and message.reply_to_message.from_user.id == (await client.get_me()).id:
          res = emilia(message.text, message.from_user.id)
          await message.reply_text(res) 
          my_list.clear()
     else:
       return
    except Exception as e:
      await message.reply_text(f'```[ERROR]{e}```')


