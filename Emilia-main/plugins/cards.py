#import pymongo,asyncio
#from pyrogram import filters,Client
#from apscheduler.schedulers.asyncio import AsyncIOScheduler
#from apscheduler.schedulers.asyncio import AsyncIOScheduler
#from datetime import datetime, timedelta
#from bs4 import BeautifulSoup as bs
#import time,requests
#import json
#
#url = pymongo.MongoClient("mongodb+srv://debayankun:das1234@cluster0.jeihm5r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
#mongo = url["DataBase"]
#userscol = mongo["users"]
#chatscol = mongo["chats"]
#
#cards = [
#    {"id": "1", "image": "image1.png", "des": "First card description", "name": "Card1"},
#    {"id": "2", "image": "image2.png", "des": "Second card description", "name": "Card2"},
#    {"id": "3", "image": "image3.png", "des": "Third card description", "name": "Card3"}
#]
#
#
#def get_card():
# url = "https://shoob.gg/cards/info/66387b67fa5cef915a524f61"
# headers = {
#     "User-Agent": "TelegramBot (like TwitterBot)",
#     "Accept": "*/*",
#     "Accept-Language": "en-us",
#     "Content-Type": "application/json",
#     "Referer": "https://telegram.org/"
# }
# START = time.time()
# resp = requests.get(url, headers=headers)
# soup = bs(resp.content, "html.parser")
# 
# name = soup.select("li~ li+ li a span")[0].get_text()
# anime = soup.select("meta+ span")[0].get_text()
# tier = soup.select(".breadcrumb-new li:nth-child(3) span")[0].get_text()
# main_card = soup.select(".text-center > .card-main")
# video = soup.find("video")
# if video:
#     src = video.get("src")
# else:
#     image = soup.find('img', class_='img-fluid')
#     src = image.get("src")
# 
# data = {"name": name, "tier": tier, "anime": anime, "image": src}
# print(json.dumps(data, indent=4))
# print(f"Time taken: {time.time() - START}")
# return data
#
#
#def get_chat_ids():
#    chat_ids = chatscol.distinct('chat_id')
#    return chat_ids
#
#cards = []
#
#def remove(lst):
#    if lst:
#        lst.pop(0)
#    return lst
#
#
### Function to send a card
#def send_card():
#    #chat_ids = get_chat_ids()
#    #for chat_id in chat_ids:
#    card = get_card()
#    cards.append(card)
#    message_text = f"Card Name: {card['name']}\ntire: {card['tier']}\nanime: {card['anime']}\nimage: {card['image']}"
#    Client.send_message(chat_id=-1002001554826, text=message_text)
#
#send_card()
##scheduler = AsyncIOScheduler()
##scheduler.add_job(send_card, 'interval', minutes=10, next_run_time=datetime.now() + timedelta(minutes=10*i), args=[app, chat_id, card])
##scheduler.start()
#
#
#
#
#
#
#