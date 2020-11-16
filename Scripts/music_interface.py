# -*- coding: utf-8 -*-

""" For Graphical Interface """
from tkinter import *

""" For download and listen music """
from threading import Thread

""" For clear RAM """
from gc import collect as clear_ram

""" Other Scripts """
from Scripts.elements import *
from Scripts.parse_music import ParseMusic
from Scripts.draw_song import Song
from Scripts.playlist_interface import DrawPlaylists

""" Images """
from Scripts.images import MyImage

""" Main """
from Scripts.main import Main


class MusicInterface:
    def search_data(self):
        if self.lib.split(" ")[0] == "Рекомендации":
            return ParseMusic.top_music()

        elif self.lib.split(" ")[0] == "Поиск":
            return ParseMusic.search_music(self.search_text, self.lib.split(" ")[1])

        elif self.lib.split(" ")[0] == "Жанр":
            return ParseMusic.genres_music(languages[self.lib.split(" ")[1]]["en"].lower(), self.lib.split(" ")[2])

    def draw_music(self):
        Main.LIST_OF_MUSIC = self.all_data

        Main.LIST_OF_IDS = [self.all_data["music"][f"song{i}"]["song_id"] for i in range(self.all_data["music"]["num"])]

        """ Draw data on page """
        # music #
        for song_num in range(self.all_data["music"]["num"]):
            # Song info #
            song_name = self.all_data["music"][f"song{song_num}"]["name"]
            song_author = self.all_data["music"][f"song{song_num}"]["author"]

            # Draw song name and author #
            name_draw = Main.DATA_CANVAS.create_text(20, self.y, text=f"{song_name}  -  ", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 12")
            author_draw = Main.DATA_CANVAS.create_text(Main.DATA_CANVAS.bbox(name_draw)[2], self.y, text=song_author, fill=themes[Main.SETTINGS.theme]["text_second_color"], anchor=W, font="Verdana 12")

            del song_name, song_author

            # Creat buttons for song #
            new_song = Song(Main.DATA_CANVAS.bbox(author_draw)[2]+34, self.y, song_num, self.all_data["music"][f"song{song_num}"])
            new_song.draw_music(new_song, self.lib)

            list_of_songs_class.append(new_song)

            if Main.SONG_PLAY_NOW["song_id"] == self.all_data["music"][f"song{song_num}"]["song_id"]:
                Main.PAST_SONG["class"] = new_song

            self.y += 40

    def draw_search(self):
        # Search #
        search_draw = Main.DATA_CANVAS.create_text(Main.DATA_CANVAS.bbox(self.lib_name)[0], Main.DATA_CANVAS.bbox(self.lib_name)[3]+25, text=languages["Поиск"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        # Search line #
        text_e = Text(width=18, height=1.4, bg=themes[Main.SETTINGS.theme]["background"], fg=themes[Main.SETTINGS.theme]["text_color"], selectbackground="red", insertbackground=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 11")
        text_e.insert(END, self.search_text)
        text_e_draw = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(search_draw)[2]+105, Main.DATA_CANVAS.bbox(search_draw)[3]-9, window=text_e)

        # Draw button for search #
        Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(text_e_draw)[2]+17, Main.DATA_CANVAS.bbox(search_draw)[3]-9, window=Button(image=MyImage.SEARCH, width=16, height=16, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE, \
            command=lambda: self.music_interface("Поиск 1", None, text_e.get(1.0, "end-1c"))))

    def draw_genres(self):
        if self.lib.split(" ")[0] == "Рекомендации" or self.lib.split(" ")[0] == "Жанр" or self.lib.split(" ")[0] == "Поиск":
            genres_text = Main.DATA_CANVAS.create_text(Main.DATA_CANVAS.bbox(self.lib_name)[0], Main.DATA_CANVAS.bbox(self.lib_name)[3]+60, text=languages["Жанры"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

            genre_pop = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(genres_text)[2]+20, Main.DATA_CANVAS.bbox(self.lib_name)[3]+61, anchor=W, window=Button(text=languages["Поп"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=0, width=7, font="Verdana 10", \
                command=lambda: self.music_interface("Жанр Поп 1", None)))

            genre_rock = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(genre_pop)[2]+7, Main.DATA_CANVAS.bbox(self.lib_name)[3]+61, anchor=W, window=Button(text=languages["Рок"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=0, width=7, font="Verdana 10", \
                command=lambda: self.music_interface("Жанр Рок 1", None)))

            genre_rap = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(genre_rock)[2]+7, Main.DATA_CANVAS.bbox(self.lib_name)[3]+61, anchor=W, window=Button(text=languages["Рэп"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=0, width=7, font="Verdana 10", \
                command=lambda: self.music_interface("Жанр Рэп 1", None)))

            genre_jazz = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(genre_rap)[2]+7, Main.DATA_CANVAS.bbox(self.lib_name)[3]+61, anchor=W, window=Button(text=languages["Джаз"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=0, width=7, font="Verdana 10", \
                command=lambda: self.music_interface("Жанр Джаз 1", None)))

            genre_shanson = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(genre_jazz)[2]+7, Main.DATA_CANVAS.bbox(self.lib_name)[3]+61, anchor=W, window=Button(text=languages["Шансон"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=0, width=9, font="Verdana 10", \
                command=lambda: self.music_interface("Жанр Шансон 1", None)))

            genre_classical = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(genre_shanson)[2]+7, Main.DATA_CANVAS.bbox(self.lib_name)[3]+61, anchor=W, window=Button(text=languages["Классика"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=0, width=9, font="Verdana 10", \
                command=lambda: self.music_interface("Жанр Классика 1", None)))

    def draw_playlists(self):
        if self.lib.split(" ")[0] == "Избранное":
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
                Main.DATA_CANVAS.create_window(x, y, window=Button(text=self.page_num, width=2, height=1, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 12", relief=RIDGE, \
                    command=lambda: self.func(*self.args)))

        page_x = Main.DATA_CANVAS.bbox(self.lib_name)[2]+35
        if self.lib.split(" ")[0] == "Поиск":
            for page_num in self.all_data["pages"]:
                PageButton(page_num, self.music_interface, (f"Поиск {page_num}", None, self.search_text)).draw_button(page_x, Main.DATA_CANVAS.bbox(self.lib_name)[3]-9)
                page_x += 29

        elif self.lib.split(" ")[0] == "Жанр":
            for page_num in self.all_data["pages"]:
                PageButton(page_num, self.music_interface, ("Жанр %s %s"%(self.lib.split(" ")[1], page_num), None, "")).draw_button(page_x, Main.DATA_CANVAS.bbox(self.lib_name)[3]-9)
                page_x += 29

    def music_interface(self, lib, all_data, search_text=""):
        clear_ram()
        Main.DATA_CANVAS.delete("all")
        Main.SETTINGS_INTERFACE.del_news_block()
        Main.MORE_INFO_INTERFACE.close_song_info()
        Main.PLAYLIST_INTERFACE.close_playlist()
        Thread(target=clear_list_of_songs).start() # delete past data

        self.lib = lib
        self.all_data = all_data
        self.search_text = search_text
        Main.PAST_SONG["lib_now"] = self.lib
        Main.LIST_OF_IDS = []
        self.y = 90 if self.lib.split(" ")[0] == "Загруженное" else 130

        # lib name #
        if lib.split(" ")[0] == "Жанр":
            lib_name_text = languages["Жанр"][Main.SETTINGS.language]+"-"+languages[lib.split(" ")[1]][Main.SETTINGS.language]+" - "+languages["Страница"][Main.SETTINGS.language]+" "+lib.split(" ")[2]
        else:
            lib_name_text = languages[lib.split(" ")[0]][Main.SETTINGS.language]+((" - "+languages["Страница"][Main.SETTINGS.language]+" "+lib.split(" ")[1]) if len(lib.split(" ")) > 1 else "")

        # delete logo #
        try: del Main.SCREENSAVER
        except: pass

        # Create background #
        if Main.SETTINGS.bg_image != "None":
            try: Main.DATA_CANVAS.create_image(0, 0, image=Main.IMAGE_BG, anchor=NW)
            except: pass

        # loading #
        load_text = Main.DATA_CANVAS.create_text(14, 15, text=languages["Загрузка"][Main.SETTINGS.language]+"...", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")
        Main.ROOT.update()

        # Search data #
        if self.all_data is None:
            self.all_data = self.search_data()

        Main.DATA_CANVAS.delete(load_text)

        # Lib name #
        self.lib_name = Main.DATA_CANVAS.create_text(14, 15, text=lib_name_text, fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        # Search line #
        self.draw_search()

        # Genres #
        self.draw_genres()

        # Playlists #
        self.draw_playlists()

        if self.all_data["error"] is None:
            # Music #
            self.draw_music()

            # Pages #
            self.draw_pages()

            # Update window #
            Main.ROOT.update()
            Main.DATA_CANVAS.config(scrollregion=Main.DATA_CANVAS.bbox("all"))

            Main.MENU.update_buttons()

            Main.JUST_LINE = Canvas(Main.ROOT, width=Main.SETTINGS.width, height=25, bg=themes[Main.SETTINGS.theme]["second_color"], bd=0, highlightthickness=0)
            Main.JUST_LINE.place(x=0, y=Main.SETTINGS.height-143)
        else:
            # Write error #
            Main.DATA_CANVAS.create_text(14, self.y, text=languages[self.all_data["error"]][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_second_color"], anchor=W, font="Verdana 12")
