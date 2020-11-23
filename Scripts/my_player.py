# -*- coding: utf-8 -*-

""" For play music """
import pyglet.media as media
from time import time as time_time
from time import sleep as time_sleep

""" Main """
from Scripts.main import Main


class MyPlayer:
    def __init__(self):
        self.player = media.Player()
        self.play_song_while = False

        self.set_volume(Main.SETTINGS.volume)

        self._time = 0.0
        self._systime = None

    def new_song(self, song_id):
        self.player.queue(media.load(f"Databases/Download_Music/{song_id}.mp3"))

    def set_volume(self, num):
        self.player.volume = num

    def get_song_time(self):
        return self.get_time()

    def set_time(self, new_time):
        self.reset()
        self._time = new_time
        self.player.seek(new_time)

    def next_song(self):
        self.player.next_source()

    def play(self):
        self.play_song_while = True
        self._systime = time_time()
        while self.play_song_while:
            self.player.play()
            time_sleep(0.4)
        return

    def pause(self):
        self.player.pause()
        self.play_song_while = False

        self._time = self.get_time()
        self._systime = None

    def stop(self):
        self.pause()
        self.player.delete()

    def reset(self):
        """ Reset the timer to 0 """
        self._time = 0.0
        if self._systime is not None:
            self._systime = time_time()

    def get_time(self):
        """ Get the elapsed time """
        if self._systime is None:
            return self._time

        return time_time() - self._systime + self._time
