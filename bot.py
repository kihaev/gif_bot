from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, run_async
import requests
import re
import logging
import os
import sys


# Enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

# Getting mode, so we could define run function for local and Heroku setup
mode = os.getenv("MODE")
TOKEN = os.getenv("TOKEN")

if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)


def get_url(tag):
    contents = requests.get('https://api.giphy.com/v1/gifs/random?api_key=u861iwK4JA9tVpZXr3XQ4Gft2BLbZbux&tag=' + tag + '&rating=R').json()
    url = contents['data']['image_original_url']
    return url


def get_image_url(url):
    allowed_extension = ['gif']
    file_extension = ''
    while file_extension not in allowed_extension:
        file_extension = re.search("([^.]*)$", url).group(1).lower()
    return url


@run_async
def sexy_gif(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="So hot")
    tag = 'sexy-boobs'
    url = get_url(tag)
    url = get_image_url(url)
    chat_id = update.message.chat_id
    bot.sendAnimation(chat_id=chat_id, animation=url)


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, Nice to meet you! Send tag, please")


@run_async
def send_text(bot, update):
    tag = update.message.text
    bot.send_message(chat_id=update.message.chat_id, text="Nice tag")
    url = get_url(tag)
    url = get_image_url(url)
    chat_id = update.message.chat_id
    bot.sendAnimation(chat_id=chat_id, animation=url)


def stop(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I'm a bot, Why you bully me?")


def unknown(bot, update):
    bot.send_message(chat_id=update.message.chat_id,
                     text="Unknown command: " + update.message.text)


def about(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="GitHub: https://github.com/kihaev \nContact: @yuranusss")


def main():
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('sexy_gif', sexy_gif))
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('stop', stop))
    dp.add_handler(CommandHandler('about', about))
    dp.add_handler(MessageHandler(Filters.text, send_text))
    dp.add_handler(MessageHandler(Filters.command, unknown))
    run(updater)
    updater.idle()


if __name__ == '__main__':
    main()
