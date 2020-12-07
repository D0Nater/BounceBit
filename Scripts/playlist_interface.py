# -*- coding: utf-8 -*-

from Scripts.elements import *
from Scripts.draw_song import DrawSong
from Scripts.playlist_storage import PlaylistStorage


class DrawPlaylist:
    def __init__(self, playlist_name, x, y, music_interface):
        self.playlist_name = playlist_name
        self.x = x
        self.y = y

        self.playlist_name_text = self.playlist_name[:40]+"..." if len(self.playlist_name) > 40 else self.playlist_name

        self.draw_playlist_name = Main.DATA_CANVAS.create_text(self.x, self.y, text=self.playlist_name_text, fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        self.button_more = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.draw_playlist_name)[2]+13, Main.DATA_CANVAS.bbox(self.draw_playlist_name)[3]+2, anchor=SW, window=Button(image=MyImage.MORE, width=20, height=20, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
            command=lambda: music_interface(f"Плейлист {self.playlist_name}", None)))

    def set_class(self, playlist_class):
        self.playlist_class = playlist_class

    def recovery_playlist(self):
        # Clear #
        Main.DATA_CANVAS.delete(self.draw_playlist_name)
        Main.DATA_CANVAS.delete(self.button_recovery)

        PlaylistStorage.add_playlist("database2.sqlite", self.playlist_name, self.music_data)

        self.draw_playlist_name = Main.DATA_CANVAS.create_text(self.x, self.y, text=self.playlist_name, fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        self.button_more = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.draw_playlist_name)[2]+13, Main.DATA_CANVAS.bbox(self.draw_playlist_name)[3]+2, anchor=SW, window=Button(image=MyImage.MORE, width=20, height=20, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
            command=lambda: Main.PLAYLIST_INTERFACE.playlist_draw(self.playlist_class, self.playlist_name)))

    def delete_playlist(self, music_data):
        self.music_data = music_data

        # Clear #
        Main.DATA_CANVAS.delete(self.draw_playlist_name)
        Main.DATA_CANVAS.delete(self.button_more)

        # Draw crossed out name #
        self.draw_playlist_name = Main.DATA_CANVAS.create_text(self.x, self.y, text="\u0336".join(self.playlist_name)+"\u0336", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        # button "recovery" #
        self.button_recovery = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.draw_playlist_name)[2]+13, Main.DATA_CANVAS.bbox(self.draw_playlist_name)[3]+2, anchor=SW, window=Button(image=MyImage.UPDATE, width=20, height=20, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
            command=lambda: self.recovery_playlist()))


class DrawPlaylists:
    def __init__(self, lib_name, music_interface):
        self.lib_name = lib_name
        self.music_interface = music_interface

    def clear_all(self, draw=True):
        try:
            Main.DATA_CANVAS.delete(self.playlist_text)

            Main.DATA_CANVAS.delete(self.set_playlist_name_draw)
            Main.DATA_CANVAS.delete(self.create_button)
            Main.DATA_CANVAS.delete(self.cancel_button)

            if draw:
                self.draw_new_playlist()
        except AttributeError:
            pass

    def draw_new_playlist(self, x, y):
        # Create playlist text #
        self.playlist_text = Main.DATA_CANVAS.create_text(x, y, text=languages["create_pl"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")
        self.playlist_button = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.playlist_text)[2]+30, y+1, window=Button(image=MyImage.NEW_PLAYLIST, width=27, height=27, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
            command=lambda: self.draw_create_playlist()))

    def save_playlist(self, event=""):
        name = self.playlist_name_var.get()

        if not len(name) > 1 or PlaylistStorage.check_playlist_in_db("database2.sqlite", name):
            return

        # Write new playlist in db #
        PlaylistStorage.add_playlist("database2.sqlite", name)

        x = Main.DATA_CANVAS.bbox(self.playlist_text)[0]
        y = Main.DATA_CANVAS.bbox(self.playlist_text)[3]

        self.clear_all(draw=False)

        new_playlist = DrawPlaylist(name, x, y, self.music_interface)
        new_playlist.set_class(new_playlist)

    def draw_playlists(self, x):
        # Draw all created playlists #
        playlists = PlaylistStorage.get_playlists("database2.sqlite")[::-1]

        self.y = Main.DATA_CANVAS.bbox(self.playlist_text)[3]+32

        # Draw playlists #
        for playlist_name in playlists:
            new_playlist = DrawPlaylist(playlist_name, x, self.y, self.music_interface)
            new_playlist.set_class(new_playlist)

            self.y += 40

    def draw_create_playlist(self):
        # Clear #
        Main.PLAYLIST_INTERFACE.close_playlist()
        Main.DATA_CANVAS.delete(self.playlist_text)
        Main.DATA_CANVAS.delete(self.playlist_button)

        self.playlist_text = Main.DATA_CANVAS.create_text(Main.DATA_CANVAS.bbox(self.lib_name)[0], Main.DATA_CANVAS.bbox(self.lib_name)[3]+60, text=languages["pl_name"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        # Draw block for set playlist name #
        self.playlist_name_var = StringVar()

        self.set_playlist_name = Entry(textvariable=self.playlist_name_var, width=18, bg=themes[Main.SETTINGS.theme]["background"], fg=themes[Main.SETTINGS.theme]["text_color"], selectbackground="red", insertbackground=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 11")
        self.set_playlist_name_draw = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.playlist_text)[2]+19, Main.DATA_CANVAS.bbox(self.playlist_text)[3]-9, window=self.set_playlist_name, anchor=W)

        self.set_playlist_name.bind("<Return>", self.save_playlist)

        # Draw button for create playlist #
        self.create_button = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.set_playlist_name_draw)[2]+12, Main.DATA_CANVAS.bbox(self.set_playlist_name_draw)[3]-3, anchor=SW, window=Button(image=MyImage.OK, width=18, height=16, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
            command=lambda: self.save_playlist()))

        # Draw button for cancel #
        self.cancel_button = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.create_button)[2]+12, Main.DATA_CANVAS.bbox(self.set_playlist_name_draw)[3]-1, anchor=SW, window=Button(image=MyImage.CLOSE, width=18, height=16, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
            command=lambda: self.clear_all()))
