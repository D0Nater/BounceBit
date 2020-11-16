# -*- coding: utf-8 -*-

""" For Graphical Interface """
from tkinter import *

""" For clear RAM """
from gc import collect as clear_ram

""" For copy text """
from pyperclip import copy as copy_text

""" Other Scripts """
from Scripts.elements import *

""" For news """
from Scripts.news import News

""" For load background """
from Scripts.load_bg import LoadBackground

""" More settings info """
from Scripts.more_settings_interface import MoreSettingsInterface

""" Images """
from Scripts.images import MyImage

""" Main """
from Scripts.main import Main


class SettingsInterface(MoreSettingsInterface, LoadBackground):
    def change_settings(self, setting, new_setting):
        # update settings #
        if setting == "theme":
            # change theme #
            Main.SETTINGS.theme = new_setting

            # update all #
            Main.SONG_LINE_CANVAS["bg"] = themes[Main.SETTINGS.theme]["second_color"]
            Main.MENU_CANVAS["bg"] = themes[Main.SETTINGS.theme]["second_color"]
            Main.DATA_CANVAS["bg"] = themes[Main.SETTINGS.theme]["background"]

            Main.JUST_LINE = Canvas(Main.ROOT, width=Main.SETTINGS.width, height=25, bg=themes[Main.SETTINGS.theme]["second_color"], bd=0, highlightthickness=0)
            Main.JUST_LINE.place(x=0, y=Main.SETTINGS.height-143)

            Main.LOAD_IMAGE.upd_images()
            Main.MENU.update_buttons()
            Main.SONG_LINE.draw_music_line(change_settings=True)

        elif setting == "lang":
            # change language #
            Main.SETTINGS.language = new_setting
            Main.MENU.update_buttons()

        self.settings_interface()

    def del_news_block(self):
        try:
            if self.text_news != None:
                self.text_news.destroy()
                self.text_news = None
        except:
            pass

    def settings_interface(self):
        clear_ram()
        Main.DATA_CANVAS.delete("all")
        Main.SETTINGS_INTERFACE.del_news_block()
        Main.MORE_INFO_INTERFACE.close_song_info()
        Main.PLAYLIST_INTERFACE.close_playlist()

        Main.PAST_SONG["lib_now"] = "Settings"
        Main.LIST_OF_IDS = []

        # delete logo #
        try: del Main.SCREENSAVER
        except: pass

        # Settings #
        self.settings_text = Main.DATA_CANVAS.create_text(15, 19, text=languages["Настройки"][Main.SETTINGS.language], anchor=W, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 13")

        # Save #
        Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.settings_text)[2]+75, 20, window=Button(text=languages["Сохранить"][Main.SETTINGS.language], command=Main.SETTINGS.change_settings, bg=themes[Main.SETTINGS.theme]["background"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=1, width=15))
        
        # Themes #
        self.theme_text = Main.DATA_CANVAS.create_text(15, 65, text=languages["Тема"][Main.SETTINGS.language], anchor=W, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 13")

        self.d_theme = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.theme_text)[2]+20, 66, anchor=W, window=Button(background=themes["dark"]["background"], activebackground=themes["dark"]["second_color"], command=lambda: self.change_settings("theme", "dark"), bd=1, width=2, height=1))
        self.l_theme = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.d_theme)[2]+20, 66, anchor=W, window=Button(background=themes["light"]["background"], activebackground=themes["light"]["second_color"], command=lambda: self.change_settings("theme", "light"), bd=1, width=2, height=1))
        self.p_theme = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.l_theme)[2]+20, 66, anchor=W, window=Button(background=themes["purple"]["background"], activebackground=themes["purple"]["second_color"], command=lambda: self.change_settings("theme", "purple"), bd=1, width=2, height=1))
        self.g_theme = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.p_theme)[2]+20, 66, anchor=W, window=Button(background=themes["green"]["background"], activebackground=themes["green"]["second_color"], command=lambda: self.change_settings("theme", "green"), bd=1, width=2, height=1))

        # Background picture #
        self.bg_text = Main.DATA_CANVAS.create_text(15, 112, text=languages["Фон"][Main.SETTINGS.language], anchor=W, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 13")
        self.bg_button = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.bg_text)[2]+20, 113, anchor=W, window=Button(text=languages["load_img"][Main.SETTINGS.language], command=lambda: self.load_background(), bg=themes[Main.SETTINGS.theme]["background"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=1, width=21))
        self.bg_file = Main.DATA_CANVAS.create_text(Main.DATA_CANVAS.bbox(self.bg_button)[2]+5, 112, text=" - "+Main.SETTINGS.bg_image.split("/")[-1], anchor=W, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 12")

        if Main.SETTINGS.bg_image != "None":
            self.del_bg = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.bg_file)[2]+13, 113, window=Button(image=MyImage.TRASHCAN, width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], command=lambda: self.del_background()), anchor=W)

        # Languages #
        self.lang_text = Main.DATA_CANVAS.create_text(15, 160, text=languages["Язык"][Main.SETTINGS.language], anchor=W, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 13")
        self.ru_lang = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.lang_text)[2]+20, 161, anchor=W, window=Button(text="Русский", width=15, bd=1, bg=themes[Main.SETTINGS.theme]["background"], fg=themes[Main.SETTINGS.theme]["text_color"], command=lambda: self.change_settings("lang", "ru")))
        self.en_lang = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.ru_lang)[2]-1, 161, anchor=W, window=Button(text="English", width=15, bd=1, bg=themes[Main.SETTINGS.theme]["background"], fg=themes[Main.SETTINGS.theme]["text_color"], command=lambda: self.change_settings("lang", "en")))

        # More #
        self.more_text = Main.DATA_CANVAS.create_text(15, 205, text=languages["more"][Main.SETTINGS.language], anchor=W, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 13")
        self.more_button = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.more_text)[2]+12, 207, anchor=W, window=Button(image=MyImage.MORE, width=20, height=20, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], command=lambda: self.draw_more()))

        # News #
        self.news_text = Main.DATA_CANVAS.create_text(135, 240, text=languages["Новости"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 14")

        # Creat block news #
        news = News.read_news()

        self.text_news = Text(bg=themes[Main.SETTINGS.theme]["background"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=1, wrap=WORD, font="Verdana 12")
        self.text_news.insert(END, news[0]+"\n\n") # write date
        self.text_news.insert(END, news[1][Main.SETTINGS.language]) # write news in block
        self.text_news.config(state=DISABLED) # update config
        self.text_news.place(x=15, y=Main.DATA_CANVAS.bbox(self.news_text)[3]+95, width=Main.DATA_CANVAS.winfo_width()/2/2, height=Main.DATA_CANVAS.winfo_height()/2, anchor=NW)

        # Copy Button #
        Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.news_text)[2]+10, 240, window=Button(image=MyImage.COPY, width=19, height=19, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], command=lambda: copy_text(self.text_news.get(1.0, "end-1c"))), anchor=W)

        # Update window #
        Main.ROOT.update()
        Main.DATA_CANVAS.config(scrollregion=Main.DATA_CANVAS.bbox("all"))

        Main.MENU.update_buttons()
