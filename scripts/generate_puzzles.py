#!/usr/bin/env python3
"""Generate and validate all puzzles for JuegosLogicos — 25 of each type."""
import json
import random
import sys
from collections import deque
from itertools import permutations

# ============================================================
# CROSSCLIMB - Expanded curated word pairs
# ============================================================
CROSSCLIMB_VALID = [
    # 3-letter
    {"start": "PATO", "end": "GATO"},
    {"start": "SOL", "end": "SAL"},
    {"start": "MAR", "end": "MAL"},
    {"start": "PAN", "end": "PAS"},
    {"start": "RED", "end": "REF"},
    {"start": "TRE", "end": "TRE"},
    {"start": "LEN", "end": "LEX"},
    {"start": "MOL", "end": "POL"},
    {"start": "RAT", "end": "ROT"},
    {"start": "VOL", "end": "BOL"},
    # 4-letter
    {"start": "CASA", "end": "CAMA"},
    {"start": "MESA", "end": "META"},
    {"start": "LUNA", "end": "MULA"},
    {"start": "ROJO", "end": "ROTO"},
    {"start": "FUEGO", "end": "JUEGO"},
    {"start": "PLAYA", "end": "PLAZA"},
    {"start": "NIEVE", "end": "LIEVE"},
    {"start": "MANGO", "end": "MANTO"},
    {"start": "NARIZ", "end": "PARIZ"},
    {"start": "CARNE", "end": "CARTE"},
    {"start": "LECHE", "end": "LECHE"},
    {"start": "BOLSA", "end": "BOLSA"},
    {"start": "TIERRA", "end": "TIERSA"},
    {"start": "PUERTA", "end": "PUERTE"},
    {"start": "VIENTO", "end": "CUENTO"},
    {"start": "CIELO", "end": "FIELO"},
    {"start": "PIANO", "end": "PIANO"},
    {"start": "CAMPO", "end": "CANPO"},
    {"start": "TIGRE", "end": "TIGRE"},
    {"start": "LIBRO", "end": "LIBRO"},
    {"start": "PERRO", "end": "PERNO"},
    {"start": "FLOR", "end": "FLON"},
    {"start": "AMOR", "end": "AVOR"},
    {"start": "CARRO", "end": "CARPO"},
    {"start": "VERDE", "end": "CERDE"},
    {"start": "RATON", "end": "RATION"},
    {"start": "HIJO", "end": "BISO"},
    {"start": "GATO", "end": "RATO"},
    {"start": "CAMA", "end": "CAPA"},
    {"start": "TAPA", "end": "TAREA"},
    {"start": "SANO", "end": "SALO"},
    {"start": "PINO", "end": "PISO"},
    {"start": "RUBI", "end": "RUDO"},
    {"start": "TUBO", "end": "TUNO"},
    {"start": "LAGO", "end": "LAGO"},
    {"start": "NARIZ", "end": "NARIS"},
]


def differs_by_one(a, b):
    if len(a) != len(b):
        return False
    return sum(1 for x, y in zip(a, b) if x != y) == 1


def generate_crossclimb(count=25):
    valid = []
    for pair in CROSSCLIMB_VALID:
        s, e = pair["start"].upper(), pair["end"].upper()
        if s == e:
            continue
        if len(s) != len(e):
            continue
        if not differs_by_one(s, e):
            continue
        valid.append({"start": s, "end": e})
    random.shuffle(valid)
    return valid[:count]


# ============================================================
# QUEENS - Backtracking solver
# ============================================================
def generate_queens_puzzle(size=7):
    queens = []

    def is_safe(row, col, placed):
        for r, c in placed:
            if r == row or c == col:
                return False
            if abs(r - row) == abs(c - col):
                return False
        return True

    def solve(row, placed):
        if row == size:
            return True
        cols = list(range(size))
        random.shuffle(cols)
        for col in cols:
            if is_safe(row, col, placed):
                placed.append((row, col))
                if solve(row + 1, placed):
                    return True
                placed.pop()
        return False

    if solve(0, queens):
        regions = assign_regions(queens, size)
        return {
            "size": size,
            "queens": [list(q) for q in queens],
            "regions": regions,
        }
    return None


def assign_regions(queens, size):
    regions = [[] for _ in queens]
    assigned = [[-1] * size for _ in range(size)]

    for i, (qr, qc) in enumerate(queens):
        regions[i].append([qr, qc])
        assigned[qr][qc] = i

    queue = deque()
    for i, (qr, qc) in enumerate(queens):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = qr + dr, qc + dc
            if 0 <= nr < size and 0 <= nc < size and assigned[nr][nc] == -1:
                queue.append((nr, nc, i))

    target = size
    while queue:
        r, c, owner = queue.popleft()
        if assigned[r][c] != -1:
            continue
        if len(regions[owner]) < target:
            assigned[r][c] = owner
            regions[owner].append([r, c])
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = r + dr, c + dc
                if 0 <= nr < size and 0 <= nc < size and assigned[nr][nc] == -1:
                    queue.append((nr, nc, owner))

    for r in range(size):
        for c in range(size):
            if assigned[r][c] == -1:
                min_d = float("inf")
                best = 0
                for i, (qr, qc) in enumerate(queens):
                    d = abs(r - qr) + abs(c - qc)
                    if d < min_d:
                        min_d = d
                        best = i
                regions[best].append([r, c])
                assigned[r][c] = best

    return regions


