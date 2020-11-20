# -*- coding: utf-8 -*-

""" For databases """
import sqlite3

""" For clear RAM """
from gc import collect as clear_ram

""" For Parse """
import requests
import lxml.html
from json import loads as json_loads

""" Other Scripts """
from Scripts.elements import *


def parse_data(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}
        api = requests.get(url, headers=headers)

        return lxml.html.document_fromstring(api.text)
    except requests.exceptions.ConnectionError:
        raise ConnectionError


class ParseMusic:
    @staticmethod
    def music_pages(tree, page):
        # Pages #
        pages_array = []
        try:
            pages_array.append(page)

            # other pages #
            page_num = (3 if page > 2 else 1)
            for num in range(0, 4):
                try:
                    pages_array.append(int(tree.xpath(f'//*[@id="pjax-container"]/div/div/section/ul/li[{page_num}]/a/text()')[0]))
                except:
                    pass

                page_num += 1

        except:
            pass
        
        # sorted and return pages #
        return sorted(pages_array)

    @staticmethod
    def search_data(url, page=1):
        clear_ram()
        search_data_json = {"music": {"num": 0}, "pages": [], "error": None}
        try:
            # parse site #
            tree = parse_data(url)

            # music #
            for num in range(1, 49):
                try:
                    new_song = json_loads(tree.xpath(f'//*[@id="pjax-container"]/div/div/ul[@class="tracks__list"]/li[{num}]/@data-musmeta')[0])

                    new_song = {
                        "name": new_song["title"],
                        "author": new_song["artist"],
                        "url": new_song["url"],
                        "song_time": tree.xpath(f'//*[@id="pjax-container"]/div/div/ul[@class="tracks__list"]/li[{num}]/div[3]/div/div/div[1]/text()')[0],
                        "song_id": new_song["id"].split("-")[-1]
                    }

                    search_data_json["music"][f"song{num-1}"] = new_song
                    search_data_json["music"]["num"] += 1

                    del new_song

                except (KeyError, IndexError):
                    break

            search_data_json["pages"] = ParseMusic.music_pages(tree, page)

            search_data_json["error"] = None

            del tree

        except ConnectionError:
            search_data_json["error"] = "connect_error"

        return search_data_json

    @staticmethod
    def top_music(page):
        page_str = "/start/" + str(48*(page-1)) if page > 1 else ""
        return ParseMusic.search_data(f"http://m.hitmos.com/songs/top-today{page_str}", page)

    @staticmethod
    def search_music(search_text, page):
        page_str = "/start/" + str(48*(page-1)) if page > 1 else ""
        return ParseMusic.search_data(f"http://m.hitmos.com/search{page_str}?q={search_text}", page)

    @staticmethod
    def genres_music(genre, page):
        page_str = "/start/" + str(48*(page-1)) if page > 1 else ""
        return ParseMusic.search_data("http://m.hitmos.com/genre/%s%s"%(languages[genre]["num"], page_str), page)

    @staticmethod
    def more_song_info(song_id):
        clear_ram()
        more_song_info_json = {"size": "", "error": None}
        try:
            # parse site #
            tree = parse_data(f"http://m.hitmos.com/song/{song_id}")

            # Song size #
            more_song_info_json["size"] = tree.xpath('//*[@id="pjax-container"]/div[1]/div/div[2]/div/select/option[2]/text()')[0].split(" ")[-2]

        except ConnectionError:
            more_song_info_json["error"] = "connect_error"

        return more_song_info_json
