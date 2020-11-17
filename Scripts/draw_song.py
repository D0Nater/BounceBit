# -*- coding: utf-8 -*-

""" For Graphical Interface """
from tkinter import *

""" For download and play music """
from threading import Thread

""" For files """
from os import path

""" For copy text """
from pyperclip import copy as copy_text

""" Other Scripts """
from Scripts.elements import *
from Scripts.music_storage import MusicStorage

""" Images """
from Scripts.images import MyImage

""" Main """
from Scripts.main import Main


class Song:
    def __init__(self, x, y, num, info):
        self.x = x
        self.y = y
        self.num = num
        self.song_data = [info["name"], info["author"], info["url"], info["song_time"], info["song_id"], info["data_key"]]

    # def __del__(self):
    #     pass

    def del_class(self):
        if self.this_class not in Main.LIST_OF_PLAY["classes"]:
            del self.x
            del self.y
            del self.num
            del self.song_data

    def draw_music(self, this_class, lib):
        self.this_class = this_class

        # for buttons #
        click_play = 0
        click_add = MusicStorage.check_song_in_db("database2.sqlite", self.song_data[4])
        click_save = MusicStorage.check_song_in_db("database3.sqlite", self.song_data[4])

        def play_click(button):
            nonlocal click_play

            if click_play:
                Main.PLAYER.pause()
                click_play = 0
                button["image"] = MyImage.PLAY
            else:
                if self.song_data[4] != Main.SONG_PLAY_NOW["song_id"]:
                    # download song #
                    Main.SONG_LINE.loading_song()
                    MusicStorage.download_music(self.song_data[4], self.song_data[2])

                    Main.PLAYER.stop()
                    Main.SONG_TIME_NOW = "00:00"
                    Main.PLAYER.new_song(self.song_data[4])

                    if Main.SONG_PLAY_NOW["song_id"] is not None:
                        Main.PLAYER.next_song()

                    # update past song #
                    if Main.PAST_SONG["class"] is not None:
                        Main.SONG_PLAY_NOW["play"] = 0
                        Main.PAST_SONG["class"].draw_music(Main.PAST_SONG["class"], Main.PAST_SONG["lib_now"])

                    if Main.LIST_OF_PLAY != Main.LIST_OF_MUSIC:
                        Main.LIST_OF_PLAY = Main.LIST_OF_MUSIC.copy()
                        Main.LIST_OF_PLAY["classes"] = list_of_songs_class

                    Main.PAST_SONG["song_id"] = self.song_data[4]
                    Main.PAST_SONG["class"] = this_class
                    Main.PAST_SONG["past_lib"] = lib

                Thread(target=Main.PLAYER.play, daemon=True).start() # play

                click_play = 1
                button["image"] = MyImage.PAUSE

            Main.SONG_PLAY_NOW = {"play": click_play, "name": self.song_data[0], "author": self.song_data[1], "time": self.song_data[3], "url": self.song_data[2], "song_id": self.song_data[4], "num": self.num}
            Main.SONG_LINE.draw_music_line()

        def add_click(button):
            nonlocal click_add

            if click_add:
                # Del song #
                MusicStorage.delete_song("database2.sqlite", self.song_data[4])
                button["image"] = MyImage.ADD
                click_add = 0
            else:
                # Add song #
                MusicStorage.add_song("database2.sqlite", self.song_data)
                button["image"] = MyImage.ADD_CLICK
                click_add = 1

        def save_click(button):
            nonlocal click_save

            if click_save:
                # Del song #
                MusicStorage.delete_music(self.song_data[4])
                MusicStorage.delete_song("database3.sqlite", self.song_data[4])
                button["image"] = MyImage.SAVE
                click_save = 0
            else:
                # Download song #
                Thread(target=MusicStorage.download_music, args=(self.song_data[4], self.song_data[2])).start()
                MusicStorage.add_song("database3.sqlite", self.song_data)
                button["image"] = MyImage.SAVE_CLICK
                click_save = 1

        def more_click():
            Main.MORE_INFO_INTERFACE.song_info_draw(self.song_data)

        # button "play" #
        if Main.SONG_PLAY_NOW["play"] and Main.SONG_PLAY_NOW["song_id"] == self.song_data[4]:
            click_play = 1
            play_button = Button(image=MyImage.PAUSE, command=lambda: play_click(play_button), width=14, height=23, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE)
        else:
            play_button = Button(image=MyImage.PLAY, command=lambda: play_click(play_button), width=14, height=23, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE)
        play_button_draw = Main.DATA_CANVAS.create_window(self.x, self.y, window=play_button) # draw button

        # button "add" #
        if click_add:
            add_button = Button(image=MyImage.ADD_CLICK, command=lambda: add_click(add_button), width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE)
        else:
            add_button = Button(image=MyImage.ADD, command=lambda: add_click(add_button), width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE)
        add_button_draw = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(play_button_draw)[2]+35, self.y, window=add_button) # draw button

        # button "download" #
        if click_save:
            save_button = Button(image=MyImage.SAVE_CLICK, command=lambda: save_click(save_button), width=18, height=24, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE)
        else:
            save_button = Button(image=MyImage.SAVE, command=lambda: save_click(save_button), width=18, height=24, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE)
        save_button_draw = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(add_button_draw)[2]+22, self.y, window=save_button) # draw button

        # button "more" #
        more_button_draw = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(save_button_draw)[2]+16, self.y+1, window=Button(image=MyImage.MORE_INFO, command=lambda: more_click(), width=12, height=16, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], relief=RIDGE)) # draw button
