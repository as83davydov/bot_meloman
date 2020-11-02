import requests
from bs4 import BeautifulSoup

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
def get_audio_genres(html):
    soup = BeautifulSoup(html, 'html.parser')
    genres = soup.select("a[href*=genre]")
    genre_links = []
    # print(genres) 
    for index, cur_genre in enumerate(genres[4:], 1):
        # title = cur_genre.findAll('a').text
        genre_title = cur_genre.text
        genre_links.append(cur_genre.get('href'))
        print(genre_links)
        print(str(index) + ':', genre_title)

    #выбор жанра и показ top 50 по каждому
    print()
    choice = input(">>> Ваш выбор (x to go back to the main menu): ")
    print()

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
        print(str(index + 1) + ':' + track.text)
        print()

 

if __name__ == "__main__":
        html = get_html("http://soundcloud.com/charts/top")
        if html:
#             # with open("soundcloud_charts_top.html", "w", encoding="utf8") as f:
#             #     f.write(html)
            get_audio_genres(html)