def generate_queens(count=25, size=7):
    puzzles = []
    attempts = 0
    while len(puzzles) < count and attempts < count * 10:
        attempts += 1
        p = generate_queens_puzzle(size)
        if p:
            # Verify no two queens attack each other
            qs = p["queens"]
            ok = True
            for i in range(len(qs)):
                for j in range(i + 1, len(qs)):
                    r1, c1 = qs[i]
                    r2, c2 = qs[j]
                    if r1 == r2 or c1 == c2 or abs(r1 - r2) == abs(c1 - c2):
                        ok = False
                        break
                if not ok:
                    break
            if ok:
                puzzles.append(p)
    return puzzles


# ============================================================
# TANGO - Backtracking grid generator
# ============================================================
def is_tango_valid(grid, idx, size):
    row = idx // size
    col = idx % size
    if col >= 2:
        a = grid[row * size + col - 2]
        b = grid[row * size + col - 1]
        c = grid[idx]
        if a != 0 and a == b and b == c:
            return False
    if row >= 2:
        a = grid[(row - 2) * size + col]
        b = grid[(row - 1) * size + col]
        c = grid[idx]
        if a != 0 and a == b and b == c:
            return False
    return True


def fill_tango(grid, idx, size):
    if idx == len(grid):
        return True
    colors = [1, 2]
    random.shuffle(colors)
    for color in colors:
        grid[idx] = color
        if is_tango_valid(grid, idx, size):
            if fill_tango(grid, idx + 1, size):
                return True
        grid[idx] = 0
    return False


def generate_tango_grid(size=6):
    for _ in range(100):
        grid = [0] * (size * size)
        if fill_tango(grid, 0, size):
            return grid
    return None


def validate_tango(grid, size=6):
    for r in range(size):
        for c in range(size - 2):
            a = grid[r * size + c]
            b = grid[r * size + c + 1]
            cv = grid[r * size + c + 2]
            if a != 0 and a == b and b == cv:
                return False
    for c in range(size):
        for r in range(size - 2):
            a = grid[r * size + c]
            b = grid[(r + 1) * size + c]
            cv = grid[(r + 2) * size + c]
            if a != 0 and a == b and b == cv:
                return False
    if any(v == 0 for v in grid):
        return False
    return True


def generate_tango(count=25, size=6):
    puzzles = []
    attempts = 0
    while len(puzzles) < count and attempts < count * 5:
        attempts += 1
        g = generate_tango_grid(size)
        if g and validate_tango(g, size):
            puzzles.append(g)
    return puzzles


# ============================================================
# ZIP - Backtracking with column constraints
# ============================================================
def generate_zip_grid(size=6):
    grid = [[-1] * size for _ in range(size)]

    def is_valid(r, c, color):
        if grid[r].count(color) >= 2:
            return False
        col_count = sum(1 for rr in range(size) if grid[rr][c] == color)
        if col_count >= 2:
            return False
        return True

    def solve(idx):
        if idx == size * size:
            return True
        r, c = idx // size, idx % size
        colors = [0, 1, 2]
        random.shuffle(colors)
        for color in colors:
            if is_valid(r, c, color):
                grid[r][c] = color
                if solve(idx + 1):
                    return True
                grid[r][c] = -1
        return False

    for _ in range(100):
        grid = [[-1] * size for _ in range(size)]
        if solve(0):
            return [grid[r][c] for r in range(size) for c in range(size)]
    return None


def validate_zip(grid, size=6):
    if len(grid) != size * size:
        return False
    for r in range(size):
        row = grid[r * size : (r + 1) * size]
        for color in range(3):
            if row.count(color) != 2:
                return False
    for c in range(size):
        col = [grid[r * size + c] for r in range(size)]
        for color in range(3):
            if col.count(color) != 2:
                return False
    return True


def generate_zip(count=25, size=6):
    puzzles = []
    attempts = 0
    while len(puzzles) < count and attempts < count * 5:
        attempts += 1
        g = generate_zip_grid(size)
        if g and validate_zip(g, size):
            puzzles.append(g)
    return puzzles


# ============================================================
# MAIN
# ============================================================
if __name__ == "__main__":
    count = int(sys.argv[1]) if len(sys.argv) > 1 else 25
    puzzles = {}

    print(f"=== Generating {count} puzzles of each type ===\n")

    print("CROSSCLIMB...")
    puzzles["crossclimb"] = generate_crossclimb(count)
    print(f"  -> {len(puzzles['crossclimb'])} pairs")

    print("QUEENS...")
    puzzles["queens"] = generate_queens(count)
    print(f"  -> {len(puzzles['queens'])} puzzles")

    print("TANGO...")
    puzzles["tango"] = generate_tango(count)
    print(f"  -> {len(puzzles['tango'])} grids")

    print("ZIP...")
    puzzles["zip"] = generate_zip(count)
    print(f"  -> {len(puzzles['zip'])} solutions")

    # Save to component folder
    output = "/home/jorge/dev/blog/src/components/juegos_logicos_puzzles.json"
    with open(output, "w") as f:
        json.dump(puzzles, f, indent=2)
    print(f"\nSaved to {output}")

    # Also save a copy to public for API access
    import shutil
    public_output = "/home/jorge/dev/blog/public/juegos_logicos_puzzles.json"
    shutil.copy2(output, public_output)
    print(f"Copied to {public_output}")
