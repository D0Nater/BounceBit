# -*- coding: utf-8 -*-

from Scripts.elements import *
from Scripts.draw_song import DrawSong
from Scripts.playlist_storage import PlaylistStorage


class PlaylistInterface:
    def __init__(self):
        self.song_num = 0

        self.num_of_wins = 0
        self.scroll_playlist = True

    def on_mousewheel(self, event):
        """ Scroll """
        if self.scroll_playlist and self.num_of_wins and self.playlist_canvas.bbox("all")[3] > self.playlist_canvas.winfo_height():
            self.playlist_canvas.yview_scroll(int(-1*(event.delta/100)), "units")

    def close_playlist(self):
        if not self.num_of_wins:
            return
        try:
            Main.SCROLL_WIN = True

            self.playlist_canvas.delete("all")
            self.playlist_canvas.destroy()
            del self.playlist_canvas

            self.bottom_line_canvas.delete("all")
            self.bottom_line_canvas.destroy()
            del self.bottom_line_canvas

            self.num_of_wins -= 1

            Main.DATA_CANVAS.bind_all("<MouseWheel>", Main.WINDOW_FOR_DATA.on_mousewheel)
        except AttributeError:
            pass

    def draw_music(self):
        if not int(self.music_data["music_num"]):
            self.playlist_canvas.create_text(40, self.playlist_canvas.bbox(self.playlists_name_draw)[3]+20, text=languages["add_error"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_second_color"], anchor=NW, font="Verdana 13")
            return

        self.y_coord = 80
        for song in self.music_data["music"]:
            new_song = DrawSong(self.playlist_canvas, self.y_coord, self.song_num, self.music_data["music"][song], self.playlist_name)

            new_song.draw_name(50)
            new_song.draw_play_button(new_song.song_bbox[2]+25, "second_color")
            new_song.draw_more_button(new_song.song_bbox[2]+9, "second_color")

            list_of_songs_class.append(new_song)

            if Main.SONG_PLAY_NOW["song_id"] == self.music_data["music"][song]["song_id"]:
                Main.PAST_SONG["class"] = new_song

            self.song_num += 1
            self.y_coord += 40

    def draw_bottom_line(self):
        self.bottom_line_canvas = Canvas(Main.ROOT, width=Main.DATA_CANVAS.winfo_width()/1.5, height=33, bg=themes[Main.SETTINGS.theme]["second_color"], highlightthickness=1, highlightbackground="grey9")
        self.bottom_line_canvas.place(x=Main.SETTINGS.width/2, y=Main.DATA_CANVAS.winfo_height()+24, anchor=N)

        self.song_num_draw = self.bottom_line_canvas.create_text(15, 8, text='Всего песен: '+str(self.song_num), fill=themes[Main.SETTINGS.theme]["text_color"], anchor=NW, font="Verdana 11")

    def delete_playlist_click(self):
        self.playlist_class.delete_playlist(self.music_data)
        PlaylistStorage.delete_playlist("database2.sqlite", self.playlist_name)
        self.close_playlist()

    def playlist_draw(self, playlist_class, playlist_name):
        self.song_num = 0
        self.num_of_wins += 1
        self.scroll_playlist = True

        self.playlist_name = playlist_name
        self.playlist_class = playlist_class
        self.music_data = PlaylistStorage.get_music("database2.sqlite", self.playlist_name)

        # Delete past window #
        self.close_playlist()
        Main.MORE_INFO_INTERFACE.close_song_info()

        # Draw window #
        self.playlist_canvas = Canvas(Main.ROOT, width=Main.DATA_CANVAS.winfo_width()/1.5, height=Main.DATA_CANVAS.winfo_height()-72, bg=themes[Main.SETTINGS.theme]["second_color"], highlightthickness=1, highlightbackground="grey9")
        self.playlist_canvas.bind_all("<MouseWheel>", self.on_mousewheel)
        self.playlist_canvas.place(x=Main.SETTINGS.width/2, y=Main.DATA_CANVAS.bbox("all")[1]+90, anchor=N)

        # Playlist name #
        self.playlists_name_draw = self.playlist_canvas.create_text(40, 34, text=languages["Плейлист"][Main.SETTINGS.language]+" - ", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")
        self.playlists_name_draw = self.playlist_canvas.create_text(self.playlist_canvas.bbox(self.playlists_name_draw)[2], 35, text=self.playlist_name, fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        # button "delete" #
        self.playlists_delete_draw = self.playlist_canvas.create_window(self.playlist_canvas.bbox(self.playlists_name_draw)[2]+15, 36, window=Button(image=MyImage.TRASHCAN, width=18, height=18, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: self.delete_playlist_click()), anchor=W)

        # button "edit" #
        self.playlists_edit_draw = self.playlist_canvas.create_window(self.playlist_canvas.bbox(self.playlists_delete_draw)[2]+8, 36, window=Button(image=MyImage.EDIT, width=18, height=18, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: print("edit playlist")), anchor=W)

        # button "close" #
        self.playlist_canvas.create_window(Main.DATA_CANVAS.winfo_width()/1.5-3, 6, window=Button(image=MyImage.CLOSE, width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: self.close_playlist()), anchor=NE)

        Main.ROOT.update()

        self.draw_music()
        self.draw_bottom_line()

        # Update window #
        self.playlist_canvas.config(scrollregion=self.playlist_canvas.bbox("all"))

        Main.SCROLL_WIN = False


class DrawPlaylist:
    def __init__(self, playlist_name, y):
        self.playlist_name = playlist_name
        self.y = y

        self.playlist_name_text = self.playlist_name[:40]+"..." if len(self.playlist_name) > 40 else self.playlist_name

        self.draw_playlist_name = Main.DATA_CANVAS.create_text(20, self.y, text=self.playlist_name_text, fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        self.button_more = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.draw_playlist_name)[2]+13, Main.DATA_CANVAS.bbox(self.draw_playlist_name)[3]+2, anchor=SW, window=Button(image=MyImage.MORE, width=20, height=20, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
            command=lambda: Main.PLAYLIST_INTERFACE.playlist_draw(self.playlist_class, self.playlist_name)))

    def set_class(self, playlist_class):
        self.playlist_class = playlist_class

    def recovery_playlist(self):
        # Clear #
        Main.DATA_CANVAS.delete(self.draw_playlist_name)
        Main.DATA_CANVAS.delete(self.button_recovery)

        PlaylistStorage.add_playlist("database2.sqlite", self.playlist_name, self.music_data)

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

            Main.DATA_CANVAS.delete(self.set_playlist_name_draw)
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

    def save_playlist(self, event=""):
        name = self.playlist_name_var.get()

        if not len(name) > 1 or PlaylistStorage.check_playlist_in_db("database2.sqlite", name):
            return

        # Write new playlist in db #
        PlaylistStorage.add_playlist("database2.sqlite", name)

        self.clear_all(draw=False)

        new_playlist = DrawPlaylist(name, Main.DATA_CANVAS.bbox(self.lib_name)[3]+64)
        new_playlist.set_class(new_playlist)

    def draw_playlists(self):
        # Draw all created playlists #
        playlists = PlaylistStorage.get_playlists("database2.sqlite")[::-1]

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
