# -*- coding: utf-8 -*-

""" For Graphical Interface """
from tkinter import *
from tkinter import filedialog

""" For files """
from shutil import copyfile
from os import path, mkdir, remove

from PIL import Image, ImageTk

""" Main """
from Scripts.main import Main


class LoadBackground:
    def load_background(self):
        def copy_image(img):
            Main.SETTINGS.bg_image = "Background/%s" % img.split("/")[-1]

            if not path.exists("Background"):
                mkdir("Background")

            if not path.exists(Main.SETTINGS.bg_image):
                copyfile(img, Main.SETTINGS.bg_image)

            Main.SETTINGS.change_settings()

            Main.IMAGE_BG = ImageTk.PhotoImage(Image.open(Main.SETTINGS.bg_image).resize((Main.SETTINGS.width, Main.DATA_CANVAS.winfo_reqheight()), Image.ANTIALIAS))

        bg_image = filedialog.askopenfilename(title="Select image", filetypes=(("jpeg files","*.jpg"), ("png files","*.png"), ("all files","*.*")))

        if bg_image:
            copy_image(bg_image)

            self.settings_interface()

    def del_background(self):
        try:
            remove(Main.SETTINGS.bg_image)
        except FileNotFoundError:
            pass

        Main.SETTINGS.bg_image = "None"
        Main.SETTINGS.change_settings()
        self.settings_interface()

        try: del Main.IMAGE_BG
        except: pass
