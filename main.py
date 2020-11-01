# -*- coding: utf-8 -*-

"""
      : READ_ME :
     : BounceBit :     
: Open Source Project :

  ~ Language: Python ~
 ~ Interface: Tkinter ~
~ Media player: Pyglet ~

     - Author:  D0Nater -
- GitHub: github.com/D0Nater -
"""

""" For Graphical Interface """
from tkinter import *

""" For download and listen music """
from threading import Thread

""" For files """
from os import path as oc_pach

""" For clear RAM """
from gc import collect as clear_ram

""" For load music on screen """
import time
from time import sleep as time_sleep

""" Other Scripts """
from elements import *
from music import Music
from settings import Settings


class PageButton:
    """ Class for pages (search music) """
    def __init__(self, page_num, search_text):
        self.page_num = page_num
        self.search_text = search_text

    def drow_button(self, x, y, text, error):
        canvas.create_window(x, y, window=Button(text=self.page_num, \
            command=lambda: music_interface(f'{text} {self.page_num}', error, None, self.search_text), \
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
        command=lambda: music_interface('Рекомендации', 'connect_error', None)).place(x=363, y=53)

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

    globals()['image_genre1'] = del_picture_background("pictures/genre1.png", themes[settings.theme]['button_color'], themes[settings.theme]['button_background'])


class PlayMusic:
    def __init__(self):
        self.song_id_now = ''
        self.time_line_now = None

    def song_time_thread(self):
        global song_time_now, num_for_time_line_now

        song_id_now = song_play_now['song_id']

        min_song, sec_song = [int(i) for i in song_time_now.split(':')] # default 00:00
        song_time_official = [int(i) for i in song_play_now['time'].split(':')] # song time
        song_time_official_str = time.strftime("%M:%S", time.gmtime(60*song_time_official[0] + song_time_official[1]+1)) # int to string

        self.time_line_bbox = line_for_song.bbox(self.time_line)

        num_for_time_line = (60*song_time_official[0] + song_time_official[1]+1) / 160

        if song_time_now == '00:00':
            # if play new song #
            num_for_time_line_now = 0 # default time line

        while song_play_now['play']:
            song_time_now = time.strftime("%M:%S", time.gmtime(60*min_song + sec_song))
            sec_song += 1

            num_for_time_line_now += num_for_time_line

            if (song_time_official_str == song_time_now) and (song_id_now == song_play_now['song_id']):
                self.behind_after_music(1)
                return

            elif (song_time_official_str != song_time_now) and (song_id_now == song_play_now['song_id']):
                line_for_song.delete(self.time)
                line_for_song.delete(self.time_line_now)

                self.time = line_for_song.create_text(self.x_time, 37, text=song_time_now, fill='grey50', anchor=W, font="Verdana 10")
                self.time_line_now = line_for_song.create_line(line_for_song.bbox(self.time)[2]+8, line_for_song.bbox(self.time)[3]-7, self.time_line_bbox[0]+globals()['num_for_time_line_now']+8, line_for_song.bbox(self.time)[3]-7, width=4, fill='black')

            else:
                return

            time_sleep(1)

    def behind_after_music(self, event):
            # new song num #
            song_num = song_play_now['num'] + (event)

            if song_num is -1:
                # play last song #
                song_num = list_of_play['music']['num'] - 1
            elif song_num > list_of_play['music']['num'] - 1:
                # play first song #
                song_num = 0

            # new song info #
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

            # update new song #
            if past_song['past_lib'] == past_song['lib_now']:
                past_song['class'].drow_music(past_song['class'], past_song['lib_now'])

            # update song time #
            globals()['song_time_now'] = '00:00'

            # stop music #
            player.stop()

            # write new song #
            player.new_song(song_play_now['song_id'])

            # play new song #
            player.next_song()

            if song_play_now['play']:
                Thread(target=player.play, daemon=True).start() # play

            # update line #
            main_player.drow_music_line()
            update_buttons()

    def loading_song(self):
        line_for_song.create_text(30, 40, text=languages['Загрузка'][settings.language]+"...", fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 12")
        root.update()

    def drow_music_line(self, change_settings=False):
        def click_play(button):
            global song_play_now

            # update button #
            if song_play_now['play']:
                player.pause()
                song_play_now['play'] = 0
                button['image'] = image_play_line
            else:
                Thread(target=player.play, daemon=True).start() # play
                song_play_now['play'] = 1
                button['image'] = image_pause_line
                Thread(target=main_player.song_time_thread, daemon=True).start()

            # update past song #
            try:
                if past_song['past_lib'] == past_song['lib_now']:
                    past_song['class'].drow_music(past_song['class'], past_song['lib_now'])
            except Exception as error:
                print(f'click_play: {error}')

            update_buttons()

        clear_ram()
        line_for_song.delete("all")

        if song_play_now['song_id'] is not None:
            # update past song #
            try:
                if past_song['past_lib'] == past_song['lib_now']:
                    past_song['class'].drow_music(past_song['class'], past_song['lib_now'])
            except:
                pass

            # Song info #
            self.song_name = line_for_song.create_text(30, 32, text=song_play_now['name'], fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 12")
            self.song_author = line_for_song.create_text(30, 52, text=song_play_now['author'], fill='grey50', anchor=W, font="Verdana 12")

            # time now #
            self.x_time = line_for_song.bbox(self.song_name)[2]+23 if line_for_song.bbox(self.song_name)[2] > line_for_song.bbox(self.song_author)[2] else line_for_song.bbox(self.song_author)[2]+23
            self.time = line_for_song.create_text(self.x_time, 37, text=song_time_now, fill='grey50', anchor=W, font="Verdana 10")

            # time line #
            self.time_line = line_for_song.create_line(line_for_song.bbox(self.time)[2]+8, line_for_song.bbox(self.time)[3]-7, line_for_song.bbox(self.time)[2]+168, line_for_song.bbox(self.time)[3]-7, width=4, fill='grey11')
            
            try:
                self.time_line_now = line_for_song.create_line(line_for_song.bbox(self.time)[2]+8, line_for_song.bbox(self.time)[3]-7, self.time_line_bbox[0]+globals()['num_for_time_line_now']+8, line_for_song.bbox(self.time)[3]-7, width=4, fill='black')
            except:
                self.time_line_now = line_for_song.create_line(line_for_song.bbox(self.time_line)[2], line_for_song.bbox(self.time_line)[3]-7, 0, line_for_song.bbox(self.time_line)[3]-7, width=4, fill='black')

            if self.song_id_now != song_play_now['song_id']:
                line_for_song.delete(self.time_line_now)

            self.song_id_now = song_play_now['song_id']

            # song time #
            self.song_time = line_for_song.create_text(line_for_song.bbox(self.time_line)[2]+8, line_for_song.bbox(self.time_line)[1]+4, text=song_play_now['time'], fill='grey50', anchor=W, font="Verdana 10")

            # Button 'behind song' #
            behind_song_button = line_for_song.create_window(line_for_song.bbox(self.song_time)[2]+30, 37, window=Button(image=image_behind_song, command=lambda: self.behind_after_music(-1), width=17, height=19, bd=0, bg=themes[settings.theme]['second_color'], relief=RIDGE))

            # Button 'play/stop' #
            if song_play_now['play']:
                play_button = Button(image=image_pause_line, command=lambda: click_play(play_button), width=15, height=21, bd=0, bg=themes[settings.theme]['second_color'], relief=RIDGE)
            else:
                play_button = Button(image=image_play_line, command=lambda: click_play(play_button), width=15, height=21, bd=0, bg=themes[settings.theme]['second_color'], relief=RIDGE)
            play_button_drow = line_for_song.create_window(line_for_song.bbox(behind_song_button)[2]+20, 38, window=play_button)

            # Button 'after song' #
            after_song_button = line_for_song.create_window(line_for_song.bbox(play_button_drow)[2]+21, 37, window=Button(image=image_after_song, command=lambda: self.behind_after_music(1), width=17, height=19, bd=0, bg=themes[settings.theme]['second_color'], relief=RIDGE))

            line_for_song.create_window(settings.width/2, 11, window=Button(text="", width=int(settings.width/3), height=1, bd=0, bg=themes[settings.theme]['second_color'], relief=RIDGE, anchor=S))

            if song_play_now['play'] and not change_settings:
                Thread(target=main_player.song_time_thread, daemon=True).start()


def change_setting(setting, new_setting):
    # update settings #
    if setting == 'theme':
        # change theme #
        settings.theme = new_setting

        # update all #
        line_for_song['bg'] = themes[settings.theme]['second_color']
        main_menu['bg'] = themes[settings.theme]['second_color']
        canvas['bg'] = themes[settings.theme]['background']

        update_pictures()
        update_buttons()
        # main_player.drow_music_line(change_settings=True)

    elif setting == 'lang':
        # change language #
        settings.language = new_setting
        update_buttons()

    settings_interface()


def settings_interface():
    clear_ram()
    canvas.delete("all")

    # delete logo #
    try: del globals()['image_logo']
    except: pass

    # Settings #
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

    # News #
    canvas.create_text(135, 240, text=languages['Новости'][settings.language], fill=themes[settings.theme]['text_color'], font="Verdana 14")

    # Creat block news #
    text_news = Text(width=28, height=20, bg=themes[settings.theme]['background'], fg=themes[settings.theme]['text_color'], bd=1, font="Verdana 12")
    text_news.insert(END, read_news()[settings.language]) # write news in block
    text_news.config(state=DISABLED) # update config
    canvas.create_window(155, 445, window=text_news) # draw news block

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
        click_add = Music.check_song_in_db("database2.sqlite", self.song_data[4])
        click_save = Music.check_song_in_db("database3.sqlite", self.song_data[4])

        def button_click(event, button):
            global past_song
            nonlocal click_play, click_add, click_save

            if event == 'click_play':
                if click_play:
                    player.pause()
                    click_play = 0
                    button['image'] = image_play
                else:
                    if self.song_data[4] != song_play_now['song_id']:
                        if not path.exists(f"Databases/Download_Music/{self.song_data[4]}.mp3"):
                            main_player.loading_song()
                            download_song = ThreadWithReturnValue(target=Music.download_music, args=(self.song_data[4], self.song_data[2]))
                            download_song.start()
                            download_song.join()
                        player.stop()
                        globals()['song_time_now'] = '00:00'
                        player.new_song(self.song_data[4])
                        if song_play_now['song_id'] != None:
                            player.next_song()

                    Thread(target=player.play, daemon=True).start() # play

                    click_play = 1
                    button['image'] = image_pause
                    past_song['class'] = this_class
                    past_song['past_lib'] = lib

                    if list_of_play != list_of_music:
                        globals()['list_of_play'] = list_of_music.copy()

                globals()['song_play_now'] = {"play": click_play, "name": self.song_data[0], "author": self.song_data[1], "time": self.song_data[3], "url": self.song_data[2], "song_id": self.song_data[4], "num": self.num}
                main_player.drow_music_line()

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
                    Thread(target=Music.download_music, args=(self.song_data[4], self.song_data[2])).start()
                    Music.add_song("database3.sqlite", self.song_data)
                    button['image'] = image_save_click
                    click_save = 1
                else:
                    Music.delete_music(self.song_data[4])
                    Music.delete_song("database3.sqlite", self.song_data[4])
                    button['image'] = image_save
                    click_save = 0

        # button 'play' #
        if (past_song['past_lib'] == past_song['lib_now']) and song_play_now['play'] and song_play_now['song_id'] == self.song_data[4]:
            click_play = 1
            play_button = Button(image=image_pause, command=lambda: button_click('click_play', play_button), width=15, height=21, bd=0, bg=themes[settings.theme]['background'], relief=RIDGE)
        else:
            play_button = Button(image=image_play, command=lambda: button_click('click_play', play_button), width=15, height=21, bd=0, bg=themes[settings.theme]['background'], relief=RIDGE)
        play_button_drow = canvas.create_window(self.x, self.y, window=play_button) # draw button

        # button 'add' #
        if click_add:
            add_button = Button(image=image_add_click, command=lambda: button_click('click_add', add_button), width=15, height=20, bd=0, bg=themes[settings.theme]['background'], relief=RIDGE)
        else:
            add_button = Button(image=image_add, command=lambda: button_click('click_add', add_button), width=15, height=20, bd=0, bg=themes[settings.theme]['background'], relief=RIDGE)
        add_button_drow = canvas.create_window(canvas.bbox(play_button_drow)[2]+40, self.y, window=add_button) # draw button

        # button 'download' #
        if click_save:
            save_button = Button(image=image_save_click, command=lambda: button_click('click_save', save_button), width=18, height=21, bd=0, bg=themes[settings.theme]['background'], relief=RIDGE)
        else:
            save_button = Button(image=image_save, command=lambda: button_click('click_save', save_button), width=18, height=21, bd=0, bg=themes[settings.theme]['background'], relief=RIDGE)
        save_button_drow = canvas.create_window(canvas.bbox(add_button_drow)[2]+20, self.y, window=save_button) # draw button


def drow_data(all_data, lib, search_text, text_error):
    clear_list_of_songs()
    clear_ram()

    load_text = canvas.create_text(14, 15, text=languages['Загрузка'][settings.language]+"...", fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")
    root.update()
    time_sleep(0.1)

    if lib.split(' ')[0] == 'Рекомендации':
        search_music_tread = ThreadWithReturnValue(target=Music.top_music, daemon=True)
        search_music_tread.start()
        all_data = search_music_tread.join()

    elif lib.split(' ')[0] == 'Поиск':
        search_music_tread = ThreadWithReturnValue(target=Music.search_music, args=(search_text, lib.split(' ')[1]), daemon=True)
        search_music_tread.start()
        all_data = search_music_tread.join()

    elif lib.split(' ')[0] == 'Жанр':
        search_music_tread = ThreadWithReturnValue(target=Music.genres_music, args=(languages[lib.split(' ')[1]]['en'].lower(), lib.split(' ')[2]), daemon=True)
        search_music_tread.start()
        all_data = search_music_tread.join()

    globals()['list_of_music'] = all_data

    """ Drow data on page """
    y = 130 if lib.split(' ')[0] == 'Рекомендации' or lib.split(' ')[0] == 'Жанр' else 90

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

        if song_play_now['song_id'] == all_data['music'][f'song{song_now}']['song_id']:
            past_song['class'] = new_song

        y += 40

    canvas.delete(load_text)

    # lib name #
    if lib.split(' ')[0] == 'Жанр':
        lib_name_text = languages['Жанр'][settings.language]+'-'+languages[lib.split(' ')[1]][settings.language]+' - '+languages['Страница'][settings.language]+' '+lib.split(' ')[2]
    else:
        lib_name_text = languages[lib.split(' ')[0]][settings.language]+((' - '+languages['Страница'][settings.language]+' '+lib.split(' ')[1]) if len(lib.split(' ')) > 1 else '')
    lib_name = canvas.create_text(14, 15, text=lib_name_text, fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")

    if (lib.split(' ')[0] == 'Рекомендации' or lib.split(' ')[0] == 'Поиск') and not all_data['connect']:
        # Errors #
        canvas.create_text(14, 60, text=languages[text_error][settings.language], fill='grey50', anchor=W, font="Verdana 12")
    else:
        # Search #
        search_draw = canvas.create_text(canvas.bbox(lib_name)[0], canvas.bbox(lib_name)[3]+25, text=languages['Поиск'][settings.language], fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")

        # Search line #
        text_e = Text(width=18, height=1.4, bg=themes[settings.theme]['background'], fg=themes[settings.theme]['text_color'], selectbackground='red', insertbackground=themes[settings.theme]['text_color'], font="Verdana 11")
        text_e.insert(END, search_text)
        text_e_drow = canvas.create_window(canvas.bbox(search_draw)[2]+105, canvas.bbox(search_draw)[3]-9, window=text_e)

        # Button for search #
        search_button = Button(image=image_search, width=16, height=16, bd=0, bg=themes[settings.theme]['background'], relief=RIDGE, \
            command=lambda: music_interface('Поиск 1', 'none_error', None, text_e.get(1.0, END)))

        search_button_drow = canvas.create_window(canvas.bbox(text_e_drow)[2]+17, canvas.bbox(search_draw)[3]-9, window=search_button)

        # Genres #
        if lib.split(' ')[0] == 'Рекомендации' or lib.split(' ')[0] == 'Жанр':
            genres_text = canvas.create_text(canvas.bbox(lib_name)[0], canvas.bbox(lib_name)[3]+60, text=languages['Жанры'][settings.language], fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")
            
            genre_pop = canvas.create_window(canvas.bbox(genres_text)[2]+20, canvas.bbox(lib_name)[3]+61, anchor=W, window=Button(text=languages['Поп'][settings.language], bg=themes[settings.theme]['second_color'], fg=themes[settings.theme]['text_color'], bd=0, width=7, font="Verdana 10", \
                command=lambda: music_interface('Жанр Поп 1', 'connect_error', None)))

            genre_rock = canvas.create_window(canvas.bbox(genre_pop)[2]+7, canvas.bbox(lib_name)[3]+61, anchor=W, window=Button(text=languages['Рок'][settings.language], bg=themes[settings.theme]['second_color'], fg=themes[settings.theme]['text_color'], bd=0, width=7, font="Verdana 10", \
                command=lambda: music_interface('Жанр Рок 1', 'connect_error', None)))

            genre_rap = canvas.create_window(canvas.bbox(genre_rock)[2]+7, canvas.bbox(lib_name)[3]+61, anchor=W, window=Button(text=languages['Рэп'][settings.language], bg=themes[settings.theme]['second_color'], fg=themes[settings.theme]['text_color'], bd=0, width=7, font="Verdana 10", \
                command=lambda: music_interface('Жанр Рэп 1', 'connect_error', None)))

            genre_jazz = canvas.create_window(canvas.bbox(genre_rap)[2]+7, canvas.bbox(lib_name)[3]+61, anchor=W, window=Button(text=languages['Джаз'][settings.language], bg=themes[settings.theme]['second_color'], fg=themes[settings.theme]['text_color'], bd=0, width=7, font="Verdana 10", \
                command=lambda: music_interface('Жанр Джаз 1', 'connect_error', None)))

            genre_shanson = canvas.create_window(canvas.bbox(genre_jazz)[2]+7, canvas.bbox(lib_name)[3]+61, anchor=W, window=Button(text=languages['Шансон'][settings.language], bg=themes[settings.theme]['second_color'], fg=themes[settings.theme]['text_color'], bd=0, width=9, font="Verdana 10", \
                command=lambda: prmusic_interface('Жанр Шансон 1', 'connect_error', None)))

            genre_classical = canvas.create_window(canvas.bbox(genre_shanson)[2]+7, canvas.bbox(lib_name)[3]+61, anchor=W, window=Button(text=languages['Классика'][settings.language], bg=themes[settings.theme]['second_color'], fg=themes[settings.theme]['text_color'], bd=0, width=9, font="Verdana 10", \
                command=lambda: music_interface('Жанр Классика 1', 'connect_error', None)))

        # Pages #
        page_x = canvas.bbox(lib_name)[2]+35
        if lib.split(' ')[0] == 'Поиск':
            for page_num in all_data['pages']:
                PageButton(page_num, search_text).drow_button(page_x, canvas.bbox(lib_name)[3]-9, 'Поиск', 'none_error')
                page_x += 29

        elif lib.split(' ')[0] == 'Жанр':
            for page_num in all_data['pages']:
                PageButton(page_num, '').drow_button(page_x, canvas.bbox(lib_name)[3]-9, 'Жанр '+lib.split(' ')[1], 'connect_error')
                page_x += 29

    line_for_song.create_window(settings.width/2, 11, window=Button(text="", width=int(settings.width/3), height=1, bd=0, bg=themes[settings.theme]['second_color'], relief=RIDGE, anchor=S))

    root.update()
    canvas.config(scrollregion=canvas.bbox('all'))

    update_buttons()


def music_interface(lib, text_error, all_data, search_text=''):
    clear_ram()

    global past_song

    past_song['lib_now'] = lib

    canvas.delete("all")

    # delete logo #
    try: del globals()['image_logo']
    except: pass

    if all_data is None:
        all_data = {"music": {"num": 0}, "music_albums": {"num": 0}, 'check_error': False}

    # drow data #
    if (all_data['music']['num'] is 0) and (all_data['music_albums']['num'] is 0) and all_data['check_error']:
        # write error or none #
        canvas.create_text(14, 15, text=languages[lib.split(' ')[0]][settings.language], fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")
        canvas.create_text(14, 60, text=languages[text_error][settings.language], fill='grey50', anchor=W, font="Verdana 12")
    else:
        # write data #
        drow_data(all_data, lib, search_text, text_error)


# Start Program #
root = Tk()
root.title("")

# Players #
player = MyPlayer() # player (pyglet)
main_player = PlayMusic() # line for songs

# Program Settings #
settings = Settings(root.winfo_screenwidth(), root.winfo_screenheight(), 'en', 'dark') # default settings
settings.update_settings() # read database
settings.create_readme(PROGRAM_NAME, VERSION, AUTHOR, GITHUB) # create readme.txt

# Window Settings #
root.iconbitmap(default="pictures/program_icon.ico")
root.geometry(f"{settings.width-50}x{settings.height-100}")
root.minsize(width=180, height=45)
root.state('zoomed')

# Parse News #
Thread(target=parse_new_news).start()

# Create scrollbar #
vscrollbar = Scrollbar(root, bg=themes[settings.theme]['background'])

# Menu #
main_menu = Canvas(root, width=settings.width, height=77, bg=themes[settings.theme]['second_color'], highlightthickness=0)
main_menu.create_text(10, 25, text=PROGRAM_NAME, fill="red", anchor=W, font="Aharoni 20") # name
main_menu.create_text(145, 27, text=f"v{VERSION}", anchor=W, fill="red") # version
main_menu.pack()

# Main canvas #
canvas = Canvas(root, width=settings.width, height=settings.height-220, yscrollcommand=vscrollbar.set, bg=themes[settings.theme]['background'], highlightthickness=0)
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
