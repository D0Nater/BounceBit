# -*- coding: utf-8 -*-

""" For load images """
import sys
from PIL import Image, ImageTk

""" For files """
from os import path

""" Main """
from Scripts.main import Main


class MyImage:
    pass


class LoadPictures:
    def upd_images(self):
        self.folder = ("pictures/Light/" if Main.SETTINGS.theme == "light" else "pictures")

        MyImage.PLAY = self.load_picture("play_button.png")
        MyImage.PAUSE = self.load_picture("pause_button.png")

        MyImage.ADD = self.load_picture("add_button.png")
        MyImage.ADD_CLICK = self.load_picture("add_button_click.png")

        MyImage.SAVE = self.load_picture("save_button.png")
        MyImage.SAVE_CLICK = self.load_picture("save_button_click.png")

        MyImage.BEHIND_SONG = self.load_picture("behind_song_button.png")
        MyImage.AFTER_SONG = self.load_picture("after_song_button.png")

        MyImage.MORE = self.load_picture("more_button.png")
        MyImage.MORE_INFO = self.load_picture("more_music_button.png")

        MyImage.CYCLE = self.load_picture("cycle_button.png")
        MyImage.CYCLE_CLICK = self.load_picture("cycle_button_click.png")

        MyImage.SEARCH = self.load_picture("search_button.png")
        MyImage.NEW_PLAYLIST = self.load_picture("new_playlist_button.png")

        MyImage.OK = self.load_picture("ok_button.png")
        MyImage.CLOSE = self.load_picture("close_button.png")

        MyImage.COPY = self.load_picture("copy_button.png")
        MyImage.TRASHCAN = self.load_picture("trashcan_button.png")

        MyImage.EDIT = self.load_picture("edit_button.png")
        MyImage.UPDATE = self.load_picture("update_button.png")

        MyImage.DOWNLOAD_UPD = self.load_picture("download_upd_button.png")

    @staticmethod
    def resource_path(relative):
        if hasattr(sys, "_MEIPASS"):
            return path.join(sys._MEIPASS, relative)
        return path.join(relative)

    @staticmethod
    def load_bg():
        if Main.SETTINGS.bg_image != "None":
            if path.exists(Main.SETTINGS.bg_image):
                Main.IMAGE_BG = ImageTk.PhotoImage(Image.open(Main.SETTINGS.bg_image).resize((Main.SETTINGS.width, Main.DATA_CANVAS.winfo_reqheight()), Image.ANTIALIAS))

    def load_picture(self, file):
        file = LoadPictures.resource_path(path.join(self.folder, file))
        return ImageTk.PhotoImage(Image.open(file))
