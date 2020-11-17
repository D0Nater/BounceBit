# -*- coding: utf-8 -*-

""" For Graphical Interface """
from tkinter import *

""" Other Scripts """
from Scripts.elements import *
from Scripts.playlist_storage import PlaylistStorage

""" Images """
from Scripts.images import MyImage

""" Main """
from Scripts.main import Main


class MoreSettingsInterface:
    def __init__(self):
        self.num_of_wins = 0

    def close_window(self):
        try:
            Main.SCROLL_WIN = True

            self.more_settings_canvas.delete("all")
            self.more_settings_canvas.destroy()

            del self.more_settings_canvas

            self.close_key_assignmet()

            self.num_of_wins -= 1
        except AttributeError:
            pass

    def close_key_assignmet(self):
        try:
            if self.key_assignmet_test != None:
                self.key_assignmet_test.destroy()
                self.key_assignmet_test = None

                self.more_settings_canvas.delete(self.key_event_more)
                self.key_event_more = self.more_settings_canvas.create_window(self.more_settings_canvas.bbox(self.key_event)[2]+10, 76, window=Button(image=MyImage.MORE, width=20, height=20, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: self.draw_key_assignmet()), anchor=W)
        except:
            pass

    def draw_key_assignmet(self):
        # change button #
        self.more_settings_canvas.delete(self.key_event_more)
        self.key_event_more = self.more_settings_canvas.create_window(self.more_settings_canvas.bbox(self.key_event)[2]+10, 77, window=Button(image=MyImage.CLOSE, width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: self.close_key_assignmet()), anchor=W)

        self.key_assignmet_test = Text(bg=themes[Main.SETTINGS.theme]["background"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=1, wrap=WORD, font="Verdana 12")
        self.key_assignmet_test.insert(END, languages["key_assignmet"][Main.SETTINGS.language]) # write data
        self.key_assignmet_test.config(state=DISABLED) # update config
        self.key_assignmet_test.place(x=Main.SETTINGS.width/2+15, y=Main.DATA_CANVAS.bbox("all")[1]+150, width=self.more_settings_canvas.winfo_width()/2/2+20, height=self.more_settings_canvas.winfo_height()/2, anchor=NE)

    def draw_more(self):
        # Delete past window #
        self.close_window()

        # Create new window #
        self.num_of_wins += 1

        # Draw window #
        self.more_settings_canvas = Canvas(Main.ROOT, width=Main.DATA_CANVAS.winfo_width()/1.5, height=Main.DATA_CANVAS.winfo_height()-40, bg=themes[Main.SETTINGS.theme]["second_color"], highlightthickness=0)
        self.more_settings_canvas.place(x=Main.SETTINGS.width/2, y=Main.DATA_CANVAS.bbox("all")[1]+90, anchor=N)

        # Lib name #
        self.lib_name_draw = self.more_settings_canvas.create_text(40, 30, text=languages["more"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        # Key assignment #
        self.key_event = self.more_settings_canvas.create_text(40, 75, text=languages["key_e"][Main.SETTINGS.language], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")
        self.key_event_more = self.more_settings_canvas.create_window(self.more_settings_canvas.bbox(self.key_event)[2]+10, 76, window=Button(image=MyImage.MORE, width=20, height=20, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: self.draw_key_assignmet()), anchor=W)

        # button 'close' #
        self.more_settings_canvas.create_window(Main.DATA_CANVAS.winfo_width()/1.5-4, 6, window=Button(image=MyImage.CLOSE, width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: self.close_window()), anchor=NE)

        Main.ROOT.update()

        Main.SCROLL_WIN = False
