# -*- coding: utf-8 -*-

""" For copy text """
from pyperclip import copy as copy_text

from Scripts.elements import *
from Scripts.parse_music import ParseMusic
from Scripts.song_manage import SongManage
from Scripts.playlist_storage import PlaylistStorage


song_more_info = {
    "name": None,
    "author": None,
    "url": None,
    "song_time": None,
    "song_id": None
}


class AddToPlaylist:
    def close_window(self):
        if not self.playlist_win_num:
            return

        try:
            self.playlist_win_canvas.delete("all")
            self.playlist_win_canvas.destroy()

            del self.playlist_win_canvas

            self.playlist_win_num -= 1

            Main.DATA_CANVAS.bind_all("<MouseWheel>", Main.WINDOW_FOR_DATA.on_mousewheel)
        except:
            pass

    def draw_playlists(self):
        class DrawPlaylist:
            def __init__(self, main_canvas, name):
                self.main_canvas = main_canvas
                self.name = name

            def draw_playlist(self, y):
                click_add = PlaylistStorage.check_song_in_playlist("database2.sqlite", self.name, song_more_info["song_id"])

                def add_to_playlist(playlists_name):
                    nonlocal click_add

                    if click_add:
                        click_add = 0
                        self.add_button["image"] = MyImage.NEW_PLAYLIST
                        PlaylistStorage.del_song_out_playlist("database2.sqlite", playlists_name, song_more_info["song_id"])

                        Main.PLAYLIST_INTERFACE.song_num -= 1
                    else:
                        click_add = 1
                        self.add_button["image"] = MyImage.NEW_PLAYLIST_CLICK
                        PlaylistStorage.add_song_in_playlist("database2.sqlite", playlists_name, song_more_info)

                        Main.PLAYLIST_INTERFACE.song_num += 1

                    if Main.PLAYLIST_INTERFACE.num_of_wins:
                        Main.PLAYLIST_INTERFACE.update_song_num_draw()

                self.draw_name = self.main_canvas.create_text(40, y, text=self.name, fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

                if click_add:
                    self.add_button = Button(image=MyImage.NEW_PLAYLIST_CLICK, width=27, height=27, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: add_to_playlist(self.name))
                else:
                    self.add_button = Button(image=MyImage.NEW_PLAYLIST, width=27, height=27, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: add_to_playlist(self.name))

                self.add_to_playlist_button = self.main_canvas.create_window(self.main_canvas.bbox(self.draw_name)[2]+20, y, window=self.add_button, anchor=W)

        playlists = PlaylistStorage.get_playlists("database2.sqlite")[::-1]

        playlist_y = self.playlist_win_canvas.bbox(self.song_name_draw)[3]+30
        for playlist_now in playlists:
            new_playlist = DrawPlaylist(self.playlist_win_canvas, playlist_now)
            new_playlist.draw_playlist(playlist_y)

            playlist_y += 40

    def draw_window(self):
        def on_mousewheel(event):
            """ Scroll """
            if self.playlist_win_num and self.playlist_win_canvas.bbox("all")[3] > self.playlist_win_canvas.winfo_height():
                self.playlist_win_canvas.yview_scroll(int(-1*(event.delta/100)), "units")

        self.playlist_win_num += 1

        self.playlist_win_canvas = Canvas(Main.ROOT, width=Main.DATA_CANVAS.winfo_width()/2/2+50, height=Main.DATA_CANVAS.winfo_height()-40, bg=themes[Main.SETTINGS.theme]["second_color"], highlightthickness=1, highlightbackground="grey9")
        self.playlist_win_canvas.bind_all("<MouseWheel>", on_mousewheel)
        self.playlist_win_canvas.place(x=Main.SETTINGS.width/2-50, y=Main.DATA_CANVAS.bbox("all")[1]+90, anchor=N)

        # just pixel #
        just_px = self.playlist_win_canvas.create_text(0, 0, text=".", fill=themes[Main.SETTINGS.theme]["second_color"], anchor=W, font="Verdana 1")

        # button "close" #
        self.playlist_win_canvas.create_window(Main.DATA_CANVAS.winfo_width()/2/2+44, 5, window=Button(image=MyImage.CLOSE, width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: self.close_window()), anchor=NE)

        # Song name #
        self.song_name_draw = self.playlist_win_canvas.create_text(30, 30, text=languages["add_pl"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        self.draw_playlists()

        # Update window #
        self.playlist_win_canvas.config(scrollregion=self.playlist_win_canvas.bbox("all"))


class MoreInfoInterface(AddToPlaylist):
    """ Draw window with more song info """
    def __init__(self):
        self.num_of_wins = 0
        self.playlist_win_num = 0

    def close_song_info(self):
        global song_more_info

        if not self.num_of_wins:
            return
        try:
            if Main.PLAYLIST_INTERFACE.num_of_wins:
                Main.PLAYLIST_INTERFACE.scroll_playlist = True
                Main.PLAYLIST_INTERFACE.playlist_canvas.bind_all("<MouseWheel>", Main.PLAYLIST_INTERFACE.on_mousewheel)
            else:
                Main.SCROLL_WIN = True

            self.close_window()

            self.song_info_canvas.delete("all")
            self.song_info_canvas.destroy()

            del self.song_info_canvas

            song_more_info = {
                "name": None,
                "author": None,
                "url": None,
                "song_time": None,
                "song_id": None
            }

            self.num_of_wins -= 1
        except AttributeError:
            pass

    def song_info_draw(self, song_data, searched_data=None):
        global song_more_info

        # Delete past window #
        self.close_song_info()

        song_more_info = song_data
        Main.PLAYLIST_INTERFACE.scroll_playlist = False

        # Create new window #
        self.num_of_wins += 1

        # Draw window #
        self.song_info_canvas = Canvas(Main.ROOT, width=Main.DATA_CANVAS.winfo_width()/2/2+50, height=Main.DATA_CANVAS.winfo_height()-38, bg=themes[Main.SETTINGS.theme]["second_color"], highlightthickness=1, highlightbackground="grey9")
        self.song_info_canvas.place(x=Main.SETTINGS.width/2-50, y=Main.DATA_CANVAS.bbox("all")[1]+90, anchor=N)

        # button "close" #
        self.song_info_canvas.create_window(Main.DATA_CANVAS.winfo_width()/2/2+46, 7, window=Button(image=MyImage.CLOSE, width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: self.close_song_info()), anchor=NE)

        # Song name #
        self.song_name_draw = self.song_info_canvas.create_text(40, 40, text=languages["Трек"][Main.SETTINGS.language]+":", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        self.song_name_text = Text(bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], selectbackground="red", width=int(Main.SETTINGS.width / 55), height=1, bd=0, wrap=NONE, font="Verdana 12", cursor="arrow")
        self.song_name_text.insert(END, song_more_info["name"]) # write song name
        self.song_name_text.config(state=DISABLED) # update config
        self.song_name_text_draw = self.song_info_canvas.create_window(self.song_info_canvas.bbox(self.song_name_draw)[2]+15, self.song_info_canvas.bbox(self.song_name_draw)[1]+11, anchor=W, window=self.song_name_text)

        # Artist #
        self.song_artist_draw = self.song_info_canvas.create_text(40, 80, text=languages["Артист"][Main.SETTINGS.language]+":", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        self.song_author_text = Text(bg=themes[Main.SETTINGS.theme]["second_color"], fg="cyan", selectbackground="red", width=int(Main.SETTINGS.width / 61), height=1, bd=0, wrap=NONE, font="Verdana 12", cursor="arrow")
        self.song_author_text.insert(END, song_more_info["author"]) # write artist
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
        self.song_url_button = self.song_info_canvas.create_window(self.song_info_canvas.bbox(self.song_url_draw)[2]+15, self.song_info_canvas.bbox(self.song_url_draw)[1]+10, window=Button(image=MyImage.COPY, width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: copy_text(SongManage.song_url(song_data["song_id"]))), anchor=W)

        Main.ROOT.update()

        if not searched_data:
            # Search data #
            self.searched_data = ParseMusic.more_song_info(song_more_info["song_id"])

        # Draw Song size #
        self.song_info_canvas.create_text(self.song_info_canvas.bbox(self.song_size_draw)[2]+11, self.song_info_canvas.bbox(self.song_size_draw)[1]+3, text=self.searched_data["size"]+" mb", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=NW, font="Verdana 12")

        # Draw Song duration #
        self.song_info_canvas.create_text(self.song_info_canvas.bbox(self.song_duration_draw)[2]+11, self.song_info_canvas.bbox(self.song_duration_draw)[1]+2, text=song_more_info["song_time"], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=NW, font="Verdana 12")

        Main.SCROLL_WIN = False
