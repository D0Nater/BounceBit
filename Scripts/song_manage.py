# -*- coding: utf-8 -*-

""" For download and play music """
from threading import Thread

""" For clear RAM """
from gc import collect as clear_ram

""" For load music on screen """
import time
from time import sleep as time_sleep

""" Other Scripts """
from Scripts.elements import *
from Scripts.music_storage import MusicStorage

""" For Player """
from Scripts.my_player import MyPlayer

""" Main """
from Scripts.main import Main


class SongManage:
    def play_song(self):
        Thread(target=Main.PLAYER.play, daemon=True).start() # play
        Thread(target=Main.SONG_LINE.song_time_thread, daemon=True).start()
        Main.SONG_PLAY_NOW["play"] = 1

    def pause_song(self):
        Main.PLAYER.pause()
        Main.SONG_PLAY_NOW["play"] = 0

    def behind_after_music(self, event):
        # new song num #
        song_num = Main.SONG_PLAY_NOW["num"] + (event)

        if song_num is -1:
            # play last song #
            song_num = Main.LIST_OF_PLAY["music"]["num"] - 1
        elif song_num > Main.LIST_OF_PLAY["music"]["num"] - 1:
            # play first song #
            song_num = 0

        # new song info #
        Main.SONG_PLAY_NOW = {
            "play": Main.SONG_PLAY_NOW["play"],
            "name": Main.LIST_OF_PLAY["music"][f"song{song_num}"]["name"],
            "author": Main.LIST_OF_PLAY["music"][f"song{song_num}"]["author"],
            "time": Main.LIST_OF_PLAY["music"][f"song{song_num}"]["song_time"],
            "url": Main.LIST_OF_PLAY["music"][f"song{song_num}"]["url"],
            "song_id": Main.LIST_OF_PLAY["music"][f"song{song_num}"]["song_id"],
            "num": song_num
        }
        # update past song #
        if Main.PAST_SONG["song_id"] in Main.LIST_OF_IDS:
            list_of_songs_class[Main.LIST_OF_IDS.index(Main.PAST_SONG["song_id"])].draw_music(Main.PAST_SONG["class"], Main.PAST_SONG["past_lib"])

        # update data #
        Main.PAST_SONG["class"] = Main.LIST_OF_PLAY["classes"][song_num]
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
        MusicStorage.download_music(Main.SONG_PLAY_NOW["song_id"], Main.SONG_PLAY_NOW["url"])

        del Main.PLAYER
        # Player #
        Main.PLAYER = MyPlayer() # just for fix bug XD

        # write new song #
        Main.PLAYER.new_song(Main.SONG_PLAY_NOW["song_id"])

        if Main.SONG_PLAY_NOW["play"]:
            Thread(target=Main.PLAYER.play, daemon=True).start() # play

        # update line #
        Main.SONG_LINE.draw_music_line()
        Main.MENU.update_buttons()
