# Spotibar

  Polybar plugin for Spotify that uses the Spotify Web API. Note that this
requires a Spotify premium account.

## Features:
  - [x] Display currently playing artist/song
  - [x] Play/Pause, Previous, Next functionality
  - [ ] Add to playlist (API work done, just needs a trigger in polybar)

## Installation:
  Installation is in three steps, the first is getting credentials from [Spotify](https://developer.spotify.com/dashboard/applications). You need to create an app (call it whatever suits) and take the `Client ID` and `Client Secret` and add them to `~/.spotibar_config.json` as follows:
```
{
  "client_id": "XXXXX",
  "client_secret": "XXXXX"
}
```

  Secondly, you need to install and authenticate `spotibar`:
```
python3 -m pip install spotibar
spotibar --auth
```
  This should open up a browser at `127.0.0.1`. Copy the entire URL and paste
it back into the terminal window you ran `spotibar --auth` from. You should see
a message similar to `Successfully authenticated.`.
  
  Once `spotibar` is installed and authenticated, you need to modify your
polybar config as follows (or however suits your needs!):
```
modules-right = <other modules> spotibar-currently-playing spotibar-previous-track spotibar-toggle-playback spotibar-next-track <other modules>

[module/spotibar-previous-track]
type = custom/script
exec = echo ""
click-left = spotibar --previous-track
exec-if = "pgrep spotify"
format-underline = #1db954
format-padding = 2

[module/spotibar-next-track]
type = custom/script
exec = echo ""
click-left = spotibar --next-track
exec-if = "pgrep spotify"
format-underline = #1db954
format-padding = 2

[module/spotibar-toggle-playback]
type = custom/script
exec = echo " "
click-left = spotibar --toggle-playback
exec-if = "pgrep spotify"
format-underline = #1db954
format-padding = 2

[module/spotibar-currently-playing]
type = custom/script
exec = spotibar --get-currently-playing
click-left = i3-msg '[class="Spotify"] focus'
exec-if = "pgrep spotify"
format-underline = #1db954
format-padding = 2
```

  Done! Enjoy! File (probably inevitable) bug reports as issues!

## Development:
  Create an issue if you have any bug reports/feature requests/want to add
a feature and are looking for help with the environment setup.
