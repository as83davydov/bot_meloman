import logging

import settings

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler

from meloman_handlers import greet_user, greet_meloman, genres_handler, get_tracks_genre_handler, number_track_handler, meloman_dontknow, operation_selection_handler


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

    meloman = ConversationHandler(
        entry_points=[
            MessageHandler(Filters.regex('music'), greet_meloman)
        ],
        states={
            "site_choice": [MessageHandler(Filters.regex('SoundCloud|BeatPort'), genres_handler)],
            "genre_choice": [MessageHandler(Filters.regex('^[0-9]$|^[123456789][0-9]$|^100$'), get_tracks_genre_handler)],
            "track_choice": [MessageHandler(Filters.regex('^[0-9]$|^[123456789][0-9]$|^100$'), number_track_handler)],
            "operation_selection": [MessageHandler(Filters.regex('К выбору сайтов|К выбору жанров|Выйти из музыки'), operation_selection_handler)]
            # "track_search": [MessageHandler(Filters.text, track_search_handler)]
        },
        fallbacks=[
            MessageHandler(Filters.text | Filters.photo | Filters.video | Filters.document | Filters.location, meloman_dontknow, operation_selection_handler)
        ]
    )

    dp.add_handler(meloman)
    
 
    logging.info('Bot have started')
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
    