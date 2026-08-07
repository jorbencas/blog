<script>
  import { onMount } from 'svelte';
  import puzzles from './juegos_logicos_puzzles.json';

  let activeGame = $state("pinpoint");

  // ============================================================
  // PINPOINT - Adivina la palabra con pistas progresivas
  // ============================================================
  const PINPOINT_WORDS = [
    { word: "ELEFANTE", hints: ["Animal", "Trompa", "Grande", "Paquidermo", "Safari", "Circus"] },
    { word: "GUITARRA", hints: ["Instrumento", "Cuerdas", "Música", "Acústica", "Rock", "Vibras"] },
    { word: "BIBLIOTECA", hints: ["Lugar", "Libros", "Lectura", "Préstamo", "Silencio", "Estanterías"] },
    { word: "CAFETERA", hints: ["Cocina", "Café", "Máquina", "Aromática", "Mañana", "Filtrado"] },
    { word: "MARIPOSA", hints: ["Insecto", "Vuelo", "Alas", "Colores", "Jardín", "Transformación"] },
    { word: "TELÉFONO", hints: ["Comunicación", "Pantalla", "Llamadas", "Móvil", "Contactos", "Selfie"] },
    { word: "DICCIONARIO", hints: ["Referencia", "Palabras", "Definiciones", "Letra", "Escritura", "Significado"] },
    { word: "MONTAÑA", hints: ["Naturaleza", "Altura", "Escalada", "Paisaje", "Nieve", "Cumbre"] },
    { word: "HOSPITAL", hints: ["Salud", "Médicos", "Pacientes", "Urgencias", "Camas", "Cirugía"] },
    { word: "PLANETA", hints: ["Espacio", "Tierra", "Órbita", "Sistema solar", "Gravity", "Azul"] },
    { word: "RELÓGIO", hints: ["Tiempo", "Manecillas", "Pulsera", "Cuarzo", "Alarma", "Digital"] },
    { word: "CANGREJO", hints: ["Mar", "Pinzas", "Caparazón", "Playa", "Movimiento lateral", "Mariscos"] },
    { word: "AEROPUERTO", hints: ["Viajes", "Aviones", "Vuelos", "Equipaje", "Pasaporte", "Terminal"] },
    { word: "PIRÁMIDE", hints: ["Egipto", "Faraón", "Arena", "Antigua", "Triángulo", "Sangre"] },
    { word: "CHOCOLATE", hints: ["Dulce", "Cacao", "Tableta", "Tostado", "Suizo", "Postre"] },
  ];

  let ppWord = $state(null);
  let ppHintIndex = $state(0);
  let ppGuess = $state("");
  let ppWon = $state(false);
  let ppLost = $state(false);
  let ppMessage = $state("");
  let ppHistory = $state([]);

  function ppStartNew() {
    ppWord = PINPOINT_WORDS[Math.floor(Math.random() * PINPOINT_WORDS.length)];
    ppHintIndex = 0;
    ppGuess = "";
    ppWon = false;
    ppLost = false;
    ppMessage = "";
    ppHistory = [];
  }

  function ppGuessWord() {
    if (!ppGuess.trim() || ppWon || ppLost) return;
    const guess = ppGuess.trim().toUpperCase();
    ppHistory.push({ guess, hint: ppHintIndex + 1, correct: guess === ppWord.word });
    if (guess === ppWord.word) {
      ppWon = true;
      ppMessage = `¡Correcto! La palabra era "${ppWord.word}" en ${ppHintIndex + 1} pista(s).`;
    } else if (ppHintIndex >= ppWord.hints.length - 1) {
      ppLost = true;
      ppMessage = `La palabra era "${ppWord.word}". ¡Mejor suerte la próxima vez!`;
    } else {
      ppHintIndex = Math.min(ppHintIndex + 1, ppWord.hints.length - 1);
      ppMessage = "Incorrecto. Pista nueva desbloqueada.";
    }
    ppGuess = "";
  }

  // ============================================================
  // CROSSCLIMB - Escalera de palabras (pre-validated pairs)
  // ============================================================
  let ccPair = $state(null);
  let ccUserPath = $state([]);
  let ccInput = $state("");
  let ccWon = $state(false);
  let ccLost = $state(false);
  let ccMessage = $state("");
  let ccHistory = $state([]);

  function ccStartNew() {
    ccPair = puzzles.crossclimb[Math.floor(Math.random() * puzzles.crossclimb.length)];
    ccUserPath = [ccPair.start.toUpperCase()];
    ccInput = "";
    ccWon = false;
    ccLost = false;
    ccMessage = `Cambia UNA letra de "${ccPair.start}" para llegar a "${ccPair.end}"`;
    ccHistory = [];
  }

  function ccDiffersByOne(a, b) {
    if (a.length !== b.length) return false;
    let diffs = 0;
    for (let i = 0; i < a.length; i++) {
      if (a[i] !== b[i]) diffs++;
    }
    return diffs === 1;
  }

  function ccStep() {
    if (!ccInput.trim() || ccWon || ccLost) return;
    const word = ccInput.trim().toUpperCase();
    const last = ccUserPath[ccUserPath.length - 1];
    if (!ccDiffersByOne(last, word)) {
      ccMessage = `"${word}" no difiere en UNA sola letra de "${last}".`;
      return;
    }
    ccUserPath.push(word);
    ccHistory.push(word);
    if (word === ccPair.end.toUpperCase()) {
      ccWon = true;
      ccMessage = `¡Llegaste a "${ccPair.end}" en ${ccUserPath.length - 1} paso(s)!`;
    } else if (ccUserPath.length > 12) {
      ccLost = true;
      ccMessage = `Demasiados pasos (${ccUserPath.length - 1}). La ruta óptima era más corta. Intenta de nuevo.`;
    } else {
      ccMessage = `Ahora desde "${word}" → llega a "${ccPair.end}"`;
    }
    ccInput = "";
  }

  // ============================================================
  // QUEENS - Pre-generated solvable puzzles
  // ============================================================
  const QUEENS_COLORS = ["#ef4444", "#3b82f6", "#22c55e", "#f59e0b", "#a855f7", "#ec4899", "#06b6d4"];
  let qSize = $state(7);
  let qPuzzle = $state(null);
  let qQueens = $state([]);
  let qMessage = $state("");
  let qWon = $state(false);

  function qInit() {
    qPuzzle = puzzles.queens[Math.floor(Math.random() * puzzles.queens.length)];
    qSize = qPuzzle.size;
    qQueens = [];
    qMessage = "";
    qWon = false;
  }

  function qCellRegion(cellIdx) {
    if (!qPuzzle) return -1;
    const row = Math.floor(cellIdx / qSize);
    const col = cellIdx % qSize;
    for (let r = 0; r < qPuzzle.regions.length; r++) {
      for (const [rr, cc] of qPuzzle.regions[r]) {
        if (rr === row && cc === col) return r;
      }
    }
    return -1;
  }

  function qCellColor(cellIdx) {
    const ri = qCellRegion(cellIdx);
    return QUEENS_COLORS[ri % QUEENS_COLORS.length];
  }

  function qToggleQueen(cellIdx) {
    if (qWon) return;
    const existingIdx = qQueens.indexOf(cellIdx);
    if (existingIdx !== -1) {
      qQueens.splice(existingIdx, 1);
    } else {
      qQueens.push(cellIdx);
    }
    qQueens = [...qQueens];
    qCheckWin();
  }

  function qIsAttacked(cellIdx) {
    const row = Math.floor(cellIdx / qSize);
    const col = cellIdx % qSize;
    for (const q of qQueens) {
      const qr = Math.floor(q / qSize);
      const qc = q % qSize;
      if (qr === row && qc === col) continue;
      if (qr === row || qc === col) return true;
      if (Math.abs(qr - row) === Math.abs(qc - col)) return true;
    }
    return false;
  }

  function qCheckWin() {
    if (qQueens.length !== qSize) return;
    for (const q of qQueens) {
      if (qIsAttacked(q)) return;
    }
    for (const region of qPuzzle.regions) {
      if (!region.some(([r, c]) => qQueens.includes(r * qSize + c))) return;
    }
    qWon = true;
    qMessage = `¡Correcto! ${qSize} reinas colocadas sin conflicto.`;
  }

  // ============================================================
  // TANGO - Pre-generated valid grids, clear cells for player
  // ============================================================
  let tSize = $state(6);
  let tSolution = $state([]);
  let tGrid = $state([]);
  let tRevealed = $state([]);
  let tMessage = $state("");
  let tWon = $state(false);

  function tInit() {
    tSolution = puzzles.tango[Math.floor(Math.random() * puzzles.tango.length)];
    tSize = 6;
    // Reveal ~40% of cells as hints
    tRevealed = Array.from({ length: 36 }, () => false);
    let revealed = 0;
    while (revealed < 14) {
      const idx = Math.floor(Math.random() * 36);
      if (!tRevealed[idx]) {
        tRevealed[idx] = true;
        revealed++;
      }
    }
    tGrid = tSolution.map((v, i) => tRevealed[i] ? v : 0);
    tMessage = "Rellena las celdas vacías. No puede haber 3+ del mismo color seguidas en fila o columna.";
    tWon = false;
  }

  function tToggleCell(idx) {
    if (tWon || tRevealed[idx]) return;
    tGrid[idx] = tGrid[idx] === 0 ? 1 : tGrid[idx] === 1 ? 2 : 0;
    tGrid = [...tGrid];
    tCheckWin();
  }

  function tCheckWin() {
    const n = tSize;
    // Check no 3+ consecutive in rows
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n - 2; c++) {
        const a = tGrid[r * n + c];
        const b = tGrid[r * n + c + 1];
        const d = tGrid[r * n + c + 2];
        if (a !== 0 && a === b && b === d) return;
      }
    }
    // Check no 3+ consecutive in cols
    for (let c = 0; c < n; c++) {
      for (let r = 0; r < n - 2; r++) {
        const a = tGrid[r * n + c];
        const b = tGrid[(r + 1) * n + c];
        const d = tGrid[(r + 2) * n + c];
        if (a !== 0 && a === b && b === d) return;
      }
    }
    // Check all filled
    if (tGrid.some(v => v === 0)) return;
    tWon = true;
    tMessage = "¡Correcto! Sin tres seguidas del mismo color.";
  }

  // ============================================================
  // ZIP - Pre-generated valid solutions, clear all for player
  // ============================================================
  let zSize = $state(6);
  let zSolution = $state([]);
  let zGrid = $state([]);
  let zMessage = $state("");
  let zWon = $state(false);

  function zInit() {
    zSolution = puzzles.zip[Math.floor(Math.random() * puzzles.zip.length)];
    zSize = 6;
    zGrid = Array(36).fill(-1);
    zMessage = "Rellena cada celda. Cada fila y columna debe tener exactamente 2 de cada color (3 colores).";
    zWon = false;
  }

  function zCycleColor(idx) {
    if (zWon) return;
    zGrid[idx] = (zGrid[idx] + 1) % 3;
    zGrid = [...zGrid];
    zCheckWin();
  }

  function zCheckWin() {
    if (zGrid.some(v => v === -1)) return;
    const n = zSize;
    // Check rows
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < 3; c++) {
        let count = 0;
        for (let col = 0; col < n; col++) {
          if (zGrid[r * n + col] === c) count++;
        }
        if (count !== 2) return;
      }
    }
    // Check cols
    for (let c = 0; c < n; c++) {
      for (let clr = 0; clr < 3; clr++) {
        let count = 0;
        for (let r = 0; r < n; r++) {
          if (zGrid[r * n + c] === clr) count++;
        }
        if (count !== 2) return;
      }
    }
    zWon = true;
    zMessage = "¡Correcto! Distribución balanceada.";
  }

  function setGame(game) {
    activeGame = game;
  }

  onMount(() => {
    ppStartNew();
    ccStartNew();
    qInit();
    tInit();
    zInit();
  });
