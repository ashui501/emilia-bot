from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pluginsuserBot.mediastream import call_py
from pyrogram.types import CallbackQuery
from pytgcalls import PyTgCalls
from Helpers.admincheck import admincheck,check_membership
from pytgcalls.types import Update
from Helpers.ytdl import music_dl
from pytgcalls import filters as call_filters
from pytgcalls.types import MediaStream, VideoQuality, AudioQuality
import mimetypes, os,time

playlist = []

playing = False


def delete_all_files(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")


def scan_folder(folder_path):
    files = []
    for root, dirs, filenames in os.walk(folder_path):
        for filename in filenames:
            file_path = os.path.join(root, filename)
            files.append(file_path)
    return files


async def play(chat_id):
    global playing
    playing = True
    if playlist:
        current_song = playlist[0]
        mime_type, _ = mimetypes.guess_type(current_song)
        if mime_type == "audio/mpeg":
            await call_py.play(
                chat_id,
                MediaStream(current_song, AudioQuality.HIGH),
            )
        else:
            await call_py.play(
                chat_id,
                MediaStream(
                    current_song,
                    video_parameters=VideoQuality.HD_720p,
                ),
            )


@call_py.on_update(call_filters.stream_end)
async def on_stream_ended(client: PyTgCalls, update: Update):
    global playing
    if playlist:
        current_song = playlist.pop(0)
        if os.path.exists(current_song):
            os.remove(current_song)
        await play(update.chat_id)
        playing = True
    else:
        await call_py.leave_call(update.chat_id)
        playing = False




@Client.on_message(filters.command("play"))
async def owner(client, message):
    user_name = message.from_user.username
    if await check_membership(message):
     if len(message.command) < 2:
         return await message.reply_text(
             f"• 🎐 ERROR: Provide the youtube video link🔗 to download."
         )
     btn = InlineKeyboardMarkup(
         [
             [
                 InlineKeyboardButton("Music 🎧", callback_data="play_music"),
                 InlineKeyboardButton("Video 📹", callback_data="play_video"),
             ]
         ]
     )
     await client.send_message(
         message.chat.id,
         f"• 🎐 What do you want to play 📹 or 🎧 {user_name} ?",
         reply_markup=btn,
     )
     global link
     link = message.command[1]
     time.sleep(1)
     await message.delete()
    else:
     await message.reply_text("• 🎐 Sir, you haven't added the user bot.")


@Client.on_callback_query(filters.regex("play_(.*)"))
async def switch(client, callback_query: CallbackQuery):
    global playlist
    user_name = callback_query.message.from_user.username
    keybord = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("▶️", callback_data="media_resume"),
                InlineKeyboardButton("⏸️ ", callback_data="media_pause"),
                InlineKeyboardButton(" 🔚", callback_data="media_stop"),
                InlineKeyboardButton(" ⏭", callback_data="media_skip"),
            ],
        ]
    )
    if await admincheck(callback_query.message):
        if callback_query.data.split("_", 1)[1] == "video":
         await client.answer_callback_query(
             callback_query_id=callback_query.id,
             text="• 🎐 This feature is currnetly unavailable !!",
             show_alert=True,
         )
        elif callback_query.data.split("_", 1)[1] == "music":
            music_dl(link, "downloads")
            folder_path = "downloads"
            playlist = scan_folder(folder_path)
            if playing == False:
                await play(callback_query.message.chat.id)
                await client.send_message(
                    callback_query.message.chat.id,
                    text=f"• 🎐 [Control center]",
                    reply_markup=keybord,
                )
    else:
        await client.edit_message_text(
            callback_query.message.chat.id,
            callback_query.message.id,
            text=f"• 🎐 {user_name} you don't have permissions do this!",
        )


@Client.on_callback_query(filters.regex("media_(.*)"))
async def controls(client, callback_query: CallbackQuery):
    user_name = callback_query.message.from_user.username
    if await admincheck(callback_query.message):
        if callback_query.data.split("_", 1)[1] == "resume":
            await call_py.resume_stream(
                callback_query.message.chat.id,
            )
        elif callback_query.data.split("_", 1)[1] == "pause":
            await call_py.pause_stream(
                callback_query.message.chat.id,
            )
        elif callback_query.data.split("_", 1)[1] == "stop":
            delete_all_files("downloads")
            playlist.clear()
            await call_py.leave_call(callback_query.message.chat.id)
            await client.send_message(
                callback_query.message.chat.id,
                text="• 🎐 stream has ended. Thanks for our services!",
            )
        elif callback_query.data.split("_", 1)[1] == "skip":
            if playlist:
                current_song = playlist.pop(0)
                if os.path.exists(current_song):
                    os.remove(current_song)
                if playlist:
                    await play(callback_query.message.chat.id)
                    await client.send_message(
                        callback_query.message.chat.id,
                        text="• 🎐 Skipped to the next song!",
                    )
                else:
                    await client.send_message(
                        callback_query.message.chat.id,
                        text="• 🎐 No more songs in the playlist!",
                    )
            else:
                await client.send_message(
                    callback_query.message.chat.id, text="• 🎐 No songs to skip!"
                )
    else:
        await client.edit_message_text(
            callback_query.message.chat.id,
            callback_query.message.id,
            text=f"• 🎐 {user_name} you don't have permissions do this!",
        )
