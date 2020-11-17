# -*- coding: utf-8 -*-

""" For databases """
import sqlite3

""" For music in playlists """
import json

""" For files """
from os import path, mkdir, remove

""" For clear RAM """
from gc import collect as clear_ram

""" For download music """
import requests
from mutagen.easyid3 import EasyID3

""" For encode/decode db4 """
from Scripts.settings import encode_text, decode_text


def error_correction():
    """
    If file "database2.sqlite" or "database3.sqlite" is damaged,
    music are reset and new ones are created
    """
    if not path.exists("Databases"):
        mkdir("Databases")

    def check_db(db_name):

        conn = sqlite3.connect(f"Databases/{db_name}")
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM user_music WHERE name=?", (encode_text("test_name"),)).fetchone()
        except sqlite3.DatabaseError:
            conn.close()
            remove(f"Databases/{db_name}")
            conn = sqlite3.connect(f"Databases/{db_name}")
            cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM user_playlists WHERE name=?", (encode_text("test_name"),)).fetchone()
        except sqlite3.DatabaseError:
            conn.close()
            remove(f"Databases/{db_name}")
            conn = sqlite3.connect(f"Databases/{db_name}")
            cursor = conn.cursor()

        try: cursor.execute("CREATE TABLE user_music (name, author, url, song_time, num, song_id, data_key)")
        except: pass

        try: cursor.execute("CREATE TABLE user_playlists (name, music)")
        except: pass

        conn.commit()
        conn.close()

    check_db("database2.sqlite") # added music & playlists
    check_db("database3.sqlite") # downloaded music


class MusicStorage:
    def download_music(song_id, url):
        if not path.exists("Databases/Download_Music"):
            mkdir("Databases/Download_Music")

        if path.exists(f"Databases/Download_Music/{song_id}.mp3"):
            return

        with open(f"Databases/Download_Music/{song_id}.mp3", "wb") as f:
            response = requests.get(requests.get(f"https://zaycev.net{url}").json()["url"], stream=True)
            total_length = response.headers.get("content-length")

            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)

        # music params #
        audio = EasyID3(f"Databases/Download_Music/{song_id}.mp3")
        audio["title"] = u""
        audio["artist"] = u""
        audio["album"] = u"BounceBit"
        audio["composer"] = u""
        audio.save()
        return

    def delete_music(song_id):
        if path.exists(f"Databases/Download_Music/{song_id}.mp3"):
            remove(f"Databases/Download_Music/{song_id}.mp3")

    def read_music(db_name, error):
        error_correction()

        conn = sqlite3.connect(f"Databases/{db_name}")
        cursor = conn.cursor()

        json_text = {"music": {"num": 0}, "error": None}

        music_list = []
        for i in cursor.execute("SELECT * FROM user_music ORDER BY song_time"):
            music_list.append(i[4])
        music_list = sorted(music_list)

        # read db #
        for num in range(0, cursor.execute("SELECT count(*) FROM user_music ORDER BY song_time").fetchone()[0]):
            song_data = cursor.execute("SELECT * FROM user_music WHERE num=?", (music_list[-num-1],)).fetchone()
            song_data = {"name": decode_text(song_data[0]), "author": decode_text(song_data[1]), "url": decode_text(song_data[2]), "song_time": decode_text(song_data[3]), "song_id": decode_text(song_data[5]), "data_key": decode_text(song_data[6])}
            json_text["music"][f"song{num}"] = song_data
            json_text["music"]["num"] += 1

        if json_text["music"]["num"] is 0:
            json_text["error"] = error

        conn.close()
        return json_text

    def check_song_in_db(db_name, song_id):
        """ Check song in database """
        error_correction()

        conn = sqlite3.connect(f"Databases/{db_name}")
        cursor = conn.cursor()

        answ = 0 if (cursor.execute("SELECT * FROM user_music WHERE song_id=?", (encode_text(song_id),))).fetchone() is None else 1

        conn.close()
        return answ

    def add_song(db_name, song_data):
        error_correction()

        conn = sqlite3.connect(f"Databases/{db_name}")
        cursor = conn.cursor()

        # new song num for database #
        try:
            song_num = cursor.execute("SELECT * FROM user_music ORDER BY num DESC LIMIT 1").fetchone()[4]+1
        except:
            song_num = cursor.execute("SELECT count(*) FROM user_music ORDER BY song_id").fetchone()[0]

        cursor.execute("INSERT INTO user_music VALUES (?,?,?,?,?,?,?)", (encode_text(song_data[0]), encode_text(song_data[1]), encode_text(song_data[2]), encode_text(song_data[3]), song_num, encode_text(song_data[4]), encode_text(song_data[5])))

        conn.commit()
        conn.close()
        clear_ram()

    def delete_song(db_name, song_id):
        error_correction()

        conn = sqlite3.connect(f"Databases/{db_name}")
        cursor = conn.cursor()

        cursor.execute("DELETE FROM user_music WHERE song_id=?", (encode_text(song_id),))

        conn.commit()
        conn.close()
        clear_ram()
