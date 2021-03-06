# -*- coding: utf-8 -*-

""" For random song """
from random import choice as rand_choice

""" For encode song id """
from Scripts.settings import encode_text

from Scripts.elements import *
from Scripts.my_player import MyPlayer
from Scripts.music_storage import MusicStorage


class SongManage:
    @staticmethod
    def song_url(song_id):
        return "BounceBit/%s/song" % encode_text(song_id)

    def click_play(self):
        def play_song():
            Main.PLAYER_SETTINGS["play"] = 1
            Thread(target=Main.PLAYER.play, daemon=True).start() # play
            Thread(target=Main.SONG_LINE.song_time_thread, daemon=True).start()

        def pause_song():
            Main.PLAYER_SETTINGS["play"] = 0
            Main.PLAYER.pause()

        # update button #
        if Main.PLAYER_SETTINGS["play"]:
            pause_song()
            self.play_button["image"] = MyImage.PLAY
        else:
            play_song()
            self.play_button["image"] = MyImage.PAUSE

        # update past song #
        if Main.PAST_SONG["song_id"] in Main.LIST_OF_IDS:
            upd_class = list_of_songs_class[Main.LIST_OF_IDS.index(Main.PAST_SONG["song_id"])]
            upd_class.draw_play_button(upd_class.song_coords["play_button"][0])

        # update window with more song info #
        if Main.MORE_INFO_INTERFACE.num_of_wins:
            Main.MORE_INFO_INTERFACE.song_info_draw(Main.PAST_SONG["class"].song_data, Main.MORE_INFO_INTERFACE.searched_data)

        draw_just_lines()

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
            upd_class = list_of_songs_class[Main.LIST_OF_IDS.index(Main.PAST_SONG["song_id"])]
            upd_class.draw_play_button(upd_class.song_coords["play_button"][0])

        # update data #
        Main.PAST_SONG["class"] = Main.LIST_OF_PLAY["classes"][self.song_num]
        Main.PAST_SONG["song_id"] = Main.SONG_PLAY_NOW["song_id"]

        # update new song #
        if Main.PAST_SONG["song_id"] in Main.LIST_OF_IDS:
            upd_class = list_of_songs_class[Main.LIST_OF_IDS.index(Main.PAST_SONG["song_id"])]
            upd_class.draw_play_button(upd_class.song_coords["play_button"][0])

        # update song time #
        Main.SONG_TIME_NOW = "00:00"
        Main.SONG_LINE_CANVAS.delete(Main.SONG_LINE.time_line_now)

        Main.PLAYER.stop()

        # download song #
        Main.SONG_LINE.loading_song()
        try:
            MusicStorage.download_music(Main.PAST_SONG["class"].song_data["song_id"], Main.PAST_SONG["class"].song_data["url"])
        except ConnectionError:
            Main.SONG_LINE.loading_song(error="connect_error")
            return

        del Main.PLAYER
        # Player #
        Main.PLAYER = MyPlayer() # just for fix bug XD

        # write new song #
        try: Main.PLAYER.new_song(Main.SONG_PLAY_NOW["song_id"])
        except EOFError: Main.SONG_LINE.loading_song(error="song_error")

        if Main.PLAYER_SETTINGS["play"]:
            Thread(target=Main.PLAYER.play, daemon=True).start() # play

        # update buttons #
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

        Thread(target=self.update_music, daemon=True).start()

    def behind_after_music(self, event):
        # new song num #
        self.song_num = Main.SONG_PLAY_NOW["num"] + (event)

        if self.song_num is -1:
            # play last song #
            self.song_num = Main.LIST_OF_PLAY["music"]["num"] - 1
        elif self.song_num > Main.LIST_OF_PLAY["music"]["num"] - 1:
            # play first song #
            self.song_num = 0

        Thread(target=self.update_music, daemon=True).start()
