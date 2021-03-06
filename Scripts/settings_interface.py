# -*- coding: utf-8 -*-

""" For copy text """
from pyperclip import copy as copy_text

from Scripts.elements import *
from Scripts.news import News


class DrawThemeButton:
    def __init__(self, x, theme_now):
        self.draw_theme = Main.DATA_CANVAS.create_window(x, 66, anchor=W, window=Button(background=themes[theme_now]["background"], activebackground=themes[theme_now]["second_color"], command=lambda: Main.SETTINGS_INTERFACE.change_settings("theme", theme_now), bd=1, width=2, height=1))

    def get_x(self):
        return Main.DATA_CANVAS.bbox(self.draw_theme)[2]


class SettingsInterface:
    def change_settings(self, setting, new_setting):
        # update settings #
        if setting == "theme":
            # change theme #
            Main.SETTINGS.theme = new_setting

            # update all #
            Main.SONG_LINE_CANVAS["bg"] = themes[Main.SETTINGS.theme]["second_color"]
            Main.MENU_CANVAS["bg"] = themes[Main.SETTINGS.theme]["second_color"]
            Main.DATA_CANVAS["bg"] = themes[Main.SETTINGS.theme]["background"]

            draw_just_lines()

            Main.LOAD_IMAGE.upd_images()
            Main.MENU.update_buttons()
            Main.UPDATE_PROGRAM.update_msg()
            Main.SONG_LINE.draw_music_line(change_settings=True)

        elif setting == "lang":
            # change language #
            Main.SETTINGS.language = new_setting
            Main.MENU.update_buttons()

            Main.UPDATE_PROGRAM.update_msg()

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

        # close all #
        Main.SETTINGS_INTERFACE.del_news_block()
        Main.MORE_INFO_INTERFACE.close_song_info()
        Main.MORE_SETTINGS.close_window()

        Main.PAST_SONG["lib_now"] = "Settings"
        Main.LIST_OF_IDS = []

        # delete logo #
        try: del Main.SCREENSAVER
        except: pass

        # just pixel #
        Main.DATA_CANVAS.create_text(0, 0, text=".", fill=themes[Main.SETTINGS.theme]["background"], anchor=W, font="Verdana 1")

        # Settings #
        self.settings_text = Main.DATA_CANVAS.create_text(15, 19, text=languages["Настройки"][Main.SETTINGS.language], anchor=W, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 13")

        # Save #
        Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.settings_text)[2]+75, 20, window=Button(text=languages["Сохранить"][Main.SETTINGS.language], command=Main.SETTINGS.change_settings, bg=themes[Main.SETTINGS.theme]["background"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=1, width=15))
        
        # Themes #
        self.theme_text = Main.DATA_CANVAS.create_text(15, 65, text=languages["Тема"][Main.SETTINGS.language], anchor=W, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 13")

        # draw all themes #
        x = Main.DATA_CANVAS.bbox(self.theme_text)[2]+20
        for theme_now in themes:
            draw_theme = DrawThemeButton(x, theme_now)
            x = draw_theme.get_x()+17

        # Languages #
        self.lang_text = Main.DATA_CANVAS.create_text(15, 115, text=languages["Язык"][Main.SETTINGS.language], anchor=W, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 13")
        self.ru_lang = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.lang_text)[2]+20, Main.DATA_CANVAS.bbox(self.lang_text)[1]-1, anchor=NW, window=Button(text="Русский", width=15, bd=1, bg=themes[Main.SETTINGS.theme]["background"], fg=themes[Main.SETTINGS.theme]["text_color"], command=lambda: self.change_settings("lang", "ru")))
        self.en_lang = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.ru_lang)[2]-1, Main.DATA_CANVAS.bbox(self.lang_text)[1]-1, anchor=NW, window=Button(text="English", width=15, bd=1, bg=themes[Main.SETTINGS.theme]["background"], fg=themes[Main.SETTINGS.theme]["text_color"], command=lambda: self.change_settings("lang", "en")))

        # More #
        self.more_text = Main.DATA_CANVAS.create_text(15, 160, text=languages["more"][Main.SETTINGS.language], anchor=W, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 13")
        self.more_button = Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.more_text)[2]+12, Main.DATA_CANVAS.bbox(self.more_text)[1]+1, anchor=NW, window=Button(image=MyImage.MORE, width=20, height=20, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], command=lambda: Main.MORE_SETTINGS.draw_more()))

        # News #
        self.news_text = Main.DATA_CANVAS.create_text(135, 210, text=languages["Новости"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 14")

        # Creat block news #
        news = News.read_news()

        self.text_news = Text(bg=themes[Main.SETTINGS.theme]["background"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=1, wrap=WORD, font="Verdana 12")
        self.text_news.insert(END, news[0]+"\n\n"+news[1][Main.SETTINGS.language]) # write date and news in block
        self.text_news.config(state=DISABLED) # update config
        self.text_news.place(x=15, y=Main.DATA_CANVAS.bbox(self.news_text)[3]+95, width=Main.DATA_CANVAS.winfo_width()/2/2, height=Main.DATA_CANVAS.winfo_height()/2, anchor=NW)

        # Copy Button #
        Main.DATA_CANVAS.create_window(Main.DATA_CANVAS.bbox(self.news_text)[2]+10, Main.DATA_CANVAS.bbox(self.news_text)[1], anchor=NW, window=Button(image=MyImage.COPY, width=19, height=19, bd=0, bg=themes[Main.SETTINGS.theme]["background"], activebackground=themes[Main.SETTINGS.theme]["background"], command=lambda: copy_text(self.text_news.get(1.0, "end-1c"))))

        # Update window #
        Main.ROOT.update()
        Main.DATA_CANVAS.config(scrollregion=Main.DATA_CANVAS.bbox("all"))

        Main.MENU.update_buttons()

        draw_just_lines()
