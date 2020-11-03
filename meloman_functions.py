from bs4 import BeautifulSoup
from meloman_config import SITE2URLS
import requests


def get_html(url):
    try:
        result = requests.get(url)
        result.raise_for_status()
        return result.text
    except (requests.RequestException, ValueError) as e:
        print(f'Сетевая ошибка: {e}')
        return False


def get_audio_genres(site_name):
    '''
    Функция парсинга жанров сайтов soundcloud и betaport 
    '''
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


def get_list_tracks(url_site, genre_link):
    """
    Функция вывода треков по жанру
    """
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


def get_track(url_site, track_link):
    '''
    Функция вывода трека по номеру
    '''
    audio_track = url_site + track_link
    print(audio_track)
    return audio_track
    # request = requests.get(audio_track)
    # soup = BeautifulSoup(request.text, 'html.parser')
    # print (soup)
    # pass
    