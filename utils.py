from telegram import ReplyKeyboardMarkup

    #функция кнопок
def main_keybord():
    return ReplyKeyboardMarkup([['SoundCloud', 'BeatPort', 'Find track']], one_time_keyboard=True)


def quit_meloman_keybord():
    reply_keyboard = [['К выбору сайтов', 'К выбору жанров', 'Выйти из музыки']]
    return ReplyKeyboardMarkup(reply_keyboard)