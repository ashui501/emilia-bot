from pyromod import Client
from pluginsuserBot.mediastream import run 


APP_ID=
API_HASH=
BOT_TOKEN=

bot = Client('Bot', api_id=APP_ID, api_hash=API_HASH, bot_token=BOT_TOKEN, plugins = dict(root="plugins"))




run()
bot.run()


 





