import argparse
import json
import os
import pylast
import spotipy

from spotibar.translate import Translatore

from .config_helper import SpotibarConfig
from datetime import datetime
from getpass import getpass
from .popups import ConfigPopup


class SpotibarClient():
    __translator = Translatore()

    def __init__(self, *args, **kwargs):
        '''
        :kwarg config_file: String path relative to ~/ of a config file to load.
        '''
        self.scope = "playlist-read-private playlist-modify-private user-read-playback-state user-modify-playback-state playlist-modify-public"

        self.config_file = kwargs.get('config_file', '.spotibar_config.json')
        self.config = SpotibarConfig(config_file=self.config_file)

        self.client_id = self.config.get(
            'client_id',
            kwargs.get('client_id', None)
        )
        self.client_secret = self.config.get(
            'client_secret',
            kwargs.get('client_secret', None)
        )

        self.currently_playing_trunclen = int(
            self.config.get('currently_playing_trunclen', 45)
        )

        self.redirect_uri = "http://127.0.0.1"
        self.cache_dir = os.path.expanduser("~") + "/.spotibar_cache"

        if not os.path.exists(self.cache_dir):
            os.makedirs(self.cache_dir)

        self.cache_file = "auth_cache"

        self.client = self.get_client()

        self.lastfm_client = self.get_lastfm_client()

    def get_client(self):
        '''
        Returns the spotipy client ready for use.

        TODO: Add links to permissions explanations here?
        Example: https://developer.spotify.com/documentation/general/guides/scopes/#playlist-modify-private
        '''
        return spotipy.Spotify(
            auth_manager=spotipy.oauth2.SpotifyOAuth(
                scope=self.scope,
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                cache_path=f"{self.cache_dir}/{self.cache_file}",
                open_browser=False
            )
        )

    def get_lastfm_client(self):
        if self.config.get('should_heart_on_lastfm', False):
            try:
                return pylast.LastFMNetwork(
                    api_key=self.config.get('lastfm_api_key', None),
                    api_secret=self.config.get('lastfm_api_secret', None),
                    username=self.config.get('lastfm_username', None),
                    password_hash=self.config.get('lastfm_password_hash', None),
                )
            except Exception as e:
                message = self.__translator.translate("Please configure ~/")
                print(f"{message} {self.config_file} with last.fm details.")
                print(e)

    def auth(self):
        '''
        Calls a method that requires authentication to ensure spotibar has
        sorted out its permissions from Spotify.
        '''
        self.is_currently_playing()
        message = self.__translator.translate(
            "Successfully authenticated."   
        )
        print(message)

    def get_user_id(self):
        me = self.client.me()
        if me is not None:
            return me['id']

    def get_current_device_id(self):
        # Get devices (needed if Spotify is paused for a period of time)
        # Lets just presume we're using the first one:

        devices = self.client.devices()
        if devices is not None:
            return devices['devices'][0]['id']

    def is_currently_playing(self):
        '''
        Returns True if there is a currently playing song, False otherwise.
        '''
        try:
            current_play = self.client.currently_playing()
            if current_play is not None:
                current_play['is_playing']
        except Exception:
            return False

    def play(self):
        if not self.is_currently_playing():
            self.client.start_playback(device_id=self.get_current_device_id())

    def pause(self):
        if self.is_currently_playing():
            self.client.pause_playback(device_id=self.get_current_device_id())

    def toggle_playback(self):
        '''
        Plays the current track if currently paused. Pauses current track if
        currently playing.
        '''
        if self.is_currently_playing():
            self.pause()
        else:
            self.play()

    def previous(self):
        '''
        Goes to the previous playing song.
        '''
        try:
            self.client.previous_track(device_id=self.get_current_device_id())
        except Exception:
            print("TODO: HANDLE ERRORS!")

    def next(self):
        '''
        Goes to the next playing song.
        '''
        try:
            self.client.next_track(device_id=self.get_current_device_id())
        except Exception:
            print("TODO: HANDLE ERRORS!")

    def get_currently_playing_string(self):
        '''
        Returns the string ready for polybar
        '''
        try:
            current_play = self.client.currently_playing()

            if current_play is not None:
                current_track_name = current_play['item']['name']
                current_artist_name = ', '.join(
                    [
                        artist['name']
                        for artist in current_play['item']['artists']
                    ]
                )

                current_string = f"{current_track_name} by {current_artist_name}"

                if len(current_string) > self.currently_playing_trunclen:
                    return current_string[:self.currently_playing_trunclen - 3] \
                        + "..."
                else:
                    return current_string
        except Exception:
            return ""

    def get_current_track_id(self):
        current_play = self.client.currently_playing()
        if current_play is not None:
            return current_play['item']['id']

    def get_track_id_from_name(self, artist_name, track_name):
        results = self.client.search(
            q=f'artist:{artist_name} track: {track_name}', type='track'
        )

        try:
            if results is not None:
                return results['tracks']['items'][0]['id']
        except Exception:
            return None

    def get_user_playlists(self):
        '''
        Returns a list of dicts representing all the users playlists.

        TODO: Support more than 50 playlists.

        :rtype: list
        :returns: [
          {
            'name': <string playlist name>,
            'id': <string playlist ID>
          }, ..
        ]
        '''
        user_pls = self.client.user_playlist(self.get_user_id())
        if user_pls is not None:
            return [
                {
                    'name': playlist['name'],
                    'id': playlist['id']
                }
                for playlist in user_pls['items']
            ]

    def create_playlist(self, name, public=False):
        '''
        Creates a playlist given a playlist name.

        :kwarg public: If True, the playlist will be public by default, else
        Private.
        '''
        self.client.user_playlist_create(self.get_user_id(), name, public=public)

    def get_playlist_id_from_name(self, name, create_if_empty=True):
        '''
        Return the string ID of the playlist name specified and if doesn't
        exist, create it.
        '''
        playlists = self.get_user_playlists()
        if playlists is not None:
            playlist_id = [
                playlist['id'] for playlist in playlists
                if playlist['name'] == name
            ]

            if len(playlist_id) == 0 and create_if_empty:
                self.create_playlist(name)
                return self.get_monthly_playlist_id(
                    name,
                    create_if_empty=create_if_empty
                )
            elif len(playlist_id) == 1:
                return playlist_id[0]
            else:
                print("TODO: ERROR HANDLING! SHOULDN'T BE POSSIBLE.")
                return playlist_id[0]

    def get_monthly_playlist_id(self, name_format="%m ¦¦ %y", create_if_empty=True):
        '''
        Returns the ID of the monthly playlist as described by the name format
        which uses strftime strings.

        :kwarg create_if_empty: If True, creates the playlist if it doesn't exist
        and return that ID.
        '''
        monthly_playlist_name = datetime.now().strftime(name_format)

        return self.get_playlist_id_from_name(
            monthly_playlist_name,
            create_if_empty=create_if_empty
        )

    def add_track_to_playlist(self, playlist_id, track_id):
        self.client.playlist_add_items(playlist_id, [track_id])

    def add_current_track_to_monthly_playlist(self):
        if self.config.get('should_put_to_monthly_playlist', True):
            self.add_track_to_playlist(
                self.get_monthly_playlist_id(),
                self.get_current_track_id()
            )

        if self.config.get('should_heart_on_lastfm', False):
            try:
                currently_playing = self.get_currently_playing_string()

                # TODO: Hacky. Works as long as the artist doesn't use the word
                # ' by '
                if currently_playing is not None:
                    artist = currently_playing.split(' by ')[-1]
                    track = ' '.join(currently_playing.split(' by ')[:-1])

                    if self.lastfm_client is not None:
                        self.lastfm_client.get_track(artist, track).love()
            except Exception as e:
                
                message = self.__translator.translate(
                  "Hearting track on lastfm failed."  
                )
                print(message)
                print(e)

    def is_live(self):
        '''
        Returns True if Spotify is currently playing, False otherwise.
        '''
        return self.is_currently_playing()

    def get_current_album_image_url(self):
        '''
        Return a string of the URL of the album cover.
        '''
        if self.is_live():
            currently_playing = self.client.currently_playing()
            if currently_playing is not None:
                return currently_playing['item']['album']['images'][0]['url']
        return ''


