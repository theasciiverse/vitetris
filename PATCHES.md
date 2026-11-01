# Changes from upstream

This is the Asciiverse packaging of [vitetris](https://github.com/vicgeralds/vitetris)
by Victor Geraldsson (BSD-2-Clause, `licence.txt`), a falling-blocks game
for the terminal with two-player and network play. Upstream is the
`upstream` remote; this build is upstream's `master` at `744b509`
(2025-02-08), release 0.59.1 plus seven commits (a glibc 2.40 build fix,
"success!" at the end of a B-type game). The `asciiverse` branch carries
the changes below.

## Code

None. vitetris is built exactly as upstream has it, from its committed
`config.mk` and `src/config.h` (1- and 2-player, network play, terminal
resizing, menus, block styles; no joystick, no curses, no Allegro).

Settings and high scores go to `~/.vitetris`, as upstream; the shared
`/var/games/vitetris-hiscores` is only used if it already exists and is
writable.

## Packaging

- `asciiverse/build.sh`: `make` with upstream's config, the binary named
  `vitetris` (upstream's default name is `tetris`), static in Alpine for
  Linux, per architecture on macOS. Leaves `out/vitetris`.
- `.github/workflows/asciiverse-release.yml`: av archives for Linux
  (static musl, x86-64 and ARM64) and macOS (Intel and Apple silicon),
  plus SHA256SUMS. No Windows build: upstream's Windows port goes through
  MinGW and conio and was not tried.
- `asciiverse/record-preview.sh` and `asciiverse/drive.py`: the catalog
  preview, a 1-player game played by a script.
- `.gitignore`: `out/`, `dist/`, `stage/`, and the default `tetris`
  binary.

## Known upstream quirk

`decodehiscore_name()` in `src/hiscore.c` writes its end-of-string byte
one past the 8-byte name when a saved name is eight characters long
(GCC warns about it). That byte is the first of the score field, which is
written straight after, so nothing is lost. Not ours to change.
