import logging
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Bot
from datetime import datetime
from dprocessor import DialogProcessor
from TextNotofocationProcessor import NotificationsORM
import threading
from log import Log
import pytz

dprocessor = DialogProcessor()
notifications = NotificationsORM()
sender = None


def start(token):
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    logger = logging.getLogger(__name__)

    updater = Updater(token=token, use_context=True)
    global sender
    sender = Bot(token=token)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start_callback))
    dp.add_handler(CommandHandler("help", help_callback))
    dp.add_handler(CommandHandler("show", show_callback))
    dp.add_handler(MessageHandler(Filters.text | Filters.video | Filters.photo | Filters.document, reply_text_callback))
    dp.add_handler(MessageHandler(Filters.photo | Filters.document, reply_document_callback))

    dp.add_error_handler(error_callback)
    updater.start_polling()
    Log("Bot Started!")
    set_checker()
    updater.idle()


def reply_text_callback(update, context):
    """Answer user message."""
    if update.message is None:
        return
    reply = dprocessor.process_text(update.message.text, update.effective_chat.id)
    update.message.reply_text(reply)


def reply_document_callback(update, context):
    """Answer user message."""
    update.message.reply_text("В данный момент не реализовано")


def show_callback(update, context):
    """Send a message when the command /show is issued."""
    update.message.reply_text(notifications.show_all(update.effective_chat.id))


def start_callback(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text(
        'Привет\nОтправь мне сообщение чтоб добавить напоминание!\nИспользуйте чтоб создать напоминание: '
        'Напомни *когда* *что*')


def help_callback(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Используйте чтоб создать напоминание: Напомни *когда* *что*')


def error_callback(update, context):
    """Log Errors caused by Updates."""
    Log(context.error)


def check():
    remindings = notifications.get_all(datetime.now())
    for remind in remindings:
        sender.send_message(chat_id=remind.chat_id, text="ВНИМАНИЕ!!! - " + remind.payload)
        Log("Send notification to %i" % (remind.chat_id))
        remind.delete_instance()


def set_checker():
    threading.Timer(10.0, set_checker).start()
    check()
