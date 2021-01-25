# -*- coding: utf-8 -*-

import requests
import lxml.html
from os import path, mkdir
from json import loads as json_loads

""" For encode/decode db4 """
from Scripts.settings import encode_text, decode_text


class News:
    @staticmethod
    def check_errors_db4():
        # check dir #
        if not path.exists("Databases"):
            mkdir("Databases")

        # check json file #
        if not path.exists("Databases/database4"):
            with open("Databases/database4", "w+") as json_db:
                json_db.write(encode_text('{"text":{"ru":"","en":""},"id":"","date":""}'))
        else:
            try:
                with open("Databases/database4") as json_db:
                    json_loads(decode_text(json_db.read()).replace("'", '"'))
            except:
                with open("Databases/database4", "w+") as json_db:
                    json_db.write(encode_text('{"text":{"ru":"","en":""},"id":"","date":""}'))

    @staticmethod
    def parse_new_news():
        def parse_news():
            text = ""

            try:
                # parse site #
                headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36"}

                api = requests.get("https://github.com/D0Nater/BounceBit/blob/main/News", headers=headers)

                tree = lxml.html.document_fromstring(api.text)

                # parse and decode text #
                text = json_loads(decode_text(tree.xpath(f'//*[@id="LC1"]/text()')[0]).replace("'", '"'))

            except Exception as error:
                with open("Databases/database4", encoding="utf-8") as json_db:
                    text = json_loads(decode_text(json_db.read()).replace("'", '"'))

            return text

        News.check_errors_db4()

        # new news #
        new_news_data = parse_news()

        # news from database4 #
        with open("Databases/database4", encoding="utf-8") as json_db:
            json_data_db = json_loads(decode_text(json_db.read()).replace("'", '"'))

        if new_news_data["id"] != json_data_db["id"]:
            with open("Databases/database4", "w+") as json_db:
                json_db.write(encode_text(str(new_news_data)))

    @staticmethod
    def read_news():
        News.check_errors_db4()

        with open("Databases/database4", encoding="utf-8") as json_db:
            json_data_db = json_loads(decode_text(json_db.read()).replace("'", '"'))

        return [json_data_db["date"], json_data_db["text"]]
