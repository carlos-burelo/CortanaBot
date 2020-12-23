from emoji import UNICODE_EMOJI
from google_trans_new import LANGUAGES, google_translator
from telegram import ParseMode, Update
from telegram.ext import Filters, MessageHandler, run_async
from haruka import dispatcher, LOGGER
from typing import Optional, List
from haruka.modules.disable import DisableAbleCommandHandler
from telegram import Message, Update, Bot, User
from telegram import MessageEntity


# @run_async
# def do_translate(bot: Bot, update: Update, args: List[str]):
#     msg = update.effective_message # type: Optional[Message]
#     lan = " ".join(args)
#     try:
#         to_translate_text = msg.reply_to_message.text
#     except:
#         return
#     # translator = google_translator()
#     trl = google_translator()
#     try:
#         translated = translator.translate(to_translate_text, dest=lan)
#         src_lang = translated.src
#         translated_text = translated.text
#         msg.reply_text("{}".format(src_lang, lan, translated_text))
#     except :
#         msg.reply_text("Error")
@run_async
def do_translate(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message
    problem_lang_code = []
    for key in LANGUAGES:
        if "-" in key:
            problem_lang_code.append(key)

    try:
        if message.reply_to_message:
            args = update.effective_message.text.split(None, 1)
            if message.reply_to_message.text:
                text = message.reply_to_message.text
            elif message.reply_to_message.caption:
                text = message.reply_to_message.caption

            try:
                source_lang = args[1].split(None, 1)[0]
            except (IndexError, AttributeError):
                source_lang = "en"

        else:
            args = update.effective_message.text.split(None, 2)
            text = args[2]
            source_lang = args[1]

        if source_lang.count('-') == 2:
            for lang in problem_lang_code:
                if lang in source_lang:
                    if source_lang.startswith(lang):
                        dest_lang = source_lang.rsplit("-", 1)[1]
                        source_lang = source_lang.rsplit("-", 1)[0]
                    else:
                        dest_lang = source_lang.split("-", 1)[1]
                        source_lang = source_lang.split("-", 1)[0]
        elif source_lang.count('-') == 1:
            for lang in problem_lang_code:
                if lang in source_lang:
                    dest_lang = source_lang
                    source_lang = None
                    break
            if dest_lang is None:
                dest_lang = source_lang.split("-")[1]
                source_lang = source_lang.split("-")[0]
        else:
            dest_lang = source_lang
            source_lang = None

        exclude_list = UNICODE_EMOJI.keys()
        for emoji in exclude_list:
            if emoji in text:
                text = text.replace(emoji, '')

        trl = google_translator()
        if source_lang is None:
            detection = trl.detect(text)
            trans_str = trl.translate(text, lang_tgt=dest_lang)
            return message.reply_text(
                f"Translated from `{detection[0]}` to `{dest_lang}`:\n`{trans_str}`",
                parse_mode=ParseMode.MARKDOWN)
        else:
            trans_str = trl.translate(
                text, lang_tgt=dest_lang, lang_src=source_lang)
            message.reply_text(
                f"Translated from `{source_lang}` to `{dest_lang}`:\n`{trans_str}`",
                parse_mode=ParseMode.MARKDOWN)

    except IndexError:
        update.effective_message.reply_text(
            "Use: `/tr en` for automatic detection and translating it into English.\n"
            "See [List of Language Codes](t.me/CortanaSupport/12) for a list of language codes.",
            parse_mode="markdown",
            disable_web_page_preview=True)
    except ValueError:
        update.effective_message.reply_text(
            "The intended language is not found!")
    else:
        return

__help__ = """Example: `/tr en` to translate to English.
"""
__mod_name__ = "Translator"

dispatcher.add_handler(DisableAbleCommandHandler("tr", do_translate, pass_args=True))
