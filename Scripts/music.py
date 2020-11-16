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
from mutagen.easyid3 import EasyID3

""" For Parse """
import requests
import lxml.html

""" For encode/decode db4 """
from Scripts.settings import encode_text, decode_text


def parse_data(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        api = requests.get(url, headers=headers)

        return lxml.html.document_fromstring(api.text)
    except requests.exceptions.ConnectionError:
        raise ConnectionError


def music_pages(tree, page, xpath_text):
        # Pages #
        pages_music_json = []
        try:
            # page now (default 1) #
            pages_music_json.append(page)

            # other pages #
            for num in range((2 if int(page) > 1 else 1), 6):
                try:
                    pages_music_json.append(tree.xpath(xpath_text % num)[0])
                except:
                    pass

            # delete last button #
            if pages_music_json[-1] == "Следующая":
                (pages_music_json).pop()

        except:
            pass
        
        # sorted and return pages #
        return sorted(pages_music_json)


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

    check_db("database2.sqlite") # add music
    check_db("database3.sqlite") # download music


top_music_json = {"music": {"num": 0}, "music_albums": {"num": 0}, "url": "", "error": None}


class Music:
    def download_music(song_id, url):
        if not path.exists("Databases/Download_Music"):
            mkdir("Databases/Download_Music")

        if not path.exists(f"Databases/Download_Music/{song_id}.mp3"):
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

    def top_music():
        clear_ram()
        global top_music_json
        try:
            if top_music_json["music"]["num"] is 0:
                top_music_json = {"music": {"num": 0}, "music_albums": {"num": 0}, "error": None}
                
                # parse site #
                tree = parse_data("https://zaycev.net/")

                # music #
                for num in range(1, 61):
                    new_song = {
                        "name": tree.xpath(f'//*[@id="top_1"]/div[2]/div[{num}]/div[1]/div[2]/div[3]/a/text()')[0],
                        "author": tree.xpath(f'//*[@id="top_1"]/div[2]/div[{num}]/div[1]/div[2]/div[1]/a/text()')[0],
                        "url": tree.xpath(f'//*[@id="top_1"]/div[2]/div[{num}]/@data-url')[0],
                        "data_key": tree.xpath(f'//*[@id="top_1"]/div[2]/div[{num}]/@data-dkey')[0],
                        "song_time": tree.xpath(f'//*[@id="top_1"]/div[2]/div[{num}]/div[2]/text()')[0],
                        "song_id": tree.xpath(f'//*[@id="top_1"]/div[2]/div[{num}]/@data-id')[0]
                    }
                    top_music_json["music"][f"song{num-1}"] = new_song
                    top_music_json["music"]["num"] += 1
                    del new_song

                top_music_json["error"] = None

                del tree

        except ConnectionError:
            top_music_json["error"] = "connect_error"

        return top_music_json

    def search_music(text, page):
        clear_ram()
        search_music_json = {"music": {"num": 0}, "music_albums": {"num": 0}, "pages": [], "error": None}
        try:
            # parse site #
            tree = parse_data(f'https://zaycev.net/search.html?page={page}&query_search={text}')

            # music #
            for num in range(1, 41):
                try:
                    new_song = {
                        "name": tree.xpath(f'//*[@id="search-results"]/div/div[3]/div/div[1]/div[1]/div[2]/div[{num}]/div[1]/div[2]/div[3]/a/text()')[0],
                        "author": tree.xpath(f'//*[@id="search-results"]/div/div[3]/div/div[1]/div[1]/div[2]/div[{num}]/div[1]/div[2]/div[1]/a/text()')[0],
                        "url": tree.xpath(f'//*[@id="search-results"]/div/div[3]/div/div[1]/div[1]/div[2]/div[{num}]/@data-url')[0],
                        "data_key": tree.xpath(f'//*[@id="search-results"]/div/div[3]/div/div[1]/div[1]/div[2]/div[{num}]/@data-dkey')[0],
                        "song_time": tree.xpath(f'//*[@id="search-results"]/div/div[3]/div/div[1]/div[1]/div[2]/div[{num}]/div[2]/text()')[0],
                        "song_id": tree.xpath(f'//*[@id="search-results"]/div/div[3]/div/div[1]/div[1]/div[2]/div[{num}]/@data-id')[0]
                    }
                    search_music_json["music"][f"song{num-1}"] = new_song
                    search_music_json["music"]["num"] += 1
                    del new_song
                except:
                    break

            # Pages #
            search_music_json["pages"] = music_pages(tree, page, '//*[@id="search-page"]/div/div/div[3]/div/a[%s]/span/text()')

            search_music_json["error"] = None

            del tree

        except ConnectionError:
            search_music_json["error"] = "connect_error"

        return search_music_json

    def genres_music(genre, page):
        clear_ram()
        genre_music_json = {"music": {"num": 0}, "music_albums": {"num": 0}, "pages": [], "error": None}
        try:
            # parse site #
            tree = parse_data(f'https://zaycev.net/genres/{genre}/index_{page}.html?spa=false&page={page}')

            # music #
            for num in range(1, 41):
                try:
                    new_song = {
                        "name": tree.xpath(f'//*[@id="genre-tracks"]/div[2]/div[1]/div[{num}]/div[1]/div[2]/div[3]/a/text()')[0],
                        "author": tree.xpath(f'//*[@id="genre-tracks"]/div[2]/div[1]/div[{num}]/div[1]/div[2]/div[1]/a/text()')[0],
                        "url": tree.xpath(f'//*[@id="genre-tracks"]/div[2]/div[1]/div[{num}]/@data-url')[0],
                        "data_key": tree.xpath(f'//*[@id="genre-tracks"]/div[2]/div[1]/div[{num}]/@data-dkey')[0],
                        "song_time": tree.xpath(f'//*[@id="genre-tracks"]/div[2]/div[1]/div[{num}]/div[2]/text()')[0],
                        "song_id": tree.xpath(f'//*[@id="genre-tracks"]/div[2]/div[1]/div[{num}]/@data-id')[0]
                    }
                    genre_music_json["music"][f"song{num-1}"] = new_song
                    genre_music_json["music"]["num"] += 1
                    del new_song
                except:
                    break

            # Pages #
            genre_music_json["pages"] = music_pages(tree, page, '//*[@id="page-body"]/div[2]/div/div[2]/div/div/div/section/div[@class="pager clearfix"]/a[%s]/span/text()')

            genre_music_json["error"] = None

            del tree

        except ConnectionError:
            genre_music_json["error"] = "connect_error"

        return genre_music_json

    def more_song_info(data_key):
        clear_ram()
        more_song_info_json = {"size": "", "text": "", "error": None}
        try:
            data_key = data_key.split(".")[0]

            # parse site #
            tree = parse_data(f'https://zaycev.net/pages{data_key}.shtml')

            # Song size #
            more_song_info_json["size"] = tree.xpath('//*[@id="audiotrack-info"]/div[1]/div[2]/p[1]/text()')[0].split(" ")[1]

            # Song text #
            try: more_song_info_json["text"] = tree.xpath('//*[@id="audiotrack-block"]/div[3]/div[2]/div/div[@class="audiotrack-lyrics__text text-expander__text"]/text()')[0]
            except: pass

        except ConnectionError:
            more_song_info_json["error"] = "connect_error"

        return more_song_info_json

    def read_music(db_name, error):
        error_correction()

        conn = sqlite3.connect(f"Databases/{db_name}")
        cursor = conn.cursor()

        json_text = {"music": {"num": 0}, "music_albums": {"num": 0}, "error": None}

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


class Playlist:
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
