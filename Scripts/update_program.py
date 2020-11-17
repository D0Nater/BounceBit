# -*- coding: utf-8 -*-

""" For Interface """
from tkinter import *

""" For Parse """
import lxml.html

""" Other """
from Scripts.elements import *
from Scripts.parse_music import parse_data

""" Main """
from Scripts.main import Main


class UpdateProgram:
    def __init__(self):
        tree = parse_data("https://github.com/D0Nater/BounceBit/blob/main/__init__.py")

        self.version = tree.xpath(f'//*[@id="LC5"]/span/text()')[0].split(': ')[-1]

        if self.version != VERSION:
            self.create_window_upd()

    def create_window_upd(self):
        Main.MENU_CANVAS.create_text(Main.MENU_CANVAS.bbox(Main.VERSION_DRAW)[2]+20, 25, text=languages["update_text"][Main.SETTINGS.language]+" \""+self.version+"\" !", anchor=W, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 11")
