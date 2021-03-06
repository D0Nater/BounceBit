# -*- coding: utf-8 -*-

from Scripts.elements import *
from Scripts.song_manage import SongManage
from Scripts.music_storage import MusicStorage
from Scripts.music_interface import MusicInterface


class SongLine(SongManage, MusicInterface):
    def __init__(self):
        Main.SONG_LINE_CANVAS = Canvas(Main.ROOT, width=Main.SETTINGS.width, height=200, bg=themes[Main.SETTINGS.theme]["second_color"], bd=0, highlightthickness=0)
        Main.SONG_LINE_CANVAS.pack()

        self.song_id_now = ""
        self.time_line_now = None

    def song_time_thread(self):
        song_id_now = Main.SONG_PLAY_NOW["song_id"]

        self.song_duration = [int(i) for i in Main.SONG_PLAY_NOW["time"].split(":")] # song time
        self.sec_song_duration = (60*self.song_duration[0] + self.song_duration[1]+1)

        self.time_line_bbox = Main.SONG_LINE_CANVAS.bbox(self.time_line)

        self.num_for_time_line = 160 / self.sec_song_duration

        if Main.SONG_TIME_NOW == "00:00":
            # if play new song #
            self.num_for_time_line_now = 0 # default time line

        while Main.PLAYER_SETTINGS["play"] and song_id_now == Main.SONG_PLAY_NOW["song_id"]:
            # after song #
            if int(Main.PLAYER.get_time()) >= self.sec_song_duration:
                if Main.PLAYER_SETTINGS["cycle"]:
                    self.behind_after_music(0)
                    return
                elif Main.PLAYER_SETTINGS["random_song"]:
                    self.play_random_song()
                    return
                self.behind_after_music(1)
                return

            elif int(Main.PLAYER.get_time()) <= self.sec_song_duration:
                self.update_time()

            time_sleep(1)

    def loading_song(self, error=None):
        Main.SONG_LINE_CANVAS.delete("all")

        text = languages[error][Main.SETTINGS.language] if error else languages["Загрузка"][Main.SETTINGS.language]+"..."

        Main.SONG_LINE_CANVAS.create_text(30, 40, text=text, fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 12")

        draw_just_lines()

        Main.ROOT.update()

    def update_time(self):
        song_time_now = int(Main.PLAYER.get_time())

        Main.SONG_TIME_NOW = time.strftime("%M:%S", time.gmtime(song_time_now))
        self.num_for_time_line_now = self.num_for_time_line*song_time_now

        Main.SONG_LINE_CANVAS.delete(self.time)
        Main.SONG_LINE_CANVAS.delete(self.time_line_now)

        self.time = Main.SONG_LINE_CANVAS.create_text(self.x_time, 42, text=Main.SONG_TIME_NOW, fill=themes[Main.SETTINGS.theme]["text_second_color"], anchor=W, font="Verdana 10")
        self.time_line_now = Main.SONG_LINE_CANVAS.create_line(Main.SONG_LINE_CANVAS.bbox(self.time)[2]+8, Main.SONG_LINE_CANVAS.bbox(self.time)[3]-7, self.time_line_bbox[0]+self.num_for_time_line_now+5, Main.SONG_LINE_CANVAS.bbox(self.time)[3]-7, width=4, fill="black")

        Main.SONG_LINE_CANVAS.tag_bind(self.time_line_now, "<Motion>", self.draw_time_under_mouse)
        Main.SONG_LINE_CANVAS.tag_bind(self.time_line_now, "<Leave>", self.del_time_under_mouse)
        Main.SONG_LINE_CANVAS.tag_bind(self.time_line_now, "<Button-1>", self.set_time)

    def set_time(self, event):
        Main.PLAYER.set_time(float(int(self.set_song_sec)))
        self.update_time()

    def draw_time_under_mouse(self, event):
        self.cursor_x = event.x - self.start_song_line
        self.set_song_sec = (self.cursor_x / self.num_for_time_line) - 3

        if self.set_song_sec > self.sec_song_duration:
            self.song_sec = time.strftime("%M:%S", time.gmtime(self.sec_song_duration-1))
        elif self.set_song_sec < 0.0:
            self.song_sec = "00:00"
        else:
            self.song_sec = time.strftime("%M:%S", time.gmtime(self.set_song_sec))

        self.del_time_under_mouse(None)

        self.time_under_cursor = Main.SONG_LINE_CANVAS.create_text(event.x, 29, text=self.song_sec, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 10")

    def del_time_under_mouse(self, event):
        try: Main.SONG_LINE_CANVAS.delete(self.time_under_cursor)
        except: pass

    def draw_music_line(self, change_settings=False):
        clear_ram()
        Main.SONG_LINE_CANVAS.delete("all")

        if Main.SONG_PLAY_NOW["song_id"] is None:
            return

        song_name = Main.SONG_PLAY_NOW["name"][:40]+'...' if len(Main.SONG_PLAY_NOW["name"]) > 40 else Main.SONG_PLAY_NOW["name"]
        song_author = Main.SONG_PLAY_NOW["author"][:40]+'...' if len(Main.SONG_PLAY_NOW["author"]) > 40 else Main.SONG_PLAY_NOW["author"]

        # Song info #
        self.song_name = Main.SONG_LINE_CANVAS.create_text(30, 32, text=song_name, fill=themes[Main.SETTINGS.theme]["text_color"], anchor=W, font="Verdana 12")
        self.song_author = Main.SONG_LINE_CANVAS.create_text(30, 52, text=song_author, fill=themes[Main.SETTINGS.theme]["text_second_color"], anchor=W, font="Verdana 12")

        # time now #
        self.x_time = Main.SONG_LINE_CANVAS.bbox(self.song_name)[2]+23 if Main.SONG_LINE_CANVAS.bbox(self.song_name)[2] > Main.SONG_LINE_CANVAS.bbox(self.song_author)[2] else Main.SONG_LINE_CANVAS.bbox(self.song_author)[2]+23
        self.time = Main.SONG_LINE_CANVAS.create_text(self.x_time, 42, text=Main.SONG_TIME_NOW, fill=themes[Main.SETTINGS.theme]["text_second_color"], anchor=W, font="Verdana 10")

        # time line #
        self.time_line = Main.SONG_LINE_CANVAS.create_line(Main.SONG_LINE_CANVAS.bbox(self.time)[2]+8, Main.SONG_LINE_CANVAS.bbox(self.time)[3]-7, Main.SONG_LINE_CANVAS.bbox(self.time)[2]+167, Main.SONG_LINE_CANVAS.bbox(self.time)[3]-7, width=4, fill=themes[Main.SETTINGS.theme]["text_second_color"])
        
        try:
            self.time_line_now = Main.SONG_LINE_CANVAS.create_line(Main.SONG_LINE_CANVAS.bbox(self.time)[2]+8, Main.SONG_LINE_CANVAS.bbox(self.time)[3]-7, self.time_line_bbox[0]+self.num_for_time_line_now+5, Main.SONG_LINE_CANVAS.bbox(self.time)[3]-7, width=4, fill="black")
        except:
            self.time_line_now = Main.SONG_LINE_CANVAS.create_line(Main.SONG_LINE_CANVAS.bbox(self.time_line)[2], Main.SONG_LINE_CANVAS.bbox(self.time_line)[3]-7, 0, Main.SONG_LINE_CANVAS.bbox(self.time_line)[3]-7, width=4, fill="black")

        self.start_song_line = Main.SONG_LINE_CANVAS.bbox(self.time_line)[0]

        Main.SONG_LINE_CANVAS.tag_bind(self.time_line, "<Motion>", self.draw_time_under_mouse)
        Main.SONG_LINE_CANVAS.tag_bind(self.time_line, "<Leave>", self.del_time_under_mouse)
        Main.SONG_LINE_CANVAS.tag_bind(self.time_line, "<Button-1>", self.set_time)

        Main.SONG_LINE_CANVAS.tag_bind(self.time_line_now, "<Motion>", self.draw_time_under_mouse)
        Main.SONG_LINE_CANVAS.tag_bind(self.time_line_now, "<Leave>", self.del_time_under_mouse)
        Main.SONG_LINE_CANVAS.tag_bind(self.time_line_now, "<Button-1>", self.set_time)

        if self.song_id_now != Main.SONG_PLAY_NOW["song_id"]:
            Main.SONG_LINE_CANVAS.delete(self.time_line_now)

        self.song_id_now = Main.SONG_PLAY_NOW["song_id"]

        # song time #
        self.song_time = Main.SONG_LINE_CANVAS.create_text(Main.SONG_LINE_CANVAS.bbox(self.time_line)[2]+7, Main.SONG_LINE_CANVAS.bbox(self.time_line)[1]+4, text=Main.SONG_PLAY_NOW["time"], fill=themes[Main.SETTINGS.theme]["text_second_color"], anchor=W, font="Verdana 10")

        # Button "behind song" #
        self.behind_song_button = Main.SONG_LINE_CANVAS.create_window(Main.SONG_LINE_CANVAS.bbox(self.song_time)[2]+15, Main.SONG_LINE_CANVAS.bbox(self.song_time)[1]+8, anchor=W, window=Button(image=MyImage.BEHIND_SONG, command=lambda: self.behind_after_music(-1), width=15, height=18, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE))

        # Button "play/stop" #
        if Main.PLAYER_SETTINGS["play"]:
            self.play_button = Button(image=MyImage.PAUSE, command=lambda: self.click_play(), width=16, height=23, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE)
        else:
            self.play_button = Button(image=MyImage.PLAY, command=lambda: self.click_play(), width=16, height=23, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE)
        self.play_button_draw = Main.SONG_LINE_CANVAS.create_window(Main.SONG_LINE_CANVAS.bbox(self.behind_song_button)[2]+8, Main.SONG_LINE_CANVAS.bbox(self.song_time)[1]+8, anchor=W, window=self.play_button)

        # Button "after song" #
        self.after_song_button = Main.SONG_LINE_CANVAS.create_window(Main.SONG_LINE_CANVAS.bbox(self.play_button_draw)[2]+9, Main.SONG_LINE_CANVAS.bbox(self.song_time)[1]+8, anchor=W, window=Button(image=MyImage.AFTER_SONG, command=lambda: self.behind_after_music(1), width=15, height=18, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE))

        # Button "cycle" #
        if Main.PLAYER_SETTINGS["cycle"]:
            self.cycle_button = Button(image=MyImage.CYCLE_CLICK, command=lambda: self.cycle_song(), width=18, height=18, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE)
        else:
            self.cycle_button = Button(image=MyImage.CYCLE, command=lambda: self.cycle_song(), width=18, height=18, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE)
        self.cycle_button_draw = Main.SONG_LINE_CANVAS.create_window(Main.SONG_LINE_CANVAS.bbox(self.after_song_button)[2]+13, Main.SONG_LINE_CANVAS.bbox(self.song_time)[1]+10, anchor=W, window=self.cycle_button)

        # Button "random song" #
        if Main.PLAYER_SETTINGS["random_song"]:
            self.rand_song_button = Button(image=MyImage.RANDOM_SONG_CLICK, command=lambda: self.random_song(), width=18, height=18, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE)
        else:
            self.rand_song_button = Button(image=MyImage.RANDOM_SONG, command=lambda: self.random_song(), width=18, height=18, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE)
        self.rand_song_button_draw = Main.SONG_LINE_CANVAS.create_window(Main.SONG_LINE_CANVAS.bbox(self.cycle_button_draw)[2]+9, Main.SONG_LINE_CANVAS.bbox(self.song_time)[1]+9, anchor=W, window=self.rand_song_button)

        # Button "more music" #
        self.more_music_button = Main.SONG_LINE_CANVAS.create_window(Main.SONG_LINE_CANVAS.bbox(self.rand_song_button_draw)[2]+9, Main.SONG_LINE_CANVAS.bbox(self.song_time)[1]+8, anchor=W, window=Button(image=MyImage.MORE_MUSIC, command=lambda: self.music_interface("Сейчас_играет", Main.LIST_OF_PLAY), width=20, height=18, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE))

        # Button "more info" #
        self.more_info_button = Main.SONG_LINE_CANVAS.create_window(Main.SONG_LINE_CANVAS.bbox(self.more_music_button)[2]+7, Main.SONG_LINE_CANVAS.bbox(self.song_time)[1]+8, anchor=W, window=Button(image=MyImage.MORE_INFO, command=lambda: (Main.MORE_INFO_INTERFACE.song_info_draw(Main.PAST_SONG["class"].song_data) if Main.PAST_SONG["lib_now"] != "Settings" else None), width=17, height=19, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE))

        draw_just_lines()

        if Main.PLAYER_SETTINGS["play"] and not change_settings:
            Thread(target=Main.SONG_LINE.song_time_thread, daemon=True).start()
