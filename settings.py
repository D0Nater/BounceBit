# -*- coding: utf-8 -*-

import sqlite3
from os import path, mkdir, remove
from base64 import b64decode, b64encode


text_for_readme = """%s v%s
 Author: %s.
 GitHub: %s
"""


def decode_text(text):
    translated = ''
    i = len(text) - 1
    while i >= 0:
        translated = translated + text[i]
        i = i - 1
    decode_text = (b64decode(translated)).decode("UTF-8")
    return decode_text


def encode_text(text):
    encode_text = (b64encode(str(text).encode("UTF-8"))).decode()
    translated = ''
    i = len(encode_text) - 1
    while i >= 0:
        translated = translated + encode_text[i]
        i = i - 1
    return translated


class Settings:
    def __init__(self, width, height, language, theme):
        self.width = int(width)
        self.height = int(height)
        self.language = language
        self.theme = theme


    def create_readme(self, PROGRAM_NAME, VERSION, AUTHOR, GITHUB):
        with open("Databases/README.md", "w+") as file:
            file.write(text_for_readme%(PROGRAM_NAME,VERSION,AUTHOR,GITHUB))


    def error_correction(self):
        """
        If file 'database1.sqlite' is damaged,
        settings are reset and new ones are created
        """
        if not path.exists('Databases'):
            mkdir('Databases')

        conn = sqlite3.connect('Databases/database1.sqlite')
        cursor = conn.cursor()

        try:
            cursor.execute('SELECT * FROM settings WHERE setting=?', (encode_text("width"),)).fetchone()
        except sqlite3.DatabaseError:
            conn.close()
            remove('Databases/database1.sqlite')
            conn = sqlite3.connect('Databases/database1.sqlite')
            cursor = conn.cursor()

        try:
            cursor.execute('CREATE TABLE settings (setting, param)')
        except:
            pass

        def check_setting(name, param):
            if cursor.execute('SELECT * FROM settings WHERE setting=?', (encode_text(name),)).fetchone() is None:
                cursor.execute('INSERT INTO settings VALUES (?,?)', (encode_text(name), encode_text(param))) 

        check_setting("width", self.width)
        check_setting("height", self.height)
        check_setting("language", self.language)
        check_setting("theme", self.theme)

        conn.commit()
        conn.close()


    def change_settings(self):
        """
        For Button 'Save'
        """
        self.error_correction()

        conn = sqlite3.connect('Databases/database1.sqlite')
        cursor = conn.cursor()

        cursor.execute('UPDATE settings SET param=? WHERE setting=?', (encode_text(self.width), encode_text("width")))
        cursor.execute('UPDATE settings SET param=? WHERE setting=?', (encode_text(self.height), encode_text("height")))
        cursor.execute('UPDATE settings SET param=? WHERE setting=?', (encode_text(self.language), encode_text("language")))
        cursor.execute('UPDATE settings SET param=? WHERE setting=?', (encode_text(self.theme), encode_text("theme")))

        conn.commit()
        conn.close()


    def update_settings(self):
        """
        Read database and give params
        """
        self.error_correction()

        conn = sqlite3.connect('Databases/database1.sqlite')
        cursor = conn.cursor()

        self.width = int(decode_text(cursor.execute('SELECT param FROM settings WHERE setting=?', (encode_text("width"),)).fetchone()[0]))
        self.height = int(decode_text(cursor.execute('SELECT param FROM settings WHERE setting=?', (encode_text("height"),)).fetchone()[0]))
        self.language = decode_text(cursor.execute('SELECT param FROM settings WHERE setting=?', (encode_text("language"),)).fetchone()[0])
        self.theme = decode_text(cursor.execute('SELECT param FROM settings WHERE setting=?', (encode_text("theme"),)).fetchone()[0])

        conn.close()
