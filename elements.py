# -*- coding: utf-8 -*-

""" For Player """
import pyglet

""" For download music """
from threading import Thread

""" For clear RAM """
from gc import collect as clear_ram

""" For news """
import json
import requests
import lxml.html
from os import path
from os import remove as del_file

""" For Pictures """
from PIL import Image, ImageTk
from numpy import array as nump_array

""" For encode/decode db4 """
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


def read_news():
	def check_errors_db4():
		# check dir #
		if not path.exists('Databases'):
			mkdir('Databases')

		# check json file #
		if not path.exists('Databases\\database4'):
			print('none file')
			with open('Databases\\database4', 'w+') as json_db:
				json_db.write(encode_text('{"text": "", "id": 0}'))
		else:
			try:
				with open('Databases\\database4') as json_db:
					json.loads('"'.join(i for i in decode_text(json_db.read()).split("'")))
			except:
				with open('Databases\\database4', 'w+') as json_db:
					json_db.write(encode_text('{"text": "", "id": 0}'))

	def parse_news():
		text = ''

		try:
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}

			api = requests.get('https://github.com/D0Nater/BounceBit/blob/main/News.json', headers=headers)
			tree = lxml.html.document_fromstring(api.text)

			num = 1
			while True:
				try:
					text += tree.xpath(f'//*[@id="LC1"]/span[{num}]/text()')[0]
					text += tree.xpath(f'//*[@id="LC1"]/text()[{num}]')[0]
					num += 1
				except Exception as error:
					break

			text = json.loads(decode_text(text).replace("'", '"'))

		except:
			with open('Databases\\database4', encoding='utf-8') as json_db:
				text = json.loads(decode_text(json_db.read()).replace("'", '"'))

		return text

	check_errors_db4()

	new_news_data = parse_news()

	with open('Databases\\database4', encoding='utf-8') as json_db:
		json_data_db = json.loads(decode_text(json_db.read()).replace("'", '"'))

	if new_news_data['id'] != json_data_db['id']:
		with open('Databases\\database4', 'w+') as json_db:
			json_db.write(encode_text(str(new_news_data)))

		return new_news_data['text']

	return json_data_db['text']


def clear_list_of_songs():
	global list_of_songs_class
	for song in list_of_songs_class:
		del song
	clear_ram()
	list_of_songs_class = []


def del_picture_background(file, color, background):
	clear_ram()
	data = nump_array(Image.open(file).convert('RGB'))
	data[(data == (46,46,46)).all(axis=-1)] = background
	data[(data == (255,255, 255)).all(axis=-1)] = color
	return ImageTk.PhotoImage(Image.fromarray(data, mode='RGB'))


def update_program():
	pass


""" Elements for main program """
VERSION = '0.1'
AUTHOR = 'D0Nater'
GITHUB = 'github.com/D0Nater'
PROGRAM_NAME = 'Bounce Bit'

song_play_now = {"play": 0, "name": "", "author": "", "time": "", "url": "", "song_id": None, "num": 0}

player = pyglet.media.Player()
player_thread = None
player_bool = False
song_play_now_control = None
time_song_thread = False

song_time_now = '0:00'

past_song = {"class": None, "past_lib": None, "lib_now": None}

list_of_music = {}

list_of_songs_class = []

list_of_play = {}

themes = {
	'dark': {
		'background': 'grey18',
		'second_color': 'grey14',
		'text_color': 'white',
		'button_color': (255, 255, 255),
		'button_background': (46, 46, 46),
		'button_second_color': (36,36,36)
	},
	'light': {
		'background': 'floral white',
		'second_color': 'grey80',
		'text_color': 'grey11',
		'button_color': (28, 28, 28),
		'button_background': (250, 250, 250),
		'button_second_color': (204, 204, 204)
	},
	'purple': {
		'background': '#800080',
		'second_color': 'magenta4',
		'text_color': 'white',
		'button_color': (255, 255, 255),
		'button_background': (128, 0, 128),
		'button_second_color': (139, 0, 139)
	}
}

languages = {
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
	"Поиск" : {
		"ru": "Поиск",
		"en": "Search"
	},
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
	"Текст": {
		"ru": "Текст",
		"en": "Text"
	},
	"Фон": {
		"ru": "Фон",
		"en": "Background"
	},
	"Новости": {
		"ru": "Новости",
		"en": "News"
	},
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
	"Альбом": {
		"ru": "Альбом",
		"en": "Album"
	},
	"page": {
		"ru": "страница",
		"en": "page"
	},
	"open": {
		"ru": "открыть",
		"en": "open"
	},
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
	},
	"none_error": {
		"ru": "Упс, ничего не найдено ;(",
		"en": "Oops, not found ;("
	}
}
