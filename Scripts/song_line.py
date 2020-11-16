# -*- coding: utf-8 -*-

""" For Graphical Interface """
from tkinter import *

""" For download and listen music """
from threading import Thread

""" For files """
from os import path

""" For clear RAM """
from gc import collect as clear_ram

""" For load music on screen """
import time
from time import sleep as time_sleep

""" Other Scripts """
from Scripts.elements import *
from Scripts.music import Music

""" Images """
from Scripts.images import MyImage

""" Main """
from Scripts.main import Main


class SongLine:
    def __init__(self):
        Main.SONG_LINE_CANVAS = Canvas(Main.ROOT, width=Main.SETTINGS.width, height=200, bg=themes[Main.SETTINGS.theme]["second_color"], bd=0, highlightthickness=0)
        Main.SONG_LINE_CANVAS.pack()

        self.song_id_now = ""
        self.time_line_now = None

    def song_time_thread(self):
        global song_time_now, num_for_time_line_now

        song_id_now = Main.SONG_PLAY_NOW["song_id"]

        min_song, sec_song = [int(i) for i in song_time_now.split(":")] # default 00:00
        song_time_official = [int(i) for i in Main.SONG_PLAY_NOW["time"].split(":")] # song time
        song_time_official_str = time.strftime("%M:%S", time.gmtime(60*song_time_official[0] + song_time_official[1]+1)) # int to string

        self.time_line_bbox = Main.SONG_LINE_CANVAS.bbox(self.time_line)

        num_for_time_line = 160 / (60*song_time_official[0] + song_time_official[1]+1)

        if song_time_now == "00:00":
            # if play new song #
            num_for_time_line_now = 0 # default time line

        while Main.SONG_PLAY_NOW["play"]:
            song_time_now = time.strftime("%M:%S", time.gmtime(60*min_song + sec_song))
            sec_song += 1

            num_for_time_line_now += num_for_time_line

            # after song #
            if (song_time_official_str == song_time_now) and (song_id_now == Main.SONG_PLAY_NOW["song_id"]):
                self.behind_after_music(1)
                return

            elif (song_time_official_str != song_time_now) and (song_id_now == Main.SONG_PLAY_NOW["song_id"]):
                Main.SONG_LINE_CANVAS.delete(self.time)
                Main.SONG_LINE_CANVAS.delete(self.time_line_now)

                self.time = Main.SONG_LINE_CANVAS.create_text(self.x_time, 42, text=song_time_now, fill=themes[Main.SETTINGS.theme]["text_second_color"], anchor=W, font="Verdana 10")
                self.time_line_now = Main.SONG_LINE_CANVAS.create_line(Main.SONG_LINE_CANVAS.bbox(self.time)[2]+8, Main.SONG_LINE_CANVAS.bbox(self.time)[3]-7, self.time_line_bbox[0]+num_for_time_line_now+5, Main.SONG_LINE_CANVAS.bbox(self.time)[3]-7, width=4, fill="black")

            else:
                return

            time_sleep(1)

    def behind_after_music(self, event):
            # new song num #
            song_num = Main.SONG_PLAY_NOW["num"] + (event)

            if song_num is -1:
                # play last song #
                song_num = Main.LIST_OF_PLAY["music"]["num"] - 1
            elif song_num > Main.LIST_OF_PLAY["music"]["num"] - 1:
                # play first song #
                song_num = 0

            # new song info #
            Main.SONG_PLAY_NOW = {
                "play": Main.SONG_PLAY_NOW["play"],
                "name": Main.LIST_OF_PLAY["music"][f"song{song_num}"]["name"],
                "author": Main.LIST_OF_PLAY["music"][f"song{song_num}"]["author"],
                "time": Main.LIST_OF_PLAY["music"][f"song{song_num}"]["song_time"],
                "url": Main.LIST_OF_PLAY["music"][f"song{song_num}"]["url"],
                "song_id": Main.LIST_OF_PLAY["music"][f"song{song_num}"]["song_id"],
                "num": song_num
            }
            # update past song #
            if Main.PAST_SONG["song_id"] in Main.LIST_OF_IDS:
                Main.LIST_OF_PLAY["classes"][Main.LIST_OF_IDS.index(Main.PAST_SONG["song_id"])].draw_music(Main.PAST_SONG["class"], Main.PAST_SONG["past_lib"])

            # update data #
            Main.PAST_SONG["class"] = Main.LIST_OF_PLAY["classes"][song_num]
            Main.PAST_SONG["song_id"] = Main.SONG_PLAY_NOW["song_id"]

            # update new song #
            if Main.PAST_SONG["song_id"] in Main.LIST_OF_IDS:
                Main.LIST_OF_PLAY["classes"][Main.LIST_OF_IDS.index(Main.PAST_SONG["song_id"])].draw_music(Main.PAST_SONG["class"], Main.PAST_SONG["past_lib"])

            # update song time #
            globals()["song_time_now"] = "00:00"
            Main.SONG_LINE_CANVAS.delete(self.time_line_now)

            # stop music #
            Main.PLAYER.stop()

            if not path.exists("Databases/Download_Music/%s.mp3" % Main.SONG_PLAY_NOW["song_id"]):
                # download song #
                Main.SONG_LINE.loading_song()
                Music.download_music(Main.SONG_PLAY_NOW["song_id"], Main.SONG_PLAY_NOW["url"])

            # write new song #
            Main.PLAYER.new_song(Main.SONG_PLAY_NOW["song_id"])

            # play new song #
            Main.PLAYER.next_song()

            if Main.SONG_PLAY_NOW["play"]:
                Thread(target=Main.PLAYER.play, daemon=True).start() # play

            # update line #
            Main.SONG_LINE.draw_music_line()
            Main.MENU.update_buttons()

    def loading_song(self):
        Main.SONG_LINE_CANVAS.delete("all")
        Main.SONG_LINE_CANVAS.create_text(30, 40, text=languages["Загрузка"][Main.SETTINGS.language]+"...", fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 12")

        Main.JUST_LINE = Canvas(Main.ROOT, width=Main.SETTINGS.width, height=25, bg=themes[Main.SETTINGS.theme]["second_color"], bd=0, highlightthickness=0)
        Main.JUST_LINE.place(x=0, y=Main.SETTINGS.height-143)

        Main.ROOT.update()

    def click_play(self):
        # update button #
        if Main.SONG_PLAY_NOW["play"]:
            Main.PLAYER.pause()
            Main.SONG_PLAY_NOW["play"] = 0
            self.play_button["image"] = MyImage.PLAY
        else:
            Thread(target=Main.PLAYER.play, daemon=True).start() # play
            Main.SONG_PLAY_NOW["play"] = 1
            self.play_button["image"] = MyImage.PAUSE
            Thread(target=Main.SONG_LINE.song_time_thread, daemon=True).start()

        # update past song #
        if Main.PAST_SONG["song_id"] in Main.LIST_OF_IDS:
            Main.PAST_SONG["class"].draw_music(Main.PAST_SONG["class"], Main.PAST_SONG["past_lib"])

        Main.MENU.update_buttons()

    def draw_music_line(self, change_settings=False):
        clear_ram()
        Main.SONG_LINE_CANVAS.delete("all")

        if Main.SONG_PLAY_NOW["song_id"] is None:
            return

        # Song info #
        self.song_name = Main.SONG_LINE_CANVAS.create_text(30, 32, text=Main.SONG_PLAY_NOW["name"], fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 12")
        self.song_author = Main.SONG_LINE_CANVAS.create_text(30, 52, text=Main.SONG_PLAY_NOW["author"], fill=themes[Main.SETTINGS.theme]["text_second_color"], anchor=W, font="Verdana 12")

        # time now #
        self.x_time = Main.SONG_LINE_CANVAS.bbox(self.song_name)[2]+23 if Main.SONG_LINE_CANVAS.bbox(self.song_name)[2] > Main.SONG_LINE_CANVAS.bbox(self.song_author)[2] else Main.SONG_LINE_CANVAS.bbox(self.song_author)[2]+23
        self.time = Main.SONG_LINE_CANVAS.create_text(self.x_time, 42, text=song_time_now, fill=themes[Main.SETTINGS.theme]["text_second_color"], anchor=W, font="Verdana 10")

        # time line #
        self.time_line = Main.SONG_LINE_CANVAS.create_line(Main.SONG_LINE_CANVAS.bbox(self.time)[2]+8, Main.SONG_LINE_CANVAS.bbox(self.time)[3]-7, Main.SONG_LINE_CANVAS.bbox(self.time)[2]+168, Main.SONG_LINE_CANVAS.bbox(self.time)[3]-7, width=4, fill=themes[Main.SETTINGS.theme]["text_second_color"])
        
        try:
            self.time_line_now = Main.SONG_LINE_CANVAS.create_line(Main.SONG_LINE_CANVAS.bbox(self.time)[2]+8, Main.SONG_LINE_CANVAS.bbox(self.time)[3]-7, self.time_line_bbox[0]+globals()["num_for_time_line_now"]+8, Main.SONG_LINE_CANVAS.bbox(self.time)[3]-7, width=4, fill="black")
        except:
            self.time_line_now = Main.SONG_LINE_CANVAS.create_line(Main.SONG_LINE_CANVAS.bbox(self.time_line)[2], Main.SONG_LINE_CANVAS.bbox(self.time_line)[3]-7, 0, Main.SONG_LINE_CANVAS.bbox(self.time_line)[3]-7, width=4, fill="black")

        if self.song_id_now != Main.SONG_PLAY_NOW["song_id"]:
            Main.SONG_LINE_CANVAS.delete(self.time_line_now)

        self.song_id_now = Main.SONG_PLAY_NOW["song_id"]

        # song time #
        self.song_time = Main.SONG_LINE_CANVAS.create_text(Main.SONG_LINE_CANVAS.bbox(self.time_line)[2]+8, Main.SONG_LINE_CANVAS.bbox(self.time_line)[1]+4, text=Main.SONG_PLAY_NOW["time"], fill=themes[Main.SETTINGS.theme]["text_second_color"], anchor=W, font="Verdana 10")

        # Button "behind song" #
        self.behind_song_button = Main.SONG_LINE_CANVAS.create_window(Main.SONG_LINE_CANVAS.bbox(self.song_time)[2]+30, 42, window=Button(image=MyImage.BEHIND_SONG, command=lambda: self.behind_after_music(-1), width=17, height=19, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE))

        # Button "play/stop" #
        if Main.SONG_PLAY_NOW["play"]:
            self.play_button = Button(image=MyImage.PAUSE, command=lambda: self.click_play(), width=14, height=23, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE)
        else:
            self.play_button = Button(image=MyImage.PLAY, command=lambda: self.click_play(), width=14, height=23, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE)
        self.play_button_draw = Main.SONG_LINE_CANVAS.create_window(Main.SONG_LINE_CANVAS.bbox(self.behind_song_button)[2]+20, 43, window=self.play_button)

        # Button "after song" #
        self.after_song_button = Main.SONG_LINE_CANVAS.create_window(Main.SONG_LINE_CANVAS.bbox(self.play_button_draw)[2]+18, 42, window=Button(image=MyImage.AFTER_SONG, command=lambda: self.behind_after_music(1), width=17, height=19, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE))

        self.more_info = Main.SONG_LINE_CANVAS.create_window(Main.SONG_LINE_CANVAS.bbox(self.after_song_button)[2]+15, 43, window=Button(image=MyImage.MORE_INFO, command=lambda: Main.MORE_INFO_INTERFACE.song_info_draw(Main.PAST_SONG["class"].song_data), width=17, height=19, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE))

        Main.JUST_LINE = Canvas(Main.ROOT, width=Main.SETTINGS.width, height=25, bg=themes[Main.SETTINGS.theme]["second_color"], bd=0, highlightthickness=0)
        Main.JUST_LINE.place(x=0, y=Main.SETTINGS.height-143)

        if Main.SONG_PLAY_NOW["play"] and not change_settings:
            Thread(target=Main.SONG_LINE.song_time_thread, daemon=True).start()
