import logging

import settings

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

from handlers import greet_user, get_audio_genres


logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

PROXY = {
    'proxy_url': settings.PROXY_URL,
    'urllib3_proxy_kwargs': {
        'username': settings.PROXY_USERNAME,
        'password': settings.PROXY_PASSWORD
    }
}


def main():
    mybot = Updater(settings.API_KEY, request_kwargs=PROXY, use_context=True)

    dp = mybot.dispatcher
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("SoundCloud", get_audio_genres))
    # dp.add_handler(CommandHandler("BeatPort", get_genres))

    logging.info('Bot have started')
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()