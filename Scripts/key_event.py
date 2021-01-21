# -*- coding: utf-8 -*-

""" Main """
from Scripts.main import Main


class KeyEvent:
    def __init__(self):
        self.is_unbind_keys = False

        Main.ROOT.bind("<space>", self.play_pause)

        Main.ROOT.bind("<Up>", self.up_volume)
        Main.ROOT.bind("<Down>", self.down_volume)

        Main.ROOT.bind("<Left>", self.behind_music)
        Main.ROOT.bind("<Right>", self.after_music)

        Main.ROOT.bind("<Shift_L>", self.more_info)
        Main.ROOT.bind("<Shift_R>", self.more_info)

    def bind_keys(self, event):
        self.is_unbind_keys = False
        Main.DATA_CANVAS.focus_set()

        Main.ROOT.unbind("<Button-1>")

    def unbind_keys(self, event):
        self.is_unbind_keys = True

        Main.ROOT.bind("<Button-1>", self.bind_keys)

    def play_pause(self, event):
        if self.is_unbind_keys:
            return

        if Main.SONG_PLAY_NOW["song_id"]:
            Main.SONG_LINE.click_play()

    def more_info(self, event):
        if self.is_unbind_keys:
            return

        if Main.PAST_SONG["class"] and Main.PAST_SONG["lib_now"] != "Settings":
            if Main.MORE_INFO_INTERFACE.num_of_wins:
                Main.MORE_INFO_INTERFACE.close_song_info()
            else:
                Main.MORE_INFO_INTERFACE.song_info_draw(Main.PAST_SONG["class"].song_data)

    def up_volume(self, event):
        if self.is_unbind_keys:
            return

        new_volume = Main.SETTINGS.volume + 0.02

        if new_volume > 1.0:
            new_volume = 1.0

        Main.MORE_SETTINGS.set_volume(new_volume*100)

    def down_volume(self, event):
        if self.is_unbind_keys:
            return

        new_volume = Main.SETTINGS.volume - 0.02

        if new_volume < 0:
            new_volume = 0

        Main.MORE_SETTINGS.set_volume(new_volume*100)

    def behind_music(self, event):
        if self.is_unbind_keys:
            return

        if Main.SONG_PLAY_NOW["song_id"]:
            Main.SONG_LINE.behind_after_music(-1)

    def after_music(self, event):
        if self.is_unbind_keys:
            return

        if Main.SONG_PLAY_NOW["song_id"]:
            Main.SONG_LINE.behind_after_music(1)

    def other_keys(self, event):
        print(event)
