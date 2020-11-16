# -*- coding: utf-8 -*-


""" For Graphical Interface """
from tkinter import *

""" Other Scripts """
from Scripts.elements import *
from Scripts.music import Playlist

""" Images """
from Scripts.images import MyImage

""" Main """
from Scripts.main import Main


class PlaylistInterface:
    def __init__(self):
        self.num_of_wins = 0

    def close_playlist(self):
        if self.num_of_wins:
            try:
                Main.SCROLL_WIN = True

                self.playlist_canvas.delete("all")
                self.playlist_canvas.destroy()

                del self.playlist_canvas

                self.num_of_wins -= 1
            except AttributeError:
                pass

    def draw_music(self):
        if int(self.music_data["music_num"]):
            for song in range(int(self.music_data["music_num"])):
                print(song)
        else:
            self.playlist_canvas.create_text(40, self.playlist_canvas.bbox(self.playlists_name_draw)[3]+20, text=languages["add_error"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_second_color"], anchor=NW, font="Verdana 13")

    def delete_playlist(self):
        self.playlist_class.delete_playlist(self.music_data)

        Playlist.delete_playlist("database2.sqlite", self.playlist_name)
        self.close_playlist()

        Main.SCROLL_WIN = True

    def playlist_draw(self, playlist_class, playlist_name):
        self.playlist_name = playlist_name
        self.playlist_class = playlist_class
        self.music_data = Playlist.get_music("database2.sqlite", self.playlist_name)

        # Delete past window #
        self.close_playlist()
        Main.MORE_INFO_INTERFACE.close_song_info()

        # Create new window #
        self.num_of_wins += 1

        # Draw window #
        self.playlist_canvas = Canvas(Main.ROOT, width=Main.DATA_CANVAS.winfo_width()/1.5, height=Main.DATA_CANVAS.winfo_height()-40, bg=themes[Main.SETTINGS.theme]["second_color"], highlightthickness=0)
        self.playlist_canvas.place(x=Main.SETTINGS.width/2, y=Main.DATA_CANVAS.bbox("all")[1]+90, anchor=N)

        # Playlist name #
        self.playlists_name_draw = self.playlist_canvas.create_text(40, 34, text=languages["Плейлист"][Main.SETTINGS.language]+" - ", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")
        self.playlists_name_draw = self.playlist_canvas.create_text(self.playlist_canvas.bbox(self.playlists_name_draw)[2], 35, text=self.playlist_name, fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        # button "delete" #
        self.playlists_delete_draw = self.playlist_canvas.create_window(self.playlist_canvas.bbox(self.playlists_name_draw)[2]+15, 36, window=Button(image=MyImage.TRASHCAN, width=18, height=18, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: self.delete_playlist()), anchor=W)

        # button "edit" #
        self.playlists_edit_draw = self.playlist_canvas.create_window(self.playlist_canvas.bbox(self.playlists_delete_draw)[2]+8, 36, window=Button(image=MyImage.EDIT, width=18, height=18, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: print("edit playlist")), anchor=W)

        # button "close" #
        self.playlist_canvas.create_window(Main.DATA_CANVAS.winfo_width()/1.5-4, 6, window=Button(image=MyImage.CLOSE, width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: self.close_playlist()), anchor=NE)

        Main.ROOT.update()

        self.draw_music()

        Main.SCROLL_WIN = False


class DrawPlaylist:
    def __init__(self, playlist_name, y):
        self.playlist_name = playlist_name
        self.y = y

        self.draw_playlist_name = Main.DATA_CANVAS.create_text(20, self.y, text=self.playlist_name, fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        self.button_more = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.draw_playlist_name)[2]+13, Main.DATA_CANVAS.bbox(self.draw_playlist_name)[3]+2, anchor=SW, window=Button(image=MyImage.MORE, width=20, height=20, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
            command=lambda: Main.PLAYLIST_INTERFACE.playlist_draw(self.playlist_class, self.playlist_name)))

    def set_class(self, playlist_class):
        self.playlist_class = playlist_class

    def recovery_playlist(self):
        # Clear #
        Main.DATA_CANVAS.delete(self.draw_playlist_name)
        Main.DATA_CANVAS.delete(self.button_recovery)

        Playlist.add_playlist("database2.sqlite", self.playlist_name, self.music_data)

        self.draw_playlist_name = Main.DATA_CANVAS.create_text(20, self.y, text=self.playlist_name, fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        self.button_more = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.draw_playlist_name)[2]+13, Main.DATA_CANVAS.bbox(self.draw_playlist_name)[3]+2, anchor=SW, window=Button(image=MyImage.MORE, width=20, height=20, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
            command=lambda: Main.PLAYLIST_INTERFACE.playlist_draw(self.playlist_class, self.playlist_name)))

    def delete_playlist(self, music_data):
        self.music_data = music_data

        # Clear #
        Main.DATA_CANVAS.delete(self.draw_playlist_name)
        Main.DATA_CANVAS.delete(self.button_more)

        # Draw crossed out name #
        self.draw_playlist_name = Main.DATA_CANVAS.create_text(20, self.y, text="\u0336".join(self.playlist_name)+"\u0336", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        # button "recovery" #
        self.button_recovery = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.draw_playlist_name)[2]+13, Main.DATA_CANVAS.bbox(self.draw_playlist_name)[3]+2, anchor=SW, window=Button(image=MyImage.UPDATE, width=20, height=20, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
            command=lambda: self.recovery_playlist()))


class DrawPlaylists:
    def __init__(self, lib_name):
        self.lib_name = lib_name

    def get_y_pos(self):
        return self.y

    def clear_all(self, draw=True):
        try:
            Main.DATA_CANVAS.delete(self.playlist_text)

            Main.DATA_CANVAS.delete(self.playlist_name_draw)
            Main.DATA_CANVAS.delete(self.create_button)
            Main.DATA_CANVAS.delete(self.cancel_button)

            if draw:
                self.draw_new_playlist()
        except AttributeError:
            pass

    def draw_new_playlist(self):
        # Create playlist text #
        self.playlist_text = Main.DATA_CANVAS.create_text(Main.DATA_CANVAS.bbox(self.lib_name)[0], Main.DATA_CANVAS.bbox(self.lib_name)[3]+60, text=languages["create_pl"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")
        self.playlist_button = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.playlist_text)[2]+30, Main.DATA_CANVAS.bbox(self.lib_name)[3]+61, window=Button(image=MyImage.NEW_PLAYLIST, width=27, height=27, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
            command=lambda: self.draw_create_playlist()))

        self.draw_playlists()

    def save_playlist(self):
        name = self.set_playlist_name.get(1.0, "end-1c").replace("\n", "-")
        if len(name) > 1:
            # Write new playlist in db #
            if not Playlist.check_playlist_in_db("database2.sqlite", name) and name is not "":
                Playlist.add_playlist("database2.sqlite", name)

                self.clear_all(draw=False)

                new_playlist = DrawPlaylist(name, Main.DATA_CANVAS.bbox(self.lib_name)[3]+60)
                new_playlist.set_class(new_playlist)
            else:
                pass

    def draw_playlists(self):
        # Draw all created playlists #
        playlists = Playlist.get_playlists("database2.sqlite")[::-1]

        self.y = Main.DATA_CANVAS.bbox(self.playlist_text)[3]+34

        # Draw playlists #
        for playlist_name in playlists:
            new_playlist = DrawPlaylist(playlist_name, self.y)
            new_playlist.set_class(new_playlist)

            self.y += 40

    def draw_create_playlist(self):
        # Clear #
        Main.PLAYLIST_INTERFACE.close_playlist()
        Main.DATA_CANVAS.delete(self.playlist_text)
        Main.DATA_CANVAS.delete(self.playlist_button)

        self.playlist_text = Main.DATA_CANVAS.create_text(Main.DATA_CANVAS.bbox(self.lib_name)[0], Main.DATA_CANVAS.bbox(self.lib_name)[3]+60, text=languages["pl_name"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        # Draw block for set playlist name #
        self.set_playlist_name = Text(width=18, height=1.4, bg=themes[Main.SETTINGS.theme]["background"], fg=themes[Main.SETTINGS.theme]["text_color"], selectbackground="red", insertbackground=themes[Main.SETTINGS.theme]["text_color"], wrap=NONE, font="Verdana 11")
        self.playlist_name_draw = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.playlist_text)[2]+15, Main.DATA_CANVAS.bbox(self.playlist_text)[3]-9, window=self.set_playlist_name, anchor=W)

        # Draw button for create playlist #
        self.create_button = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.playlist_name_draw)[2]+12, Main.DATA_CANVAS.bbox(self.playlist_name_draw)[3]-3, anchor=SW, window=Button(image=MyImage.OK, width=18, height=16, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
            command=lambda: self.save_playlist()))

        # Draw button for cancel #
        self.cancel_button = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.create_button)[2]+12, Main.DATA_CANVAS.bbox(self.playlist_name_draw)[3]-1, anchor=SW, window=Button(image=MyImage.CLOSE, width=18, height=16, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
            command=lambda: self.clear_all()))