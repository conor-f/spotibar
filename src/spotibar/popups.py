from .config_helper import SpotibarConfig
from tkinter import *


class ConfigPopup():

    def __init__(self):
        self.root = Tk(className="Spotibar")
        self.root.attributes('-type', 'dialog')
        self.config = SpotibarConfig()

        self.position_window()

        Label(self.root, text="Put to monthly playlist: ").grid(row=0)

        self.should_put_to_monthly_playlist = BooleanVar(
            self.root,
            self.config.get('should_put_to_monthly_playlist', True)
        )
        Checkbutton(
            self.root,
            variable=self.should_put_to_monthly_playlist,
            command=self.handle_should_put_to_monthly_playlist_change
        ).grid(row=0, column=1)

        self.attach_close_window_handler()
        self.root.mainloop()

    def position_window(self):
        width = 250
        height = 150

        x = self.root.winfo_pointerx()
        y = self.root.winfo_pointery()
        abs_coord_x = self.root.winfo_pointerx() - self.root.winfo_vrootx()
        abs_coord_y = self.root.winfo_pointery() - self.root.winfo_vrooty()

        abs_coord_x -= int(width / 2)
        abs_coord_y -= int(height) - int(height / 10)

        self.root.geometry(f"{width}x{height}+{abs_coord_x}+{abs_coord_y}")

    def attach_close_window_handler(self):
        def close_window(event=None):
            self.root.destroy()
        self.root.bind("<FocusOut>", close_window)

    def handle_should_put_to_monthly_playlist_change(self):
        self.config.set(
            'should_put_to_monthly_playlist',
            self.should_put_to_monthly_playlist.get()
        )
