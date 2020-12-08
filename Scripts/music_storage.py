# -*- coding: utf-8 -*-

""" For databases """
import sqlite3

""" For files """
from os import path, mkdir, remove

""" For download music """
import requests
from mutagen.easyid3 import EasyID3

""" For encode/decode db4 """
from Scripts.settings import encode_text, decode_text, sql_request


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

        try: cursor.execute("CREATE TABLE user_music (name, author, url, song_time, num, song_id)")
        except: pass

        try: cursor.execute("CREATE TABLE user_playlists (name, music, playlist_id)")
        except: pass

        conn.commit()
        conn.close()

    check_db("database2.sqlite") # added music & playlists
    check_db("database3.sqlite") # downloaded music


class MusicStorage:
    def download_music(song_id, url):
        if not path.exists("Databases/Download_Music"):
            mkdir("Databases/Download_Music")

        if path.exists(f"Databases/Download_Music/{song_id}.mp3") and path.getsize(f"Databases/Download_Music/{song_id}.mp3") is not 0:
            return

        try:
            response = requests.get(url, stream=True)
        except requests.exceptions.ConnectionError:
            raise ConnectionError

        with open(f"Databases/Download_Music/{song_id}.mp3", "wb") as f:
            for data in response.iter_content(chunk_size=4096):
                f.write(data)

        # music params #
        audio = EasyID3(f"Databases/Download_Music/{song_id}.mp3")
        audio["title"] = u""
        audio["artist"] = u""
        audio["album"] = u"BounceBit"
        audio["composer"] = u""
        audio.save()
        return

    def delete_song_file(song_id):
        if path.exists(f"Databases/Download_Music/{song_id}.mp3"):
            remove(f"Databases/Download_Music/{song_id}.mp3")

    def check_song_in_db(db_name, song_id):
        error_correction()

        return 0 if sql_request(
            db_name,
            "SELECT * FROM user_music WHERE song_id=?",
            (encode_text(song_id),)
        ) is None else 1

    def read_music(db_name, error):
        error_correction()

        conn = sqlite3.connect(f"Databases/{db_name}")
        cursor = conn.cursor()

        json_text = {"music": {"num": 0}, "error": None}

        music_list = []
        for i in cursor.execute("SELECT * FROM user_music ORDER BY song_time"):
            music_list.append(i[4])
        music_list = sorted(music_list)[::-1]

        # read db #
        song_num = 0
        for num in music_list:
            song_data = cursor.execute("SELECT * FROM user_music WHERE num=?", (num,)).fetchone()
            song_data = {
                "name": decode_text(song_data[0]),
                "author": decode_text(song_data[1]),
                "url": decode_text(song_data[2]),
                "song_time": decode_text(song_data[3]),
                "song_id": decode_text(song_data[5])
            }
            json_text["music"][f"song{song_num}"] = song_data
            json_text["music"]["num"] += 1

            song_num += 1

        if json_text["music"]["num"] is 0:
            json_text["error"] = error

        conn.close()
        return json_text

    def add_song(db_name, song_data):
        error_correction()

        # new song num for database #
        try:
            song_num = sql_request(db_name, "SELECT * FROM user_music ORDER BY num DESC LIMIT 1")[4]+1
        except:
            song_num = sql_request(db_name, "SELECT count(*) FROM user_music ORDER BY song_id")[0]

        sql_request(
            db_name,
            "INSERT INTO user_music VALUES (?,?,?,?,?,?)",
            (
                encode_text(song_data["name"]),
                encode_text(song_data["author"]),
                encode_text(song_data["url"]),
                encode_text(song_data["song_time"]),
                song_num,
                encode_text(song_data["song_id"])
            )
        )

    def delete_song(db_name, song_id):
        error_correction()

        sql_request(
            db_name,
            "DELETE FROM user_music WHERE song_id=?",
            (encode_text(song_id),)
        )
