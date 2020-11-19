# -*- coding: utf-8 -*-

""" For Interface """
from tkinter import *
from tkinter import messagebox

""" For Parse """
import lxml.html

""" Other """
from Scripts.elements import *
from Scripts.parse_music import parse_data

""" Images """
from Scripts.images import MyImage

""" Main """
from Scripts.main import Main


class UpdateProgram:
    def __init__(self):
        self.draw_update = False

    def search_upd(self):
        try:
            tree = parse_data("https://github.com/D0Nater/BounceBit/blob/main/__init__.py")

            self.version = tree.xpath(f'//*[@id="LC5"]/span/text()')[0].split(': ')[-1]

            if self.version != VERSION:
                self.draw_update = True

                self.create_text_upd()

        except ConnectionError:
            pass

    def create_text_upd(self):
        if self.draw_update:
            # update text #
            self.update_text_draw = Main.MENU_CANVAS.create_text(Main.MENU_CANVAS.bbox(Main.VERSION_DRAW)[2]+20, 25, text=languages["update_text"][Main.SETTINGS.language]+" \""+self.version+"\" !", anchor=W, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 11")

            # button 'download' #
            self.download_button = Main.MENU_CANVAS.create_window(Main.MENU_CANVAS.bbox(self.update_text_draw)[2]+15, Main.MENU_CANVAS.bbox(self.update_text_draw)[3]-10, anchor=W, window=Button(image=MyImage.DOWNLOAD_UPD, width=18, height=20, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE, \
                command=lambda: self.download_upd()))

            # button 'close' #
            self.close_button = Main.MENU_CANVAS.create_window(Main.MENU_CANVAS.bbox(self.download_button)[2]+12, Main.MENU_CANVAS.bbox(self.update_text_draw)[3]-7, anchor=W, window=Button(image=MyImage.CLOSE, width=16, height=16, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE, \
                command=lambda: self.close_upd()))

    def download_upd(self):
        messagebox.showinfo("BounceBit Update", "Download function is testing!")

    def update_msg(self):
        if self.draw_update:
            self.close_upd()
            self.draw_update = True
            self.create_text_upd()

    def close_upd(self):
        Main.MENU_CANVAS.delete(self.update_text_draw)
        Main.MENU_CANVAS.delete(self.download_button)
        Main.MENU_CANVAS.delete(self.close_button)

        self.draw_update = False