</script>

<div class="juegos-wrapper text-slate-800 dark:text-slate-100">
  <div class="tabs-navigation bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
    <button type="button" class="tab-btn text-slate-600 dark:text-slate-400" class:active={activeGame === 'pinpoint'} onclick={() => setGame('pinpoint')}>🎯 Pinpoint</button>
    <button type="button" class="tab-btn text-slate-600 dark:text-slate-400" class:active={activeGame === 'crossclimb'} onclick={() => setGame('crossclimb')}>🪜 Crossclimb</button>
    <button type="button" class="tab-btn text-slate-600 dark:text-slate-400" class:active={activeGame === 'queens'} onclick={() => setGame('queens')}>♛ Queens</button>
    <button type="button" class="tab-btn text-slate-600 dark:text-slate-400" class:active={activeGame === 'tango'} onclick={() => setGame('tango')}>💃 Tango</button>
    <button type="button" class="tab-btn text-slate-600 dark:text-slate-400" class:active={activeGame === 'zip'} onclick={() => setGame('zip')}>📦 Zip</button>
  </div>

  <div class="game-card bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-xl p-5">

    <!-- PINPOINT -->
    {#if activeGame === 'pinpoint'}
      <div class="game-content">
        <h2 class="game-title text-slate-900 dark:text-white">🎯 Pinpoint</h2>
        <p class="game-desc text-slate-500 dark:text-slate-400">Adivina la palabra oculta. Empiezas con 1 pista; cada error desbloquea la siguiente. La pista #6 es la más directa.</p>
        <div class="rules-box bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-lg p-3 text-sm text-slate-600 dark:text-slate-400">
          <strong>Reglas:</strong> Escribe una palabra y pulsa Enter. Si fallas, se muestra una pista nueva. Gana el que adivine en menos intentos. Máximo 6 pistas.
        </div>
        {#if !ppWord}
          <button type="button" class="btn btn-primary" onclick={ppStartNew}>Empezar</button>
        {:else}
          {#if ppWon}
            <div class="result-banner win-banner">
              <div class="result-icon">🎉</div>
              <div class="result-text">
                <span class="result-title">¡Victoria!</span>
                <span class="result-detail">Adivinaste "{ppWord.word}" en {ppHistory.length} intento(s)</span>
              </div>
            </div>
          {:else if ppLost}
            <div class="result-banner lose-banner">
              <div class="result-icon">😔</div>
              <div class="result-text">
                <span class="result-title">¡Derrota!</span>
                <span class="result-detail">La palabra era "{ppWord.word}"</span>
              </div>
            </div>
          {/if}
          <div class="hints-list">
            {#each ppWord.hints.slice(0, ppHintIndex + 1) as hint, i}
              <div class="hint-pill" class:hint-current={i === ppHintIndex && !ppWon && !ppLost}>
                Pista {i + 1}/6: {hint}
              </div>
            {/each}
          </div>
          {#if !ppWon && !ppLost}
            <div class="input-row">
              <input type="text" bind:value={ppGuess} placeholder="Tu guess..." class="game-input bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100"
                onkeydown={(e) => e.key === 'Enter' && ppGuessWord()} />
              <button type="button" class="btn btn-primary" onclick={ppGuessWord}>Adivinar</button>
            </div>
          {/if}
          {#if ppHistory.length > 0}
            <div class="history">
              {#each ppHistory as h, i}
                <span class="history-item" class:correct={h.correct}>{#if h.correct}✓{:else}✗{/if} #{i + 1} {h.guess}</span>
              {/each}
            </div>
          {/if}
          <button type="button" class="btn btn-secondary mt-3" onclick={ppStartNew}>Nueva palabra</button>
        {/if}
      </div>

    <!-- CROSSCLIMB -->
    {:else if activeGame === 'crossclimb'}
      <div class="game-content">
        <h2 class="game-title text-slate-900 dark:text-white">🪜 Crossclimb</h2>
        <p class="game-desc text-slate-500 dark:text-slate-400">Conecta "{ccPair?.start}" con "{ccPair?.end}" cambiando UNA letra en cada paso.</p>
        <div class="rules-box bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-lg p-3 text-sm text-slate-600 dark:text-slate-400">
          <strong>Reglas:</strong> Cada palabra nueva debe diferir en exactamente 1 letra de la anterior. Misma longitud. Ejemplo: PATO → GATO (cambia P→G). Intenta llegar en el menor número de pasos.
        </div>
        {#if ccPair}
          {#if ccWon}
            <div class="result-banner win-banner">
              <div class="result-icon">🎉</div>
              <div class="result-text">
                <span class="result-title">¡Llegaste!</span>
                <span class="result-detail">{ccPair.start} → {ccPair.end} en {ccUserPath.length - 1} paso(s)</span>
              </div>
            </div>
          {:else if ccLost}
            <div class="result-banner lose-banner">
              <div class="result-icon">😔</div>
              <div class="result-text">
                <span class="result-title">Demasiados pasos</span>
                <span class="result-detail">{ccUserPath.length - 1} pasos. Intenta una ruta más corta.</span>
              </div>
            </div>
          {/if}
          <div class="ladder">
            {#each ccUserPath as word, i}
              <div class="ladder-step" class:step-first={i === 0} class:step-current={i === ccUserPath.length - 1 && !ccWon} class:step-end={word === ccPair.end.toUpperCase()}>
                <span class="step-num text-slate-400 dark:text-slate-500">{i}.</span>
                <span class="step-word text-slate-900 dark:text-white">{word}</span>
              </div>
            {/each}
          </div>
          {#if !ccWon && !ccLost}
            <p class="text-sm text-slate-500 dark:text-slate-400">
              Pasos: {ccUserPath.length - 1} | Palabras de {ccPair.start.length} letras
            </p>
            <div class="input-row">
              <input type="text" bind:value={ccInput} placeholder="Siguiente palabra..." class="game-input bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100"
                onkeydown={(e) => e.key === 'Enter' && ccStep()} />
              <button type="button" class="btn btn-primary" onclick={ccStep}>Paso</button>
            </div>
          {/if}
          {#if ccMessage && !ccWon && !ccLost}
            <div class="game-message">{ccMessage}</div>
          {/if}
          <button type="button" class="btn btn-secondary mt-3" onclick={ccStartNew}>Nueva escalera</button>
        {/if}
      </div>

    <!-- QUEENS -->
    {:else if activeGame === 'queens'}
      <div class="game-content">
        <h2 class="game-title text-slate-900 dark:text-white">♛ Queens</h2>
        <p class="game-desc text-slate-500 dark:text-slate-400">Coloca {qSize} reinas en un tablero {qSize}×{qSize} sin que se ataquen entre sí.</p>
        <div class="rules-box bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-lg p-3 text-sm text-slate-600 dark:text-slate-400">
          <strong>Reglas:</strong> 1 reina por fila, 1 por columna, 1 por región de color. Las reinas no pueden compartir fila, columna ni diagonal. Clic para colocar/quitar. Las celdas en rojo están atacadas.
        </div>
        {#if qWon}
          <div class="result-banner win-banner">
            <div class="result-icon">🎉</div>
            <div class="result-text">
              <span class="result-title">¡Tablero resuelto!</span>
              <span class="result-detail">{qSize} reinas colocadas sin conflicto</span>
            </div>
          </div>
        {/if}
        {#if qPuzzle}
          <div class="queens-grid" style="grid-template-columns: repeat({qSize}, 1fr);">
            {#each Array(qSize * qSize) as _, i}
              {@const regionColor = qCellColor(i)}
              {@const isQueen = qQueens.includes(i)}
              {@const attacked = qIsAttacked(i)}
              <button type="button"
                class="queen-cell"
                class:has-queen={isQueen}
                class:attacked={attacked && !isQueen}
                style="background-color: {regionColor}22; border-color: {regionColor}44;"
                onclick={() => qToggleQueen(i)}>
                {#if isQueen}♛{/if}
              </button>
            {/each}
          </div>
          <div class="legend text-slate-500 dark:text-slate-400">
            <span class="legend-item">♛ = reina colocada</span>
            <span class="legend-item" style="color: #ef4444;">■ = celda atacada</span>
            <span class="legend-item">{qQueens.length}/{qSize} reinas</span>
            <span class="legend-item">Tablero {qSize}×{qSize}</span>
            <span class="legend-item">Clic para colocar/quitar</span>
          </div>
        {/if}
        <button type="button" class="btn btn-secondary mt-3" onclick={qInit}>Nuevo tablero</button>
      </div>

    <!-- TANGO -->
    {:else if activeGame === 'tango'}
      <div class="game-content">
        <h2 class="game-title text-slate-900 dark:text-white">💃 Tango</h2>
        <p class="game-desc text-slate-500 dark:text-slate-400">Completa la cuadrícula 6×6 con dos colores sin crear bloques de 3+ iguales.</p>
        <div class="rules-box bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-lg p-3 text-sm text-slate-600 dark:text-slate-400">
          <strong>Reglas:</strong> Clic en las celdas vacías para alternar entre ● Azul y ○ Naranja. Las celdas gris ya están fijas y no se pueden cambiar. No pueden haber 3+ del mismo color seguidas en fila ni en columna.
        </div>
        {#if tWon}
          <div class="result-banner win-banner">
            <div class="result-icon">🎉</div>
            <div class="result-text">
              <span class="result-title">¡Completado!</span>
              <span class="result-detail">Sin tres seguidas del mismo color</span>
            </div>
          </div>
        {/if}
        <div class="tango-grid" style="grid-template-columns: repeat({tSize}, 1fr);">
          {#each tGrid as cell, i}
            <button type="button"
              class="tango-cell"
              class:cell-a={cell === 1}
              class:cell-b={cell === 2}
              class:cell-revealed={tRevealed[i]}
              onclick={() => tToggleCell(i)}>
              {#if cell === 1}●{:else if cell === 2}○{/if}
            </button>
          {/each}
        </div>
          <div class="legend text-slate-500 dark:text-slate-400">
            <span class="legend-item">● Azul | ○ Naranja | Vacío</span>
            <span class="legend-item">Gris = bloqueado (no se cambia)</span>
            <span class="legend-item">Clic para alternar color</span>
          </div>
        <button type="button" class="btn btn-secondary mt-3" onclick={tInit}>Nuevo tablero</button>
      </div>

    <!-- ZIP -->
    {:else if activeGame === 'zip'}
      <div class="game-content">
        <h2 class="game-title text-slate-900 dark:text-white">📦 Zip</h2>
        <p class="game-desc text-slate-500 dark:text-slate-400">Distribuye 3 colores en una cuadrícula 6×6 respetando la proporción exacta.</p>
        <div class="rules-box bg-slate-50 dark:bg-slate-800/50 border border-slate-200 dark:border-slate-700 rounded-lg p-3 text-sm text-slate-600 dark:text-slate-400">
          <strong>Reglas:</strong> Clic en una celda para ciclar entre 🔴 Rojo, 🔵 Azul y 🟢 Verde. Cada fila y cada columna debe tener exactamente 2 de cada color. Rellena las 36 celdas.
        </div>
        {#if zWon}
          <div class="result-banner win-banner">
            <div class="result-icon">🎉</div>
            <div class="result-text">
              <span class="result-title">¡Distribución perfecta!</span>
              <span class="result-detail">2 de cada color en cada fila y columna</span>
            </div>
          </div>
        {/if}
        <div class="zip-grid" style="grid-template-columns: repeat({zSize}, 1fr);">
          {#each zGrid as cell, i}
            <button type="button"
              class="zip-cell"
              class:z-red={cell === 0}
              class:z-blue={cell === 1}
              class:z-green={cell === 2}
              onclick={() => zCycleColor(i)}>
              {#if cell >= 0}{['🔴', '🔵', '🟢'][cell]}{:else}?{/if}
            </button>
          {/each}
        </div>
          <div class="legend text-slate-500 dark:text-slate-400">
            <span class="legend-item">🔴 Rojo | 🔵 Azul | 🟢 Verde</span>
            <span class="legend-item">2 de cada por fila y columna</span>
            <span class="legend-item">Clic para ciclar color</span>
          </div>
        <button type="button" class="btn btn-secondary mt-3" onclick={zInit}>Nuevo tablero</button>
      </div>
    {/if}
  </div>
</div>

<style>
  .juegos-wrapper { max-width: 700px; margin: 0 auto; font-family: system-ui, sans-serif; }
  .tabs-navigation { display: flex; gap: 4px; padding: 4px; border-radius: 8px; margin-bottom: 16px; flex-wrap: wrap; }
  .tab-btn { flex: 1; min-width: 80px; border: none; background: transparent; padding: 10px 6px; font-weight: 600; font-size: 0.8rem; cursor: pointer; border-radius: 6px; transition: all 0.15s; }
  .tab-btn.active { background: #ffffff !important; color: #1e293b !important; box-shadow: 0 2px 6px rgba(0,0,0,0.05); }
  :global(.dark) .tab-btn.active { background: #1e293b !important; color: #ffffff !important; }
  .game-card { border-radius: 12px; }
  .game-content { display: flex; flex-direction: column; gap: 14px; }
  .game-title { font-size: 1.3rem; font-weight: 800; margin: 0; }
  .game-desc { font-size: 0.9rem; margin: 0; }
  .rules-box { line-height: 1.5; }

  .input-row { display: flex; gap: 8px; }
  .game-input { flex: 1; padding: 10px 14px; border: 1px solid; border-radius: 8px; font-size: 1rem; outline: none; }
  .game-input:focus { border-color: #3498db; box-shadow: 0 0 0 2px rgba(52,152,219,0.2); }

  .btn { padding: 10px 18px; border: none; border-radius: 8px; cursor: pointer; font-weight: 600; font-size: 0.9rem; transition: all 0.15s; }
  .btn-primary { background: #3498db; color: white; }
  .btn-primary:hover { background: #2980b9; }
  .btn-secondary { background: #e2e8f0; color: #475569; }
  .btn-secondary:hover { background: #cbd5e1; }
  :global(.dark) .btn-secondary { background: #334155; color: #94a3b8; }
  :global(.dark) .btn-secondary:hover { background: #475569; }
  .mt-3 { margin-top: 12px; }

  .game-message { padding: 10px 14px; border-radius: 8px; font-weight: 600; font-size: 0.9rem; background: #fef2f2; color: #991b1b; }
  .game-message.success { background: #dcfce7; color: #166534; }
  :global(.dark) .game-message { background: #451a1a; color: #fca5a5; }
  :global(.dark) .game-message.success { background: #14532d; color: #86efac; }

  .result-banner { display: flex; align-items: center; gap: 14px; padding: 14px 18px; border-radius: 12px; font-weight: 600; }
  .result-icon { font-size: 2rem; line-height: 1; }
  .result-text { display: flex; flex-direction: column; gap: 2px; }
  .result-title { font-size: 1.1rem; font-weight: 800; }
  .result-detail { font-size: 0.85rem; font-weight: 500; opacity: 0.85; }
  .win-banner { background: linear-gradient(135deg, #dcfce7, #bbf7d0); color: #166534; border: 1px solid #86efac; }
  :global(.dark) .win-banner { background: linear-gradient(135deg, #14532d, #166534); color: #86efac; border-color: #22c55e; }
  .lose-banner { background: linear-gradient(135deg, #fef2f2, #fecaca); color: #991b1b; border: 1px solid #fca5a5; }
  :global(.dark) .lose-banner { background: linear-gradient(135deg, #451a1a, #7f1d1d); color: #fca5a5; border-color: #ef4444; }

  /* PINPOINT */
  .hints-list { display: flex; flex-wrap: wrap; gap: 6px; }
  .hint-pill { padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 600; background: #e0f2fe; color: #0369a1; }
  :global(.dark) .hint-pill { background: #0c4a6e; color: #7dd3fc; }
  .hint-current { outline: 2px solid currentColor; outline-offset: 1px; }
  .history { display: flex; flex-wrap: wrap; gap: 6px; font-size: 0.8rem; }
  .history-item { padding: 2px 8px; background: #fee2e2; color: #991b1b; border-radius: 4px; font-weight: 600; }
  :global(.dark) .history-item { background: #451a1a; color: #fca5a5; }
  .history-item.correct { background: #dcfce7; color: #166534; }
  :global(.dark) .history-item.correct { background: #14532d; color: #86efac; }

  /* CROSSCLIMB */
  .ladder { display: flex; flex-direction: column; gap: 4px; }
  .ladder-step { display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 6px; background: #f8fafc; border: 1px solid #e2e8f0; }
  :global(.dark) .ladder-step { background: #1e293b; border-color: #334155; }
  .step-first { border-left: 3px solid #22c55e; }
  .step-current { border-left: 3px solid #3498db; }
  .step-end { border-left: 3px solid #22c55e; background: #f0fdf4; }
  :global(.dark) .step-end { background: #14532d; }
  .step-num { font-size: 0.8rem; font-weight: 700; min-width: 20px; }
  .step-word { font-family: monospace; font-size: 1.1rem; font-weight: 700; letter-spacing: 2px; }

  /* QUEENS */
  .queens-grid { display: grid; gap: 3px; max-width: 400px; }
  .queen-cell { aspect-ratio: 1; border: 2px solid; border-radius: 6px; font-size: 1.3rem; cursor: pointer; transition: all 0.1s; display: flex; align-items: center; justify-content: center; }
  .queen-cell:hover { filter: brightness(0.9); transform: scale(1.05); }
  .queen-cell.has-queen { box-shadow: 0 0 0 2px #1e293b; }
  .queen-cell.attacked { background: rgba(239,68,68,0.3) !important; }
  .legend { display: flex; gap: 12px; font-size: 0.8rem; flex-wrap: wrap; }
  .legend-item { padding: 2px 8px; background: #f1f5f9; border-radius: 4px; }
  :global(.dark) .legend-item { background: #1e293b; }

  /* TANGO */
  .tango-grid { display: grid; gap: 3px; max-width: 360px; }
  .tango-cell { aspect-ratio: 1; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 1.2rem; cursor: pointer; transition: all 0.1s; display: flex; align-items: center; justify-content: center; background: #f8fafc; }
  :global(.dark) .tango-cell { background: #1e293b; border-color: #475569; }
  .tango-cell:hover { transform: scale(1.05); }
  .tango-cell.cell-revealed { opacity: 0.6; cursor: not-allowed; }
  .cell-a { background: #dbeafe !important; color: #2563eb; }
  .cell-b { background: #ffedd5 !important; color: #ea580c; }
  :global(.dark) .cell-a { background: #1e3a5f !important; }
  :global(.dark) .cell-b { background: #431407 !important; }

  /* ZIP */
  .zip-grid { display: grid; gap: 3px; max-width: 320px; }
  .zip-cell { aspect-ratio: 1; border: 1px solid #cbd5e1; border-radius: 6px; font-size: 1.3rem; cursor: pointer; transition: all 0.1s; display: flex; align-items: center; justify-content: center; background: #f8fafc; }
  :global(.dark) .zip-cell { background: #1e293b; border-color: #475569; }
  .zip-cell:hover { transform: scale(1.08); }
  .z-red { background: #fee2e2 !important; }
  .z-blue { background: #dbeafe !important; }
  .z-green { background: #dcfce7 !important; }
</style>
