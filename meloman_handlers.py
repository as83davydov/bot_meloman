
from meloman_config import SITE2URLS
from meloman_functions import get_audio_genres, get_list_tracks, get_track
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
from utils import start_keyboard, main_keybord, quit_meloman_keybord


def greet_user(update, context):
    '''Функция приветсвия
    '''
    text = 'Добро пожаловать!'
    update.message.reply_text(text, reply_markup=start_keyboard())
        

def greet_meloman(update, context):
    '''Функция старта Conversation meloman
    '''
    text = 'Ваш выбор'
    update.message.reply_text(text, reply_markup=main_keybord())
    return "site_choice"


def genres_handler(update, context):
    '''Хендлер вывода жанров
    '''
    selected_site = update.message.text
    context.user_data['meloman'] = {'url_site': SITE2URLS[selected_site]['main_url']}
    # print(selected_site)
    if selected_site == 'SoundCloud' or 'BeatPort':
        genres, genre_links = get_audio_genres(selected_site)
        context.user_data['meloman']['genres'] = genres
        context.user_data['meloman']['genre_links'] = genre_links
    # print(genres)
        update.message.reply_text(genres)
        update.message.reply_text(
            'Введите номер жанра',
            reply_markup=ReplyKeyboardRemove()
        )
        return 'genre_choice'
    elif 'Find track':
        update.message.reply_text("Введи название трека")
        return 'track_search'
    else:
        pass


def number_genre_handler(update, context):
    '''Хендлер вывода треков по жанру 
    '''
    number_choice = int(update.message.text) - 1
    url_site = context.user_data['meloman']['url_site']
    print(url_site)
    genres = context.user_data['meloman']['genres']
    genre_links = context.user_data['meloman']['genre_links']
    genres_index = {idx:link for idx, link in enumerate(genre_links)}
    selected_genre = genres_index[number_choice]
    if not isinstance(number_choice, int):
        update.message.reply_text('Введите номер жанра')
        return 'genre_choice'
    else:        
        all_tracks, track_links = get_list_tracks(url_site, selected_genre)
        update.message.reply_text(all_tracks)
        context.user_data['meloman']['track_links'] = track_links
        update.message.reply_text('Введите номер трека')
        return "track_choice"

    # elif 'Find track':
    #     update.message.reply_text("Введи название трека")
    #     return 'track_search'
    # else:
    #     pass


def number_track_handler(update, context):
    '''Хендлер вывода трека по номеру
    '''
    number_choice = int(update.message.text) - 1
    if number_choice > 0:
        url_site = context.user_data['meloman']['url_site']
        # tracks = context.user_data['meloman']['tracks']
        track_links = context.user_data['meloman']['track_links']
        tracks_index = {idx:link for idx, link in enumerate(track_links)}
        selected_track = track_links[number_choice]
        # print(selected_track)
        track_link = get_track(url_site, selected_track)
        update.message.reply_text(track_link)
        update.message.reply_text("Введите номер трека из списка выше или введите '0' для возврата в меню")       
        return "track_choice"
    else:
        number_choice == 0
        update.message.reply_text('Сделайте выбор', reply_markup=quit_meloman_keybord())
        return "operation_selection"


def operation_selection_handler(update, context):
    '''хендлер выбора действий
    '''
    selected_choice = update.message.text
    if selected_choice == 'К выбору сайтов':
        update.message.reply_text('Введите имя сайта или нажмите кнопку ниже', reply_markup=main_keybord())
        return 'site_choice'
    elif selected_choice == 'К выбору жанров':
        update.message.reply_text('Введите номер жанра')
        return 'genre_choice'
    else:
        selected_choice == 'Выйти из музыки'
        update.message.reply_text('Приходи еще', reply_markup=ReplyKeyboardRemove())
        # update.message.reply_text(reply_markup=start_keyboard())
        return ConversationHandler.END
    

def meloman_dontknow(update, context):
    update.message.reply_text('Я вас не понимаю')
