# Spotibar

  Polybar plugin for Spotify that uses the Spotify Web API. Note that this
requires a Spotify premium account.

## Features:
  - [x] Display currently playing artist/song
  - [x] Play/Pause, Previous, Next functionality
  - [x] Add to playlist
  - [ ] Scroll currently playing tracking output
  - [ ] Have other options for selecting what playlist to add to
  - [x] Add last.fm hearting track option

![Spotibar Config Menu](https://user-images.githubusercontent.com/2671067/111181822-42feeb00-85a6-11eb-820e-585864233923.png)
![spotibar_Closed](https://user-images.githubusercontent.com/2671067/111181789-3aa6b000-85a6-11eb-8511-da536700438a.png)

## Usage/Experience:
  After installing and configuring `spotibar` to run on your Polybar as
described below, you should see the currently playing track/artist, interactive
controls to go to the previous song, play/pause and go to the next track. The
thing that justifies the little bit of extra work to set up this module is in
the final icon, options/playlists. If you right click on this option, you will
get a config option popup which lets you enable/disable adding tracks you like
to a Spotify playlist, hearting the track on last.fm, the different display
options, etc. It will also allow you to select multiple playlists to add to at
once, and other options. Clicking it will trigger all liking/adding to playlist
options.

## Installation:
  Installation is in three steps, the first is getting credentials from [Spotify](https://developer.spotify.com/dashboard/applications). You need to create an app (call it whatever suits) and take the `Client ID` and `Client Secret` and add them to `~/.spotibar_config.json` as follows:
```
{
  "client_id": "XXXXX",
  "client_secret": "XXXXX",
}
```
  After getting these values from the Spotify Developer Console, you need to add a redirect URL. Click "Edit Settings" and paste `http://127.0.0.1` under *Redirect URIs*.
  Secondly, you need to install and authenticate `spotibar`:
```
python3 -m pip install spotibar
spotibar --auth
```
  This should open up a browser at `127.0.0.1`. Copy the entire URL and paste
it back into the terminal window you ran `spotibar --auth` from. You should see
a message similar to `Successfully authenticated.`.

  If you're getting errors, try removing spotibar and reinstalling under sudo permissions. If you get an error involving `libtk8.6.so`, install tk using your distro's package manager.
  
  Once `spotibar` is installed and authenticated, you need to modify your
polybar config as follows (or however suits your needs!):
```
modules-right = <other modules> spotibar-currently-playing spotibar-previous-track spotibar-toggle-playback spotibar-next-track spotibar-add-to-playlist <other modules>

[module/spotibar-previous-track]
type = custom/script
exec = echo ""
click-left = spotibar --previous-track
exec-if = [ $(spotibar --is-live) = "True" ]
format-underline = #1db954
format-padding = 2

[module/spotibar-next-track]
type = custom/script
exec = echo ""
click-left = spotibar --next-track
exec-if = [ $(spotibar --is-live) = "True" ]
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
exec-if = [ $(spotibar --is-live) = "True" ]
format-underline = #1db954
format-padding = 2

[module/spotibar-add-to-playlist]
type = custom/script
exec = echo "≣"
click-left = spotibar --add-track-to-monthly-playlist
click-right = spotibar --config-popup
exec-if = [ $(spotibar --is-live) = "True" ]
format-underline = #1db954
format-padding = 2
```

  Done! Enjoy! File (probably inevitable) bug reports as issues!

  If you like, you can run `spotibar --init` in order to get some extra
features like LastFM integration.

## Development:
  Create an issue if you have any bug reports/feature requests/want to add
a feature and are looking for help with the environment setup.