def first_run(__translator: Translatore):
    '''
    Runs the first time Spotibar is initialized. Gives a basic interactive menu
    and asks the user for details to init the config file.
    '''
    welcome_message = __translator.translate(
     "\tWelcome to Spotibar!"   
    )
    config_message = __translator.translate(
     "This script will set up the initial config file and enable/disable/configure features based on your preferences."   
    )
    print(welcome_message)
    print(config_message)

    config = {}

    monthly_playlist_message = __translator.translate(
        "Do you want to add tracks to a monthly playlist?"
    )
    response = input(monthly_playlist_message + "[Y/n]")
    if response == "" or response.lower() == "y":
        config['should_put_to_monthly_playlist'] = True
    else:
        config['should_put_to_monthly_playlist'] = False

    lastfm_message = __translator.translate(
        "Do you want to set up LastFM track hearting?"
    )
    response = input(lastfm_message + "[Y/n]")
    if response == "" or response.lower() == "y":
        print(__translator.translate("Setting up LastFM track hearting..."))
        print(__translator.translate("Please go to https://www.last.fm/api/account/create to get your credentials:"))

        config['should_heart_on_lastfm'] = True

        response = input("\tAPI Key: ")
        config['lastfm_api_key'] = response

        response = input("\tShared Secret: ")
        config['lastfm_api_secret'] = response

        response = input("\tLastFM Username: ")
        config['lastfm_username'] = response

        response = pylast.md5(getpass("\tLastFM Password (This will be immediately hashed): "))
        config['lastfm_password_hash'] = response
    else:
        config['should_heart_on_lastfm'] = False
        config['lastfm_api_key'] = ''
        config['lastfm_api_secret'] = ''
        config['lastfm_username'] = ''
        config['lastfm_password_hash'] = ''
        print(__translator.translate("Skipping LastFM track hearting setup."))

    print(__translator.translate("Please go to https://developer.spotify.com/dashboard/applications to set up an application to get the following API keys. See the README for more details."))
    response = input("\tSpotify client ID: ")
    config['client_id'] = response
    response = input("\tSpotify client secret: ")
    config['client_secret'] = response

    spotibar_client = SpotibarClient(
        client_id=config['client_id'],
        client_secret=config['client_secret']
    )
    spotibar_client.auth()

    try:
        config_file_dir = spotibar_client.config_file
        path = os.path.expanduser("~") + f"/{config_file_dir}"
        with open(path, 'w') as fh:
            json.dump(config, fh)
    except Exception as e:
        message_err = __translator.translate(
         "Problem writing config file:"
        )
        print(message_err)
        print(e)

        message_config = __translator.translate(
         "Here's your config to manually add:"   
        )
        print(message_config)
        print(config)

        return


