# -*- coding: utf-8 -*-

import sys
from os import path

from tkinter import *

from threading import Thread

import time
from time import sleep as time_sleep

from gc import collect as clear_ram

from Scripts.images import MyImage

from Scripts.main import Main


def draw_just_lines():
    Main.JUST_LINE = Canvas(Main.ROOT, width=Main.SETTINGS.width, height=25, bg=themes[Main.SETTINGS.theme]["second_color"], bd=0, highlightthickness=0)
    Main.JUST_LINE.place(x=0, y=Main.SETTINGS.height-143)
    Main.JUST_LINE.create_line(0, 0, Main.SETTINGS.width, 0, width=1, fill="grey9")


def clear_list_of_songs():
    global list_of_songs_class
    for song in list_of_songs_class:
        if song not in Main.LIST_OF_PLAY["classes"] and song is not Main.PAST_SONG["class"]:
            song.del_class()
            del song
    clear_ram()
    list_of_songs_class.clear()


""" Elements for main program """
VERSION = "0.5.5"
AUTHOR = "D0Nater"
GITHUB = "https://github.com/D0Nater/BounceBit/"
LICENSE = "https://github.com/D0Nater/BounceBit/blob/main/LICENSE"
PROGRAM_NAME = "Bounce Bit"

text_for_readme = """ %s v%s

 Author: %s
 GitHub: %s
 License: %s

 Language: Python
 Interface: Tkinter
 Media player: Pyglet

 Don't delete files because you will lose data!

 BounceBit  -  Main File
 |
 |___Databases  -  Folder With Data
     |
     |___README  -  Readme
     |
     |___LICENSE  -  License
     |
     |___database1  -  Settings
     |
     |___database2  -  Added Music & Playlists
     |
     |___database3  -  Saved Music
     |
     |___database4  -  News
     |
     |___Download_Music  -  Folder With Your Music
"""

text_for_license = """
(The MIT License)

Copyright © 2021 D0Nater. All rights reserved.

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the
'Software'), to deal in the Software without restriction, including
without limitation the rights to use, copy, modify, merge, publish,
distribute, sublicense, and/or sell copies of the Software, and to
permit persons to whom the Software is furnished to do so, subject to
the following conditions:

The above copyright notice and this permission notice shall be
included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED 'AS IS', WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

list_of_music = {}

list_of_songs_class = []

themes = {
    "dark": {
        "background": "grey17",
        "second_color": "grey13",
        "text_color": "white",
        "text_second_color": "grey55"
    },
    "light": {
        "background": "grey90",
        "second_color": "grey75",
        "text_color": "grey4",
        "text_second_color": "grey35"
    },
    "purple": {
        "background": "#7D007D",
        "second_color": "#690069",
        "text_color": "white",
        "text_second_color": "grey60"
    },
    "red": {
        "background": "#AA1F1F",
        "second_color": "#821F1F",
        "text_color": "white",
        "text_second_color": "grey70"
    },
    "green": {
        "background": "#1E8C46",
        "second_color": "#1E6E46",
        "text_color": "white",
        "text_second_color": "grey80"
    },
    "blue": {
        "background": "#3C5AFA",
        "second_color": "#323CFA",
        "text_color": "white",
        "text_second_color": "grey75"
    }
}

languages = {
    # Buttons #
    "Загруженное": {
        "ru": "Загруженное",
        "en": "Loaded"
    },
    "Избранное": {
        "ru": "Избранное",
        "en": "Favorites"
    },
    "Рекомендации": {
        "ru": "Рекомендации",
        "en": "Recommendations"
    },
    "Сейчас_играет": {
        "ru": "Сейчас играет",
        "en": "Playing now"
    },

    # Settings #
    "Настройки": {
        "ru": "Настройки",
        "en": "Settings"
    },
    "Сохранить": {
        "ru": "Сохранить",
        "en": "Save"
    },
    "Тема": {
        "ru": "Тема",
        "en": "Theme"
    },
    "Фон": {
        "ru": "Фон",
        "en": "Background"
    },
    "Язык": {
        "ru": "Язык",
        "en": "Language"
    },
    "volume": {
        "ru": "Громкость",
        "en": "Volume"
    },
    "more": {
        "ru": "Больше",
        "en": "More"
    },
    "key_e": {
        "ru": "Назначение клавиш",
        "en": "Key assignment"
    },

    # Music genres #
    "Жанры": {
        "ru": "Жанры",
        "en": "Genres"
    },
    "Жанр": {
        "ru": "Жанр",
        "en": "Genre"
    },
    "Поп": {
        "ru": "Поп",
        "en": "Pop",
        "num": "2"
    },
    "Рок": {
        "ru": "Рок",
        "en": "Rock",
        "num": "6"
    },
    "Рэп": {
        "ru": "Рэп",
        "en": "Rap",
        "num": "3"
    },
    "Джаз": {
        "ru": "Джаз",
        "en": "Jazz",
        "num": "39"
    },
    "Шансон": {
        "ru": "Шансон",
        "en": "Shanson",
        "num": "14"
    },
    "Классика": {
        "ru": "Классика",
        "en": "Classical",
        "num": "28"
    },

    # Song info #
    "Трек": {
        "ru": "Трек",
        "en": "Track"
    },
    "Артист": {
        "ru": "Артист",
        "en": "Artist"
    },
    "Длительность": {
        "ru": "Длительность",
        "en": "Duration"
    },
    "Размер": {
        "ru": "Размер",
        "en": "Size"
    },

    # Playlists #
    "Плейлист": {
        "ru": "Плейлист",
        "en": "Playlist"
    },
    "add_pl": {
        "ru": "Добавить в плейлист",
        "en": "Add to playlist"
    },
    "create_pl": {
        "ru": "Создать Плейлист",
        "en": "Create Playlist"
    },
    "pl_name": {
        "ru": "Название Плейлиста",
        "en": "Playlist Name"
    },

    # Errors #
    "not_found": {
        "ru": "Упс, ничего не найдено ;(",
        "en": "Oops, nothing found ;("
    },
    "load_error": {
        "ru": "Упс, ничего не загружено ;(",
        "en": "Oops, nothing uploaded ;("
    },
    "add_error": {
        "ru": "Упс, сюда ничего не добавлено ;(",
        "en": "Oops, nothing added here ;("
    },
    "song_error": {
        "ru": "Упс, не удалось воспроизвести трек ;(",
        "en": "Oops, failed to play track ;("
    },
    "connect_error": {
        "ru": "Упс, не удалось подключиться к интернету ;(",
        "en": "Oops, could not connect to the internet ;("
    },

    # Other #
    "update_text": {
        "ru": "Доступно обновление",
        "en": "Update is available"
    },
    "Загрузка": {
        "ru": "Загрузка",
        "en": "Loading"
    },
    "Новости": {
        "ru": "Новости",
        "en": "News"
    },
    "Поиск" : {
        "ru": "Поиск",
        "en": "Search"
    },
    "Страница": {
        "ru": "страница",
        "en": "page"
    },
    "key_assignmet": {
        "ru": "Клавишы\n\n< SPACE > - Плей/Пауза\n\n< UP > - Сделать громче\n\n< DOWN > - Сделать тише\n\n< RIGHT > - Следующая песня\n\n< LEFT > - Предыдущая песня\n\n< Shift > - Информация о песне",
        "en": "Keyboard keys\n\n< SPACE > - Play/Pause\n\n< UP > - Make it louder\n\n< DOWN > - Make it quieter\n\n< RIGHT > - After song\n\n< LEFT > - Behind song\n\n< Shift > - Information about song"
    }
}
