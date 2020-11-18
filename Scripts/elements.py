# -*- coding: utf-8 -*-

""" For clear RAM """
from gc import collect as clear_ram


def clear_list_of_songs():
    global list_of_songs_class
    for song in list_of_songs_class:
        song.del_class()
        del song
    clear_ram()
    list_of_songs_class.clear()


""" Elements for main program """
VERSION = "0.3"
AUTHOR = "D0Nater"
GITHUB = "https://github.com/D0Nater/BounceBit/"
PROGRAM_NAME = "Bounce Bit"

song_time_now = "00:00"

list_of_music = {}

list_of_songs_class = []

themes = {
    "dark": {
        "background": "grey17",
        "second_color": "grey13",
        "text_color": "white",
        "text_second_color": "grey55"
    },
    "light": {
        "background": "grey90",
        "second_color": "grey75",
        "text_color": "grey4",
        "text_second_color": "grey35"
    },
    "purple": {
        "background": "#7D007D",
        "second_color": "#690069",
        "text_color": "white",
        "text_second_color": "grey60"
    },
    "red": {
        "background": "#AA1F1F",
        "second_color": "#821F1F",
        "text_color": "white",
        "text_second_color": "grey70"
    },
    "green": {
        "background": "#1E8C46",
        "second_color": "#1E7346",
        "text_color": "white",
        "text_second_color": "grey80"
    },
    "blue": {
        "background": "#3C5AFA",
        "second_color": "#323CFA",
        "text_color": "white",
        "text_second_color": "grey75"
    }
}

languages = {
    # Buttons #
    "Загруженное": {
        "ru": "Загруженное",
        "en": "Loaded"
    },
    "Избранное": {
        "ru": "Избранное",
        "en": "Favorites"
    },
    "Рекомендации": {
        "ru": "Рекомендации",
        "en": "Recommendations"
    },

    # Settings #
    "Настройки": {
        "ru": "Настройки",
        "en": "Settings"
    },
    "Сохранить": {
        "ru": "Сохранить",
        "en": "Save"
    },
    "Тема": {
        "ru": "Тема",
        "en": "Theme"
    },
    "Фон": {
        "ru": "Фон",
        "en": "Background"
    },
    "load_img": {
        "ru": "Загрузить изображение",
        "en": "Load picture"
    },
    "Язык": {
        "ru": "Язык",
        "en": "Lang"
    },
    "more": {
        "ru": "Больше",
        "en": "More"
    },
    "key_e": {
        "ru": "Назначение клавиш",
        "en": "Key assignment"
    },

    # Music genres #
    "Жанры": {
        "ru": "Жанры",
        "en": "Genres"
    },
    "Жанр": {
        "ru": "Жанр",
        "en": "Genre"
    },
    "Поп": {
        "ru": "Поп",
        "en": "Pop"
    },
    "Рок": {
        "ru": "Рок",
        "en": "Rock"
    },
    "Рэп": {
        "ru": "Рэп",
        "en": "Rap"
    },
    "Джаз": {
        "ru": "Джаз",
        "en": "Jazz"
    },
    "Шансон": {
        "ru": "Шансон",
        "en": "Shanson"
    },
    "Классика": {
        "ru": "Классика",
        "en": "Classical"
    },

    # Song info #
    "Трек": {
        "ru": "Трек",
        "en": "Track"
    },
    "Артист": {
        "ru": "Артист",
        "en": "Artist"
    },
    "Длительность": {
        "ru": "Длительность",
        "en": "Duration"
    },
    "Размер": {
        "ru": "Размер",
        "en": "Size"
    },
    "Текст": {
        "ru": "Текст",
        "en": "Text"
    },

    # Playlists #
    "Плейлист": {
        "ru": "Плейлист",
        "en": "Playlist"
    },
    "create_pl": {
        "ru": "Создать Плейлист",
        "en": "Create Playlist"
    },
    "pl_name": {
        "ru": "Название Плейлиста",
        "en": "Playlist Name"
    },

    # Errors #
    "load_error": {
        "ru": "Упс, ничего не загружено ;(",
        "en": "Oops, nothing uploaded ;("
    },
    "add_error": {
        "ru": "Упс, сюда ничего не добавлено ;(",
        "en": "Oops, nothing added here ;("
    },
    "connect_error": {
        "ru": "Упс, не удалось подключиться к интернету ;(",
        "en": "Oops, could not connect to the internet ;("
    },

    # Other #
    "update_text": {
        "ru": "Доступно обновление",
        "en": "Update is available"
    },
    "Загрузка": {
        "ru": "Загрузка",
        "en": "Loading"
    },
    "Новости": {
        "ru": "Новости",
        "en": "News"
    },
    "Поиск" : {
        "ru": "Поиск",
        "en": "Search"
    },
    "Страница": {
        "ru": "страница",
        "en": "page"
    },
    "key_assignmet": {
        "ru": "Клавишы\n\n< SPACE > - Плей/Пауза\n\n< RIGHT > - Следующая песня\n\n< LEFT > - Предыдущая песня\n\n< Shift > - Информация о песне",
        "en": "Keyboard keys\n\n< SPACE > - Play/Pause\n\n< RIGHT > - After song\n\n< LEFT > - Behind song\n\n< Shift > - Information about song"
    }
}
