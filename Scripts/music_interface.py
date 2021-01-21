# -*- coding: utf-8 -*-

""" For encode song id """
from Scripts.settings import decode_text

from Scripts.elements import *
from Scripts.draw_song import DrawSong
from Scripts.parse_music import ParseMusic
from Scripts.music_storage import MusicStorage
from Scripts.playlist_storage import PlaylistStorage
from Scripts.playlist_interface import DrawPlaylists


class SearchData:
    ALL_TAGS = ["song"]

    def parse_data(self, song_id):
        parse_data_json = {"music": {"num": 0}, "pages": [], "error": None}

        Main.DATA_CANVAS.delete("all")
        # loading #
        load_text = Main.DATA_CANVAS.create_text(14, 15, text=languages["Загрузка"][Main.SETTINGS.language]+"...", fill=themes[Main.SETTINGS.theme]["text_color"],  font="Verdana 13", anchor=W)
        Main.ROOT.update()

        try:
            parse_data_json["music"]["song0"] = ParseMusic.more_song_info(song_id)
            parse_data_json["music"]["num"] = 1
        except ConnectionError:
            parse_data_json["error"] = "connect_error"
        except:
            parse_data_json["error"] = "not_found"

        Main.DATA_CANVAS.delete(load_text)

        return parse_data_json

    def get_text(self, text_str):
        self.text_arr = text_str.split("/")

        if self.text_arr[-1] not in SearchData.ALL_TAGS:
            self.music_interface("Поиск 1", None, text_str)
            return

        try:
            song_id = decode_text(self.text_arr[-2])
            self.music_interface("Поиск 1", self.parse_data(song_id), text_str)
        except:
            pass


