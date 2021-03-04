from .config_helper import SpotibarConfig
from tkinter import *


class ConfigPopup():

    def __init__(self):
        self.root = Tk(className="Spotibar")
        self.root.attributes('-type', 'dialog')
        self.config = SpotibarConfig()

        self.position_window()

        self.should_put_to_monthly_playlist = BooleanVar(
            self.root,
            self.config.get('should_put_to_monthly_playlist', True)
        )
        self.should_heart_on_lastfm = BooleanVar(
            self.root,
            self.config.get('should_heart_on_lastfm', True)
        )
        self.currently_playing_trunclen = IntVar(
            self.root,
            self.config.get('currently_playing_trunclen', 45)
        )

        Label(self.root, text="Put to monthly playlist?").grid(row=0, column=0)
        Checkbutton(
            self.root,
            variable=self.should_put_to_monthly_playlist,
            command=self.handle_should_put_to_monthly_playlist_change
        ).grid(row=0, column=1)

        Label(self.root, text="Heart on last.fm?").grid(row=1, column=0)
        Checkbutton(
            self.root,
            variable=self.should_heart_on_lastfm,
            command=self.handle_should_heart_on_lastfm
        ).grid(row=1, column=1)

        Label(self.root, text="Currently playing max length: ").grid(
            row=2,
            column=0
        )
        trunclen_entry_box = Entry(
            self.root,
            textvariable=self.currently_playing_trunclen,
            width=3
        )
        trunclen_entry_box.grid(
            row=2, column=1
        )
        trunclen_entry_box.bind(
            "<Return>",
            lambda event: self.handle_set_currently_playing_trunclen()
        )

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

    def handle_should_heart_on_lastfm(self):
        self.config.set(
            'should_heart_on_lastfm',
            self.should_heart_on_lastfm.get()
        )

    def handle_set_currently_playing_trunclen(self):
        self.config.set(
            'currently_playing_trunclen',
            int(self.currently_playing_trunclen.get())
        )
