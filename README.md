# Spotibar

Polybar plugin for Spotify

## Features:
 - [ ] Display currently playing artist/song
 - [ ] Play/Pause, Previous, Next functionality
 - [ ] Add to playlist

## Development:
 - `sudo make setup`


## Install:
 - `pip install spotibar`
 - Get credentials from [Spotify](https://developer.spotify.com/dashboard/applications)
 - Set the following:
```
export SPOTIBAR_CLIENT_ID='XXX'
export SPOTIBAR_CLIENT_SECRET='XXX'
```
    - Add a redirect URL of anything.
      Neccessary?
      Add it in the script for auth and redirect to the github/pypi page
    - Not necessary. Make it 127.0.0.1
    - Specify a cache directory?


## Issues:
  - URL specification for initial auth?
    - Solution: Add an entrypoint which will run the auth getting and parsing
      the returned URL
  - Cache location:
    - Solution: Specify an env var for the spotibar cache and pass it on auth
