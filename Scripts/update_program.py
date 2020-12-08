# -*- coding: utf-8 -*-

""" For Parse """
import json
import requests
import lxml.html

from Scripts.elements import *
from Scripts.parse_music import parse_data


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
            self.update_text_draw = Main.MENU_CANVAS.create_text(Main.MENU_CANVAS.bbox(Main.VERSION_DRAW)[2]+20, 27, text=languages["update_text"][Main.SETTINGS.language]+" \""+self.version+"\" !", anchor=W, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 11")

            # button 'download' #
            self.download_button = Main.MENU_CANVAS.create_window(Main.MENU_CANVAS.bbox(self.update_text_draw)[2]+15, Main.MENU_CANVAS.bbox(self.update_text_draw)[3]-12, anchor=W, window=Button(image=MyImage.DOWNLOAD_UPD, width=18, height=20, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE, \
                command=lambda: Thread(target=self.download_upd).start()))

            # button 'close' #
            self.close_button = Main.MENU_CANVAS.create_window(Main.MENU_CANVAS.bbox(self.download_button)[2]+12, Main.MENU_CANVAS.bbox(self.update_text_draw)[3]-10, anchor=W, window=Button(image=MyImage.CLOSE, width=16, height=16, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE, \
                command=lambda: self.close_msg()))

    def get_download_url(self):
        # parse site #
        tree = parse_data("https://github.com/D0Nater/BounceBit/blob/main/DownloadProgram")

        # parse and decode text #
        return tree.xpath(f'//*[@id="LC1"]/text()')[0]

    def download_upd(self):

        self.__google_file__ = self.get_download_url()

        print(self.__google_file__)

        with open(f"BounceBitInstall_{self.version}.exe", "wb") as f:
            response = requests.get(self.__google_file__, stream=True)

            for data in response.iter_content(chunk_size=4096):
                f.write(data)

        self.close_msg()

    def update_msg(self):
        if self.draw_update:
            self.close_msg()
            self.draw_update = True
            self.create_text_upd()

    def close_msg(self):
        Main.MENU_CANVAS.delete(self.update_text_draw)
        Main.MENU_CANVAS.delete(self.download_button)
        Main.MENU_CANVAS.delete(self.close_button)

        self.draw_update = False
