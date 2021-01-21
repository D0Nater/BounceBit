# -*- coding: utf-8 -*-

""" For Parse """
import requests
import lxml.html

from os import remove, startfile

""" For make message box """
from tkinter.messagebox import showinfo, askyesno

from Scripts.elements import *
from Scripts.parse_music import parse_data


class UpdateProgram:
    def __init__(self):
        self.draw_update = False

        self.downloading = False

    def search_upd(self):
        try:
            tree = parse_data("https://github.com/D0Nater/BounceBit/blob/main/__init__.py")

            self.new_version = tree.xpath('//*[@id="LC5"]/span/text()')[0].split(": ")[-1]
            self.total_length = int(tree.xpath('//*[@id="LC7"]/span/text()')[0].split(": ")[-1])

            if self.new_version != VERSION:
                self.draw_update = True

                self.create_text_upd()

        except ConnectionError:
            pass

    def create_text_upd(self):
        if self.draw_update:
            # update text #
            self.update_text_draw = Main.MENU_CANVAS.create_text(Main.MENU_CANVAS.bbox(Main.VERSION_DRAW)[2]+20, 27, text=languages["update_text"][Main.SETTINGS.language]+" \""+self.new_version+"\" !", anchor=W, fill=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 11")

            # button 'download' #
            self.download_button = Main.MENU_CANVAS.create_window(Main.MENU_CANVAS.bbox(self.update_text_draw)[2]+15, Main.MENU_CANVAS.bbox(self.update_text_draw)[3]-12, anchor=W, window=Button(image=MyImage.DOWNLOAD_UPD, width=18, height=20, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE, \
                command=lambda: Thread(target=self.download_upd).start()))

            # button 'close' #
            self.close_button = Main.MENU_CANVAS.create_window(Main.MENU_CANVAS.bbox(self.download_button)[2]+12, Main.MENU_CANVAS.bbox(self.update_text_draw)[3]-10, anchor=W, window=Button(image=MyImage.CLOSE, width=16, height=16, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE, \
                command=lambda: self.close_msg()))

    def get_download_url(self):
        tree = parse_data("https://github.com/D0Nater/BounceBit/blob/main/DownloadProgram")

        return tree.xpath('//*[@id="LC1"]/text()')[0]

    def download_upd(self):
        def stop_download():
            self.downloading = False

        def delete_update():
            try: remove(f"BounceBit_{self.new_version}.exe")
            except: pass

        self.downloading = True

        Main.MENU_CANVAS.delete(self.close_button)

        self.close_button = Main.MENU_CANVAS.create_window(Main.MENU_CANVAS.bbox(self.download_button)[2]+40, Main.MENU_CANVAS.bbox(self.update_text_draw)[3]-10, anchor=W, window=Button(image=MyImage.CLOSE, width=16, height=16, bd=0, bg=themes[Main.SETTINGS.theme]["second_color"], activebackground=themes[Main.SETTINGS.theme]["second_color"], relief=RIDGE, \
            command=lambda: stop_download()))

        Main.MENU_CANVAS.delete(self.download_button)

        downloading_num = StringVar()
        downloading_num.set("0 %")

        draw_downloading_num_label = Label(Main.MENU_CANVAS, textvariable=downloading_num, bg=themes[Main.SETTINGS.theme]["second_color"], fg=themes[Main.SETTINGS.theme]["text_color"], font="Verdana 11")

        self.draw_downloading_num = Main.MENU_CANVAS.create_window(Main.MENU_CANVAS.bbox(self.update_text_draw)[2]+15, Main.MENU_CANVAS.bbox(self.update_text_draw)[3]-11, window=draw_downloading_num_label, anchor=W)

        self.__google_file__ = self.get_download_url()

        with open(f"BounceBit_{self.new_version}.exe", "wb") as f:
            response = requests.get(self.__google_file__, stream=True)

            dl = 0
            for data in response.iter_content(chunk_size=4000):
                if self.downloading:
                    f.write(data)

                    dl += len(data)
                    done = int(100 * dl / self.total_length)

                    if done > 100:
                        done = 100

                    downloading_num.set(f"{done} %")

                    continue

                break

        self.close_msg()

        if self.downloading:
            answer = askyesno(title=f"BounceBit Update {self.new_version}", message="Program was updated!\nStart program?")
            if answer:
                try:
                    Main.ROOT.quit()
                    startfile(f"BounceBit_{self.new_version}.exe")
                except:
                    showinfo(title="BounceBit", message="Starting Error!")
        else:
            delete_update()
            showinfo(title=f"BounceBit Update {self.new_version}", message="Program was not updated!")

        self.downloading = False

    def update_msg(self):
        if self.draw_update:
            self.close_msg()
            self.draw_update = True
            self.create_text_upd()

    def close_msg(self):
        Main.MENU_CANVAS.delete(self.update_text_draw)
        Main.MENU_CANVAS.delete(self.download_button)
        Main.MENU_CANVAS.delete(self.close_button)
        Main.MENU_CANVAS.delete(self.draw_downloading_num)

        self.draw_update = False
