#!/usr/bin/env python3
"""drive.py SOCKET SESSION [SECONDS]: plays vitetris in a tmux pane.

Starts a 1-player game from the menu, then for each new piece reads the
board off the pane (cells are two columns wide), tries
every rotation and column (the falling piece is drawn '##', settled
blocks '# '), and picks the placement that keeps the stack
low, flat and free of holes and clears the most lines (the usual
height/lines/holes/bumpiness weighting). It turns the piece with Up until
the shape on screen matches, slides it with Left and Right, and drops it
with Space, a key at a time at a human pace. After SECONDS (default 40)
it leaves the game with Esc and quits from the menu with q. Run by
record-preview.sh while asciinema records the pane."""
import subprocess, sys, time

SOCK, S = sys.argv[1], sys.argv[2]
PLAY = float(sys.argv[3]) if len(sys.argv) > 3 else 40.0
W, H = 10, 20

def tmux(*a): return subprocess.run(["tmux", "-L", SOCK, *a], capture_output=True, text=True).stdout
def key(*k):
    tmux("send-keys", "-t", S, *k)
    time.sleep(0.09)
def pane(): return tmux("capture-pane", "-p", "-t", S).split("\n")

def board():
    """(settled, piece): 20x10 booleans for the settled blocks and the set
    of (row, col) cells of the falling piece; None off the playfield."""
    rows = pane()
    top = next((i for i, l in enumerate(rows) if "_|" in l and "|_" in l), None)
    if top is None or top + 1 + H > len(rows):
        return None
    left = rows[top].index("_")     # the underscores span the inside
    settled, piece = [], set()
    for r in range(H):
        l = rows[top + 1 + r]
        row = []
        for c in range(W):
            cell = l[left + 2 * c:left + 2 * c + 2]
            row.append(cell[:1] == "#" and cell != "##")
            if cell == "##": piece.add((r, c))
        settled.append(row)
    return settled, piece

def norm(cells):
    r0 = min(r for r, c in cells); c0 = min(c for r, c in cells)
    return frozenset((r - r0, c - c0) for r, c in cells)

def rotations(shape):
    out, s = [], shape
    for _ in range(4):
        if s not in out: out.append(s)
        s = norm({(c, -r) for r, c in s})
    return out

def evaluate(g, shape, col):
    """drop shape at column col onto g; the score, or None if it can't go there"""
    if any(c + col < 0 or c + col >= W for r, c in shape): return None
    row = -min(r for r, c in shape)
    def fits(dr): return all(0 <= r + dr < H and not g[r + dr][c + col] for r, c in shape)
    if not fits(row):
        row = 0
        if not fits(0): return None
    while fits(row + 1): row += 1
    b = [list(x) for x in g]
    for r, c in shape: b[r + row][c + col] = True
    full = [r for r in range(H) if all(b[r])]
    b = [[False] * W for _ in full] + [b[r] for r in range(H) if r not in full]
    heights = [next((H - r for r in range(H) if b[r][c]), 0) for c in range(W)]
    holes = sum(1 for c in range(W) for r in range(H)
                if not b[r][c] and any(b[rr][c] for rr in range(r)))
    bump = sum(abs(heights[i] - heights[i + 1]) for i in range(W - 1))
    return -0.51 * sum(heights) + 0.76 * len(full) - 0.36 * holes - 0.18 * bump

def main():
    time.sleep(2)
    key("Enter"); time.sleep(0.8)          # 1-Player Game
    key("Enter"); time.sleep(1.2)          # start with the options shown
    key("Down"); time.sleep(0.5)           # any key past PRESS KEY
    t0 = time.time()
    while time.time() - t0 < PLAY:
        b = board()
        if b is None: break
        base, cur = b
        if len(cur) != 4 or max(r for r, c in cur) > H - 4:
            time.sleep(0.08)    # between pieces, or a line clear flashing
            continue
        best = None
        for shape in rotations(norm(cur)):
            for col in range(-3, W):
                s = evaluate(base, shape, col)
                if s is not None and (best is None or s > best[0]):
                    best = (s, shape, col)
        if best is None: break
        _, shape, col = best
        time.sleep(0.15)                    # a moment to think
        def whole():
            """the board once all four cells of the piece are in view
            (just after a turn, part of it can be above the field)"""
            for _ in range(20):
                b = board()
                if b is None or len(b[1]) == 4: return b
                time.sleep(0.05)
            return b
        for _ in range(3):                  # turn until the shape matches
            b = whole()
            if b is None or len(b[1]) != 4 or norm(b[1]) == shape: break
            key("Up")
        b = whole()
        if b and len(b[1]) == 4:
            dx = col - min(c for r, c in b[1])
            for _ in range(abs(dx)):
                key("Right" if dx > 0 else "Left")
        dropped = b[1] if b else set()
        key("Space")
        # wait for the dropped piece to settle and the next to appear
        end = time.time() + 2
        while time.time() < end:
            b = board()
            if b is None or (len(b[1]) == 4 and b[1] != dropped
                             and min(r for r, c in b[1]) < 3):
                break
            time.sleep(0.05)
        time.sleep(0.12)
    time.sleep(2)
    key("Escape"); time.sleep(1.5)
    for _ in range(3):
        rows = pane()
        if any("1-Player Game" in l for l in rows): break
        key("Escape"); time.sleep(1)
    time.sleep(1.5)
    key("q")

main()
