# -*- coding: utf-8 -*-

import sys
from os import path
from codecs import open as codecs_open

from tkinter import *

from threading import Thread

import time
from time import sleep as time_sleep

from json import loads as json_loads

from gc import collect as clear_ram

from Scripts.images import MyImage

from Scripts.main import Main


def draw_just_lines():
    Main.JUST_LINE = Canvas(Main.ROOT, width=Main.SETTINGS.width, height=25, bg=themes[Main.SETTINGS.theme]["second_color"], bd=0, highlightthickness=0)
    Main.JUST_LINE.place(x=0, y=Main.SETTINGS.height-143)
    Main.JUST_LINE.create_line(0, 0, Main.SETTINGS.width, 0, width=1, fill="grey9")


def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return path.join(sys._MEIPASS, relative)
    return path.join(relative)


def clear_list_of_songs():
    global list_of_songs_class
    for song in list_of_songs_class:
        if song not in Main.LIST_OF_PLAY["classes"] and song is not Main.PAST_SONG["class"]:
            song.del_class()
            del song
    clear_ram()
    list_of_songs_class.clear()


""" Elements for main program """
VERSION = "0.5.5"
AUTHOR = "D0Nater"
GITHUB = "https://github.com/D0Nater/BounceBit/"
LICENSE = "https://github.com/D0Nater/BounceBit/blob/main/LICENSE"
PROGRAM_NAME = "Bounce Bit"

list_of_music = {}

list_of_songs_class = []

json_folder = "JsonFiles"

file = open(resource_path(path.join(json_folder, "themes.json")))
themes = json_loads(file.read())
file.close()

file = codecs_open(resource_path(path.join(json_folder, "languages.json")), "r", "utf_8_sig")
languages = json_loads(file.read())
file.close()
