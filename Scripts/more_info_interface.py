# -*- coding: utf-8 -*-

""" For Graphical Interface """
from tkinter import *

""" For copy text """
from pyperclip import copy as copy_text

""" Other Scripts """
from Scripts.elements import *
from Scripts.parse_music import ParseMusic

""" For song manage """
from Scripts.song_manage import SongManage

""" Images """
from Scripts.images import MyImage

""" Main """
from Scripts.main import Main


class AddToPlaylist:
    def close_window(self):
        if not self.playlist_win_num:
            return

        try:
            self.playlist_win_canvas.delete("all")
            self.playlist_win_canvas.destroy()

            del self.playlist_win_canvas

            self.playlist_win_num -= 1
        except:
            pass

    def draw_playlists(self):
        pass

    def draw_window(self):
        self.playlist_win_num += 1

        self.playlist_win_canvas = Canvas(Main.ROOT, width=Main.DATA_CANVAS.winfo_width()/2/2+50, height=Main.DATA_CANVAS.winfo_height()-40, bg=themes[Main.SETTINGS.theme]["second_color"], highlightthickness=0)
        self.playlist_win_canvas.place(x=Main.SETTINGS.width/2-50, y=Main.DATA_CANVAS.bbox("all")[1]+90, anchor=N)

        # button 'close' #
        self.playlist_win_canvas.create_window(Main.DATA_CANVAS.winfo_width()/2/2+45, 6, window=Button(image=MyImage.CLOSE, width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: self.close_window()), anchor=NE)

        # Song name #
        self.song_name_draw = self.playlist_win_canvas.create_text(30, 30, text=languages["add_pl"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")


class MoreInfoInterface(AddToPlaylist):
    """ Draw window with more song info """
    def __init__(self):
        self.num_of_wins = 0
        self.playlist_win_num = 0

    def close_song_info(self):
        if not self.num_of_wins:
            return
        try:
            Main.SCROLL_WIN = True

            self.close_window()

            self.song_info_canvas.delete("all")
            self.song_info_canvas.destroy()

            del self.song_info_canvas

            self.num_of_wins -= 1
        except AttributeError:
            pass

    def song_info_draw(self, data, searched_data=None):
        # Delete past window #
        self.close_song_info()
        Main.PLAYLIST_INTERFACE.close_playlist()

        # Create new window #
        self.num_of_wins += 1

        # Draw window #
        self.song_info_canvas = Canvas(Main.ROOT, width=Main.DATA_CANVAS.winfo_width()/2/2+50, height=Main.DATA_CANVAS.winfo_height()-40, bg=themes[Main.SETTINGS.theme]["second_color"], highlightthickness=0)
        self.song_info_canvas.place(x=Main.SETTINGS.width/2-50, y=Main.DATA_CANVAS.bbox("all")[1]+90, anchor=N)

        # button 'close' #
        self.song_info_canvas.create_window(Main.DATA_CANVAS.winfo_width()/2/2+45, 6, window=Button(image=MyImage.CLOSE, width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: self.close_song_info()), anchor=NE)

        # Song name #
        self.song_name_draw = self.song_info_canvas.create_text(40, 40, text=languages["Трек"][Main.SETTINGS.language]+":", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        self.song_name_text = Text(bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], selectbackground="red", width=int(Main.SETTINGS.width / 55), height=1, bd=0, wrap=NONE, font="Verdana 12", cursor="arrow")
        self.song_name_text.insert(END, data[0]) # write song name
        self.song_name_text.config(state=DISABLED) # update config
        self.song_name_text_draw = self.song_info_canvas.create_window(self.song_info_canvas.bbox(self.song_name_draw)[2]+15, self.song_info_canvas.bbox(self.song_name_draw)[1]+11, anchor=W, window=self.song_name_text)

        # Artist #
        self.song_artist_draw = self.song_info_canvas.create_text(40, 80, text=languages["Артист"][Main.SETTINGS.language]+":", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        self.song_author_text = Text(bg=themes[Main.SETTINGS.theme]["second_color"], fg="cyan", selectbackground="red", width=int(Main.SETTINGS.width / 61), height=1, bd=0, wrap=NONE, font="Verdana 12", cursor="arrow")
        self.song_author_text.insert(END, data[1]) # write song name
        self.song_author_text.config(state=DISABLED) # update config
        self.song_name_text_draw = self.song_info_canvas.create_window(self.song_info_canvas.bbox(self.song_artist_draw)[2]+15, self.song_info_canvas.bbox(self.song_artist_draw)[1]+11, anchor=W, window=self.song_author_text)

        # Song size #
        self.song_size_draw = self.song_info_canvas.create_text(40, 110, text=languages["Размер"][Main.SETTINGS.language]+":", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        # Song duration #
        self.song_duration_draw = self.song_info_canvas.create_text(40, 140, text=languages["Длительность"][Main.SETTINGS.language]+":", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        # Button for add to playlist #
        self.add_to_pl_text = self.song_info_canvas.create_text(40, 175, text=languages["add_pl"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")
        self.add_to_pl_bttn = self.song_info_canvas.create_window(self.song_info_canvas.bbox(self.add_to_pl_text)[2]+15, self.song_info_canvas.bbox(self.add_to_pl_text)[1]+10, window=Button(image=MyImage.NEW_PLAYLIST, width=27, height=27, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: self.draw_window()), anchor=W)

        # Copy song url #
        self.song_url_draw = self.song_info_canvas.create_text(40, 210, text="URL", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")
        self.song_url_button = self.song_info_canvas.create_window(self.song_info_canvas.bbox(self.song_url_draw)[2]+15, self.song_info_canvas.bbox(self.song_url_draw)[1]+10, window=Button(image=MyImage.COPY, width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: copy_text(SongManage.song_url(data[4]))), anchor=W)

        Main.ROOT.update()

        if not searched_data:
            # Search data #
            self.searched_data = ParseMusic.more_song_info(data[4])

        # Draw Song size #
        self.song_info_canvas.create_text(self.song_info_canvas.bbox(self.song_size_draw)[2]+11, self.song_info_canvas.bbox(self.song_size_draw)[1]+3, text=self.searched_data["size"]+" mb", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=NW, font="Verdana 12")

        # Draw Song duration #
        self.song_info_canvas.create_text(self.song_info_canvas.bbox(self.song_duration_draw)[2]+11, self.song_info_canvas.bbox(self.song_duration_draw)[1]+2, text=data[3], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=NW, font="Verdana 12")

        Main.SCROLL_WIN = False
