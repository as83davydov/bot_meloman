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
    if site_name == 'SoundCloud':
        url_soundcloud = get_html("http://soundcloud.com/charts/top")
        soup = BeautifulSoup(url_soundcloud, 'html.parser')
        genres = soup.select("a[href*=genre]")
        genre_sc_links = []
        # print(genres)
        all_sc_genres = ''
        for index, cur_sc_genre in enumerate(genres[4:], 1):
            genre_sc_title = cur_sc_genre.text
            genre_sc_links.append(cur_sc_genre.get('href'))
            uot = str(index) + ': ' + genre_sc_title
            # update.message.reply_text(uot)
            all_sc_genres += '\n'+ uot           
        return all_sc_genres
        
        #ненужно начало
        # update.message.reply_text('Введите номер жанра')
        # choise = context.args
        # # print(choise)
        # # update.message.reply_text(choise)
        # # choice = input(">>> Ваш выбор (x to go back to the main menu): ")
        # # print()

        # if choice == "x": # загадка, пока не разобрался зачем это
        #     print ('Введите номер жанра') # в примере исп-ся break
        # else:
        #     choice = (int(choice) - 1)
        #ненужно конец
        
        # url = "http://soundcloud.com" + genre_links[choice]
        # request = requests.get(url)
        # soup = BeautifulSoup(request.text, "html.parser")

        # tracks = soup.select('h2')[3:]
        # # print(tracks) #для проверки
        # track_links = [] #нужно далее для выбора конкретного трека
        # track_names = [] #нужно далее для выбора конкретного трека

        # all_genres = ''
        # for index, track in enumerate(tracks):
        #     # track_links.append(track.a.get('href')) #смотри выше
        #     # track_names.append(track.text) #смотри выше
        #     uottt = str(index + 1) + ':' + track.text
        # #     all_genres += '\n'+ uottt            
        # # return all_genres

    elif site_name == 'BeatPort':
        url_beatport = get_html("http://beatport.com")
        soup = BeautifulSoup(url_beatport, 'html.parser')
        all_bp_genres = soup.findAll(class_="genre-drop-list__genre")
        genre_bp_links = []
        bp_genres = ''
        for index, cur_bp_genre in enumerate(all_bp_genres, 1):
            genre_bp_title = cur_bp_genre.text
            genre_bp_links.append(cur_bp_genre.get('href'))                     
            out_bp = str(index) + ': ' + genre_bp_title
            print(out_bp)
            bp_genres += '\n'+ out_bp
        return bp_genres        
    else:
        return "Вы ввели неверно наименование сайта"

    # хендлер вывода жанров
def genres_handler(update, context):
    selected_site = update.message.text
    # print(selected_site)
    genres = get_audio_genres(selected_site)
    # print(genres)
    update.message.reply_text(genres)
    update.message.reply_text('Введите номер жанра')
    return 'track_choice'

    # хендлер должен идти следующим после genres_handler
def site_choice_handler(update, context): 
    choice = update.message.text
    
    if choice == 'SoundCloud' or 'BeatPort':
        get_genres = get_audio_genres(choice)
        update.message.reply_text('Введите название трека')
        return 'genre_choice'

    # elif 'Find track':
    #     update.message.reply_text("Введи название трека")
    #     return 'track_search'
    else:
        pass

def meloman_dontknow(update, context):
    update.message.reply_text('Я вас не понимаю')
