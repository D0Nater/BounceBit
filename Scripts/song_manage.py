# -*- coding: utf-8 -*-

""" For Graphical Interface """
from tkinter import *

""" For download and play music """
from threading import Thread

""" For random song """
from random import choice as rand_choice

""" Other Scripts """
from Scripts.elements import *
from Scripts.music_storage import MusicStorage

""" For Player """
from Scripts.my_player import MyPlayer

""" Images """
from Scripts.images import MyImage

""" Main """
from Scripts.main import Main

""" For encode song id """
from Scripts.settings import encode_text


class SongManage:
    @staticmethod
    def song_url(song_id):
        return "BounceBit/%s/song" % encode_text(song_id)

    def click_play(self):
        def play_song():
            Thread(target=Main.PLAYER.play, daemon=True).start() # play
            Thread(target=Main.SONG_LINE.song_time_thread, daemon=True).start()
            Main.PLAYER_SETTINGS["play"] = 1

        def pause_song():
            Main.PLAYER.pause()
            Main.PLAYER_SETTINGS["play"] = 0

        # update button #
        if Main.PLAYER_SETTINGS["play"]:
            pause_song()
            self.play_button["image"] = MyImage.PLAY
        else:
            play_song()
            self.play_button["image"] = MyImage.PAUSE

        # update past song #
        if Main.PAST_SONG["song_id"] in Main.LIST_OF_IDS:
            list_of_songs_class[Main.LIST_OF_IDS.index(Main.PAST_SONG["song_id"])].draw_music(Main.PAST_SONG["class"], Main.PAST_SONG["past_lib"])

        # update window with more song info #
        if Main.MORE_INFO_INTERFACE.num_of_wins:
            Main.MORE_INFO_INTERFACE.song_info_draw(Main.PAST_SONG["class"].song_data, Main.MORE_INFO_INTERFACE.searched_data)

        Main.JUST_LINE = Canvas(Main.ROOT, width=Main.SETTINGS.width, height=25, bg=themes[Main.SETTINGS.theme]["second_color"], bd=0, highlightthickness=0)
        Main.JUST_LINE.place(x=0, y=Main.SETTINGS.height-143)

        Main.MENU.update_buttons()

    def cycle_song(self):
        if Main.PLAYER_SETTINGS["cycle"]:
            Main.PLAYER_SETTINGS["cycle"] = False
            self.cycle_button["image"] = MyImage.CYCLE
        else:
            Main.PLAYER_SETTINGS["cycle"] = True
            self.cycle_button["image"] = MyImage.CYCLE_CLICK

            Main.PLAYER_SETTINGS["random_song"] = False
            self.rand_song_button["image"] = MyImage.RANDOM_SONG

    def random_song(self):
        if Main.PLAYER_SETTINGS["random_song"]:
            Main.PLAYER_SETTINGS["random_song"] = False
            self.rand_song_button["image"] = MyImage.RANDOM_SONG
        else:
            Main.PLAYER_SETTINGS["random_song"] = True
            self.rand_song_button["image"] = MyImage.RANDOM_SONG_CLICK

            Main.PLAYER_SETTINGS["cycle"] = False
            self.cycle_button["image"] = MyImage.CYCLE

    def update_music(self):
        # new song info #
        Main.SONG_PLAY_NOW = {
            "name": Main.LIST_OF_PLAY["music"][f"song{self.song_num}"]["name"],
            "author": Main.LIST_OF_PLAY["music"][f"song{self.song_num}"]["author"],
            "time": Main.LIST_OF_PLAY["music"][f"song{self.song_num}"]["song_time"],
            "url": Main.LIST_OF_PLAY["music"][f"song{self.song_num}"]["url"],
            "song_id": Main.LIST_OF_PLAY["music"][f"song{self.song_num}"]["song_id"],
            "num": self.song_num
        }

        # update past song #
        if Main.PAST_SONG["song_id"] in Main.LIST_OF_IDS:
            list_of_songs_class[Main.LIST_OF_IDS.index(Main.PAST_SONG["song_id"])].draw_music(Main.PAST_SONG["class"], Main.PAST_SONG["past_lib"])

        # update data #
        Main.PAST_SONG["class"] = Main.LIST_OF_PLAY["classes"][self.song_num]
        Main.PAST_SONG["song_id"] = Main.SONG_PLAY_NOW["song_id"]

        # update new song #
        if Main.PAST_SONG["song_id"] in Main.LIST_OF_IDS:
            list_of_songs_class[Main.LIST_OF_IDS.index(Main.PAST_SONG["song_id"])].draw_music(Main.PAST_SONG["class"], Main.PAST_SONG["past_lib"])

        # update song time #
        Main.SONG_TIME_NOW = "00:00"
        Main.SONG_LINE_CANVAS.delete(self.time_line_now)

        Main.PLAYER.stop()

        # download song #
        Main.SONG_LINE.loading_song()
        try:
            MusicStorage.download_music(self.song_data[4], self.song_data[2])
        except ConnectionError:
            Main.SONG_LINE.loading_song(error="connect_error")
            return

        del Main.PLAYER
        # Player #
        Main.PLAYER = MyPlayer() # just for fix bug XD

        # write new song #
        Main.PLAYER.new_song(Main.SONG_PLAY_NOW["song_id"])

        if Main.PLAYER_SETTINGS["play"]:
            Thread(target=Main.PLAYER.play, daemon=True).start() # play

        # update line #
        Main.SONG_LINE.draw_music_line()
        Main.MENU.update_buttons()

    def play_random_song(self):
        if Main.RANDOM_MUSIC_LIST == []:
            Main.RANDOM_MUSIC_LIST = [num for num in range(Main.LIST_OF_PLAY["music"]["num"])]

        try: Main.RANDOM_MUSIC_LIST.remove(Main.SONG_PLAY_NOW["num"])
        except ValueError: pass

        if Main.RANDOM_MUSIC_LIST == []:
            Main.RANDOM_MUSIC_LIST = [num for num in range(Main.LIST_OF_PLAY["music"]["num"])]

        self.song_num = rand_choice(Main.RANDOM_MUSIC_LIST)

        self.update_music()

    def behind_after_music(self, event):
        # new song num #
        self.song_num = Main.SONG_PLAY_NOW["num"] + (event)

        if self.song_num is -1:
            # play last song #
            self.song_num = Main.LIST_OF_PLAY["music"]["num"] - 1
        elif self.song_num > Main.LIST_OF_PLAY["music"]["num"] - 1:
            # play first song #
            self.song_num = 0

        self.update_music()
