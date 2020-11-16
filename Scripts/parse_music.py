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


top_music_json = {"music": {"num": 0}, "music_albums": {"num": 0}, "url": "", "error": None}


class ParseMusic:
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