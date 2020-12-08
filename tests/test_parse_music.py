# -*- coding: utf-8 -*-

""" For Parse """
import requests
import lxml.html

from json import loads as json_loads

from gc import collect as clear_ram

""" For tests """
from pympler import asizeof
from time import time as time_time
from json import dumps as json_dumps


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
        pages_array = [page]

        page_num = (3 if page > 2 else 1)
        for num in range(0, 4):
            try:
                pages_array.append(int(tree.xpath(f'//*[@id="pjax-container"]/div/div/section/ul/li[{page_num}]/a/text()')[0]))
            except IndexError:
                pass
            page_num += 1

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
                    song_data = json_loads(tree.xpath(f'//*[@id="pjax-container"]/div/div/ul[@class="tracks__list"]/li[{num}]/@data-musmeta')[0])

                    song_data = {
                        "name": song_data["title"],
                        "author": song_data["artist"],
                        "url": song_data["url"],
                        "song_time": tree.xpath(f'//*[@id="pjax-container"]/div/div/ul[@class="tracks__list"]/li[{num}]/div[3]/div/div/div[1]/text()')[0],
                        "song_id": song_data["id"].split("-")[-1]
                    }

                    search_data_json["music"][f"song{num-1}"] = song_data
                    search_data_json["music"]["num"] += 1

                    del song_data

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
    def genres_music(genre_num, page):
        page_str = "/start/" + str(48*(page-1)) if page > 1 else ""
        return ParseMusic.search_data("http://m.hitmos.com/genre/%s%s" % (genre_num, page_str), page)

    @staticmethod
    def more_song_info(song_id):
        clear_ram()
        more_song_info_json = {"size": "", "error": None}
        try:
            # parse site #
            tree = parse_data(f"http://m.hitmos.com/song/{song_id}")

            song_data = json_loads(tree.xpath(f'//*[@id="pjax-container"]/div[1]/div/div[1]/@data-musmeta')[0])

            return {
                "name": song_data["title"],
                "author": song_data["artist"],
                "url": song_data["url"],
                "song_time": tree.xpath(f'//*[@id="pjax-container"]/div[1]/div/div[1]/div[3]/div[2]/div/div[1]/text()')[0],
                "size": tree.xpath('//*[@id="pjax-container"]/div[1]/div/div[2]/div/select/option[2]/text()')[0].split(" ")[-2],
                "song_id": song_id,
                "error": None
            }

        except ConnectionError:
            more_song_info_json["error"] = "connect_error"

        return more_song_info_json


def humanize_bytes(num, suffix="B"):
    for unit in ["", "K", "M", "G", "T", "P", "E", "Z"]:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, "Yi", suffix)

def test_top_music():
    return ParseMusic.top_music(page=1)

def test_search_music():
    return ParseMusic.search_music(search_text="relaxing music", page=1)

def test_genres_music():
    genres = {
        "pop": "2",
        "rock": "6",
        "rap": "3",
        "jazz": "39",
        "shanson": "14",
        "classical": "28"
    }

    return ParseMusic.genres_music(genre_num=genres["pop"], page=1)

def test_more_song_info():
    song_data_json = {
        "author": "Dabro",
        "name": "\u041d\u0430 \u043a\u0440\u044b\u0448\u0435",
        "song_id": "71520975",
        "song_time": "03:18",
        "url": "http://m.hitmos.com/get/cuts/01/a2/01a2be02fe76f8d1a94bf1cfb8f606af/71520975/Dabro_-_Na_kryshe_b128f0d198.mp3"
    }

    return ParseMusic.more_song_info(song_data_json["song_id"])

def main():
    start_time = time_time()

    music_data_json = test_top_music()
    # music_data_json = test_search_music()
    # music_data_json = test_genres_music()
    # music_data_json = test_more_song_info()

    end_time = time_time() - start_time

    # print(json_dumps(music_data_json, sort_keys=True, indent=4)) # print answer
    print("\n Work time: ", end_time)
    print("\n Size: ", humanize_bytes(asizeof.asizeof(music_data_json)))


if __name__ == "__main__":
    main()
