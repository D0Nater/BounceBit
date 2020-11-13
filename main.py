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
from os import path, remove

""" For clear RAM """
from gc import collect as clear_ram

""" For load music on screen """
import time
from time import sleep as time_sleep

""" For copy text """
from pyperclip import copy as copy_text

""" Other Scripts """
from elements import *
from music import Music
from music import Playlist
from settings import Settings


class SongLine:
    def __init__(self, root, update_buttons):
        self.root = root
        self.song_id_now = ''
        self.time_line_now = None
        self.update_buttons = update_buttons

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

            # after song #
            if (song_time_official_str == song_time_now) and (song_id_now == song_play_now['song_id']):
                self.behind_after_music(1)
                return

            elif (song_time_official_str != song_time_now) and (song_id_now == song_play_now['song_id']):
                line_for_song.delete(self.time)
                line_for_song.delete(self.time_line_now)

                self.time = line_for_song.create_text(self.x_time, 37, text=song_time_now, fill='grey50', anchor=W, font="Verdana 10")
                self.time_line_now = line_for_song.create_line(line_for_song.bbox(self.time)[2]+8, line_for_song.bbox(self.time)[3]-7, self.time_line_bbox[0]+num_for_time_line_now+8, line_for_song.bbox(self.time)[3]-7, width=4, fill='black')

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
            if past_song['song_id'] in list_of_ids:
                globals()['list_of_play']['classes'][list_of_ids.index(past_song['song_id'])].draw_music(past_song['class'], past_song['past_lib'])

            # update data #
            globals()['past_song']['class'] = globals()['list_of_play']['classes'][song_num] # list_of_play['music'][f'song{song_num}']['class']
            globals()['past_song']['song_id'] = song_play_now['song_id']

            # update new song #
            if past_song['song_id'] in list_of_ids:
                globals()['list_of_play']['classes'][list_of_ids.index(past_song['song_id'])].draw_music(past_song['class'], past_song['past_lib'])

            # update song time #
            globals()['song_time_now'] = '00:00'

            # stop music #
            player.stop()

            if not path.exists("Databases/Download_Music/%s.mp3" % song_play_now['song_id']):
                # download song #
                song_line.loading_song()
                download_song = ThreadWithReturnValue(target=Music.download_music, args=(song_play_now['song_id'], song_play_now['url']))
                download_song.start()
                download_song.join()

            # write new song #
            player.new_song(song_play_now['song_id'])

            # play new song #
            player.next_song()

            if song_play_now['play']:
                Thread(target=player.play, daemon=True).start() # play

            # update line #
            song_line.draw_music_line()
            self.update_buttons()

    def loading_song(self):
        line_for_song.delete('all')
        line_for_song.create_text(30, 40, text=languages['Загрузка'][settings.language]+"...", fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 12")
        line_for_song.create_window(settings.width/2, 11, window=Button(text="", width=int(settings.width/3), height=1, bd=0, bg=themes[settings.theme]['second_color'], activebackground=themes[settings.theme]['second_color'], relief=RIDGE, anchor=S))
        self.root.update()

    def draw_music_line(self, change_settings=False):
        def click_play(button):
            global song_play_now

            # update button #
            if song_play_now['play']:
                player.pause()
                song_play_now['play'] = 0
                button['image'] = image_play
            else:
                Thread(target=player.play, daemon=True).start() # play
                song_play_now['play'] = 1
                button['image'] = image_pause
                Thread(target=song_line.song_time_thread, daemon=True).start()

            # update past song #
            if past_song['song_id'] in list_of_ids:
                globals()['list_of_play']['classes'][list_of_ids.index(past_song['song_id'])].draw_music(past_song['class'], past_song['past_lib'])

            self.update_buttons()

        clear_ram()
        line_for_song.delete("all")

        if song_play_now['song_id'] is not None:
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
            behind_song_button = line_for_song.create_window(line_for_song.bbox(self.song_time)[2]+30, 37, window=Button(image=image_behind_song, command=lambda: self.behind_after_music(-1), width=17, height=19, bd=0, bg=themes[settings.theme]['second_color'], activebackground=themes[settings.theme]['second_color'], relief=RIDGE))

            # Button 'play/stop' #
            if song_play_now['play']:
                play_button = Button(image=image_pause, command=lambda: click_play(play_button), width=14, height=23, bd=0, bg=themes[settings.theme]['second_color'], activebackground=themes[settings.theme]['second_color'], relief=RIDGE)
            else:
                play_button = Button(image=image_play, command=lambda: click_play(play_button), width=14, height=23, bd=0, bg=themes[settings.theme]['second_color'], activebackground=themes[settings.theme]['second_color'], relief=RIDGE)
            play_button_draw = line_for_song.create_window(line_for_song.bbox(behind_song_button)[2]+20, 38, window=play_button)

            # Button 'after song' #
            after_song_button = line_for_song.create_window(line_for_song.bbox(play_button_draw)[2]+21, 37, window=Button(image=image_after_song, command=lambda: self.behind_after_music(1), width=17, height=19, bd=0, bg=themes[settings.theme]['second_color'], activebackground=themes[settings.theme]['second_color'], relief=RIDGE))

            line_for_song.create_window(settings.width/2, 11, window=Button(text="", width=int(settings.width/3), height=1, bd=0, bg=themes[settings.theme]['second_color'], activebackground=themes[settings.theme]['second_color'], relief=RIDGE, anchor=S))

            if song_play_now['play'] and not change_settings:
                Thread(target=song_line.song_time_thread, daemon=True).start()


class Song:
    def __init__(self, x, y, num, info):
        self.x = x
        self.y = y
        self.num = num
        self.song_data = [info['name'], info['author'], info['url'], info['song_time'], info['song_id'], info['data_key']]

    # def __del__(self):
    #     pass

    def del_class(self):
        if self.this_class not in globals()['list_of_play']['classes']:
            del self.x
            del self.y
            del self.num
            del self.song_data

    def draw_music(self, this_class, lib):
        self.this_class = this_class

        # for buttons #
        click_play = 0
        click_add = Music.check_song_in_db("database2.sqlite", self.song_data[4])
        click_save = Music.check_song_in_db("database3.sqlite", self.song_data[4])

        def play_click(button):
            global past_song
            nonlocal click_play

            if click_play:
                player.pause()
                click_play = 0
                button['image'] = image_play
            else:
                if self.song_data[4] != song_play_now['song_id']:
                    if not path.exists(f"Databases/Download_Music/{self.song_data[4]}.mp3"):
                        # download song #
                        song_line.loading_song()
                        download_song = ThreadWithReturnValue(target=Music.download_music, args=(self.song_data[4], self.song_data[2]))
                        download_song.start()
                        download_song.join()

                    player.stop()
                    globals()['song_time_now'] = '00:00'
                    player.new_song(self.song_data[4])

                    if song_play_now['song_id'] is not None:
                        player.next_song()

                    # update past song #
                    if past_song['class'] is not None:
                        globals()['song_play_now']['play'] = 0
                        past_song['class'].draw_music(past_song['class'], past_song['lib_now'])

                    if list_of_play != list_of_music:
                        globals()['list_of_play'] = list_of_music.copy()
                        globals()['list_of_play']['classes'] = list_of_songs_class

                    past_song['song_id'] = self.song_data[4]
                    past_song['class'] = this_class
                    past_song['past_lib'] = lib

                Thread(target=player.play, daemon=True).start() # play

                click_play = 1
                button['image'] = image_pause

            globals()['song_play_now'] = {"play": click_play, "name": self.song_data[0], "author": self.song_data[1], "time": self.song_data[3], "url": self.song_data[2], "song_id": self.song_data[4], "num": self.num}
            song_line.draw_music_line()

        def add_click(button):
            nonlocal click_add

            if click_add:
                # Del song #
                Music.delete_song("database2.sqlite", self.song_data[4])
                button['image'] = image_add
                click_add = 0
            else:
                # Add song #
                Music.add_song("database2.sqlite", self.song_data)
                button['image'] = image_add_click
                click_add = 1

        def save_click(button):
            nonlocal click_save

            if click_save:
                # Del song #
                Music.delete_music(self.song_data[4])
                Music.delete_song("database3.sqlite", self.song_data[4])
                button['image'] = image_save
                click_save = 0
            else:
                # Download song #
                Thread(target=Music.download_music, args=(self.song_data[4], self.song_data[2])).start()
                Music.add_song("database3.sqlite", self.song_data)
                button['image'] = image_save_click
                click_save = 1

        def more_click():
            more_info_interface.song_info_draw(self.song_data)

        # button 'play' #
        if song_play_now['play'] and song_play_now['song_id'] == self.song_data[4]:
            click_play = 1
            play_button = Button(image=image_pause, command=lambda: play_click(play_button), width=14, height=23, bd=0, bg=themes[settings.theme]['background'], activebackground=themes[settings.theme]['background'], relief=RIDGE)
        else:
            play_button = Button(image=image_play, command=lambda: play_click(play_button), width=14, height=23, bd=0, bg=themes[settings.theme]['background'], activebackground=themes[settings.theme]['background'], relief=RIDGE)
        play_button_draw = canvas.create_window(self.x, self.y, window=play_button) # draw button

        # button 'add' #
        if click_add:
            add_button = Button(image=image_add_click, command=lambda: add_click(add_button), width=18, height=17, bd=0, bg=themes[settings.theme]['background'], activebackground=themes[settings.theme]['background'], relief=RIDGE)
        else:
            add_button = Button(image=image_add, command=lambda: add_click(add_button), width=18, height=17, bd=0, bg=themes[settings.theme]['background'], activebackground=themes[settings.theme]['background'], relief=RIDGE)
        add_button_draw = canvas.create_window(canvas.bbox(play_button_draw)[2]+40, self.y, window=add_button) # draw button

        # button 'download' #
        if click_save:
            save_button = Button(image=image_save_click, command=lambda: save_click(save_button), width=18, height=24, bd=0, bg=themes[settings.theme]['background'], activebackground=themes[settings.theme]['background'], relief=RIDGE)
        else:
            save_button = Button(image=image_save, command=lambda: save_click(save_button), width=18, height=24, bd=0, bg=themes[settings.theme]['background'], activebackground=themes[settings.theme]['background'], relief=RIDGE)
        save_button_draw = canvas.create_window(canvas.bbox(add_button_draw)[2]+20, self.y, window=save_button) # draw button

        # button 'more' #
        more_button_draw = canvas.create_window(canvas.bbox(save_button_draw)[2]+17, self.y+1, window=Button(image=image_more_info, command=lambda: more_click(), width=12, height=16, bd=0, bg=themes[settings.theme]['background'], activebackground=themes[settings.theme]['background'], relief=RIDGE)) # draw button


class MoreInfoInterface:
    def __init__(self):
        self.num_of_wins = 0

    def close_song_info(self):
        if self.num_of_wins:
            try:
                globals()['scroll_win'] = True

                self.song_info_canvas.delete("all")
                self.song_info_canvas.destroy()

                del self.song_info_canvas

                self.num_of_wins -= 1
            except AttributeError:
                pass

    def song_info_draw(self, data):
        # Delete past window #
        self.close_song_info()
        playlist_interface.close_playlist()

        # Create new window #
        self.num_of_wins += 1

        # Draw window #
        self.song_info_canvas = Canvas(root, width=canvas.winfo_width()/2/2+50, height=canvas.winfo_height()-40, bg=themes[settings.theme]['second_color'], highlightthickness=0)
        self.song_info_canvas.place(x=settings.width/2-50, y=canvas.bbox("all")[1]+90, anchor=N)

        # button 'close' #
        self.song_info_canvas.create_window(canvas.winfo_width()/2/2+45, 6, window=Button(image=image_close, width=17, height=17, bd=0, bg=themes[settings.theme]['second_color'], activebackground=themes[settings.theme]['second_color'], command=lambda: self.close_song_info()), anchor=NE)

        # Song name #
        self.song_name_draw = self.song_info_canvas.create_text(40, 40, text=languages['Трек'][settings.language]+':', fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")
        self.song_name_draw = self.song_info_canvas.create_text(self.song_info_canvas.bbox(self.song_name_draw)[2]+15, 41, text=data[0], fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 12")

        # Artist #
        self.song_artist_draw = self.song_info_canvas.create_text(40, 80, text=languages['Артист'][settings.language]+':', fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")
        self.song_info_canvas.create_text(self.song_info_canvas.bbox(self.song_artist_draw)[2]+11, self.song_info_canvas.bbox(self.song_artist_draw)[1]+3, text=data[1], fill='cyan', anchor=NW, font="Verdana 12")

        # Song size #
        self.song_size_draw = self.song_info_canvas.create_text(40, 110, text=languages['Размер'][settings.language]+':', fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")

        # Song duration #
        self.song_duration_draw = self.song_info_canvas.create_text(40, 140, text=languages['Длительность'][settings.language]+':', fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")

        root.update()

        # Button for add to playlist #
        self.song_info_canvas.create_window(self.song_info_canvas.bbox(self.song_name_draw)[2]+15, 41, window=Button(image=image_new_playlist, width=28, height=28, bd=0, bg=themes[settings.theme]['second_color'], activebackground=themes[settings.theme]['second_color'], command=lambda: print('add song')), anchor=W)

        # Search data #
        self.song_data = Music.more_song_info(data[5])

        # Draw Song size #
        self.song_info_canvas.create_text(self.song_info_canvas.bbox(self.song_size_draw)[2]+11, self.song_info_canvas.bbox(self.song_size_draw)[1]+3, text=self.song_data['size']+' mb', fill=themes[settings.theme]['text_color'], anchor=NW, font="Verdana 12")

        # Draw Song duration #
        self.song_info_canvas.create_text(self.song_info_canvas.bbox(self.song_duration_draw)[2]+11, self.song_info_canvas.bbox(self.song_duration_draw)[1]+2, text=data[3], fill=themes[settings.theme]['text_color'], anchor=NW, font="Verdana 12")

        # Draw Song text #
        self.song_info_canvas.create_text(40, 180, text=languages['Текст'][settings.language]+':', fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")

        # Draw Block for text #
        self.song_text_draw = Text(width=37, height=22, bg=themes[settings.theme]['second_color'], fg=themes[settings.theme]['text_color'], bd=1, wrap=WORD, font="Verdana 12") # create text block
        self.song_text_draw.insert(END, self.song_data['text']) # write text in block
        self.song_text_draw.config(state=DISABLED) # update config
        self.song_info_canvas.create_window(40, 200, window=self.song_text_draw, anchor=NW) # draw text block

        globals()['scroll_win'] = False


class PlaylistInterface:
    def __init__(self):
        self.num_of_wins = 0

    def close_playlist(self):
        if self.num_of_wins:
            try:
                globals()['scroll_win'] = True

                self.playlist_canvas.delete("all")
                self.playlist_canvas.destroy()

                del self.playlist_canvas

                self.num_of_wins -= 1
            except AttributeError:
                pass

    def draw_music(self):
        if int(self.music_data['music_num']):
            for song in range(int(self.music_data['music_num'])):
                print(song)
        else:
            self.playlist_canvas.create_text(40, self.playlist_canvas.bbox(self.playlists_name_draw)[3]+20, text=languages['add_error'][settings.language], fill='grey50', anchor=NW, font="Verdana 13")

    def delete_playlist(self):
        self.playlist_class.delete_playlist(self.music_data)

        Playlist.delete_playlist("database2.sqlite", self.playlist_name)
        self.close_playlist()

        globals()['scroll_win'] = True

    def playlist_draw(self, playlist_class, playlist_name):
        self.playlist_name = playlist_name
        self.playlist_class = playlist_class
        self.music_data = Playlist.get_music("database2.sqlite", self.playlist_name)

        # Delete past window #
        self.close_playlist()
        more_info_interface.close_song_info()

        # Create new window #
        self.num_of_wins += 1

        # Draw window #
        self.playlist_canvas = Canvas(root, width=canvas.winfo_width()/1.5, height=canvas.winfo_height()-40, bg=themes[settings.theme]['second_color'], highlightthickness=0)
        self.playlist_canvas.place(x=settings.width/2, y=canvas.bbox("all")[1]+90, anchor=N)

        # Playlist name #
        self.playlists_name_draw = self.playlist_canvas.create_text(40, 34, text=languages['Плейлист'][settings.language]+' - ', fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")
        self.playlists_name_draw = self.playlist_canvas.create_text(self.playlist_canvas.bbox(self.playlists_name_draw)[2], 35, text=self.playlist_name, fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")

        # button 'delete' #
        self.playlists_delete_draw = self.playlist_canvas.create_window(self.playlist_canvas.bbox(self.playlists_name_draw)[2]+15, 36, window=Button(image=image_trashcan, width=18, height=18, bd=0, bg=themes[settings.theme]['second_color'], activebackground=themes[settings.theme]['second_color'], command=lambda: self.delete_playlist()), anchor=W)

        # button 'edit' #
        self.playlists_edit_draw = self.playlist_canvas.create_window(self.playlist_canvas.bbox(self.playlists_delete_draw)[2]+8, 36, window=Button(image=image_edit, width=18, height=18, bd=0, bg=themes[settings.theme]['second_color'], activebackground=themes[settings.theme]['second_color'], command=lambda: print('edit playlist')), anchor=W)

        # button 'close' #
        self.playlist_canvas.create_window(canvas.winfo_width()/1.5-4, 6, window=Button(image=image_close, width=17, height=17, bd=0, bg=themes[settings.theme]['second_color'], activebackground=themes[settings.theme]['second_color'], command=lambda: self.close_playlist()), anchor=NE)

        root.update()

        self.draw_music()

        globals()['scroll_win'] = False


class DrawPlaylist:
    def __init__(self, playlist_name, y):
        self.playlist_name = playlist_name
        self.y = y

        self.draw_playlist_name = canvas.create_text(20, self.y, text=self.playlist_name, fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")

        self.button_more = canvas.create_window(canvas.bbox(self.draw_playlist_name)[2]+13, canvas.bbox(self.draw_playlist_name)[3]+2, anchor=SW, window=Button(image=image_more, width=20, height=20, bd=0, bg=themes[settings.theme]['background'], activebackground=themes[settings.theme]['background'], relief=RIDGE, \
            command=lambda: playlist_interface.playlist_draw(self.playlist_class, self.playlist_name)))

    def set_class(self, playlist_class):
        self.playlist_class = playlist_class

    def recovery_playlist(self):
        # Clear #
        canvas.delete(self.draw_playlist_name)
        canvas.delete(self.button_recovery)

        Playlist.add_playlist("database2.sqlite", self.playlist_name, self.music_data)

        self.draw_playlist_name = canvas.create_text(20, self.y, text=self.playlist_name, fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")

        self.button_more = canvas.create_window(canvas.bbox(self.draw_playlist_name)[2]+13, canvas.bbox(self.draw_playlist_name)[3]+2, anchor=SW, window=Button(image=image_more, width=20, height=20, bd=0, bg=themes[settings.theme]['background'], activebackground=themes[settings.theme]['background'], relief=RIDGE, \
            command=lambda: playlist_interface.playlist_draw(self.playlist_class, self.playlist_name)))

    def delete_playlist(self, music_data):
        self.music_data = music_data

        # Clear #
        canvas.delete(self.draw_playlist_name)
        canvas.delete(self.button_more)

        # Draw crossed out name #
        self.draw_playlist_name = canvas.create_text(20, self.y, text='\u0336'.join(self.playlist_name)+'\u0336', fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")

        # button 'recovery' #
        self.button_recovery = canvas.create_window(canvas.bbox(self.draw_playlist_name)[2]+13, canvas.bbox(self.draw_playlist_name)[3]+2, anchor=SW, window=Button(image=image_update, width=20, height=20, bd=0, bg=themes[settings.theme]['background'], activebackground=themes[settings.theme]['background'], relief=RIDGE, \
            command=lambda: self.recovery_playlist()))


class DrawPlaylists:
    def __init__(self, lib_name):
        self.lib_name = lib_name

    def get_y_pos(self):
        return self.y

    def clear_all(self, draw=True):
        try:
            canvas.delete(self.playlist_text)

            canvas.delete(self.playlist_name_draw)
            canvas.delete(self.create_button)
            canvas.delete(self.cancel_button)

            if draw:
                self.draw_new_playlist()
        except AttributeError:
            pass

    def draw_new_playlist(self):
        # Create playlist text #
        self.playlist_text = canvas.create_text(canvas.bbox(self.lib_name)[0], canvas.bbox(self.lib_name)[3]+60, text=languages['create_pl'][settings.language], fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")
        self.playlist_button = canvas.create_window(canvas.bbox(self.playlist_text)[2]+30, canvas.bbox(self.lib_name)[3]+61, window=Button(image=image_new_playlist, width=28, height=28, bd=0, bg=themes[settings.theme]['background'], activebackground=themes[settings.theme]['background'], relief=RIDGE, \
            command=lambda: self.draw_create_playlist()))

        self.draw_playlists()

    def save_playlist(self):
        name = self.set_playlist_name.get(1.0, "end-1c").replace("\n", "-")
        # Write new playlist in db #
        if not Playlist.check_playlist_in_db("database2.sqlite", name) and name is not "":
            Playlist.add_playlist("database2.sqlite", name)

            self.clear_all(draw=False)

            new_playlist = DrawPlaylist(name, canvas.bbox(self.lib_name)[3]+60)
            new_playlist.set_class(new_playlist)
        else:
            pass

    def draw_playlists(self):
        # Draw all created playlists #
        playlists = Playlist.get_playlists("database2.sqlite")[::-1]

        self.y = canvas.bbox(self.playlist_text)[3]+34

        # Draw playlists #
        for playlist_name in playlists:
            new_playlist = DrawPlaylist(playlist_name, self.y)
            new_playlist.set_class(new_playlist)

            self.y += 40

    def draw_create_playlist(self):
        # Clear #
        playlist_interface.close_playlist()
        canvas.delete(self.playlist_text)
        canvas.delete(self.playlist_button)

        self.playlist_text = canvas.create_text(canvas.bbox(self.lib_name)[0], canvas.bbox(self.lib_name)[3]+60, text=languages['pl_name'][settings.language], fill=themes[settings.theme]['text_color'], anchor=W, font="Verdana 13")

        # Draw block for set playlist name #
        self.set_playlist_name = Text(width=18, height=1.4, bg=themes[settings.theme]['background'], fg=themes[settings.theme]['text_color'], selectbackground='red', insertbackground=themes[settings.theme]['text_color'], wrap=NONE, font="Verdana 11")
        self.playlist_name_draw = canvas.create_window(canvas.bbox(self.playlist_text)[2]+15, canvas.bbox(self.playlist_text)[3]-9, window=self.set_playlist_name, anchor=W)

        # Draw button for create playlist #
        self.create_button = canvas.create_window(canvas.bbox(self.playlist_name_draw)[2]+12, canvas.bbox(self.playlist_name_draw)[3]-3, anchor=SW, window=Button(image=image_ok, width=18, height=16, bd=0, bg=themes[settings.theme]['background'], activebackground=themes[settings.theme]['background'], relief=RIDGE, \
            command=lambda: self.save_playlist()))

        # Draw button for cancel #
        self.cancel_button = canvas.create_window(canvas.bbox(self.create_button)[2]+12, canvas.bbox(self.playlist_name_draw)[3]-1, anchor=SW, window=Button(image=image_close, width=18, height=16, bd=0, bg=themes[settings.theme]['background'], activebackground=themes[settings.theme]['background'], relief=RIDGE, \
            command=lambda: self.clear_all()))


class SettingsInterface:
    def change_settings(self, setting, new_setting):
        # update settings #
        if setting == 'theme':
            # change theme #
            self.settings.theme = new_setting

            # update all #
            line_for_song['bg'] = themes[self.settings.theme]['second_color']
            self.main_menu['bg'] = themes[self.settings.theme]['second_color']
            self.canvas['bg'] = themes[self.settings.theme]['background']

            self.update_pictures()
            self.update_buttons()
            song_line.draw_music_line(change_settings=True)

        elif setting == 'lang':
            # change language #
            self.settings.language = new_setting
            self.update_buttons()

        self.settings_interface()

    def settings_interface(self):
        clear_ram()
        self.canvas.delete("all")
        more_info_interface.close_song_info()
        playlist_interface.close_playlist()

        # delete logo #
        try: del self.image_logo
        except: pass

        # Settings #
        self.settings_text = self.canvas.create_text(15, 19, text=languages['Настройки'][self.settings.language], anchor=W, fill=themes[self.settings.theme]['text_color'], font="Verdana 13")

        # Save #
        self.canvas.create_window(self.canvas.bbox(self.settings_text)[2]+75, 20, window=Button(text=languages['Сохранить'][self.settings.language], command=self.settings.change_settings, bg=themes[self.settings.theme]['background'], fg=themes[self.settings.theme]['text_color'], bd=1, width=15))
        
        # Themes #
        self.theme_text = self.canvas.create_text(15, 87, text=languages['Тема'][self.settings.language], anchor=W, fill=themes[self.settings.theme]['text_color'], font="Verdana 13")
        self.d_theme = self.canvas.create_window(self.canvas.bbox(self.theme_text)[2]+70, 88, window=Button(text=languages['Темная'][self.settings.language], command=lambda: self.change_settings('theme', 'dark'), bg=themes[self.settings.theme]['background'], fg=themes[self.settings.theme]['text_color'], bd=1, width=15))
        self.l_theme = self.canvas.create_window(self.canvas.bbox(self.d_theme)[2]+55, 88, window=Button(text=languages['Светлая'][self.settings.language], command=lambda: self.change_settings('theme', 'light'), bg=themes[self.settings.theme]['background'], fg=themes[self.settings.theme]['text_color'], bd=1, width=15))
        self.canvas.create_window(self.canvas.bbox(self.l_theme)[2]+55, 88, window=Button(text=languages['Пурпурная'][self.settings.language], command=lambda: self.change_settings('theme', 'purple'), bg=themes[self.settings.theme]['background'], fg=themes[self.settings.theme]['text_color'], bd=1, width=15))

        # Languages #
        self.lang_text = self.canvas.create_text(15, 140, text=languages['Язык'][self.settings.language], anchor=W, fill=themes[self.settings.theme]['text_color'], font="Verdana 13")
        self.ru_lang = self.canvas.create_window(self.canvas.bbox(self.lang_text)[2]+70, 141, window=Button(text="Русский", command=lambda: self.change_settings('lang', 'ru'), bg=themes[self.settings.theme]['background'], fg=themes[self.settings.theme]['text_color'], bd=1, width=15))
        self.canvas.create_window(self.canvas.bbox(self.ru_lang)[2]+55, 141, window=Button(text="English", command=lambda: self.change_settings('lang', 'en'), bg=themes[self.settings.theme]['background'], fg=themes[self.settings.theme]['text_color'], bd=1, width=15))

        # News #
        self.news_text = self.canvas.create_text(135, 240, text=languages['Новости'][self.settings.language], fill=themes[self.settings.theme]['text_color'], font="Verdana 14")

        # Creat block news #
        self.text_news = Text(width=28, height=20, bg=themes[self.settings.theme]['background'], fg=themes[self.settings.theme]['text_color'], bd=1, wrap=WORD, font="Verdana 12")
        self.text_news.insert(END, read_news()[0]+'\n\n') # write date
        self.text_news.insert(END, read_news()[1][self.settings.language]) # write news in block
        self.text_news.config(state=DISABLED) # update config
        self.canvas.create_window(155, 445, window=self.text_news) # draw news block

        # Copy Button #
        self.canvas.create_window(self.canvas.bbox(self.news_text)[2]+10, 240, window=Button(image=image_copy, width=19, height=19, bd=0, bg=themes[settings.theme]['background'], activebackground=themes[settings.theme]['background'], command=lambda: copy_text(self.text_news.get(1.0, 'end-1c'))), anchor=W)

        # Update window #
        self.root.update()
        self.canvas.config(scrollregion=self.canvas.bbox('all'))

        self.update_buttons()


class MusicInterface:
    def search_data(self):
        if self.lib.split(' ')[0] == 'Рекомендации':
            search_music_tread = ThreadWithReturnValue(target=Music.top_music, daemon=True)
            search_music_tread.start()
            return search_music_tread.join()

        elif self.lib.split(' ')[0] == 'Поиск':
            search_music_tread = ThreadWithReturnValue(target=Music.search_music, args=(self.search_text, self.lib.split(' ')[1]), daemon=True)
            search_music_tread.start()
            return search_music_tread.join()

        elif self.lib.split(' ')[0] == 'Жанр':
            search_music_tread = ThreadWithReturnValue(target=Music.genres_music, args=(languages[self.lib.split(' ')[1]]['en'].lower(), self.lib.split(' ')[2]), daemon=True)
            search_music_tread.start()
            return search_music_tread.join()

    def draw_music(self):
        globals()['list_of_music'] = self.all_data

        globals()['list_of_ids'] = [self.all_data['music'][f'song{i}']['song_id'] for i in range(self.all_data['music']['num'])]

        """ Draw data on page """
        # music #
        for song_num in range(self.all_data['music']['num']):
            # Song info #
            song_name = self.all_data['music'][f'song{song_num}']['name']
            song_author = self.all_data['music'][f'song{song_num}']['author']

            # Draw song name and author #
            name_draw = self.canvas.create_text(20, self.y, text=f"{song_name}  -  ", fill=themes[self.settings.theme]['text_color'], anchor=W, font="Verdana 12")
            author_draw = self.canvas.create_text(self.canvas.bbox(name_draw)[2], self.y, text=song_author, fill='grey50', anchor=W, font="Verdana 12")

            del song_name, song_author

            # Creat buttons for song #
            new_song = Song(self.canvas.bbox(author_draw)[2]+34, self.y, song_num, self.all_data['music'][f'song{song_num}'])
            new_song.draw_music(new_song, self.lib)

            list_of_songs_class.append(new_song)

            if song_play_now['song_id'] in list_of_ids:
                past_song['class'] = new_song

            self.y += 40

    def draw_search(self):
        # Search #
        search_draw = self.canvas.create_text(self.canvas.bbox(self.lib_name)[0], self.canvas.bbox(self.lib_name)[3]+25, text=languages['Поиск'][self.settings.language], fill=themes[self.settings.theme]['text_color'], anchor=W, font="Verdana 13")

        # Search line #
        text_e = Text(width=18, height=1.4, bg=themes[self.settings.theme]['background'], fg=themes[self.settings.theme]['text_color'], selectbackground='red', insertbackground=themes[self.settings.theme]['text_color'], font="Verdana 11")
        text_e.insert(END, self.search_text)
        text_e_draw = self.canvas.create_window(self.canvas.bbox(search_draw)[2]+105, self.canvas.bbox(search_draw)[3]-9, window=text_e)

        # Draw button for search #
        self.canvas.create_window(self.canvas.bbox(text_e_draw)[2]+17, self.canvas.bbox(search_draw)[3]-9, window=Button(image=image_search, width=16, height=16, bd=0, bg=themes[self.settings.theme]['background'], activebackground=themes[self.settings.theme]['background'], relief=RIDGE, \
            command=lambda: self.music_interface('Поиск 1', None, text_e.get(1.0, 'end-1c'))))

    def draw_genres(self):
        if self.lib.split(' ')[0] == 'Рекомендации' or self.lib.split(' ')[0] == 'Жанр' or self.lib.split(' ')[0] == 'Поиск':
            genres_text = self.canvas.create_text(self.canvas.bbox(self.lib_name)[0], self.canvas.bbox(self.lib_name)[3]+60, text=languages['Жанры'][self.settings.language], fill=themes[self.settings.theme]['text_color'], anchor=W, font="Verdana 13")

            genre_pop = self.canvas.create_window(self.canvas.bbox(genres_text)[2]+20, self.canvas.bbox(self.lib_name)[3]+61, anchor=W, window=Button(text=languages['Поп'][self.settings.language], bg=themes[self.settings.theme]['second_color'], fg=themes[self.settings.theme]['text_color'], bd=0, width=7, font="Verdana 10", \
                command=lambda: self.music_interface('Жанр Поп 1', None)))

            genre_rock = self.canvas.create_window(self.canvas.bbox(genre_pop)[2]+7, self.canvas.bbox(self.lib_name)[3]+61, anchor=W, window=Button(text=languages['Рок'][self.settings.language], bg=themes[self.settings.theme]['second_color'], fg=themes[self.settings.theme]['text_color'], bd=0, width=7, font="Verdana 10", \
                command=lambda: self.music_interface('Жанр Рок 1', None)))

            genre_rap = self.canvas.create_window(self.canvas.bbox(genre_rock)[2]+7, self.canvas.bbox(self.lib_name)[3]+61, anchor=W, window=Button(text=languages['Рэп'][self.settings.language], bg=themes[self.settings.theme]['second_color'], fg=themes[self.settings.theme]['text_color'], bd=0, width=7, font="Verdana 10", \
                command=lambda: self.music_interface('Жанр Рэп 1', None)))

            genre_jazz = self.canvas.create_window(self.canvas.bbox(genre_rap)[2]+7, self.canvas.bbox(self.lib_name)[3]+61, anchor=W, window=Button(text=languages['Джаз'][self.settings.language], bg=themes[self.settings.theme]['second_color'], fg=themes[self.settings.theme]['text_color'], bd=0, width=7, font="Verdana 10", \
                command=lambda: self.music_interface('Жанр Джаз 1', None)))

            genre_shanson = self.canvas.create_window(self.canvas.bbox(genre_jazz)[2]+7, self.canvas.bbox(self.lib_name)[3]+61, anchor=W, window=Button(text=languages['Шансон'][self.settings.language], bg=themes[self.settings.theme]['second_color'], fg=themes[self.settings.theme]['text_color'], bd=0, width=9, font="Verdana 10", \
                command=lambda: self.music_interface('Жанр Шансон 1', None)))

            genre_classical = self.canvas.create_window(self.canvas.bbox(genre_shanson)[2]+7, self.canvas.bbox(self.lib_name)[3]+61, anchor=W, window=Button(text=languages['Классика'][self.settings.language], bg=themes[self.settings.theme]['second_color'], fg=themes[self.settings.theme]['text_color'], bd=0, width=9, font="Verdana 10", \
                command=lambda: self.music_interface('Жанр Классика 1', None)))

    def draw_playlists(self):
        if self.lib.split(' ')[0] == 'Избранное':
            playlists = DrawPlaylists(self.lib_name)
            playlists.draw_new_playlist()
            self.y = playlists.get_y_pos()

    def draw_pages(self):
        class PageButton:
            """ Class for pages (search music / genres) """
            def __init__(self, page_num, func, args):
                self.page_num = page_num
                self.func = func
                self.args = args

            def draw_button(self, x, y):
                canvas.create_window(x, y, window=Button(text=self.page_num, width=2, height=1, bd=0, bg=themes[settings.theme]['second_color'], fg=themes[settings.theme]['text_color'], font="Verdana 12", relief=RIDGE, \
                    command=lambda: self.func(*self.args)))

        page_x = self.canvas.bbox(self.lib_name)[2]+35
        if self.lib.split(' ')[0] == 'Поиск':
            for page_num in self.all_data['pages']:
                PageButton(page_num, self.music_interface, (f'Поиск {page_num}', None, self.search_text)).draw_button(page_x, canvas.bbox(self.lib_name)[3]-9)
                page_x += 29

        elif self.lib.split(' ')[0] == 'Жанр':
            for page_num in self.all_data['pages']:
                PageButton(page_num, self.music_interface, ('Жанр %s %s'%(self.lib.split(' ')[1], page_num), None, '')).draw_button(page_x, canvas.bbox(self.lib_name)[3]-9)
                page_x += 29

    def music_interface(self, lib, all_data, search_text=''):
        clear_ram()
        self.canvas.delete("all")
        more_info_interface.close_song_info()
        playlist_interface.close_playlist()
        Thread(target=clear_list_of_songs).start() # delete past data

        self.lib = lib
        self.all_data = all_data
        self.search_text = search_text
        past_song['lib_now'] = self.lib
        self.y = 90 if self.lib.split(' ')[0] == 'Загруженное' else 130

        # lib name #
        if lib.split(' ')[0] == 'Жанр':
            lib_name_text = languages['Жанр'][self.settings.language]+'-'+languages[lib.split(' ')[1]][self.settings.language]+' - '+languages['Страница'][self.settings.language]+' '+lib.split(' ')[2]
        else:
            lib_name_text = languages[lib.split(' ')[0]][self.settings.language]+((' - '+languages['Страница'][self.settings.language]+' '+lib.split(' ')[1]) if len(lib.split(' ')) > 1 else '')

        # delete logo #
        try: del self.image_logo
        except: pass

        # loading #
        load_text = self.canvas.create_text(14, 15, text=languages['Загрузка'][self.settings.language]+"...", fill=themes[self.settings.theme]['text_color'], anchor=W, font="Verdana 13")
        self.root.update()
        # time_sleep(0.1)

        # Search data #
        if self.all_data is None:
            self.all_data = self.search_data()

        self.canvas.delete(load_text)

        # Lib name #
        self.lib_name = self.canvas.create_text(14, 15, text=lib_name_text, fill=themes[self.settings.theme]['text_color'], anchor=W, font="Verdana 13")

        # Search line #
        self.draw_search()

        # Genres #
        self.draw_genres()

        # Playlists #
        self.draw_playlists()

        if self.all_data['error'] is None:
            # Music #
            self.draw_music()

            # Pages #
            self.draw_pages()

            # Update window #
            self.root.update()
            self.canvas.config(scrollregion=self.canvas.bbox('all'))

            self.update_buttons()

            line_for_song.create_window(self.settings.width/2, 11, window=Button(text="", width=int(self.settings.width/3), height=1, bd=0, bg=themes[self.settings.theme]['second_color'], activebackground=themes[self.settings.theme]['second_color'], relief=RIDGE, anchor=S))
        else:
            # Write error #
            self.canvas.create_text(14, self.y, text=languages[self.all_data['error']][self.settings.language], fill='grey50', anchor=W, font="Verdana 12")


class BounceBit(SettingsInterface, MusicInterface, LoadPicture):
    def __init__(self):
        # Parse News #
        Thread(target=parse_new_news).start()

        # Start Program #
        self.root = Tk()
        self.root.title("")

        # Program Settings #
        self.settings = Settings('en', 'dark') # default settings
        self.settings.update_settings() # read database
        self.settings.create_readme(PROGRAM_NAME, VERSION, AUTHOR, GITHUB) # create readme.txt

        # Window Settings #
        self.root.iconbitmap(default=resource_path(path.join('pictures', "program_icon.ico")))
        self.root.geometry(f"{self.settings.width-50}x{self.settings.height-100}")
        self.root.minsize(width=180, height=45)
        self.root.state('zoomed')

        # Create scrollbar #
        self.vscrollbar = Scrollbar(self.root, bg=themes[self.settings.theme]['background'])

        # Menu #
        self.main_menu = Canvas(self.root, width=self.settings.width, height=77, bg=themes[self.settings.theme]['second_color'], highlightthickness=0)
        self.main_menu.create_text(10, 25, text=PROGRAM_NAME, fill="red", anchor=W, font="Aharoni 20") # program name
        self.main_menu.create_text(145, 27, text=f"v{VERSION}", anchor=W, fill="red") # version
        self.main_menu.pack()

        # Main canvas #
        self.canvas = Canvas(self.root, width=self.settings.width, height=self.settings.height-220, yscrollcommand=self.vscrollbar.set, bg=themes[self.settings.theme]['background'], highlightthickness=0)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        self.canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.vscrollbar.config(command=self.canvas.yview)
        # self.vscrollbar.pack(side=LEFT, fill=Y) # draw scrollbar
        self.canvas.pack()

        # Line for songs #
        globals()['line_for_song'] = Canvas(self.root, width=self.settings.width, height=200, bg=themes[self.settings.theme]['second_color'], bd=0, highlightthickness=0)
        line_for_song.pack()

        # Create and draw logo #
        self.image_logo = ImageTk.PhotoImage(Image.open(resource_path(path.join('pictures', "main_logo1.jpg"))).resize((self.settings.width, self.canvas.winfo_reqheight()), Image.ANTIALIAS))
        self.canvas.create_image(0, 0, image=self.image_logo, anchor=NW)

        # Loading Buttons #
        self.update_pictures()

        # Draw main buttons #
        self.update_buttons()

        # Globals #
        globals()['root'] = self.root
        globals()['canvas'] = self.canvas
        globals()['settings'] = self.settings

        # Players #
        globals()['player'] = MyPlayer() # player (pyglet)
        globals()['song_line'] = SongLine(self.root, self.update_buttons) # line for songs

        globals()['more_info_interface'] = MoreInfoInterface()
        globals()['playlist_interface'] = PlaylistInterface()

        # Start window #
        self.root.mainloop()

    def on_mousewheel(self, event):
        """ Scroll """
        if scroll_win and self.canvas.bbox('all')[3] > self.settings.height-210:
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def update_buttons(self):
        download_music_button = Button(text=languages['Загруженное'][self.settings.language], bg=themes[self.settings.theme]['second_color'], fg=themes[self.settings.theme]['text_color'], bd=1, width=25, \
            command=lambda: self.music_interface('Загруженное', Music.read_music("database3.sqlite", "load_error"))).place(x=-1, y=53)

        selected_music_button = Button(text=languages['Избранное'][self.settings.language], bg=themes[self.settings.theme]['second_color'], fg=themes[self.settings.theme]['text_color'], bd=1, width=25, \
            command=lambda: self.music_interface('Избранное', Music.read_music("database2.sqlite", "add_error"))).place(x=181, y=53)

        recommended_music_button = Button(text=languages['Рекомендации'][self.settings.language], bg=themes[self.settings.theme]['second_color'], fg=themes[self.settings.theme]['text_color'], bd=1, width=25, \
            command=lambda: self.music_interface('Рекомендации', None)).place(x=363, y=53)

        settings_button = Button(text=languages['Настройки'][self.settings.language], bg=themes[self.settings.theme]['second_color'], fg=themes[self.settings.theme]['text_color'], bd=1, width=25, \
            command=lambda: self.settings_interface()).place(x=544, y=53)

    def update_pictures(self):
        globals()['image_play'] = self.load_picture("play_button.png")
        globals()['image_pause'] = self.load_picture("pause_button.png")

        globals()['image_add'] = self.load_picture("add_button.png")
        globals()['image_add_click'] = self.load_picture("add_button_click.png")

        globals()['image_save'] = self.load_picture("save_button.png")
        globals()['image_save_click'] = self.load_picture("save_button_click.png")

        globals()['image_behind_song'] = self.load_picture("behind_song_button.png")
        globals()['image_after_song'] = self.load_picture("after_song_button.png")

        globals()['image_more'] = self.load_picture("more_button.png")
        globals()['image_more_info'] = self.load_picture("more_music_button.png")

        globals()['image_search'] = self.load_picture("search_button.png")
        globals()['image_new_playlist'] = self.load_picture("new_playlist_button.png")

        globals()['image_ok'] = self.load_picture("ok_button.png")
        globals()['image_close'] = self.load_picture("close_button.png")

        globals()['image_copy'] = self.load_picture("copy_button.png")
        globals()['image_trashcan'] = self.load_picture("trashcan_button.png")

        globals()['image_edit'] = self.load_picture("edit_button.png")
        globals()['image_update'] = self.load_picture("update_button.png")


if __name__ == '__main__':
    BounceBit()
