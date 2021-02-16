import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import time

client_id = os.environ['SPOTIBAR_CLIENT_ID']
client_secret = os.environ['SPOTIBAR_CLIENT_SECRET']

print(client_id)
print(client_secret)


# TODO: Add links to permissions explanations here?
# Example: https://developer.spotify.com/documentation/general/guides/scopes/#playlist-modify-private
scope = "playlist-read-private"
scope += " playlist-modify-private"
scope += " user-read-playback-state"
scope += " user-modify-playback-state"
scope += " playlist-modify-public"

print(f"Scope: \"{scope}\"")


# TODO: Add cache location
client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope, client_id=client_id, client_secret=client_secret, redirect_uri="http://127.0.0.1"))
time.sleep(1)

# Get current user ID:
user_id = client.me()['id']
time.sleep(1)
print(f"User ID: {user_id}")

# Get devices (needed if Spotify is paused for a period of time)
devices = client.devices()
time.sleep(1)

# Lets just presume we're using the first one:
device_id = devices['devices'][0]['id']
print(f"Device ID: {device_id}")

# Play/Pause:
# TODO: Bug here: If already playing, this doesn't NOOP, it throws a nasty
# exception.
print("Starting playback...")
client.start_playback(device_id=device_id)
time.sleep(5)

print("Pausing playback...")
client.pause_playback(device_id=device_id)
time.sleep(5)

# Previous/Next:
print("Going to previous track...")
client.previous_track(device_id=device_id)
time.sleep(5)

print("Going to next track...")
client.next_track(device_id=device_id)
time.sleep(5)

# Current track name/artist name:
# TODO: Support podcast shows
print("Getting currently playing...")
current_track_name = client.currently_playing()['item']['name']
current_artist_name = ', '.join([artist['name'] for artist in client.currently_playing()['item']['artists']])
current_track_id = client.currently_playing()['item']['id']
print(f"Currently Playing: {current_track_name} by {current_artist_name}")

# Playlists:
# TODO: Support paginated responses for more playlists
print("Getting playlists for user...")
playlists = [
    {
        'name': playlist['name'],
        'id': playlist['id']
    }

    for playlist in client.user_playlists(user=user_id)['items']
]

# This is the test playlist:
playlist_id = '6HMWaQYY95pvB1Hou1EqOX'

# Add track to playlist:
print("Adding current trak to playlist...")
client.playlist_add_items(playlist_id, [current_track_id])
