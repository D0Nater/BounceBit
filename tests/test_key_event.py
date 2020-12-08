# -*- coding: utf-8 -*-

from tkinter import *


class KeyEvent:
    def __init__(self, root):
        root.bind('<space>', self.play_pause)

        root.bind('<Left>', self.behind_music)
        root.bind('<Right>', self.after_music)

        root.bind('<Shift_L>', self.more_info)
        root.bind('<Shift_R>', self.more_info)

    def play_pause(self, event):
        print("\n - click play/pause :", event)

    def more_info(self, event):
        print("\n - click more info :", event)

    def behind_music(self, event):
        print("\n - click behind :", event)

    def after_music(self, event):
        print("\n - click after :", event)


def main():
    root = Tk()

    # Window settings #
    root.title("BounceBit Test")
    root.geometry("350x300")

    KeyEvent(root)

    key_events = "Keyboard keys\n\n< SPACE > - Play/Pause\n\n< RIGHT > - After song\n\n< LEFT > - Behind song\n\n< Shift > - Information about song"

    draw_text = Text(wrap=WORD)
    draw_text.insert(END, key_events)
    draw_text.config(state=DISABLED)
    draw_text.place(x=0, y=0, width=350, height=300)

    root.mainloop()


if __name__ == "__main__":
    main()
