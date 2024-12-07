#!/bin/bash

# Get the directory of the current script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# Launch Spotify
spotify &
SPOTIFY_PID=$!

# Wait for Spotify to start
sleep 2

# Launch the custom Python script
python3 "${SCRIPT_DIR}/dist/main.py" &
OVERLAY_PID=$!

# Wait for Spotify to close
wait $SPOTIFY_PID

# Kill the overlay script
kill $OVERLAY_PID
