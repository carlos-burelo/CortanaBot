from gtts import gTTS
import time
from datetime import datetime
from telegram import ChatAction

from telegram import ParseMode, Update, Bot
from telegram.ext import run_async
from haruka.modules.disable import DisableAbleCommandHandler
from haruka import dispatcher
import os

@run_async
def tts(bot: Bot, update: Update):
    message = update.effective_message
    reply = ""
    if message.reply_to_message:
        reply = message.reply_to_message.text

    current_time = datetime.strftime(datetime.now(), "%d.%m.%Y %H:%M:%S")
    filename = datetime.now().strftime("%d%m%y-%H%M%S%f")
    update.message.chat.send_action(ChatAction.RECORD_AUDIO)
    lang="ml"
    tts = gTTS(reply, lang)
    tts.save("k.mp3")
    with open("k.mp3", "rb") as f:
        linelist = list(f)
        linecount = len(linelist)
    if linecount == 1:
        update.message.chat.send_action(ChatAction.RECORD_AUDIO)
        lang = "en"
        tts = gTTS(reply, lang)
        tts.save("k.mp3")
    with open("k.mp3", "rb") as speech:
        update.message.reply_voice(speech, quote=False)

    os.remove("k.mp3")


__help__ = """
 - /tts text : Converted tex to speech"""

__mod_name__ = "Text to Speech"
tts_handle = DisableAbleCommandHandler("tts", tts)
dispatcher.add_handler(tts_handle)
