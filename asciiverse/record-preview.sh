#!/bin/sh
# Records the 100x30 catalog preview, asciiverse/vitetris.cast
# (hub/RECORDING.md): the menu, then about 40 s of a 1-player game played
# by asciiverse/drive.py (it reads the board, picks the placement that
# keeps the stack low and flat, and turns, slides and drops each piece),
# then back out through the menu. asciinema records a tmux pane (own
# socket, no status line, no user config) that drive.py reads and plays
# in. Needs asciinema 3 and tmux.
#   asciiverse/record-preview.sh out/vitetris
set -eu
binary=$(cd "$(dirname "$1")" && pwd)/$(basename "$1")
here=$(cd "$(dirname "$0")" && pwd)
out=$here/vitetris.cast
home=$(mktemp -d)
trap 'tmux -L avrec kill-server 2>/dev/null; rm -rf "$home"' EXIT
mkdir "$home/bin" && cp "$binary" "$home/bin/vitetris"
cd "$home"  # nothing in the recording names a local path
export HOME="$home" PATH="$home/bin:$PATH" TERM=xterm-256color COLORTERM=truecolor LANG=C.UTF-8
tmux -L avrec -f /dev/null new-session -d -s rec -x 100 -y 30 "vitetris" \; set -g status off
python3 -I "$here/drive.py" avrec rec 40 &
drive=$!
asciinema rec --headless --overwrite -q \
  --window-size 100x30 --idle-time-limit 2 \
  --capture-env "TERM,COLORTERM,LANG" --title "vitetris" \
  --command "tmux -L avrec attach -t rec" "$out"
wait "$drive"
