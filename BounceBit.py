# -*- coding: utf-8 -*-

"""
      : READ_ME :
     : BounceBit :     
: Open Source Project :

  ~ Language: Python ~
 ~ Interface: Tkinter ~
~ Media player: Pyglet ~

     - Author:  D0Nater -
- GitHub: github.com/D0Nater -
"""

""" For Interface """
from tkinter import *

""" For icon """
from os import path

""" For parse news """
from threading import Thread
from Scripts.news import News
from Scripts.elements import *

""" For Player """
from Scripts.my_player import MyPlayer

""" For key events """
from Scripts.key_event import KeyEvent

""" For search update program """
from Scripts.update_program import UpdateProgram

""" For load Images """
from Scripts.images import LoadPictures

""" Settings """
from Scripts.settings import Settings

""" Interface """
from Scripts.menu_interface import Menu
from Scripts.window_for_data import WindowForData
from Scripts.song_line import SongLine

""" Main """
from Scripts.main import Main


class BounceBit:
    def __init__(self):
        # Parse News #
        Thread(target=News.parse_new_news).start()

        # Start Program #
        Main.ROOT = Tk()
        Main.ROOT.title("")

        # Settings #
        Main.SETTINGS = Settings("en", "dark") # default settings
        Main.SETTINGS.update_settings() # get settings from database

        # Window settings #
        Main.ROOT.iconbitmap(default=LoadPictures.resource_path(path.join("pictures", "program_icon.ico")))
        Main.ROOT.geometry(f"{Main.SETTINGS.width-50}x{Main.SETTINGS.height-100}+10+10")
        Main.ROOT.minsize(width=180, height=45)
        Main.ROOT.state("zoomed")

        # Player #
        Main.PLAYER = MyPlayer()

        # Draw menu #
        Main.MENU = Menu()
        Main.MENU.draw_menu()
        Main.MENU.update_buttons()

        # Draw main canvas for data #
        Main.WINDOW_FOR_DATA = WindowForData()
        Main.WINDOW_FOR_DATA.drow_data()

        # Draw line for song #
        Main.SONG_LINE = SongLine()

        # Load images #
        Main.LOAD_IMAGE = LoadPictures()
        Main.LOAD_IMAGE.upd_images()
        Main.LOAD_IMAGE.load_bg()

        # Search updates #
        Thread(target=UpdateProgram).start()

        # Keys settings #
        KeyEvent()

        # Start window #
        Main.ROOT.mainloop()


if __name__ == "__main__":
    BounceBit()
