# vitetris (Asciiverse packaging)

Victor Geraldsson's vitetris (C, BSD-2-Clause), a falling-blocks game with
two-player and network play, packaged for the Asciiverse catalog (id
`vitetris`). Not our code: no code changes so far; list any in PATCHES.md.

- `upstream` is github.com/vicgeralds/vitetris (branch `master`); ours is
  branch `asciiverse`, `origin` github.com/theasciiverse/vitetris.
- Build: `sh asciiverse/build.sh` (just make and a C compiler; Alpine in CI
  for a static binary). Don't run `./configure`: the committed config.mk
  and src/config.h are what we build with.
- Release: tag `v<upstream version>+<upstream commit date>-av.<n>` (first
  `v0.59.1+20250208-av.1`). Linux musl and macOS; no Windows.
- The board adapts to the terminal; 40x22 shows it whole (no next-piece
  box), 60 columns add the statistics.
- Preview: `asciiverse/record-preview.sh out/vitetris` (asciinema 3, tmux):
  drive.py reads the board (falling piece '##', settled blocks '# ') and
  places pieces with a height/lines/holes/bumpiness score; about 50 s.
- Name: the catalog keeps "vitetris", upstream's name; our texts say
  "falling blocks" rather than using the trademark on its own.
