# playaplaya

A simple, dedicated audiobook player, which keeps your place in multiple books and resumes automatically


## Features

  * Saves position regularly, and automatically recovers from logout/login, killing the process, hardware failures, etc.
  * Playlist based:
    - M3U, PLS, etc.
    - Generate playlists from any program
  * GStreamer-based audio playback -- supports mp3, ogg, and anything else gstreamer can play (including gst plugins)
  * Uses GTK
  * Supports multiple books, at the same time
  * Stores your position in a simple ini-style config file in your home dir, which allows:
    - Storing the config elsewhere via symlinks
    - Sharing config between machines over NFS, dropbox, etc.
    - Gathering reading/listening position stats from the config over time, to derive stats like reading speed / books per month
    - Modifying the reading positions via external programs
  * Python-based; easy to modify & enhance
