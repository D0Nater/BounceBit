# -*- coding: utf-8 -*-

""" Main """
from Scripts.main import Main


class KeyEvent:
    def __init__(self):
        Main.ROOT.bind('<space>', self.play_pause)

        Main.ROOT.bind('<Left>', self.behind_music)
        Main.ROOT.bind('<Right>', self.after_music)

        Main.ROOT.bind('<Shift_L>', self.more_info)
        Main.ROOT.bind('<Shift_R>', self.more_info)

        Main.ROOT.bind('<Key>', self.print_event)

    def play_pause(self, event):
        if Main.SONG_PLAY_NOW["song_id"]:
            Main.SONG_LINE.click_play()

    def more_info(self, event):
        if Main.PAST_SONG["class"] and Main.PAST_SONG["lib_now"] != "Settings":
            if Main.MORE_INFO_INTERFACE.num_of_wins:
                Main.MORE_INFO_INTERFACE.close_song_info()
            else:
                Main.MORE_INFO_INTERFACE.song_info_draw(Main.PAST_SONG["class"].song_data)

    def behind_music(self, event):
        if Main.SONG_PLAY_NOW["song_id"]:
            Main.SONG_LINE.behind_after_music(-1)

    def after_music(self, event):
        if Main.SONG_PLAY_NOW["song_id"]:
            Main.SONG_LINE.behind_after_music(1)

    def print_event(self, event):
        print(event)
