import logging

import settings

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from handlers import greet_user, genres_handler, get_audio_genres, site_choice_handler, meloman_dontknow #add


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

    meloman = ConversationHandler(
        entry_points=[
            CommandHandler('Start', greet_user) #add
        ],
        states={
            "site_choice": [MessageHandler(Filters.regex('SoundCloud|BeatPort'), genres_handler)],
            # "site_choice": [MessageHandler(Filters.regex('SoundCloud|BeatPort'), site_choice_handler)], #название хендлера иное см строку 100 в handlers
            # "genre_choice": [MessageHandler(Filters.regex, genre_choice_handler)], #add
            # "track_choice": [MessageHandler(Filters.text, get_sc_tracks)] #add
            # "track_search": [MessageHandler(Filters.text, file_search_handler)]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, meloman_dontknow)
        ]
    )

    dp.add_handler(meloman)
    

    # dp.add_handler(CommandHandler("Start", greet_user))
    # dp.add_handler(CommandHandler("BeatPort", get_genres))

    logging.info('Bot have started')
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()