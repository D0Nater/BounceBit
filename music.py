# -*- coding: utf-8 -*-

import sqlite3
from os import path, mkdir, remove
from base64 import b64decode, b64encode

""" For clear RAM """
from gc import collect as clear_ram

""" For download music """
import requests
from mutagen.easyid3 import EasyID3

""" For Parse """
import requests
import lxml.html
from lxml import etree


def decode_text(text):
	"""
	Return decoced text
	"""
	translated = ''
	i = len(text) - 1
	while i >= 0:
		translated = translated + text[i]
		i = i - 1
	decode_text = (b64decode(translated)).decode("UTF-8")
	return decode_text


def encode_text(text):
	"""
	Return encoded text
	"""
	encode_text = (b64encode(text.encode("UTF-8"))).decode()
	translated = ''
	i = len(encode_text) - 1
	while i >= 0:
		translated = translated + encode_text[i]
		i = i - 1
	return translated


def error_correction():
	"""
	If file 'database2.sqlite' or 'database3.sqlite' is damaged,
	music are reset and new ones are created
	"""
	if not path.exists("Databases"):
		mkdir("Databases")

	def check_db(db_name):

		conn = sqlite3.connect(f'Databases\\{db_name}')
		cursor = conn.cursor()

		try:
			cursor.execute('SELECT * FROM user_music WHERE name=?', (encode_text("test_name"),)).fetchone()
		except sqlite3.DatabaseError:
			conn.close()
			remove(f'Databases\\{db_name}')
			conn = sqlite3.connect(f'Databases\\{db_name}')
			cursor = conn.cursor()

		try:
			cursor.execute('SELECT * FROM user_albums WHERE name=?', (encode_text("test_name"),)).fetchone()
		except sqlite3.DatabaseError:
			conn.close()
			remove(f'Databases\\{db_name}')
			conn = sqlite3.connect(f'Databases\\{db_name}')
			cursor = conn.cursor()

		try: cursor.execute('CREATE TABLE user_music (name, author, url, song_time, num, song_id)')
		except: pass

		try: cursor.execute('CREATE TABLE user_albums (name, params, num)')
		except: pass

		conn.commit()
		conn.close()

	check_db('database2.sqlite') # add music
	check_db('database3.sqlite') # download music


search_music_json = {"music": {"num": 0}, "music_albums": {"num": 0}, "url": "", "connect": False}


