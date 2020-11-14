# -*- coding: utf-8 -*-

""" For download music """
from threading import Thread

""" For clear RAM """
from gc import collect as clear_ram

""" For play music """
import pyglet
import pyglet.media as media
from time import sleep as time_sleep

""" For news """
import json
import requests
import lxml.html
from os import path

""" For Pictures """
import sys
from PIL import Image, ImageTk

""" For encode/decode db4 """
from music import parse_data
from settings import encode_text, decode_text


class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None, args=(), kwargs=None, *, daemon=None):
        Thread.__init__(self, group, target, name, args, kwargs, daemon=daemon)

        self._return = None

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join(self):
        Thread.join(self)
        return self._return


class MyPlayer:
    def __init__(self):
        self.player = pyglet.media.Player()
        self.play_song_while = False

    def new_song(self, song_id):
        self.player.queue(media.load(f'Databases/Download_Music/{song_id}.mp3'))

    def jump(self, time):
        self.player.seek(time)

    def next_song(self):
        self.player.next_source()

    def play(self):
        self.play_song_while = True
        while self.play_song_while:
            self.player.play()
            time_sleep(0.4)
        return

    def pause(self):
        self.player.pause()
        self.play_song_while = False

    def stop(self):
        self.pause()
        self.player.delete()


def resource_path(relative):
    # For EXE file #
    if hasattr(sys, "_MEIPASS"):
        return path.join(sys._MEIPASS, relative)
    return path.join(relative)


class LoadPicture:
    def load_picture(self, file):
        file = resource_path(path.join(self.folder, file))

        return ImageTk.PhotoImage(Image.open(file))


def check_errors_db4():
    # check dir #
    if not path.exists('Databases'):
        mkdir('Databases')

    # check json file #
    if not path.exists('Databases/database4'):
        with open('Databases/database4', 'w+') as json_db:
            json_db.write(encode_text('{"text":{"ru":"","en":""},"id":"","date":""}'))
    else:
        try:
            with open('Databases/database4') as json_db:
                json.loads(decode_text(json_db.read()).replace("'", '"'))
        except:
            with open('Databases/database4', 'w+') as json_db:
                json_db.write(encode_text('{"text":{"ru":"","en":""},"id":"","date":""}'))


def parse_new_news():
    def parse_news():
        text = ''

        try:
            # parse site #
            headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

            api = requests.get('https://github.com/D0Nater/BounceBit/blob/main/News', headers=headers)

            tree = lxml.html.document_fromstring(api.text)

            # parse and decode json text #
            text = json.loads(decode_text(tree.xpath(f'//*[@id="LC1"]/text()')[0]).replace("'", '"'))

        except Exception as error:
            with open('Databases/database4', encoding='utf-8') as json_db:
                text = json.loads(decode_text(json_db.read()).replace("'", '"'))

        return text

    check_errors_db4()

    # new news #
    new_news_data = parse_news()

    # news from database4 #
    with open('Databases/database4', encoding='utf-8') as json_db:
        json_data_db = json.loads(decode_text(json_db.read()).replace("'", '"'))

    if new_news_data['id'] != json_data_db['id']:
        with open('Databases/database4', 'w+') as json_db:
            json_db.write(encode_text(str(new_news_data)))


def read_news():
    check_errors_db4()

    with open('Databases/database4', encoding='utf-8') as json_db:
        json_data_db = json.loads(decode_text(json_db.read()).replace("'", '"'))

    return [json_data_db['date'], json_data_db['text']]


def clear_list_of_songs():
    global list_of_songs_class
    for song in list_of_songs_class:
        song.del_class()
        del song
    clear_ram()
    list_of_songs_class.clear()


""" Elements for main program """
VERSION = '0.2'
AUTHOR = 'D0Nater'
GITHUB = 'https://github.com/D0Nater/BounceBit/'
PROGRAM_NAME = 'Bounce Bit'

song_play_now = {"play": 0, "name": "", "author": "", "time": "", "url": "", "song_id": None, "num": 0, "loaded": False}

song_time_now = '00:00'

past_song = {"class": None, "song_id": None, "past_lib": None, "lib_now": None}

list_of_music = {}

list_of_songs_class = []

list_of_play = {'classes': []}

scroll_win = True

themes = {
    'dark': {
        'background': 'grey18',
        'second_color': 'grey14',
        'text_color': 'white'
    },
    'light': {
        'background': 'floral white',
        'second_color': 'grey80',
        'text_color': 'grey11'
    },
    'purple': {
        'background': '#7D007D',
        'second_color': '#690069',
        'text_color': 'white'
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

    # Settings #
    "Настройки": {
        "ru": "Настройки",
        "en": "Settings"
    },
    "Сохранить": {
        "ru": "Сохранить",
        "en": "Save"
    },
    "Язык": {
        "ru": "Язык",
        "en": "Lang"
    },

    # Themes #
    "Тема": {
        "ru": "Тема",
        "en": "Theme"
    },
    "Темная": {
        "ru": "Темная",
        "en": "Dark"
    },
    "Светлая": {
        "ru": "Светлая",
        "en": "Light"
    },
    "Пурпурная": {
        "ru": "Пурпурная",
        "en": "Purple"
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
        "en": "Pop"
    },
    "Рок": {
        "ru": "Рок",
        "en": "Rock"
    },
    "Рэп": {
        "ru": "Рэп",
        "en": "Rap"
    },
    "Джаз": {
        "ru": "Джаз",
        "en": "Jazz"
    },
    "Шансон": {
        "ru": "Шансон",
        "en": "Shanson"
    },
    "Классика": {
        "ru": "Классика",
        "en": "Classical"
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
    "Текст": {
        "ru": "Текст",
        "en": "Text"
    },

    # Playlists #
    "Плейлист": {
        "ru": "Плейлист",
        "en": "Playlist"
    },
    "add_song": {
        "ru": "Добавить трек",
        "en": "Add track"
    },
    "create_pl": {
        "ru": "Создать Плейлист",
        "en": "Create Playlist"
    },
    "pl_name": {
        "ru": "Название Плейлиста",
        "en": "Playlist Name"
    },
    "del_pl": {
        "ru": "Удалить плейлист?",
        "en": "Delete playlist?"
    },

    # Other #
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

    # Errors #
    "load_error": {
        "ru": "Упс, ничего не загружено ;(",
        "en": "Oops, nothing uploaded ;("
    },
    "add_error": {
        "ru": "Упс, сюда ничего не добавлено ;(",
        "en": "Oops, nothing added here ;("
    },
    "connect_error": {
        "ru": "Упс, не удалось подключиться к интернету ;(",
        "en": "Oops, could not connect to the internet ;("
    }
}
