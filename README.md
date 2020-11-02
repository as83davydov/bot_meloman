# Meloman Bot

Meloman Bot - это telegram-бот для отслеживания новинок и top музыкальных треков по жанрам на сайтах популярных мировых музыкальных чартов [SoundCloud.com](http://soundcloud.com/charts/top) и [BeatPort.com](http://beatport.com).
Пользователь вводит или выбирает на всплывающей клавиатуре наименование сайта 'SoundCloud' или 'BeatPort'.

<img src= "https://github.com/as83davydov/bot_meloman/blob/main/ScreenShots/Screenshot_1.jpg" width = "300" height = "633" >

Далее в мессенджере выводится список существующих на сайте музыкальных жанров и категорий и пользователю предлагается выбрать один из жанров, путем ввода порядкогового номера.

<img src= "https://github.com/as83davydov/bot_meloman/blob/main/ScreenShots/Screenshot_2.jpg" width = "300" height = "633" >

Затем пользователь получает список top (по версии сайта) композиций и бот предлагает выбрать номер трека по порядковому номеру для дальнейшего его прослушивания в встроенном браузере telegram или для дальнейшего перехода по ссылке на сайт.

<img src= "https://github.com/as83davydov/bot_meloman/blob/main/ScreenShots/Screenshot_3.jpg" width = "300" height = "633" >

После это пользователь получает список выбора дальнейших действий в виде всплывающей клавиатуры. Пользователь может перейти к выбору сайта, к списку жанров или выйти из музыкального режима и продолжить работу с ботом, используя его функционал.

<img src= "https://github.com/as83davydov/bot_meloman/blob/main/ScreenShots/Screenshot_4.jpg" width = "300" height = "633" >

Попробовать можно по ссылке [Meloman Bot](https://t.me/IamMelomanBot)
Из-за блокировки телеграма ссылка может не работать, в этом случае откройте телеграм и введите в поиске '@Meloman Bot'

## Установка

Скачайте проект с github:

```
https://github.com/as83davydov/bot_meloman
```

Создайте виртуальное окружение и установите зависимости
```
pip install -r requirements.txt
```

Создайте файл settings.py и создайте в нем базовае переменные:
```
API_KEY = "API ключ, который вы получили у BotFather"
PROXY_URL = "socks5://ВАШ_ПРОКСИ:1080"
PROXY_USERNAME = ЛОГИН
PROXY_PASSWORD = ПАРОЛЬ
```

## Запуск программы

Для запуска программы запустите файл 'bot.py', бот в мессенджере поприветствует Вас и предложит дальнейшие действия

```
python bot.py
```
или
```
python3 bot.py
```
если используете Mac OS