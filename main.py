# -*- coding: utf-8 -*-

""" For errors """
import traceback
import requests

""" For Graphical Interface """
from tkinter import *

""" For play music """
import pyglet
from pyglet.media import *

""" For download and listen music """
from threading import Thread

""" For clear RAM """
from gc import collect as clear_ram

""" For load music on screen """
from time import sleep as time_sleep

""" Other Scripts """
from elements import *
from settings import Settings
from music import Music


class PageButton:
	def __init__(self, num, text):
		self.num = num
		self.text = text

	def drow_button(self, x, y):
		canvas.create_window(x, y, window=Button(text=self.num, \
			command=lambda: music_interface(f'Поиск {self.num}', 'none_error', {"music": {"num": 0}, "music_albums": {"num": 0}}, self.text), \
			width=2, height=1, bd=0, bg=themes[settings.theme]['second_color'], fg=themes[settings.theme]['text_color'], font="Verdana 12", relief=RIDGE))


def on_mousewheel(event):
	""" Scroll """
	if canvas.bbox('all')[3] > settings.height-200:
		canvas.yview_scroll(int(-1*(event.delta/120)), "units")


def update_buttons():
	globals()['download_music_button'] = Button(text=languages['Загруженное'][settings.language], bg=themes[settings.theme]['second_color'], fg=themes[settings.theme]['text_color'], bd=1, width=25, \
		command=lambda: music_interface('Загруженное', 'load_error', Music.read_music("database3.sqlite"))).place(x=-1, y=53)

	globals()['selected_music_button'] = Button(text=languages['Избранное'][settings.language], bg=themes[settings.theme]['second_color'], fg=themes[settings.theme]['text_color'], bd=1, width=25, \
		command=lambda: music_interface('Избранное', 'add_error', Music.read_music("database2.sqlite"))).place(x=181, y=53)

	globals()['recommended_music_button'] = Button(text=languages['Рекомендации'][settings.language], bg=themes[settings.theme]['second_color'], fg=themes[settings.theme]['text_color'], bd=1, width=25, \
		command=lambda: music_interface('Рекомендации', 'connect_error', {"music": {"num": 0}, "music_albums": {"num": 0}})).place(x=363, y=53)

	globals()['settings_button'] = Button(text=languages['Настройки'][settings.language], bg=themes[settings.theme]['second_color'], fg=themes[settings.theme]['text_color'], bd=1, width=25, \
		command=settings_interface).place(x=544, y=53)


def update_pictures():
	globals()['image_play'] = del_picture_background("pictures/play_button.png", themes[settings.theme]['button_color'], themes[settings.theme]['button_background'])
	globals()['image_pause'] = del_picture_background("pictures/pause_button.png", themes[settings.theme]['button_color'], themes[settings.theme]['button_background'])

	globals()['image_play_line'] = del_picture_background("pictures/play_button.png", themes[settings.theme]['button_color'], themes[settings.theme]['button_second_color'])
	globals()['image_pause_line'] = del_picture_background("pictures/pause_button.png", themes[settings.theme]['button_color'], themes[settings.theme]['button_second_color'])

	globals()['image_add'] = del_picture_background("pictures/add_button.png", themes[settings.theme]['button_color'], themes[settings.theme]['button_background'])
	globals()['image_save'] = del_picture_background("pictures/save_button.png", themes[settings.theme]['button_color'], themes[settings.theme]['button_background'])

	globals()['image_add_click'] = del_picture_background("pictures/add_button_click.png", themes[settings.theme]['button_color'], themes[settings.theme]['button_background'])
	globals()['image_save_click'] = del_picture_background("pictures/save_button_click.png", themes[settings.theme]['button_color'], themes[settings.theme]['button_background'])

	globals()['image_behind_song'] = del_picture_background("pictures/behind_song_button.png", themes[settings.theme]['button_color'], themes[settings.theme]['button_second_color'])
	globals()['image_after_song'] = del_picture_background("pictures/after_song_button.png", themes[settings.theme]['button_color'], themes[settings.theme]['button_second_color'])

	globals()['image_more'] = del_picture_background("pictures/more_button.png", themes[settings.theme]['button_color'], themes[settings.theme]['button_background'])
	globals()['image_search'] = del_picture_background("pictures/search_button.png", themes[settings.theme]['button_color'], themes[settings.theme]['button_background'])