class MusicInterface(SearchData):
    def search_data(self):
        if self.lib.startswith("Рекомендации"):
            return ParseMusic.top_music(int(self.lib.split(" ")[1]))

        elif self.lib.startswith("Поиск"):
            return ParseMusic.search_music(self.search_text, int(self.lib.split(" ")[1]))

        elif self.lib.startswith("Жанр"):
            return ParseMusic.genres_music(languages[self.lib.split(" ")[1]]["num"] , int(self.lib.split(" ")[2]))

        elif self.lib.startswith("Плейлист"):
            self.playlist_name = " ".join(self.lib.split(" ")[1:])

            music_data = PlaylistStorage.get_music("database2.sqlite", self.playlist_name)

            all_data = {"music": {"num": int(music_data["music"]["num"])}, "error": None if int(music_data["music"]["num"]) else "add_error"}

            song_num = int(music_data["music"]["num"])-1
            for song in music_data["music"]:
                if "song" in song:
                    all_data["music"][f"song{song_num}"] = music_data["music"][song]
                    song_num -= 1

            return all_data

    def draw_playlist_interface(self):
        def delete_playlist_click():
            PlaylistStorage.delete_playlist("database2.sqlite", self.playlist_name)
            self.music_interface("Избранное", MusicStorage.read_music("database2.sqlite", "add_error"))

        def edit_playlist_click():
            def cancel_entry(save=False):
                Main.DATA_CANVAS.delete(self.lib_name)
                self.lib_name_text = languages["Плейлист"][Main.SETTINGS.language]+" - "+self.playlist_name_var.get() if save else self.lib_name_text
                self.lib_name = Main.DATA_CANVAS.create_text(14, 15, text=self.lib_name_text, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 13", anchor=W)

                del self.playlist_name_var

                Main.DATA_CANVAS.delete(self.create_button)
                Main.DATA_CANVAS.delete(self.cancel_button)
                Main.DATA_CANVAS.delete(self.set_playlist_name_draw)

                self.set_playlist_name.unbind("<Return>")

                self.draw_playlist_interface()

            def save_playlist(event):
                new_name = self.playlist_name_var.get()
                if not len(new_name) > 1 or PlaylistStorage.check_playlist_in_db("database2.sqlite", new_name):
                    return

                PlaylistStorage.change_playlist("database2.sqlite", self.playlist_name, new_name)

                cancel_entry(save=True)

            Main.DATA_CANVAS.delete(self.playlists_delete_draw)
            Main.DATA_CANVAS.delete(self.playlists_edit_draw)

            # Draw block for set playlist name #
            self.playlist_name_var = StringVar()

            Main.DATA_CANVAS.delete(self.lib_name)
            self.lib_name = Main.DATA_CANVAS.create_text(14, 15, text=languages["pl_name"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 13", anchor=W)

            self.set_playlist_name = Entry(textvariable=self.playlist_name_var, width=18, bg=themes[Main.SETTINGS.theme]["background"], fg=themes[Main.SETTINGS.theme]["text_color"], selectbackground="red", insertbackground=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 11")
            self.set_playlist_name.insert(0, self.playlist_name)
            self.set_playlist_name_draw = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.lib_name)[2]+19, Main.DATA_CANVAS.bbox(self.lib_name)[3]-9, window=self.set_playlist_name, anchor=W)

            self.set_playlist_name.bind("<Return>", save_playlist)

            # Draw button for create playlist #
            self.create_button = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.set_playlist_name_draw)[2]+12, Main.DATA_CANVAS.bbox(self.set_playlist_name_draw)[3]-3, anchor=SW, window=Button(image=MyImage.OK, width=18, height=16, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
                command=lambda: save_playlist(None)))

            # Draw button for cancel #
            self.cancel_button = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.create_button)[2]+12, Main.DATA_CANVAS.bbox(self.set_playlist_name_draw)[3]-1, anchor=SW, window=Button(image=MyImage.CLOSE, width=18, height=16, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
                command=lambda: cancel_entry()))

        # button "delete" #
        self.playlists_delete_draw = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.lib_name)[2]+15, Main.DATA_CANVAS.bbox(self.lib_name)[1], anchor=NW, window=Button(image=MyImage.TRASHCAN, width=18, height=18, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], command=lambda: delete_playlist_click()))

        # button "edit" #
        self.playlists_edit_draw = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.playlists_delete_draw)[2]+8, Main.DATA_CANVAS.bbox(self.lib_name)[1], anchor=NW, window=Button(image=MyImage.EDIT, width=18, height=18, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], command=lambda: edit_playlist_click()))

    def draw_music(self):
        Main.LIST_OF_MUSIC = self.all_data

        Main.LIST_OF_IDS = [self.all_data["music"][f"song{i}"]["song_id"] for i in range(self.all_data["music"]["num"])]

        self.y += 20
        for song_num in range(self.all_data["music"]["num"]):
            new_song = DrawSong(Main.DATA_CANVAS, self.y, song_num, self.all_data["music"][f"song{song_num}"], self.lib)

            new_song.draw_name(25)
            new_song.draw_play_button(new_song.song_bbox[2]+25)
            new_song.draw_add_button(new_song.song_bbox[2]+13)
            new_song.draw_save_button(new_song.song_bbox[2]+11)
            new_song.draw_more_button(new_song.song_bbox[2]+7)

            list_of_songs_class.append(new_song)

            self.y += 40

        if Main.SONG_PLAY_NOW["song_id"] in Main.LIST_OF_IDS:
            Main.PAST_SONG["class"] = list_of_songs_class[Main.LIST_OF_IDS.index(Main.PAST_SONG["song_id"])]

    def draw_search(self):
        def search_interface(event):
            self.get_text(search_text_var.get())

        # Search #
        search_draw = Main.DATA_CANVAS.create_text(Main.DATA_CANVAS.bbox(self.lib_name)[0], self.y+12, text=languages["Поиск"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 13", anchor=NW)
        self.y = Main.DATA_CANVAS.bbox(search_draw)[3]+10

        # Search line #
        search_text_var = StringVar()

        text_entry = Entry(textvariable=search_text_var, width=18, bg=themes[Main.SETTINGS.theme]["background"], fg=themes[Main.SETTINGS.theme]["text_color"], selectbackground="red", insertbackground=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 11")
        text_entry.insert(0, self.search_text)
        text_entry_draw = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(search_draw)[2]+19, Main.DATA_CANVAS.bbox(search_draw)[3]-9, window=text_entry, anchor=W)

        text_entry.bind("<Return>", search_interface)
        text_entry.bind("<FocusIn>", Main.KEY_EVENT.unbind_keys)

        # Draw button for search #
        Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(text_entry_draw)[2]+17, Main.DATA_CANVAS.bbox(search_draw)[3]-9, anchor=W, window=Button(image=MyImage.SEARCH, width=16, height=16, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
            command=lambda: self.get_text(search_text_var.get())))

    def draw_genres(self):
        if self.lib.startswith("Рекомендации") or self.lib.startswith("Жанр") or self.lib.startswith("Поиск"):
            genres_text = Main.DATA_CANVAS.create_text(Main.DATA_CANVAS.bbox(self.lib_name)[0], self.y+10, text=languages["Жанры"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=NW, font="Verdana 13")

            genre_pop = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(genres_text)[2]+20, self.y+10, anchor=NW, window=Button(text=languages["Поп"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=0, width=7, font="Verdana 10", \
                command=lambda: self.music_interface("Жанр Поп 1", None)))

            genre_rock = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(genre_pop)[2]+7, self.y+10, anchor=NW, window=Button(text=languages["Рок"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=0, width=7, font="Verdana 10", \
                command=lambda: self.music_interface("Жанр Рок 1", None)))

            genre_rap = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(genre_rock)[2]+7, self.y+10, anchor=NW, window=Button(text=languages["Рэп"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=0, width=7, font="Verdana 10", \
                command=lambda: self.music_interface("Жанр Рэп 1", None)))

            genre_jazz = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(genre_rap)[2]+7, self.y+10, anchor=NW, window=Button(text=languages["Джаз"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=0, width=7, font="Verdana 10", \
                command=lambda: self.music_interface("Жанр Джаз 1", None)))

            genre_shanson = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(genre_jazz)[2]+7, self.y+10, anchor=NW, window=Button(text=languages["Шансон"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=0, width=9, font="Verdana 10", \
                command=lambda: self.music_interface("Жанр Шансон 1", None)))

            genre_classical = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(genre_shanson)[2]+7, self.y+10, anchor=NW, window=Button(text=languages["Классика"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=0, width=9, font="Verdana 10", \
                command=lambda: self.music_interface("Жанр Классика 1", None)))

            self.y = Main.DATA_CANVAS.bbox(genre_classical)[3]+10

    def draw_playlists(self):
        if self.lib.startswith("Избранное"):
            playlists = DrawPlaylists(self.lib_name, self.music_interface)
            playlists.draw_new_playlist(Main.DATA_CANVAS.bbox(self.lib_name)[0], self.y+20)
            playlists.draw_playlists(Main.DATA_CANVAS.bbox(self.lib_name)[0])
            self.y = playlists.y - 20

    def draw_pages(self):
        class PageButton:
            """ Class for pages (search music / genres) """
            def __init__(self, page_num, func, args):
                self.page_num = page_num
                self.func = func
                self.args = args

            def draw_button(self, x, y):
                Main.DATA_CANVAS.create_window(x, y, window=Button(text=self.page_num, width=2, height=1, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 12", relief=RIDGE, \
                    command=lambda: self.func(*self.args)))

        page_x = Main.DATA_CANVAS.bbox(self.lib_name)[2]+35
        if self.lib.startswith("Поиск"):
            for page_num in self.all_data["pages"]:
                PageButton(page_num, self.music_interface, (f"Поиск {page_num}", None, self.search_text)).draw_button(page_x, Main.DATA_CANVAS.bbox(self.lib_name)[3]-12)
                page_x += 29

        elif self.lib.startswith("Жанр"):
            for page_num in self.all_data["pages"]:
                PageButton(page_num, self.music_interface, ("Жанр %s %s"%(self.lib.split(" ")[1], page_num), None, "")).draw_button(page_x, Main.DATA_CANVAS.bbox(self.lib_name)[3]-12)
                page_x += 29

        elif self.lib.startswith("Рекомендации"):
            for page_num in self.all_data["pages"]:
                PageButton(page_num, self.music_interface, (f"Рекомендации {page_num}", None)).draw_button(page_x, Main.DATA_CANVAS.bbox(self.lib_name)[3]-12)
                page_x += 29

    def music_interface(self, lib, all_data, search_text=""):
        clear_ram()
        # clear window #
        Main.DATA_CANVAS.delete("all")

        # close all #
        Main.SETTINGS_INTERFACE.del_news_block()
        Main.MORE_INFO_INTERFACE.close_song_info()
        Main.MORE_SETTINGS.close_window()

        Thread(target=clear_list_of_songs).start() # delete past songs

        self.lib = lib
        self.all_data = all_data
        self.search_text = search_text
        Main.PAST_SONG["lib_now"] = self.lib
        Main.LIST_OF_IDS = []
        self.y = 90 if self.lib.startswith("Загруженное") else 130

        # lib name #
        if self.lib.startswith("Жанр"):
            self.lib_name_text = languages["Жанр"][Main.SETTINGS.language]+"-"+languages[self.lib.split(" ")[1]][Main.SETTINGS.language]+" - "+languages["Страница"][Main.SETTINGS.language]+" "+self.lib.split(" ")[2]
        elif self.lib.startswith("Плейлист"):
           self.lib_name_text = languages["Плейлист"][Main.SETTINGS.language]+" - "+" ".join(self.lib.split(" ")[1:])
        else:
            self.lib_name_text = languages[self.lib.split(" ")[0]][Main.SETTINGS.language]+((" - "+languages["Страница"][Main.SETTINGS.language]+" "+self.lib.split(" ")[1]) if len(self.lib.split(" ")) > 1 else "")

        # delete logo #
        try: del Main.SCREENSAVER
        except: pass

        just_px = Main.DATA_CANVAS.create_text(0, 0, text=".", fill=themes[Main.SETTINGS.theme]["background"], anchor=W, font="Verdana 1")

        # loading #
        load_text = Main.DATA_CANVAS.create_text(14, 15, text=languages["Загрузка"][Main.SETTINGS.language]+"...", fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 13", anchor=W)
        Main.ROOT.update()

        if self.all_data is None:
            self.all_data = self.search_data()

        Main.DATA_CANVAS.delete(load_text)

        self.lib_name = Main.DATA_CANVAS.create_text(14, 15, text=self.lib_name_text, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 13", anchor=W)
        self.y = Main.DATA_CANVAS.bbox(self.lib_name)[3]

        self.draw_search()

        self.draw_genres()

        self.draw_playlists()

        if self.lib.startswith("Плейлист"):
            self.draw_playlist_interface()

        if self.all_data["error"] is None:
            self.draw_music()

            self.draw_pages()

            Main.ROOT.update()
            # Update window #
            Main.DATA_CANVAS.config(scrollregion=Main.DATA_CANVAS.bbox("all"))

            Main.MENU.update_buttons()

            draw_just_lines()
        else:
            # Write error #
            Main.DATA_CANVAS.create_text(25, self.y+20, text=languages[self.all_data["error"]][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_second_color"], font="Verdana 12", anchor=W)
