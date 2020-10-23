from utils import main_keybord

import requests
from bs4 import BeautifulSoup
    
#ф-я старта Conversation
def greet_user(update, context):
    text = 'Привет, пользователь! Выбирай сайт'
    # print(text)
    update.message.reply_text(text, reply_markup=main_keybord())
    return "site_choice"


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError) as e:
        print(f'Сетевая ошибка: {e}')
        return False


    # функция парсинга жанров сайтов soundcloud и betaport 
def get_audio_genres(site_name):
    context.user_data['meloman'] = {'url_site': url_user_site} # проверить
    if site_name == 'SoundCloud':
        url_user_site = get_html("http://soundcloud.com") # хардкод, скорее всего нужно перепарсить SoundCloud, чтобы старотовать с начальной страницы
        sc_user_site = get_html("http://soundcloud.com/charts/top")        
        soup = BeautifulSoup(sc_user_site, 'html.parser')
        genres = soup.select("a[href*=genre]")
        genre_links = []
        # print(genres)
        all_genres = ''
        for index, cur_genre in enumerate(genres[4:], 1):
            genre_title = cur_genre.text
            genre_links.append(cur_genre.get('href'))
            uot = str(index) + ': ' + genre_title
            # update.message.reply_text(uot)
            all_genres += '\n'+ uot           
        return all_genres        
    elif site_name == 'BeatPort':
        url_user_site = get_html("http://beatport.com")
        soup = BeautifulSoup(url_user_site, 'html.parser')
        genres = soup.findAll(class_="genre-drop-list__genre")
        genre_links = []
        all_genres = ''
        for index, cur_genre in enumerate(genres, 1):
            genre_title = cur_genre.text
            genre_bp_links.append(cur_genre.get('href'))                     
            out_bp = str(index) + ': ' + genre_title
            # print(out_bp)
            all_genres += '\n'+ out_bp
        return all_genres        
    else:
        return "Вы ввели неверно наименование сайта"


        # функция вывода треков по жанру
def get_list_tracks(number_track):
    number_track = (int(number_track) - 1)
    list_tracks = context.user_data['meloman']['url_site'] + genre_links[number_track]
    request = requests.get(list_tracks)
    soup = BeautifulSoup(requests.text, "html.parser")
    tracks = soup.select('h2')[3:]
    all_tracks = ''
    for index, track in enumerate(tracks):
        show_tracks = str(index + 1) + ': ' + track.text
        all_tracks += '\n' + show_tracks
    return all_tracks

    # хендлер вывода жанров
def genres_handler(update, context):
    selected_site = update.message.text
    # print(selected_site)
    if selected_site == 'SoundCloud' or 'BeatPort':
        genres = get_audio_genres(selected_site)
    # print(genres)
        update.message.reply_text(genres)
        update.message.reply_text('Введите номер жанра')
        return 'genre_choice' #chenged
    elif 'Find track':
        update.message.reply_text("Введи название трека")
        return 'track_search'
    else:
        pass

    хендлер вывода треков по жанру 
def number_genre_handler(update, context): 
    number_choice = update.message.text
    
    if not (type(number_choice) == int):
        # get_genres = get_audio_genres(number_choice)
        update.message.reply_text('Введите номер жанра')
        return 'genres_choice'
    else:        
        list_tracks = get_list_tracks(number_choice)
        update.message.reply_text(list_tracks)
        update.message.reply_text('Введите номер трека')
        return "next state" # изменить

    # elif 'Find track':
    #     update.message.reply_text("Введи название трека")
    #     return 'track_search'
    # else:
    #     pass


def number_track_handler(update, context):
    pass


def meloman_dontknow(update, context):
    update.message.reply_text('Я вас не понимаю')
