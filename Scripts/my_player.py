# -*- coding: utf-8 -*-

""" For play music """
import pyglet
import pyglet.media as media
from time import sleep as time_sleep


class MyPlayer:
    def __init__(self):
        self.player = pyglet.media.Player()
        self.play_song_while = False

    def new_song(self, song_id):
        self.player.queue(media.load(f"Databases/Download_Music/{song_id}.mp3"))

    def jump(self, time):
        self.player.seek(time)

    def next_song(self):
        self.player.next_source()

    def play(self):
        self.play_song_while = True
        while self.play_song_while:
            self.player.play()
            time_sleep(0.4)
        return

    def pause(self):
        self.player.pause()
        self.play_song_while = False

    def stop(self):
        self.pause()
        self.player.delete()
