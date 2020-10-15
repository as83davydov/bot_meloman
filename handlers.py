from utils import main_keybord

    #soundcloud
import requests
from bs4 import BeautifulSoup
    
    # приветсвие
def greet_user(update, context):
    text = 'Привет, пользователь! Выбирай сайт'
    # print(text)
    update.message.reply_text(text, reply_markup=main_keybord())


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError) as e:
        print(f'Сетевая ошибка: {e}')
        return False

#     # вызов html жанров
# def get_soundcloud_genres(sc_top_html="http://soundcloud.com/charts/top")
#     sc_html = get_html(sc_top_html)
#     get_audio_genres

    # получаем список жанров и композиций
def get_audio_genres(update, context):
    url_soundcloud = get_html("http://soundcloud.com/charts/top")
    soup = BeautifulSoup(url_soundcloud, 'html.parser')
    genres = soup.select("a[href*=genre]")
    genre_links = []
    print(genres) 
    for index, cur_genre in enumerate(genres[4:], 1):
        genre_title = cur_genre.text
        genre_links.append(cur_genre.get('href'))
        # print(genre_links)
        uot = str(index) + ':', genre_title
        update.message.reply_text(uot)#, reply_markup=main_keybord())
    

    update.message.reply_text('Введите номер жанра')
    choise = context.args
    # print(choise)
    # update.message.reply_text(choise)
    # choice = input(">>> Ваш выбор (x to go back to the main menu): ")
    # print()

    if choice == "x": # загадка, пока не разобрался зачем это
        print ('Введите номер жанра') # в примере исп-ся break
    else:
        choice = (int(choice) - 1)

    url = "http://soundcloud.com" + genre_links[choice]
    request = requests.get(url)
    soup = BeautifulSoup(request.text, "html.parser")

    tracks = soup.select('h2')[3:]
    # print(tracks) #для проверки
    track_links = [] #нужно далее для выбора конкретного трека
    track_names = [] #нужно далее для выбора конкретного трека

    for index, track in enumerate(tracks):
        # track_links.append(track.a.get('href')) #смотри выше
        # track_names.append(track.text) #смотри выше
        uottt = str(index + 1) + ':' + track.text
        update.message.reply_text(uottt)
        # print()

# html = get_html("http://soundcloud.com/charts/top")
# if html:
#     get_audio_genres(html) 