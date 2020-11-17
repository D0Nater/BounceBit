# -*- coding: utf-8 -*-

""" For databases """
import sqlite3

""" For music in playlists """
import json

""" For clear RAM """
from gc import collect as clear_ram

""" For encode/decode db4 """
from Scripts.settings import encode_text, decode_text

from Scripts.music_storage import error_correction


class PlaylistStorage:
    def check_playlist_in_db(db_name, playlist_name):
        """ Check playlist in database """
        error_correction()

        conn = sqlite3.connect(f"Databases/{db_name}")
        cursor = conn.cursor()

        answ = 0 if (cursor.execute("SELECT * FROM user_playlists WHERE name=?", (encode_text(playlist_name),))).fetchone() is None else 1

        conn.close()
        return answ

    def get_playlists(db_name):
        error_correction()

        conn = sqlite3.connect(f"Databases/{db_name}")
        cursor = conn.cursor()

        playlists = []

        for playlist_name in cursor.execute("SELECT name FROM user_playlists ORDER BY music"):
            playlists.append(decode_text(playlist_name[0]))

        conn.close()
        return playlists

    def get_music(db_name, playlist_name):
        error_correction()

        conn = sqlite3.connect(f"Databases/{db_name}")
        cursor = conn.cursor()

        music_data = decode_text(cursor.execute("SELECT music FROM user_playlists WHERE name=?", (encode_text(playlist_name),)).fetchone()[0])

        conn.close()
        return json.loads(music_data)

    def add_playlist(db_name, playlist_name, music_data={"music_num":0}):
        error_correction()

        conn = sqlite3.connect(f"Databases/{db_name}")
        cursor = conn.cursor()

        cursor.execute("INSERT INTO user_playlists VALUES (?,?)", (encode_text(playlist_name), encode_text(json.dumps(music_data))))

        conn.commit()
        conn.close()
        clear_ram()

    def delete_playlist(db_name, playlist_name):
        error_correction()

        conn = sqlite3.connect(f"Databases/{db_name}")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM user_playlists WHERE name=?", (encode_text(playlist_name),))

        conn.commit()

        conn.close()
        clear_ram()