def main():
    parser = argparse.ArgumentParser(
        description='Entrypoint for Spotify/Polybar integration.'
    )

    group = parser.add_mutually_exclusive_group()
    group.add_argument("--get-currently-playing", action="store_true")
    group.add_argument("--previous-track", action="store_true")
    group.add_argument("--next-track", action="store_true")
    group.add_argument("--toggle-playback", action="store_true")
    group.add_argument("--add-track-to-monthly-playlist", action="store_true")
    group.add_argument("--auth", action="store_true")
    group.add_argument("--config-popup", action="store_true")
    group.add_argument("--is-live", action="store_true")
    group.add_argument("--init", action="store_true")

    args = parser.parse_args()

    __translator = Translatore()
    if args.init:
        first_run(__translator)

    spotibar_client = SpotibarClient()

    if args.get_currently_playing:
        print(spotibar_client.get_currently_playing_string())
    elif args.previous_track:
        spotibar_client.previous()
    elif args.next_track:
        spotibar_client.next()
    elif args.toggle_playback:
        spotibar_client.toggle_playback()
    elif args.add_track_to_monthly_playlist:
        spotibar_client.add_current_track_to_monthly_playlist()
    elif args.auth:
        spotibar_client.auth()
    elif args.config_popup:
        ConfigPopup()
    elif args.is_live:
        print(spotibar_client.is_live())


if __name__ == '__main__':
    main()
