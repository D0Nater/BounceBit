# -*- coding: utf-8 -*-

""" For Graphical Interface """
from tkinter import *

""" Other Scripts """
from Scripts.elements import *
from Scripts.parse_music import ParseMusic

""" Images """
from Scripts.images import MyImage

""" Main """
from Scripts.main import Main


class MoreInfoInterface:
    """ Draw window with more song info """

    def __init__(self):
        self.num_of_wins = 0

    def close_song_info(self):
        if self.num_of_wins:
            try:
                Main.SCROLL_WIN = True

                self.song_info_canvas.delete("all")
                self.song_info_canvas.destroy()
                self.song_text_draw.destroy()

                del self.song_info_canvas
                del self.song_text_draw

                self.num_of_wins -= 1
            except AttributeError:
                pass

    def song_info_draw(self, data):
        # Delete past window #
        self.close_song_info()
        Main.PLAYLIST_INTERFACE.close_playlist()

        # Create new window #
        self.num_of_wins += 1

        # Draw window #
        self.song_info_canvas = Canvas(Main.ROOT, width=Main.DATA_CANVAS.winfo_width()/2/2+50, height=Main.DATA_CANVAS.winfo_height()-40, bg=themes[Main.SETTINGS.theme]["second_color"], highlightthickness=0)
        self.song_info_canvas.place(x=Main.SETTINGS.width/2-50, y=Main.DATA_CANVAS.bbox("all")[1]+90, anchor=N)

        # button "close" #
        self.song_info_canvas.create_window(Main.DATA_CANVAS.winfo_width()/2/2+45, 6, window=Button(image=MyImage.CLOSE, width=17, height=17, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: self.close_song_info()), anchor=NE)

        # Song name #
        self.song_name_draw = self.song_info_canvas.create_text(40, 40, text=languages["Трек"][Main.SETTINGS.language]+":", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")
        self.song_name_draw = self.song_info_canvas.create_text(self.song_info_canvas.bbox(self.song_name_draw)[2]+15, 41, text=data[0], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 12")

        # Artist #
        self.song_artist_draw = self.song_info_canvas.create_text(40, 80, text=languages["Артист"][Main.SETTINGS.language]+":", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")
        self.song_info_canvas.create_text(self.song_info_canvas.bbox(self.song_artist_draw)[2]+11, self.song_info_canvas.bbox(self.song_artist_draw)[1]+3, text=data[1], fill="cyan", anchor=NW, font="Verdana 12")

        # Song size #
        self.song_size_draw = self.song_info_canvas.create_text(40, 110, text=languages["Размер"][Main.SETTINGS.language]+":", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        # Song duration #
        self.song_duration_draw = self.song_info_canvas.create_text(40, 140, text=languages["Длительность"][Main.SETTINGS.language]+":", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        Main.ROOT.update()

        # Button for add to playlist #
        self.song_info_canvas.create_window(self.song_info_canvas.bbox(self.song_name_draw)[2]+15, 41, window=Button(image=MyImage.NEW_PLAYLIST, width=27, height=27, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], command=lambda: print("add song")), anchor=W)

        # Search data #
        self.song_data = ParseMusic.more_song_info(data[5])

        # Draw Song size #
        self.song_info_canvas.create_text(self.song_info_canvas.bbox(self.song_size_draw)[2]+11, self.song_info_canvas.bbox(self.song_size_draw)[1]+3, text=self.song_data["size"]+" mb", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=NW, font="Verdana 12")

        # Draw Song duration #
        self.song_info_canvas.create_text(self.song_info_canvas.bbox(self.song_duration_draw)[2]+11, self.song_info_canvas.bbox(self.song_duration_draw)[1]+2, text=data[3], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=NW, font="Verdana 12")

        # Draw Song text #
        self.song_info_canvas.create_text(40, 180, text=languages["Текст"][Main.SETTINGS.language]+":", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 13")

        # Draw Block for text #
        self.song_text_draw = Text(bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], bd=1, wrap=WORD, font="Verdana 12") # create text block
        self.song_text_draw.insert(END, self.song_data["text"]) # write text in block
        self.song_text_draw.config(state=DISABLED) # update config
        self.song_text_draw.place(x=Main.SETTINGS.width/2-49, y=300, width=self.song_info_canvas.winfo_width()-74, height=self.song_info_canvas.winfo_height()/2, anchor=N)

        Main.SCROLL_WIN = False
