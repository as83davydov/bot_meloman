from bs4 import BeautifulSoup
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ConversationHandler
import requests
from utils import main_keybord, quit_meloman_keybord

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
        return "Вы ввели неверно наименование сайта" # в данном случае это не нужно, сообщение можно выводить в хендлере


# функция вывода треков по жанру
def get_list_tracks(url_site, genre_link):
    list_tracks = url_site + genre_link
    print(list_tracks)
    request = requests.get(list_tracks)
    soup = BeautifulSoup(request.text, "html.parser")
    tracks = soup.select('h2')[3:33]
    track_links = []
    all_tracks = ''
    for index, track in enumerate(tracks):
        show_tracks = str(index + 1) + ': ' + track.text
        all_tracks += '\n' + show_tracks
        track_links.append(track.a.get('href'))
        print(track_links)
    return all_tracks, track_links
    # return all_tracks


#функция вывода трека по номеру
def get_track(url_site, track_link):
    audio_track = url_site + track_link
    print(audio_track)
    return audio_track
    # request = requests.get(audio_track)
    # soup = BeautifulSoup(request.text, 'html.parser')
    # print (soup)
    # pass
    


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


# хендлер вывода треков по жанру 
def number_genre_handler(update, context): 
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
        context.user_data['meloman']['track_links'] = track_links #added
        update.message.reply_text('Введите номер трека')
        return "track_choice"

    # elif 'Find track':
    #     update.message.reply_text("Введи название трека")
    #     return 'track_search'
    # else:
    #     pass


# хендлер вывода трека по номеру
def number_track_handler(update, context):
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
        update.message.reply_text("Для выбора трека введите номер из списка выше или введите '0' для возврата в меню")       
        return "track_choice"
    else:
        number_choice == 0
        update.message.reply_text('Сделайте выбор', reply_markup=quit_meloman_keybord())
        return "operation_selection"

# хендлер выбора действий
def operation_selection_handler(update, context):
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
        return ConversationHandler.END
    

def meloman_dontknow(update, context):
    update.message.reply_text('Я вас не понимаю')
