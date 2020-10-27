from utils import main_keybord

import requests
from bs4 import BeautifulSoup

SITE2URLS = {
    'SoundCloud':{
        'top_url': "http://soundcloud.com/charts/top",
        'main_url': "http://soundcloud.com"
    },
    'BeatPort':{
        'main_url': "http://beatport.com"
    }
}

    
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
    if site_name == 'SoundCloud':
        #url_user_site = get_html("http://soundcloud.com") # хардкод, скорее всего нужно перепарсить SoundCloud, чтобы старотовать с начальной страницы
        sc_user_site = get_html(SITE2URLS[site_name]['top_url'])        
        soup = BeautifulSoup(sc_user_site, 'html.parser')
        genres = soup.select("a[href*=genre]")
        genre_links = []
        # print(genres)
        all_genres = ''
        for index, cur_genre in enumerate(genres[4:], 1):
            genre_title = cur_genre.text
            genre_links.append(cur_genre.get('href'))
            # print(genre_links)
            uot = str(index) + ': ' + genre_title
            # update.message.reply_text(uot)
            all_genres += '\n'+ uot           
        return all_genres, genre_links            
    elif site_name == 'BeatPort':
        url_user_site = get_html(SITE2URLS[site_name]['main_url'])
        soup = BeautifulSoup(url_user_site, 'html.parser')
        genres = soup.findAll(class_="genre-drop-list__genre")
        genre_links = []
        all_genres = ''
        for index, cur_genre in enumerate(genres, 1):
            genre_title = cur_genre.text
            genre_links.append(cur_genre.get('href'))                     
            out_bp = str(index) + ': ' + genre_title
            # print(out_bp)
            all_genres += '\n'+ out_bp
        return all_genres, genre_links        
    else:
        return "Вы ввели неверно наименование сайта"


        # функция вывода треков по жанру
def get_list_tracks(url_site, genre_link):
    list_tracks = url_site + genre_link
    print(list_tracks)
    request = requests.get(list_tracks)
    soup = BeautifulSoup(request.text, "html.parser")
    tracks = soup.select('h2')[3:]
    all_tracks = ''
    for index, track in enumerate(tracks):
        show_tracks = str(index + 1) + ': ' + track.text
        all_tracks += '\n' + show_tracks
    return all_tracks

    # хендлер вывода жанров
def genres_handler(update, context):
    selected_site = update.message.text
    context.user_data['meloman'] = {'url_site': SITE2URLS[selected_site]['main_url']} # проверить
    # print(selected_site)
    if selected_site == 'SoundCloud' or 'BeatPort':
        genres, genre_links = get_audio_genres(selected_site)
        context.user_data['meloman']['genres'] = genres
        context.user_data['meloman']['genre_links'] = genre_links
    # print(genres)
        update.message.reply_text(genres)
        update.message.reply_text('Введите номер жанра')
        return 'genre_choice' #chenged
    elif 'Find track':
        update.message.reply_text("Введи название трека")
        return 'track_search'
    else:
        pass

   # хендлер вывода треков по жанру 
def number_genre_handler(update, context): 
    number_choice = int(update.message.text) - 1
    url_site = context.user_data['meloman']['url_site']
    print(url_site)
    genres = context.user_data['meloman']['genres']
    genre_links = context.user_data['meloman']['genre_links']
    # print(genres)
    genres_index = {idx:link for idx, link in enumerate(genre_links)}
    # print(genres_index)
    selected_genre = genres_index[number_choice]
    # selected_genre = '/charts/top?genre=' + ss[number_choice]
    print(selected_genre)

    # print(number_choice, type(number_choice), selected_genre)

    if not isinstance(number_choice, int):
        # get_genres = get_audio_genres(number_choice)
        update.message.reply_text('Введите номер жанра')
        return 'genres_choice'
    else:        
        list_tracks = get_list_tracks(url_site, selected_genre)
        update.message.reply_text(list_tracks)
        update.message.reply_text('Введите номер трека')
        return "number_track_handler" # изменить

    # elif 'Find track':
    #     update.message.reply_text("Введи название трека")
    #     return 'track_search'
    # else:
    #     pass


def number_track_handler(update, context):
    pass


def meloman_dontknow(update, context):
    update.message.reply_text('Я вас не понимаю')
