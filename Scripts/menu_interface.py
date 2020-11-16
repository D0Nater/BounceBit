# -*- coding: utf-8 -*-

""" For Interface """
from tkinter import *

""" For take Data """
from Scripts.music import Music

""" Interfaces """
from Scripts.music_interface import MusicInterface
from Scripts.settings_interface import SettingsInterface

""" Other """
from Scripts.elements import *

""" Main """
from Scripts.main import Main


class Menu(MusicInterface):
    def __init__(self):
        Main.SETTINGS_INTERFACE = SettingsInterface()

    def draw_menu(self):
        Main.MENU_CANVAS = Canvas(Main.ROOT, width=Main.SETTINGS.width, height=77, bg=themes[Main.SETTINGS.theme]["second_color"], highlightthickness=0)
        Main.MENU_CANVAS.create_text(10, 25, text=PROGRAM_NAME, fill="red", anchor=W, font="Aharoni 20") # program name
        Main.MENU_CANVAS.create_text(145, 27, text=f"v{VERSION}", anchor=W, fill="red") # version
        Main.MENU_CANVAS.pack()

    def update_buttons(self):
        self.download_music_button = Button(text=languages["Загруженное"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=1, width=25, \
            command=lambda: self.music_interface("Загруженное", Music.read_music("database3.sqlite", "load_error"))).place(x=-1, y=53)

        self.selected_music_button = Button(text=languages["Избранное"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=1, width=25, \
            command=lambda: self.music_interface("Избранное", Music.read_music("database2.sqlite", "add_error"))).place(x=181, y=53)

        self.recommended_music_button = Button(text=languages["Рекомендации"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=1, width=25, \
            command=lambda: self.music_interface("Рекомендации", None)).place(x=363, y=53)

        self.settings_button = Button(text=languages["Настройки"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=1, width=25, \
            command=lambda: Main.SETTINGS_INTERFACE.settings_interface()).place(x=544, y=53)
