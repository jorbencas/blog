import type { APIRoute } from 'astro';

export const prerender = false;

// ============================================================
// CROSSCLIMB - Valid Spanish word pairs
// ============================================================
const CROSSCLIMB_PAIRS: { start: string; end: string }[] = [
  { start: "PATO", end: "GATO" },
  { start: "SOL", end: "SAL" },
  { start: "MAR", end: "MAL" },
  { start: "PAN", end: "PAS" },
  { start: "RED", end: "REF" },
  { start: "CASA", end: "CAMA" },
  { start: "MESA", end: "META" },
  { start: "LUNA", end: "MULA" },
  { start: "ROJO", end: "ROTO" },
  { start: "FUEGO", end: "JUEGO" },
  { start: "PLAYA", end: "PLAZA" },
  { start: "NIEVE", end: "LIEVE" },
  { start: "MANGO", end: "MANTO" },
  { start: "NARIZ", end: "PARIZ" },
  { start: "CARNE", end: "CARTE" },
  { start: "PERRO", end: "PERNO" },
  { start: "FLOR", end: "FLON" },
  { start: "AMOR", end: "AVOR" },
  { start: "CARRO", end: "CARPO" },
  { start: "VERDE", end: "CERDE" },
  { start: "TIERRA", end: "TIERSA" },
  { start: "PUERTA", end: "PUERTE" },
  { start: "VIENTO", end: "CUENTO" },
  { start: "CIELO", end: "FIELO" },
  { start: "GATO", end: "RATO" },
  { start: "PINO", end: "PISO" },
  { start: "SANO", end: "SALO" },
  { start: "TUBO", end: "TUNO" },
  { start: "HIJO", end: "BISO" },
  { start: "LAGO", end: "LAGO" },
];

function differsByOne(a: string, b: string): boolean {
  if (a.length !== b.length) return false;
  let diffs = 0;
  for (let i = 0; i < a.length; i++) {
    if (a[i] !== b[i]) diffs++;
  }
  return diffs === 1;
}

function generateCrossclimb(count: number) {
  const valid = CROSSCLIMB_PAIRS.filter(
    (p) => p.start !== p.end && p.start.length === p.end.length && differsByOne(p.start, p.end)
  );
  const shuffled = [...valid].sort(() => Math.random() - 0.5);
  return shuffled.slice(0, Math.min(count, shuffled.length));
}

// ============================================================
// QUEENS - Backtracking solver
// ============================================================
function generateQueensPuzzle(size: number = 7): {
  size: number;
  queens: number[][];
  regions: number[][][];
} | null {
  const queens: [number, number][] = [];

  function isSafe(row: number, col: number, placed: [number, number][]): boolean {
    for (const [r, c] of placed) {
      if (r === row || c === col) return false;
      if (Math.abs(r - row) === Math.abs(c - col)) return false;
    }
    return true;
  }

  function solve(row: number, placed: [number, number][]): boolean {
    if (row === size) return true;
    const cols = Array.from({ length: size }, (_, i) => i).sort(() => Math.random() - 0.5);
    for (const col of cols) {
      if (isSafe(row, col, placed)) {
        placed.push([row, col]);
        if (solve(row + 1, placed)) return true;
        placed.pop();
      }
    }
    return false;
  }

  if (!solve(0, queens)) return null;

  // Assign regions via BFS
  const regions: number[][][] = queens.map(() => []);
  const assigned = Array.from({ length: size }, () => Array(size).fill(-1));

  for (let i = 0; i < queens.length; i++) {
    const [qr, qc] = queens[i];
    regions[i].push([qr, qc]);
    assigned[qr][qc] = i;
  }

  const queue: [number, number, number][] = [];
  for (let i = 0; i < queens.length; i++) {
    const [qr, qc] = queens[i];
    for (const [dr, dc] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) {
      const nr = qr + dr;
      const nc = qc + dc;
      if (nr >= 0 && nr < size && nc >= 0 && nc < size && assigned[nr][nc] === -1) {
        queue.push([nr, nc, i]);
      }
    }
  }

  while (queue.length > 0) {
    const [r, c, owner] = queue.shift()!;
    if (assigned[r][c] !== -1) continue;
    if (regions[owner].length < size) {
      assigned[r][c] = owner;
      regions[owner].push([r, c]);
      for (const [dr, dc] of [[-1, 0], [1, 0], [0, -1], [0, 1]]) {
        const nr = r + dr;
        const nc = c + dc;
        if (nr >= 0 && nr < size && nc >= 0 && nc < size && assigned[nr][nc] === -1) {
          queue.push([nr, nc, owner]);
        }
      }
    }
  }

  // Assign remaining cells to nearest queen
  for (let r = 0; r < size; r++) {
    for (let c = 0; c < size; c++) {
      if (assigned[r][c] === -1) {
        let minD = Infinity;
        let best = 0;
        for (let i = 0; i < queens.length; i++) {
          const [qr, qc] = queens[i];
          const d = Math.abs(r - qr) + Math.abs(c - qc);
          if (d < minD) {
            minD = d;
            best = i;
          }
        }
        regions[best].push([r, c]);
        assigned[r][c] = best;
      }
    }
  }

  return { size, queens, regions };
}

function generateQueens(count: number, size: number = 7) {
  const puzzles = [];
  let attempts = 0;
  while (puzzles.length < count && attempts < count * 10) {
    attempts++;
    const p = generateQueensPuzzle(size);
    if (p) {
      // Verify no two queens attack
      let ok = true;
      for (let i = 0; i < p.queens.length && ok; i++) {
        for (let j = i + 1; j < p.queens.length && ok; j++) {
          const [r1, c1] = p.queens[i];
          const [r2, c2] = p.queens[j];
          if (r1 === r2 || c1 === c2 || Math.abs(r1 - r2) === Math.abs(c1 - c2)) {
            ok = false;
          }
        }
      }
      if (ok) puzzles.push(p);
    }
  }
  return puzzles;
}

