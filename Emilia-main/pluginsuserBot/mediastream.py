from pyrogram import Client
from pytgcalls import PyTgCalls
from pyrogram import filters
from Helpers.admincheck import is_sudoadmin
import time 

APP_ID=28359218
API_HASH='7b00b1e0f2abd35cd81bdfe931570b50'
OWNER = 1152935968


app = Client('app', api_id=APP_ID, api_hash=API_HASH, plugins = dict(root="pluginsuserBot"))
call_py = PyTgCalls(app)




run = call_py.start






        






