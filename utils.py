from telegram import ReplyKeyboardMarkup

def start_keyboard():
	'''Клавиатура старта бота
	'''
	return ReplyKeyboardMarkup([['/music', 'dark side']], one_time_keyboard=True)


def main_keybord():
	'''Клавиатура старта Conversation meloman
	'''
	return ReplyKeyboardMarkup([['SoundCloud', 'BeatPort', 'Find track']], one_time_keyboard=True)


def quit_meloman_keybord():
	'''Клавиатура выхода Conversation meloman
	'''
	reply_keyboard = [['К выбору сайтов', 'К выбору жанров', 'Выйти из музыки']]
	return ReplyKeyboardMarkup(reply_keyboard)