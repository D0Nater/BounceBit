# -*- coding: utf-8 -*-

""" For Graphical Interface """
from tkinter import *

""" For download and play music """
from threading import Thread

""" For files """
from os import path

import requests

""" For copy text """
from pyperclip import copy as copy_text

""" Other Scripts """
from Scripts.elements import *
from Scripts.music_storage import MusicStorage

""" For song manage """
from Scripts.song_manage import SongManage

""" For Player """
from Scripts.my_player import MyPlayer

""" Images """
from Scripts.images import MyImage

""" Main """
from Scripts.main import Main


class Song(SongManage):
    def __init__(self, y, song_num, info):
        self.y = y
        self.song_num = song_num
        self.song_data = [info["name"], info["author"], info["url"], info["song_time"], info["song_id"]]

    # def __del__(self):
    #     pass

    def del_class(self):
        if self.this_class not in Main.LIST_OF_PLAY["classes"]:
            del self.x
            del self.y
            del self.song_num
            del self.song_data

    def draw_name(self):
        song_name = self.song_data[0][:34]+'...' if len(self.song_data[0]) > 34 else self.song_data[0]
        song_author = self.song_data[1][:34]+'...' if len(self.song_data[1]) > 34 else self.song_data[1]

        # Draw song name and author #
        self.name_draw = Main.DATA_CANVAS.create_text(20, self.y, text=f"{song_name}  -  ", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 12")
        self.author_draw = Main.DATA_CANVAS.create_text(Main.DATA_CANVAS.bbox(self.name_draw)[2], self.y, text=song_author, fill=themes[Main.SETTINGS.theme]["text_second_color"], anchor=W, font="Verdana 12")

        self.x = Main.DATA_CANVAS.bbox(self.author_draw)[2]

    def draw_music(self, this_class, lib):
        self.this_class = this_class

        # for buttons #
        click_play = 0
        click_add = MusicStorage.check_song_in_db("database2.sqlite", self.song_data[4])
        click_save = MusicStorage.check_song_in_db("database3.sqlite", self.song_data[4])

        def play_click():
            nonlocal click_play

            if click_play:
                click_play = 0
                Main.PLAYER_SETTINGS["play"] = 0
                self.play_button["image"] = MyImage.PLAY

                Main.PLAYER.pause()

                # update buttons #
                Main.SONG_LINE.draw_music_line()
                Main.MENU.update_buttons()
            else:
                click_play = 1
                Main.PLAYER_SETTINGS["play"] = 1
                self.play_button["image"] = MyImage.PAUSE

                if self.song_data[4] != Main.SONG_PLAY_NOW["song_id"]:
                    # update lists #
                    if Main.LIST_OF_PLAY != Main.LIST_OF_MUSIC:
                        Main.RANDOM_MUSIC_LIST = []
                        Main.LIST_OF_PLAY = Main.LIST_OF_MUSIC.copy()
                        Main.LIST_OF_PLAY["classes"] = list_of_songs_class.copy()

                    Main.PAST_SONG["past_lib"] = lib

                    Thread(target=self.update_music, daemon=True).start()
                else:
                    Thread(target=Main.PLAYER.play, daemon=True).start() # play

                    # update buttons #
                    Main.SONG_LINE.draw_music_line()
                    Main.MENU.update_buttons()

                # update window with more song info #
                if Main.MORE_INFO_INTERFACE.num_of_wins:
                    Main.MORE_INFO_INTERFACE.song_info_draw(Main.PAST_SONG["class"].song_data, Main.MORE_INFO_INTERFACE.searched_data)

        def add_click():
            nonlocal click_add

            if click_add:
                # Delete song #
                click_add = 0
                self.add_button["image"] = MyImage.ADD
                MusicStorage.delete_song("database2.sqlite", self.song_data[4])
            else:
                # Add song #
                click_add = 1
                self.add_button["image"] = MyImage.ADD_CLICK
                MusicStorage.add_song("database2.sqlite", self.song_data)

        def save_click():
            nonlocal click_save

            if click_save:
                # Delete song #
                click_save = 0
                self.save_button["image"] = MyImage.SAVE
                MusicStorage.delete_music(self.song_data[4])
                MusicStorage.delete_song("database3.sqlite", self.song_data[4])
            else:
                # Download song #
                click_save = 1
                self.save_button["image"] = MyImage.SAVE_CLICK
                Thread(target=MusicStorage.download_music, args=(self.song_data[4], self.song_data[2])).start()
                MusicStorage.add_song("database3.sqlite", self.song_data)

        def more_click():
            Main.MORE_INFO_INTERFACE.song_info_draw(self.song_data)

        # button "play" #
        if Main.PLAYER_SETTINGS["play"] and Main.SONG_PLAY_NOW["song_id"] == self.song_data[4]:
            click_play = 1
            self.play_button = Button(image=MyImage.PAUSE, command=lambda: play_click(), width=16, height=23, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE)
        else:
            self.play_button = Button(image=MyImage.PLAY, command=lambda: play_click(), width=16, height=23, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE)
        play_button_draw = Main.DATA_CANVAS.create_window(self.x+25, self.y, anchor=W, window=self.play_button) # draw button

        # button "add" #
        if click_add:
            self.add_button = Button(image=MyImage.ADD_CLICK, command=lambda: add_click(), width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE)
        else:
            self.add_button = Button(image=MyImage.ADD, command=lambda: add_click(), width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE)
        add_button_draw = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(play_button_draw)[2]+13, self.y, anchor=W, window=self.add_button) # draw button

        # button "download" #
        if click_save:
            self.save_button = Button(image=MyImage.SAVE_CLICK, command=lambda: save_click(), width=18, height=24, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE)
        else:
            self.save_button = Button(image=MyImage.SAVE, command=lambda: save_click(), width=18, height=24, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE)
        save_button_draw = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(add_button_draw)[2]+11, self.y, anchor=W, window=self.save_button) # draw button

        # button "more" #
        more_button_draw = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(save_button_draw)[2]+7, self.y+1, anchor=W, window=Button(image=MyImage.MORE_INFO, command=lambda: more_click(), width=12, height=16, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE)) # draw button
