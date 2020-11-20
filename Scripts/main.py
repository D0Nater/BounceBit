# -*- coding: utf-8 -*-


class Main:
    LIST_OF_IDS = []
    RANDOM_MUSIC_LIST = []
    SONG_TIME_NOW = "00:00"
    LIST_OF_PLAY = {"classes": []}
    PLAYER_SETTINGS = {"play": 0, "cycle": False, "random_song": False}
    PAST_SONG = {"class": None, "song_id": None, "past_lib": None, "lib_now": None}
    SONG_PLAY_NOW = {"name": "", "author": "", "time": "", "url": "", "song_id": None, "num": 0, "loaded": False}