class Music:
	def download_music(song_id, url):
		if not path.exists("Databases\\Download_Music"):
			mkdir("Databases\\Download_Music")

		with open(f'Databases\\Download_Music\\{song_id}.mp3', "wb") as f:
			response = requests.get(requests.get(f'https://zaycev.net{url}').json()['url'], stream=True)
			total_length = response.headers.get('content-length')

			if total_length is None:
				f.write(response.content)
			else:
				dl = 0
				total_length = int(total_length)
				for data in response.iter_content(chunk_size=4096):
					dl += len(data)
					f.write(data)

		audio = EasyID3(f'Databases\\Download_Music\\{song_id}.mp3')
		audio['title'] = u""
		audio['artist'] = u""
		audio['album'] = u"BounceBit"
		audio['composer'] = u""
		audio.save()

	def delete_music(song_id):
		if path.exists(f'Databases\\Download_Music\\{song_id}.mp3'):
			remove(f'Databases\\Download_Music\\{song_id}.mp3')

	def top_music(url='https://zaycev.net/'):
		global search_music_json
		clear_ram()
		try:
			if search_music_json['url'] != url or not search_music_json['connect']:
				search_music_json = {"music": {"num": 0}, "music_albums": {"num": 0}, "url": ""}
				search_music_json['url'] = url
				
				headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
				api = requests.get(url, headers=headers)

				search_music_json['connect'] = True

				tree = lxml.html.document_fromstring(api.text)

				for num in range(1, 61):
					new_song = {
						"name": tree.xpath(f'//*[@id="top_1"]/div[2]/div[{num}]/div[1]/div[2]/div[3]/a/text()')[0],
						"author": tree.xpath(f'//*[@id="top_1"]/div[2]/div[{num}]/div[1]/div[2]/div[1]/a/text()')[0],
						"url": tree.xpath(f'//*[@id="top_1"]/div[2]/div[{num}]/@data-url')[0],
						"song_time": tree.xpath(f'//*[@id="top_1"]/div[2]/div[{num}]/div[2]/text()')[0],
						"song_id": tree.xpath(f'//*[@id="top_1"]/div[2]/div[{num}]/@data-id')[0]
					}
					search_music_json['music'][f'song{num-1}'] = new_song
					search_music_json['music']['num'] += 1
					del new_song

				del tree

		except requests.exceptions.ConnectionError:
			search_music_json['connect'] = False

		return search_music_json

	def search_music(text, page):
		clear_ram()
		try:
			search_music_json = {"music": {"num": 0}, "music_albums": {"num": 0}, "pages": []}
				
			headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
			api = requests.get(f'https://zaycev.net/search.html?page={page}&query_search={text}', headers=headers)

			tree = lxml.html.document_fromstring(api.text)

			try:
				for num in range(1, 41):
					try:
						new_song = {
							"name": tree.xpath(f'//*[@id="search-results"]/div/div[3]/div/div[1]/div[1]/div[2]/div[{num}]/div[1]/div[2]/div[3]/a/text()')[0],
							"author": tree.xpath(f'//*[@id="search-results"]/div/div[3]/div/div[1]/div[1]/div[2]/div[{num}]/div[1]/div[2]/div[1]/a/text()')[0],
							"url": tree.xpath(f'//*[@id="search-results"]/div/div[3]/div/div[1]/div[1]/div[2]/div[{num}]/@data-url')[0],
							"song_time": tree.xpath(f'//*[@id="search-results"]/div/div[3]/div/div[1]/div[1]/div[2]/div[{num}]/div[2]/text()')[0],
							"song_id": tree.xpath(f'//*[@id="search-results"]/div/div[3]/div/div[1]/div[1]/div[2]/div[{num}]/@data-id')[0]
						}
						search_music_json['music'][f'song{num-1}'] = new_song
						search_music_json['music']['num'] += 1
						del new_song
					except:
						break

				try:
					search_music_json['pages'].append(tree.xpath('//*[@id="search-page"]/div/div/div[3]/div/span/span/text()')[0])

					for num in range((2 if int(page) > 1 else 1), 6):
						try:
							search_music_json['pages'].append(tree.xpath(f'//*[@id="search-page"]/div/div/div[3]/div/a[{num}]/span/text()')[0])
						except:
							pass

					if search_music_json['pages'][-1] == 'Следующая':
						(search_music_json['pages']).pop()

					search_music_json['pages'] = sorted(search_music_json['pages'])
				except:
					pass

				del tree

			except:
				return {"music": {"num": 0}, "music_albums": {"num": 0}, "pages": []}

		except requests.exceptions.ConnectionError:
			pass

		return search_music_json

	def read_music(db_name):
		error_correction()

		conn = sqlite3.connect(f'Databases\\{db_name}')
		cursor = conn.cursor()

		json_text = {"music": {"num": 0}, "music_albums": {"num": 0}}

		music_list = []
		for i in cursor.execute('SELECT * FROM user_music ORDER BY song_time'):
			music_list.append(i[4])
		music_list = sorted(music_list)

		for num in range(0, cursor.execute('SELECT count(*) FROM user_music ORDER BY song_time').fetchone()[0]):
			song_data = cursor.execute('SELECT * FROM user_music WHERE num=?', (music_list[-num-1],)).fetchone()
			song_data = {'name': decode_text(song_data[0]), 'author': decode_text(song_data[1]), 'url': decode_text(song_data[2]), 'song_time': decode_text(song_data[3]), 'song_id': decode_text(song_data[5])}
			json_text['music'][f'song{num}'] = song_data
			json_text['music']['num'] += 1

		conn.close()

		return json_text

	def check_song(db_name, song_id):
		error_correction()

		conn = sqlite3.connect(f'Databases\\{db_name}')
		cursor = conn.cursor()
		answ = 0 if (cursor.execute('SELECT * FROM user_music WHERE song_id=?', (encode_text(song_id),))).fetchone() == None else 1

		conn.close()
		return answ

	def add_song(db_name, song_data):
		error_correction()

		conn = sqlite3.connect(f'Databases\\{db_name}')
		cursor = conn.cursor()

		try:
			song_num = cursor.execute('SELECT * FROM user_music ORDER BY num DESC LIMIT 1').fetchone()[4]+1
		except:
			song_num = cursor.execute('SELECT count(*) FROM user_music ORDER BY song_id').fetchone()[0]

		cursor.execute('INSERT INTO user_music VALUES (?,?,?,?,?,?)', (encode_text(song_data[0]), encode_text(song_data[1]), encode_text(song_data[2]), encode_text(song_data[3]), song_num, encode_text(song_data[4])))

		conn.commit()
		conn.close()

		clear_ram()

	def delete_song(db_name, song_id):
		error_correction()

		conn = sqlite3.connect(f'Databases\\{db_name}')
		cursor = conn.cursor()

		cursor.execute('DELETE FROM user_music WHERE song_id=?', (encode_text(song_id),))

		conn.commit()
		conn.close()

		clear_ram()


class Albums:
	def check_album(self, db_name, album_data):
		for num in range(data['music_albums']['num']):
			if data['music_albums'][f'album{num+1}']['name'] == self.name and data['music_albums'][f'album{num+1}']['author'] == self.author:
				return '1'
		return '0'

	def add_album(self, db_name, album_data):
		error_correction()

		conn = sqlite3.connect(f'Databases\\{db_name}')
		cursor = conn.cursor()

		try:
			song_num = cursor.execute('SELECT * FROM user_albums ORDER BY num DESC LIMIT 1').fetchone()[4]+1
		except:
			song_num = cursor.execute('SELECT count(*) FROM user_albums ORDER BY song_time').fetchone()[0]
		cursor.execute('INSERT INTO user_albums VALUES (?,?,?,?,?)', (encode_text(song_data[0]), encode_text(song_data[1]), encode_text(song_data[2]), encode_text(song_data[3]), song_num))

		conn.commit()
		conn.close()

		clear_ram()

	def delete_album(self, db_name, data):
		error_correction()

		conn = sqlite3.connect(f'Databases\\{db_name}')
		cursor = conn.cursor()

		cursor.execute('DELETE FROM user_albums WHERE (name=?) AND (author=?)', (encode_text(song_data[0]), encode_text(song_data[1]), encode_text(song_data[2])))

		conn.commit()
		conn.close()

		clear_ram()
