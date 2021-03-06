# -*- coding: utf-8 -*-

from Scripts.elements import *
from Scripts.music_storage import MusicStorage
from Scripts.music_interface import MusicInterface


class Menu(MusicInterface):
    def draw_menu(self):
        Main.MENU_CANVAS = Canvas(Main.ROOT, width=Main.SETTINGS.width, height=70, bg=themes[Main.SETTINGS.theme]["second_color"], highlightthickness=1, highlightbackground="grey9")
        Main.PROGRAM_NAME_DRAW = Main.MENU_CANVAS.create_text(10, 28, text=PROGRAM_NAME, fill="red", anchor=W, font="Aharoni 20") # program name
        Main.VERSION_DRAW = Main.MENU_CANVAS.create_text(Main.MENU_CANVAS.bbox(Main.PROGRAM_NAME_DRAW)[2]+3, 30, text=f"v{VERSION}", fill="red", anchor=W) # version
        Main.MENU_CANVAS.pack()

    def update_buttons(self):
        self.download_music_button = Button(text=languages["Загруженное"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=1, width=25, \
            command=lambda: self.music_interface("Загруженное", MusicStorage.read_music("database3.sqlite", "load_error"))).place(x=-1, y=48)

        self.selected_music_button = Button(text=languages["Избранное"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=1, width=25, \
            command=lambda: self.music_interface("Избранное", MusicStorage.read_music("database2.sqlite", "add_error"))).place(x=181, y=48)

        self.recommended_music_button = Button(text=languages["Рекомендации"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=1, width=25, \
            command=lambda: self.music_interface("Рекомендации 1", None)).place(x=363, y=48)

        self.settings_button = Button(text=languages["Настройки"][Main.SETTINGS.language], bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=1, width=25, \
            command=lambda: Main.SETTINGS_INTERFACE.settings_interface()).place(x=544, y=48)
