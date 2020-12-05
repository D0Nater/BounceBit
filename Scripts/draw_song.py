# -*- coding: utf-8 -*-

""" For Graphical Interface """
from tkinter import *

""" For download and play music """
from threading import Thread

""" Other Scripts """
from Scripts.elements import *
from Scripts.music_storage import MusicStorage

""" For song manage """
from Scripts.song_manage import SongManage

""" Images """
from Scripts.images import MyImage

""" Main """
from Scripts.main import Main


class DrawSong(SongManage):
    def __init__(self, canvas, y, song_num, info, lib):
        self.canvas = canvas

        self.y = y
        self.lib = lib
        self.song_num = song_num
        self.song_data = info

        self.song_bbox = None
        self.song_coords = {}

    # def __del__(self):
    #     pass

    def del_class(self):
        del self.y
        del self.canvas
        del self.song_num
        del self.song_data
        del self.song_bbox

    def play_click(self):
        if self.click_play:
            self.click_play = 0
            Main.PLAYER_SETTINGS["play"] = 0
            self.play_button["image"] = MyImage.PLAY

            Main.PLAYER.pause()

            # update buttons #
            Main.SONG_LINE.draw_music_line()
            Main.MENU.update_buttons()
        else:
            self.click_play = 1
            Main.PLAYER_SETTINGS["play"] = 1
            self.play_button["image"] = MyImage.PAUSE

            if self.song_data["song_id"] != Main.SONG_PLAY_NOW["song_id"]:
                # update lists #
                if Main.LIST_OF_PLAY != Main.LIST_OF_MUSIC:
                    Main.RANDOM_MUSIC_LIST = []
                    Main.LIST_OF_PLAY = Main.LIST_OF_MUSIC.copy()
                    Main.LIST_OF_PLAY["classes"] = list_of_songs_class.copy()

                Main.PAST_SONG["past_lib"] = self.lib

                Thread(target=self.update_music, daemon=True).start()
            else:
                Thread(target=Main.PLAYER.play, daemon=True).start() # play

                # update buttons #
                Main.SONG_LINE.draw_music_line()
                Main.MENU.update_buttons()

            # update window with more song info #
            if Main.MORE_INFO_INTERFACE.num_of_wins:
                Main.MORE_INFO_INTERFACE.song_info_draw(Main.PAST_SONG["class"].song_data, Main.MORE_INFO_INTERFACE.searched_data)

    def add_click(self):
        if self.click_add:
            # Delete song #
            self.click_add = 0
            self.add_button["image"] = MyImage.ADD
            MusicStorage.delete_song("database2.sqlite", self.song_data["song_id"])
        else:
            # Add song #
            self.click_add = 1
            self.add_button["image"] = MyImage.ADD_CLICK
            MusicStorage.add_song("database2.sqlite", self.song_data)

    def save_click(self):
        if self.click_save:
            # Delete song #
            self.click_save = 0
            self.save_button["image"] = MyImage.SAVE
            MusicStorage.delete_song_file(self.song_data["song_id"])
            MusicStorage.delete_song("database3.sqlite", self.song_data["song_id"])
        else:
            # Download song #
            self.click_save = 1
            self.save_button["image"] = MyImage.SAVE_CLICK
            Thread(target=MusicStorage.download_music, args=(self.song_data["song_id"], self.song_data["url"])).start()
            MusicStorage.add_song("database3.sqlite", self.song_data)

    def more_click(self):
        Main.MORE_INFO_INTERFACE.song_info_draw(self.song_data)

    def draw_play_button(self, x_coord, button_color="background"):
        self.click_play = 0

        if Main.PLAYER_SETTINGS["play"] and Main.SONG_PLAY_NOW["song_id"] == self.song_data["song_id"]:
            self.click_play = 1
            self.play_button = Button(image=MyImage.PAUSE, command=lambda: self.play_click(), width=16, height=23, bd=0, bg=themes[Main.SETTINGS.theme][button_color], activebackground=themes[Main.SETTINGS.theme][button_color], relief=RIDGE)
        else:
            self.play_button = Button(image=MyImage.PLAY, command=lambda: self.play_click(), width=16, height=23, bd=0, bg=themes[Main.SETTINGS.theme][button_color], activebackground=themes[Main.SETTINGS.theme][button_color], relief=RIDGE)
        self.play_button_draw = self.canvas.create_window(x_coord, self.y, anchor=W, window=self.play_button)

        self.song_bbox = self.canvas.bbox(self.play_button_draw)
        self.song_coords["play_button"] = self.canvas.bbox(self.play_button_draw)

    def draw_add_button(self, x_coord, button_color="background"):
        self.click_add = MusicStorage.check_song_in_db("database2.sqlite", self.song_data["song_id"])

        if self.click_add:
            self.add_button = Button(image=MyImage.ADD_CLICK, command=lambda: self.add_click(), width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme][button_color], activebackground=themes[Main.SETTINGS.theme][button_color], relief=RIDGE)
        else:
            self.add_button = Button(image=MyImage.ADD, command=lambda: self.add_click(), width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme][button_color], activebackground=themes[Main.SETTINGS.theme][button_color], relief=RIDGE)
        self.add_button_draw = self.canvas.create_window(x_coord, self.y, anchor=W, window=self.add_button)

        self.song_bbox = self.canvas.bbox(self.add_button_draw)
        self.song_coords["add_button"] = self.canvas.bbox(self.add_button_draw)

    def draw_save_button(self, x_coord, button_color="background"):
        self.click_save = MusicStorage.check_song_in_db("database3.sqlite", self.song_data["song_id"])

        if self.click_save:
            self.save_button = Button(image=MyImage.SAVE_CLICK, command=lambda: self.save_click(), width=18, height=24, bd=0, bg=themes[Main.SETTINGS.theme][button_color], activebackground=themes[Main.SETTINGS.theme][button_color], relief=RIDGE)
        else:
            self.save_button = Button(image=MyImage.SAVE, command=lambda: self.save_click(), width=18, height=24, bd=0, bg=themes[Main.SETTINGS.theme][button_color], activebackground=themes[Main.SETTINGS.theme][button_color], relief=RIDGE)
        self.save_button_draw = self.canvas.create_window(x_coord, self.y, anchor=W, window=self.save_button)

        self.song_bbox = self.canvas.bbox(self.save_button_draw)
        self.song_coords["save_button"] = self.canvas.bbox(self.save_button_draw)

    def draw_more_button(self, x_coord, button_color="background"):
        self.more_button_draw = self.canvas.create_window(x_coord, self.y+1, anchor=W, window=Button(image=MyImage.MORE_INFO, command=lambda: self.more_click(), width=12, height=16, bd=0, bg=themes[Main.SETTINGS.theme][button_color], activebackground=themes[Main.SETTINGS.theme][button_color], relief=RIDGE))

        self.song_bbox = self.canvas.bbox(self.more_button_draw)
        self.song_coords["more_button"] = self.canvas.bbox(self.more_button_draw)

    def draw_name(self, x_coord):
        song_name = self.song_data["name"][:34]+'...' if len(self.song_data["name"]) > 34 else self.song_data["name"]
        song_author = self.song_data["author"][:34]+'...' if len(self.song_data["author"]) > 34 else self.song_data["author"]

        self.name_draw = self.canvas.create_text(x_coord, self.y, text=f"{song_name}  -  ", fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 12", anchor=W)
        self.author_draw = self.canvas.create_text(self.canvas.bbox(self.name_draw)[2], self.y, text=song_author, fill=themes[Main.SETTINGS.theme]["text_second_color"], font="Verdana 12", anchor=W)

        self.song_bbox = self.canvas.bbox(self.author_draw)
        self.song_coords["name"] = self.canvas.bbox(self.author_draw)