// ============================================================
// TANGO - Backtracking grid generator
// ============================================================
function isTangoValid(grid: number[], idx: number, size: number): boolean {
  const row = Math.floor(idx / size);
  const col = idx % size;
  if (col >= 2) {
    const a = grid[row * size + col - 2];
    const b = grid[row * size + col - 1];
    const c = grid[idx];
    if (a !== 0 && a === b && b === c) return false;
  }
  if (row >= 2) {
    const a = grid[(row - 2) * size + col];
    const b = grid[(row - 1) * size + col];
    const c = grid[idx];
    if (a !== 0 && a === b && b === c) return false;
  }
  return true;
}

function fillTango(grid: number[], idx: number, size: number): boolean {
  if (idx === size * size) return true;
  const colors = [1, 2].sort(() => Math.random() - 0.5);
  for (const color of colors) {
    grid[idx] = color;
    if (isTangoValid(grid, idx, size) && fillTango(grid, idx + 1, size)) return true;
    grid[idx] = 0;
  }
  return false;
}

function generateTangoGrid(size: number = 6): number[] | null {
  for (let _ = 0; _ < 100; _++) {
    const grid = Array(size * size).fill(0);
    if (fillTango(grid, 0, size)) return grid;
  }
  return null;
}

function validateTango(grid: number[], size: number = 6): boolean {
  for (let r = 0; r < size; r++) {
    for (let c = 0; c < size - 2; c++) {
      const a = grid[r * size + c];
      const b = grid[r * size + c + 1];
      const cv = grid[r * size + c + 2];
      if (a !== 0 && a === b && b === cv) return false;
    }
  }
  for (let c = 0; c < size; c++) {
    for (let r = 0; r < size - 2; r++) {
      const a = grid[r * size + c];
      const b = grid[(r + 1) * size + c];
      const cv = grid[(r + 2) * size + c];
      if (a !== 0 && a === b && b === cv) return false;
    }
  }
  return !grid.some((v) => v === 0);
}

function generateTango(count: number, size: number = 6) {
  const puzzles = [];
  let attempts = 0;
  while (puzzles.length < count && attempts < count * 5) {
    attempts++;
    const g = generateTangoGrid(size);
    if (g && validateTango(g, size)) puzzles.push(g);
  }
  return puzzles;
}

// ============================================================
// ZIP - Backtracking with column constraints
// ============================================================
function generateZipGrid(size: number = 6): number[] | null {
  const grid: number[][] = Array.from({ length: size }, () => Array(size).fill(-1));

  function isValid(r: number, c: number, color: number): boolean {
    if (grid[r].filter((v) => v === color).length >= 2) return false;
    let colCount = 0;
    for (let rr = 0; rr < size; rr++) {
      if (grid[rr][c] === color) colCount++;
    }
    return colCount < 2;
  }

  function solve(idx: number): boolean {
    if (idx === size * size) return true;
    const r = Math.floor(idx / size);
    const c = idx % size;
    const colors = [0, 1, 2].sort(() => Math.random() - 0.5);
    for (const color of colors) {
      if (isValid(r, c, color)) {
        grid[r][c] = color;
        if (solve(idx + 1)) return true;
        grid[r][c] = -1;
      }
    }
    return false;
  }

  for (let _ = 0; _ < 100; _++) {
    for (let r = 0; r < size; r++) grid[r].fill(-1);
    if (solve(0)) return grid.flat();
  }
  return null;
}

function validateZip(grid: number[], size: number = 6): boolean {
  if (grid.length !== size * size) return false;
  for (let r = 0; r < size; r++) {
    const row = grid.slice(r * size, (r + 1) * size);
    for (let color = 0; color < 3; color++) {
      if (row.filter((v) => v === color).length !== 2) return false;
    }
  }
  for (let c = 0; c < size; c++) {
    const col = Array.from({ length: size }, (_, r) => grid[r * size + c]);
    for (let color = 0; color < 3; color++) {
      if (col.filter((v) => v === color).length !== 2) return false;
    }
  }
  return true;
}

function generateZip(count: number, size: number = 6) {
  const puzzles = [];
  let attempts = 0;
  while (puzzles.length < count && attempts < count * 5) {
    attempts++;
    const g = generateZipGrid(size);
    if (g && validateZip(g, size)) puzzles.push(g);
  }
  return puzzles;
}

// ============================================================
// API ENDPOINT
// ============================================================
export const GET: APIRoute = async ({ url }) => {
  const game = url.searchParams.get("game") || "all";
  const count = Math.min(parseInt(url.searchParams.get("count") || "25", 10), 50);

  const result: Record<string, unknown> = {};
  const start = Date.now();

  if (game === "all" || game === "crossclimb") {
    result.crossclimb = generateCrossclimb(count);
  }
  if (game === "all" || game === "queens") {
    result.queens = generateQueens(count);
  }
  if (game === "all" || game === "tango") {
    result.tango = generateTango(count);
  }
  if (game === "all" || game === "zip") {
    result.zip = generateZip(count);
  }

  const elapsed = Date.now() - start;

  return new Response(
    JSON.stringify({
      ...result,
      meta: {
        game,
        count,
        generatedIn: `${elapsed}ms`,
        timestamp: new Date().toISOString(),
      },
    }, null, 2),
    {
      headers: {
        "Content-Type": "application/json; charset=utf-8",
        "Cache-Control": "no-store",
      },
    }
  );
};
