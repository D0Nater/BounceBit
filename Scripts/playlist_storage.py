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


def sql_request(db_name, text, args=()):
    error_correction()

    conn = sqlite3.connect(f"Databases/{db_name}")
    cursor = conn.cursor()

    answer = cursor.execute(text, args).fetchone()

    conn.commit()
    conn.close()

    return answer


class PlaylistStorage:
    def check_playlist_in_db(db_name, playlist_name):
        return 0 if sql_request(
            db_name,
            "SELECT * FROM user_playlists WHERE name=?",
            (encode_text(playlist_name),)
        ) is None else 1

    def get_playlists(db_name):
        error_correction()

        conn = sqlite3.connect(f"Databases/{db_name}")
        cursor = conn.cursor()

        playlists = []

        playlist_ids = []
        for playlist in cursor.execute("SELECT * FROM user_playlists ORDER BY playlist_id"):
            playlist_ids.append(playlist[2])
        playlist_ids = sorted(playlist_ids)

        for playlist_id in playlist_ids:
            playlists.append(
                decode_text(
                    cursor.execute(
                        "SELECT name FROM user_playlists WHERE playlist_id=?",
                        (playlist_id,)
                    ).fetchone()
                )
            )

        conn.close()
        return playlists

    def add_playlist(db_name, playlist_name, music_data={"music":{"num":0}}):
        # new playlist id for database #
        try:
            playlist_id = sql_request(db_name, "SELECT * FROM user_playlists ORDER BY playlist_id DESC LIMIT 1")[2]+1
        except:
            playlist_id = sql_request(db_name, "SELECT count(*) FROM user_playlists ORDER BY playlist_id")[0]

        sql_request(
            db_name,
            "INSERT INTO user_playlists VALUES (?,?,?)",
            (encode_text(playlist_name), encode_text(json.dumps(music_data)), playlist_id)
        )

    def delete_playlist(db_name, playlist_name):
        sql_request(
            db_name,
            "DELETE FROM user_playlists WHERE name=?",
            (encode_text(playlist_name),)
        )

    def check_song_in_playlist(db_name, playlist_name, song_id):
        try:
            PlaylistStorage.get_music(db_name, playlist_name)["music"][song_id]
            return 1
        except KeyError:
            return 0

    def get_music(db_name, playlist_name):
        return json.loads(
            decode_text(
                sql_request(
                    db_name,
                    "SELECT music FROM user_playlists WHERE name=?",
                    (encode_text(playlist_name),)
                )[0]
            )
        )

    def add_song_in_playlist(db_name, playlist_name, song_data):
        music_json = PlaylistStorage.get_music(db_name, playlist_name)

        song_num = "song"+str(music_json["music"]["num"])
        music_json["music"][song_num] = song_data

        music_json["music"][song_data["song_id"]] = song_num # song link

        music_json["music"]["num"] += 1

        sql_request(
            db_name,
            "UPDATE user_playlists SET music=? WHERE name=?",
            (encode_text(json.dumps(music_json)), encode_text(playlist_name))
        )

    def del_song_out_playlist(db_name, playlist_name, song_id):
        music_json = PlaylistStorage.get_music(db_name, playlist_name)

        del music_json["music"][music_json["music"][song_id]]
        del music_json["music"][song_id]

        music_json["music"]["num"] -= 1

        sql_request(
            db_name,
            "UPDATE user_playlists SET music=? WHERE name=?",
            (encode_text(json.dumps(music_json)), encode_text(playlist_name))
        )