def new_music_control(song_id):
	player.queue(pyglet.media.load(f'Databases/Download_Music/{song_id}.mp3'))
	player.play()

	if not player_bool:
		pyglet.app.run()
		globals()['player_bool'] = True


def play_music():
	clear_ram()
	line_for_song.delete("all")

	def song_time_thread():
		global song_time_now
		nonlocal time, time_line_now

		song_time_now_num = [int(i) for i in song_time_now.split(':')]
		song_time_official = [int(i) for i in song_play_now['time'].split(':')]

		time_line_bbox = line_for_song.bbox(time_line)

		num_for_time_line = ((song_time_official[0]*60) + song_time_official[1]) / 200
		num_for_time_line_now = (((song_time_official[0]*60) + song_time_official[1]) / 200) + num_for_time_line*2

		while song_play_now['play']:
			if (song_time_official[0] == song_time_now_num[0]) and (song_time_official[1] == song_time_now_num[1]):
				return
			else:
				if song_time_now_num[1] == 59:
					song_time_now_num[0] += 1
					song_time_now_num[1] = 0
					song_time_now = f'{song_time_now_num[0]}:00'
				else:
					song_time_now_num[1] += 1

				if len(str(song_time_now_num[1])) == 1:
					song_time_now = f'{song_time_now_num[0]}:0{song_time_now_num[1]}'
				else:
					song_time_now = f'{song_time_now_num[0]}:{song_time_now_num[1]}'


				num_for_time_line_now += num_for_time_line

				line_for_song.delete(time)
				line_for_song.delete(time_line_now)

				time = line_for_song.create_text(x_time, 30, text=song_time_now, fill='grey50', anchor=W, font="Verdana 10")
				time_line_now = line_for_song.create_line(time_line_bbox[0]+5, time_line_bbox[1]+5, float(time_line_bbox[0])+num_for_time_line_now+5.0, time_line_bbox[1]+5, width=4, fill='black')

				time_sleep(1)

	def click_play(button):
		global song_play_now

		if song_play_now['play'] == 1:
			# time_thread = Thread(target=song_time_thread, daemon=True)
			# time_thread.start()
			player.pause()
			song_play_now['play'] = 0
			button['image'] = image_play_line
		else:
			player.play()
			song_play_now['play'] = 1
			button['image'] = image_pause_line
		# update past song #
		try:
			if past_song['past_lib'] == past_song['lib_now']:
				past_song['class'].drow_music(past_song['class'], past_song['lib_now'])
		except:
			pass

		update_buttons()

	def behind_after_music(event):
		song_num = song_play_now['num'] + (event)
		if song_num is -1:
			song_num = list_of_play['music']['num'] - 1
		elif song_num > list_of_play['music']['num'] - 1:
			song_num = 0

		globals()['song_play_now'] = {
			"play": song_play_now['play'],
			"name": list_of_play['music'][f'song{song_num}']['name'],
			"author": list_of_play['music'][f'song{song_num}']['author'],
			"time": list_of_play['music'][f'song{song_num}']['song_time'],
			"url": list_of_play['music'][f'song{song_num}']['url'],
			"song_id": list_of_play['music'][f'song{song_num}']['song_id'],
			"num": song_num
		}
		# update past song #
		if past_song['past_lib'] == past_song['lib_now']:
			past_song['class'].drow_music(past_song['class'], past_song['lib_now'])

		globals()['past_song']['class'] = list_of_play['music'][f'song{song_num}']['class']

		if past_song['past_lib'] == past_song['lib_now']:
			past_song['class'].drow_music(past_song['class'], past_song['lib_now'])

		song_time_now = '0:00'

		play_music()

		update_buttons()


	if song_play_now['name'] is not "" and song_play_now['author'] is not "":
		# update past song #
		try:
			if past_song['past_lib'] == past_song['lib_now']:
				past_song['class'].drow_music(past_song['class'], past_song['lib_now'])
		except:
			pass

		# Song info #
		song_name = line_for_song.create_text(30, 19, text=song_play_now['name'], fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 12")
		song_author = line_for_song.create_text(30, 39, text=song_play_now['author'], fill='grey50', anchor=W, font="Verdana 12")

		# time now #
		x_time = line_for_song.bbox(song_name)[2]+23 if line_for_song.bbox(song_name)[2] > line_for_song.bbox(song_author)[2] else line_for_song.bbox(song_author)[2]+23
		time = line_for_song.create_text(x_time, 30, text=song_time_now, fill='grey50', anchor=W, font="Verdana 10")

		# time line #
		time_line = line_for_song.create_line(line_for_song.bbox(time)[2]+8, line_for_song.bbox(time)[3]-7, line_for_song.bbox(time)[2]+130, line_for_song.bbox(time)[3]-7, width=4, fill='grey11')
		time_line_now = line_for_song.create_line(line_for_song.bbox(time_line)[2], line_for_song.bbox(time_line)[3]-7, 0, line_for_song.bbox(time_line)[3]-7, width=4, fill='black')

		line_for_song.delete(time)
		line_for_song.delete(time_line_now)

		# song time #
		song_time = line_for_song.create_text(line_for_song.bbox(time_line)[2]+8, line_for_song.bbox(time_line)[1]+4, text=song_play_now['time'], fill='grey50', anchor=W, font="Verdana 10")

		# Button 'behind song' #
		behind_song_button = line_for_song.create_window(line_for_song.bbox(song_time)[2]+30, 30, window=Button(image=image_behind_song, command=lambda: behind_after_music(-1), width=17, height=19, bd=0, bg=themes[settings.theme]['second_color'], relief=RIDGE))

		# Button 'play/stop' #
		if song_play_now['play'] == 1:
			play_button = Button(image=image_pause_line, command=lambda: click_play(play_button), width=15, height=21, bd=0, bg=themes[settings.theme]['second_color'], relief=RIDGE)
		else:
			play_button = Button(image=image_play_line, command=lambda: click_play(play_button), width=15, height=21, bd=0, bg=themes[settings.theme]['second_color'], relief=RIDGE)
		play_button_drow = line_for_song.create_window(line_for_song.bbox(behind_song_button)[2]+20, 31, window=play_button)

		# Button 'after song' #
		after_song_button = line_for_song.create_window(line_for_song.bbox(play_button_drow)[2]+21, 30, window=Button(image=image_after_song, command=lambda: behind_after_music(1), width=17, height=19, bd=0, bg=themes[settings.theme]['second_color'], relief=RIDGE))

		if not time_song_thread:
			time_thread = Thread(target=song_time_thread, daemon=True)
			time_thread.start()
			globals()['time_song_thread'] = True


def change_setting(setting, new_setting):
	# update settings #
	if setting == 'theme':
		settings.theme = new_setting
		line_for_song['bg'] = themes[settings.theme]['second_color']
		main_menu['bg'] = themes[settings.theme]['second_color']
		canvas['bg'] = themes[settings.theme]['background']

		update_pictures()
		update_buttons()
		play_music()

	elif setting == 'lang':
		settings.language = new_setting
		update_buttons()

	settings_interface()


def settings_interface():
	clear_ram()
	canvas.delete("all")

	try:
		del globals()['image_logo']
	except:
		pass

	settings_text = canvas.create_text(15, 19, text=languages['Настройки'][settings.language], anchor=W, fill=themes[settings.theme]['text_color'], font="Verdana 13")

	# Save #
	canvas.create_window(canvas.bbox(settings_text)[2]+75, 20, window=Button(text=languages['Сохранить'][settings.language], command=settings.change_settings, bg=themes[settings.theme]['background'], fg=themes[settings.theme]['text_color'], bd=1, width=15))
	
	# Themes #
	theme_text = canvas.create_text(15, 87, text=languages['Тема'][settings.language], anchor=W, fill=themes[settings.theme]['text_color'], font="Verdana 13")
	d_theme = canvas.create_window(canvas.bbox(theme_text)[2]+70, 88, window=Button(text=languages['Темная'][settings.language], command=lambda: change_setting('theme', 'dark'), bg=themes[settings.theme]['background'], fg=themes[settings.theme]['text_color'], bd=1, width=15))
	l_theme = canvas.create_window(canvas.bbox(d_theme)[2]+55, 88, window=Button(text=languages['Светлая'][settings.language], command=lambda: change_setting('theme', 'light'), bg=themes[settings.theme]['background'], fg=themes[settings.theme]['text_color'], bd=1, width=15))
	canvas.create_window(canvas.bbox(l_theme)[2]+55, 88, window=Button(text=languages['Пурпурная'][settings.language], command=lambda: change_setting('theme', 'purple'), bg=themes[settings.theme]['background'], fg=themes[settings.theme]['text_color'], bd=1, width=15))

	# Languages #
	lang_text = canvas.create_text(15, 140, text=languages['Язык'][settings.language], anchor=W, fill=themes[settings.theme]['text_color'], font="Verdana 13")
	ru_lang = canvas.create_window(canvas.bbox(lang_text)[2]+70, 141, window=Button(text="Русский", command=lambda: change_setting('lang', 'ru'), bg=themes[settings.theme]['background'], fg=themes[settings.theme]['text_color'], bd=1, width=15))
	canvas.create_window(canvas.bbox(ru_lang)[2]+55, 141, window=Button(text="English", command=lambda: change_setting('lang', 'en'), bg=themes[settings.theme]['background'], fg=themes[settings.theme]['text_color'], bd=1, width=15))

	root.update()
	canvas.config(scrollregion=canvas.bbox('all'))

	update_buttons()


class Song:
	def __init__(self, x, y, num, info):
		self.x = x
		self.y = y
		self.num = num
		self.song_data = [info['name'], info['author'], info['url'], info['song_time'], info['song_id']]

	def drow_music(self, this_class, lib):
		# for buttons #
		click_play = 0
		click_add = Music.check_song("database2.sqlite", self.song_data[4])
		click_save = Music.check_song("database3.sqlite", self.song_data[4])

		def button_click(event, button):
			global past_song
			nonlocal click_play, click_add, click_save

			if event == 'click_play':
				if click_play == 0:
					if self.song_data[4] != globals()['song_play_now']['song_id']:
						# if globals()['player_thread'] != None:
						# 	globals()['player_thread'].exit()
						globals()['song_time_now'] = '0:00'
						globals()['player_thread']=Thread(target=new_music_control, args=(self.song_data[4],), daemon=True)
						globals()['player_thread'].start()
					player.play()
					click_play = 1
					button['image'] = image_pause
					if list_of_play != list_of_music:
						globals()['list_of_play'] = list_of_music.copy()
				else:
					player.pause()
					click_play = 0
					button['image'] = image_play

				globals()['song_play_now'] = {"play": click_play, "name": self.song_data[0], "author": self.song_data[1], "time": self.song_data[3], "url": self.song_data[2], "song_id": self.song_data[4], "num": self.num}
				play_music()
				past_song['class'] = this_class
				past_song['past_lib'] = lib

			elif event == 'click_add':
				if click_add == 0:
					Music.add_song("database2.sqlite", self.song_data)
					button['image'] = image_add_click
					click_add = 1
				else:
					Music.delete_song("database2.sqlite", self.song_data[4])
					button['image'] = image_add
					click_add = 0

			elif event == 'click_save':
				if click_save == 0:
					t = Thread(target=Music.download_music, args=(self.song_data[4], self.song_data[2]))
					t.start()
					Music.add_song("database3.sqlite", self.song_data)
					button['image'] = image_save_click
					click_save = 1
				else:
					Music.delete_music(self.song_data[4])
					Music.delete_song("database3.sqlite", self.song_data[4])
					button['image'] = image_save
					click_save = 0

		# button 'play' #
		if (past_song['past_lib'] == past_song['lib_now']) and song_play_now['play'] == 1 and song_play_now['song_id'] == self.song_data[4]:
			click_play = 1
			play_button = Button(image=image_pause, command=lambda: button_click('click_play', play_button), width=15, height=21, bd=0, bg=themes[settings.theme]['background'], relief=RIDGE)
		else:
			play_button = Button(image=image_play, command=lambda: button_click('click_play', play_button), width=15, height=21, bd=0, bg=themes[settings.theme]['background'], relief=RIDGE)
		play_button_drow = canvas.create_window(self.x, self.y, window=play_button)

		# button 'add' #
		if click_add == 0:
			add_button = Button(image=image_add, command=lambda: button_click('click_add', add_button), width=15, height=20, bd=0, bg=themes[settings.theme]['background'], relief=RIDGE)
		else:
			add_button = Button(image=image_add_click, command=lambda: button_click('click_add', add_button), width=15, height=20, bd=0, bg=themes[settings.theme]['background'], relief=RIDGE)
		add_button_drow = canvas.create_window(canvas.bbox(play_button_drow)[2]+40, self.y, window=add_button)

		# button 'download' #
		if click_save == 0:
			save_button = Button(image=image_save, command=lambda: button_click('click_save', save_button), width=18, height=21, bd=0, bg=themes[settings.theme]['background'], relief=RIDGE)
		else:
			save_button = Button(image=image_save_click, command=lambda: button_click('click_save', save_button), width=18, height=21, bd=0, bg=themes[settings.theme]['background'], relief=RIDGE)
		save_button_drow = canvas.create_window(canvas.bbox(add_button_drow)[2]+20, self.y, window=save_button)


def drow_data(all_data, lib, text, text_error):
	clear_list_of_songs()
	clear_ram()

	load_text = canvas.create_text(14, 15, text="Загрузка...", fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")
	root.update()
	time_sleep(0.1)

	if lib.split(' ')[0] == 'Рекомендации':
		search_music_tread = ThreadWithReturnValue(target=Music.top_music, daemon=True)
		search_music_tread.start()
		all_data = search_music_tread.join()

	elif lib.split(' ')[0] == 'Поиск':
		search_music_tread = ThreadWithReturnValue(target=Music.search_music, args=(text, lib.split(' ')[1]), daemon=True)
		search_music_tread.start()
		all_data = search_music_tread.join()

	globals()['list_of_music'] = all_data

	""" Drow data on page """
	y = 90

	# albums #
	# for num in range(all_data['music_albums']['num']):
	# 	new_album = Album(20, y, num+1, all_data['music_albums'][f'album{num+1}'])
	# 	new_album.drow_album(new_album, lib)
	# 	list_of_songs_class.append(new_album)
	# 	y += 40

	# y += (0 if all_data['music_albums']['num'] == 0 else 25)

	# music #
	for song_now in range(all_data['music']['num']):
		# Song info #
		song_name = all_data['music'][f'song{song_now}']['name']
		song_author = all_data['music'][f'song{song_now}']['author']

		text_song = canvas.create_text(20, y, text=f"{song_name}  -  ", fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 12")
		text_author = canvas.create_text(canvas.bbox(text_song)[2], y, text=song_author, fill='grey50', anchor=W, font="Verdana 12")

		del song_name, song_author
		new_song = Song(canvas.bbox(text_author)[2]+34, y, song_now, all_data['music'][f'song{song_now}'])
		new_song.drow_music(new_song, lib)
		list_of_songs_class.append(new_song)
		globals()['list_of_music']['music'][f'song{song_now}']['class'] = new_song
		y += 40

	canvas.delete(load_text)

	# lib name #
	lib_name_text = languages[lib.split(' ')[0]][settings.language]+((' - '+languages['page'][settings.language]+' '+lib.split(' ')[1]) if len(lib.split(' ')) > 1 else '')
	lib_name = canvas.create_text(14, 15, text=lib_name_text, fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")

	if (lib.split(' ')[0] == 'Рекомендации' or lib.split(' ')[0] == 'Поиск') and not all_data['connect']:
		# errors #
		canvas.create_text(14, 60, text=languages[text_error][settings.language], fill='grey50', anchor=W, font="Verdana 12")

	else:
		""" Search """
		search_text = canvas.create_text(canvas.bbox(lib_name)[0], canvas.bbox(lib_name)[3]+25, text=languages['Поиск'][settings.language], fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")
		text_e = Text(width=18, height=1.4, bg=themes[settings.theme]['background'], fg=themes[settings.theme]['text_color'], selectbackground='red', insertbackground=themes[settings.theme]['text_color'], font="Verdana 11")
		text_e.insert(END,text)
		text_e_drow = canvas.create_window(canvas.bbox(search_text)[2]+105, canvas.bbox(search_text)[3]-9, window=text_e)

		search_button = Button(image=image_search, \
			command=lambda: music_interface('Поиск 1', 'none_error', {"music": {"num": 0}, "music_albums": {"num": 0}}, text_e.get(1.0, END)), \
			width=16, height=16, bd=0, bg=themes[settings.theme]['background'], relief=RIDGE)

		search_button_drow = canvas.create_window(canvas.bbox(text_e_drow)[2]+17, canvas.bbox(search_text)[3]-9, window=search_button)

		""" Pages """
		x = canvas.bbox(lib_name)[2]+35
		if lib.split(' ')[0] == 'Поиск':
			for num in all_data['pages']:
				PageButton(num, text).drow_button(x, canvas.bbox(lib_name)[3]-9)
				x += 29

	root.update()
	canvas.config(scrollregion=canvas.bbox('all'))

	update_buttons()


def music_interface(lib, text_error, all_data, text=''):
	clear_ram()

	global past_song

	past_song['lib_now'] = lib

	canvas.delete("all")

	try:
		del globals()['image_logo']
	except:
		pass

	try:
		# drow data #
		if (all_data['music']['num'] is 0) and (all_data['music_albums']['num'] is 0) and lib.split(' ')[0] != 'Рекомендации' and lib.split(' ')[0] != 'Поиск':
			# write error or none #
			canvas.create_text(14, 15, text=languages[lib.split(' ')[0]][settings.language], fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")
			canvas.create_text(14, 60, text=languages[text_error][settings.language], fill='grey50', anchor=W, font="Verdana 12")
		else:
			# write data #
			drow_data(all_data, lib, text, text_error)
	except Exception as error:
		canvas.delete('all')

		text_lib = canvas.create_text(14, 15, text=languages[lib.split(' ')[0]][settings.language], fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")

		text_error = canvas.create_text(20, canvas.bbox(text_lib)[3]+25, text=f'Error:\n{traceback.format_exc()}', fill='red', anchor=NW, font="Verdana 15")
		text_error = canvas.create_text(20, canvas.bbox(text_error)[3]+25, text='Сообщить об ошибке', fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")

		add_button = Button(text="VK", bg=themes[settings.theme]['second_color'], fg=themes[settings.theme]['text_color'], bd=1, width=10, command=lambda: print(' - none :('))
		add_button_drow = canvas.create_window(canvas.bbox(text_error)[2]+50, canvas.bbox(text_error)[3]-11, window=add_button)


# Start Program #
root = Tk()
root.title("")

# Program Settings #
settings = Settings(root.winfo_screenwidth(), root.winfo_screenheight(), 'en', 'dark') # default settings
settings.update_settings() # read database
settings.create_readme(PROGRAM_NAME, VERSION, AUTHOR, GITHUB) # create readme.txt

# Window Settings #
root.iconbitmap(default="pictures/program_icon.ico")
root.geometry(f"{settings.width-50}x{settings.height-100}")
root.minsize(width=180, height=45)
root.maxsize(width=settings.width, height=settings.height)

# Create scrollbar #
vscrollbar = Scrollbar(root, bg=themes[settings.theme]['background'])

# Menu #
main_menu = Canvas(root, width=settings.width, height=77, bg=themes[settings.theme]['second_color'], highlightthickness=0)
main_menu.create_text(10, 25, text=PROGRAM_NAME, fill="red", anchor=W, font="Aharoni 20") # name
main_menu.create_text(145, 27, text=f"v{VERSION}", anchor=W, fill="red") # version
main_menu.pack()

# Main canvas #
canvas = Canvas(root, width=settings.width, height=settings.height-200, yscrollcommand=vscrollbar.set, bg=themes[settings.theme]['background'], highlightthickness=0)
canvas.configure(scrollregion=canvas.bbox("all"))
canvas.bind_all("<MouseWheel>", on_mousewheel)
vscrollbar.config(command=canvas.yview)
# vscrollbar.pack(side=LEFT, fill=Y) # draw scrollbar
canvas.pack()

# Line for songs #
line_for_song = Canvas(root, width=settings.width, height=200, bg=themes[settings.theme]['second_color'], bd=0, highlightthickness=0)
line_for_song.pack()

# Create and drow logo #
image_logo = ImageTk.PhotoImage(Image.open("pictures/main_logo1.jpg").resize((canvas.winfo_reqwidth(), canvas.winfo_reqheight()), Image.ANTIALIAS))
canvas.create_image(0, 0, image=image_logo, anchor=NW)

# Drow buttons for music #
update_pictures()

# Drow main buttons #
update_buttons()

# Start window #
root.mainloop()
