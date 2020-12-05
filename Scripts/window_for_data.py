# -*- coding: utf-8 -*-

from Scripts.elements import *

""" Load logo """
from PIL import Image, ImageTk
from Scripts.images import LoadPictures


class WindowForData:
    def __init__(self):
        Main.SCROLL_WIN = True

    def drow_data(self):
        vscrollbar = Scrollbar(Main.ROOT, bg=themes[Main.SETTINGS.theme]["background"])

        # Main canvas #
        Main.DATA_CANVAS = Canvas(Main.ROOT, width=Main.SETTINGS.width, height=Main.SETTINGS.height-220, yscrollcommand=vscrollbar.set, bg=themes[Main.SETTINGS.theme]["background"], highlightthickness=0)
        Main.DATA_CANVAS.configure(scrollregion=Main.DATA_CANVAS.bbox("all"))
        Main.DATA_CANVAS.bind_all("<MouseWheel>", self.on_mousewheel)
        vscrollbar.config(command=Main.DATA_CANVAS.yview)
        # vscrollbar.pack(side=LEFT, fill=Y) # draw scrollbar (if you havn't got a mouse)
        Main.DATA_CANVAS.pack()

        # Create and draw logo #
        Main.SCREENSAVER = ImageTk.PhotoImage(Image.open(LoadPictures.resource_path(path.join("pictures", "main_logo1.jpg"))).resize((Main.SETTINGS.width, Main.DATA_CANVAS.winfo_reqheight()), Image.ANTIALIAS))
        Main.DATA_CANVAS.create_image(0, 0, image=Main.SCREENSAVER, anchor=NW)

    def on_mousewheel(self, event):
        """ Scroll """
        if Main.SCROLL_WIN and Main.DATA_CANVAS.bbox("all")[3] > Main.SETTINGS.height-210:
            Main.DATA_CANVAS.yview_scroll(int(-1*(event.delta/100)), "units")
