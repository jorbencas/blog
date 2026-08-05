<script>
  let activeGame = $state("pinpoint");

  // ============================================================
  // PINPOINT - Adivina la palabra con pistas progresivas
  // ============================================================
  const PINPOINT_WORDS = [
    { word: "ELEFANTE", hints: ["Animal", "Tronco", "Trompa", "Grande", "Película Disney", "Paquidermo"] },
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
    { word: "PIRÁMIDE", hints: ["Egipto", "Farayón", "Arena", "Antigua", "Triángulo", "Sangre"] },
    { word: "CHOCOLATE", hints: ["Dulce", "Cacao", "Tableta", "Tostado", "Suizo", "Postre"] },
  ];

  let ppWord = $state(null);
  let ppHintIndex = $state(0);
  let ppGuess = $state("");
  let ppWon = $state(false);
  let ppMessage = $state("");
  let ppHistory = $state([]);

  function ppStartNew() {
    ppWord = PINPOINT_WORDS[Math.floor(Math.random() * PINPOINT_WORDS.length)];
    ppHintIndex = 0;
    ppGuess = "";
    ppWon = false;
    ppMessage = "";
    ppHistory = [];
  }

  function ppGuessWord() {
    if (!ppGuess.trim() || ppWon) return;
    const guess = ppGuess.trim().toUpperCase();
    ppHistory.push({ guess, hint: ppHintIndex + 1 });
    if (guess === ppWord.word) {
      ppWon = true;
      ppMessage = `¡Correcto! La palabra era "${ppWord.word}" en ${ppHintIndex + 1} pista(s).`;
    } else {
      ppHintIndex = Math.min(ppHintIndex + 1, ppWord.hints.length - 1);
      ppMessage = "Incorrecto. Pista nueva desbloqueada.";
    }
    ppGuess = "";
  }

  // ============================================================
  // CROSSCLIMB - Escalera de palabras (misma longitud, 1 letra por paso)
  // ============================================================
  const CROSSCLIMB_PAIRS = [
    { start: "PATO", end: "GATO" },
    { start: "SOL", end: "SOP" },
    { start: "ROJO", end: "ROTO" },
    { start: "LUNA", end: "MUNA" },
    { start: "CASA", end: "CASA" },
    { start: "TRES", end: "PRES" },
    { start: "FLOR", end: "FLON" },
    { start: "MESA", end: "MESA" },
    { start: "AMOR", end: "AVOR" },
    { start: "CARRO", end: "CARPO" },
    { start: "VERDE", end: "CERDE" },
    { start: "PERRO", end: "PERNO" },
  ];

  let ccPair = $state(null);
  let ccUserPath = $state([]);
  let ccInput = $state("");
  let ccWon = $state(false);
  let ccMessage = $state("");
  let ccHistory = $state([]);

  function ccStartNew() {
    const valid = CROSSCLIMB_PAIRS.filter(p => p.start !== p.end);
    ccPair = valid[Math.floor(Math.random() * valid.length)];
    ccUserPath = [ccPair.start.toUpperCase()];
    ccInput = "";
    ccWon = false;
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
    if (!ccInput.trim() || ccWon) return;
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
    } else {
      ccMessage = `Ahora desde "${word}" → llega a "${ccPair.end}"`;
    }
    ccInput = "";
  }

  // ============================================================
  // QUEENS - Colocar reinas por fila/columna/región sin tocarse
  // ============================================================
  const QUEENS_COLORS = ["#ef4444", "#3b82f6", "#22c55e", "#f59e0b", "#a855f7", "#ec4899", "#06b6d4"];
  let qSize = $state(7);
  let qGrid = $state([]);
  let qRegions = $state([]);
  let qQueens = $state([]);
  let qMessage = $state("");
  let qWon = $state(false);

  function qGenerateRegions() {
    const n = qSize;
    const totalCells = n * n;
    const numRegions = Math.min(n, 7);
    const regionSize = Math.floor(totalCells / numRegions);
    let cells = Array.from({ length: totalCells }, (_, i) => i);
    let regions = [];
    for (let r = 0; r < numRegions; r++) {
      let region = [];
      let startIdx = Math.floor(Math.random() * cells.length);
      region.push(cells.splice(startIdx, 1)[0]);
      while (region.length < regionSize && cells.length > 0) {
        let lastCell = region[region.length - 1];
        let neighbors = cells.filter(c => {
          let r1 = Math.floor(lastCell / n), c1 = lastCell % n;
          let r2 = Math.floor(c / n), c2 = c % n;
          return Math.abs(r1 - r2) <= 1 && Math.abs(c1 - c2) <= 1;
        });
        if (neighbors.length > 0) {
          let next = neighbors[Math.floor(Math.random() * neighbors.length)];
          region.push(cells.splice(cells.indexOf(next), 1)[0]);
        } else {
          let idx = Math.floor(Math.random() * cells.length);
          region.push(cells.splice(idx, 1)[0]);
        }
      }
      regions.push(region);
    }
    while (cells.length > 0) {
      regions[regions.length - 1].push(cells.shift());
    }
    return regions;
  }

  function qInit() {
    qQueens = [];
    qMessage = "";
    qWon = false;
    qRegions = qGenerateRegions();
    qGrid = Array.from({ length: qSize * qSize }, (_, i) => i);
  }

  function qCellRegion(cellIdx) {
    return qRegions.findIndex(r => r.includes(cellIdx));
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
    for (const region of qRegions) {
      if (!region.some(c => qQueens.includes(c))) return;
    }
    qWon = true;
    qMessage = `¡Correcto! ${qSize} reinas colocadas sin conflicto.`;
  }

  // ============================================================
  // TANGO - Cuadrícula con reglas de color/fila/columna
  // ============================================================
  let tSize = $state(6);
  let tGrid = $state([]);
  let tMessage = $state("");
  let tWon = $state(false);

  function tInit() {
    const n = tSize;
    tGrid = Array.from({ length: n * n }, () => 0);
    tMessage = "Alterna las celdas (clic) para que no haya 3+ seguidas del mismo color en fila o columna. Rellena todas las celdas.";
    tWon = false;
  }

  function tToggleCell(idx) {
    if (tWon) return;
    tGrid[idx] = tGrid[idx] === 0 ? 1 : tGrid[idx] === 1 ? 2 : 0;
    tGrid = [...tGrid];
    tCheckWin();
  }

  function tCheckWin() {
    const n = tSize;
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < n - 2; c++) {
        const a = tGrid[r * n + c];
        const b = tGrid[r * n + c + 1];
        const d = tGrid[r * n + c + 2];
        if (a !== 0 && a === b && b === d) return;
      }
    }
    for (let c = 0; c < n; c++) {
      for (let r = 0; r < n - 2; r++) {
        const a = tGrid[r * n + c];
        const b = tGrid[(r + 1) * n + c];
        const d = tGrid[(r + 2) * n + c];
        if (a !== 0 && a === b && b === d) return;
      }
    }
    if (tGrid.some(v => v === 0)) return;
    tWon = true;
    tMessage = "¡Correcto! Sin tres seguidas del mismo color.";
  }

  // ============================================================
  // ZIP - Completar cuadrícula con reglas de color
  // ============================================================
  const ZIP_COLORS = ["#ef4444", "#3b82f6", "#22c55e"];
  let zSize = $state(6);
  let zGrid = $state([]);
  let zSolution = $state([]);
  let zMessage = $state("");
  let zWon = $state(false);

  function zInit() {
    const n = zSize;
    zSolution = Array.from({ length: n * n }, () => Math.floor(Math.random() * 3));
    zGrid = Array.from({ length: n * n }, () => -1);
    zMessage = "Rellena cada celda con el color correcto. Cada fila y columna debe tener exactamente 2 de cada color (3 colores, 6 celdas).";
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
    for (let r = 0; r < n; r++) {
      for (let c = 0; c < 3; c++) {
        let count = 0;
        for (let col = 0; col < n; col++) {
          if (zGrid[r * n + col] === c) count++;
        }
        if (count !== 2) return;
      }
    }
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
    zMessage = "¡Correcto! Distribución平衡ada.";
  }

  // Init
  $effect(() => {
    ppStartNew();
    ccStartNew();
    qInit();
    tInit();
    zInit();
  });
</script>

<div class="juegos-wrapper text-slate-800 dark:text-slate-100">
  <div class="tabs-navigation bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
    <button type="button" class="tab-btn text-slate-600 dark:text-slate-400" class:active={activeGame === 'pinpoint'} onclick={() => activeGame = 'pinpoint'}>🎯 Pinpoint</button>
    <button type="button" class="tab-btn text-slate-600 dark:text-slate-400" class:active={activeGame === 'crossclimb'} onclick={() => activeGame = 'crossclimb'}>🪜 Crossclimb</button>
    <button type="button" class="tab-btn text-slate-600 dark:text-slate-400" class:active={activeGame === 'queens'} onclick={() => activeGame = 'queens'}>♛ Queens</button>
    <button type="button" class="tab-btn text-slate-600 dark:text-slate-400" class:active={activeGame === 'tango'} onclick={() => activeGame = 'tango'}>💃 Tango</button>
    <button type="button" class="tab-btn text-slate-600 dark:text-slate-400" class:active={activeGame === 'zip'} onclick={() => activeGame = 'zip'}>📦 Zip</button>
  </div>

  <div class="game-card bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800 rounded-xl p-5">

    <!-- PINPOINT -->
    {#if activeGame === 'pinpoint'}
      <div class="game-content">
        <h2 class="game-title text-slate-900 dark:text-white">🎯 Pinpoint</h2>
        <p class="game-desc text-slate-500 dark:text-slate-400">Adivina la palabra. Cada intento fallido desbloquea una pista.</p>
        {#if !ppWord}
          <button type="button" class="btn btn-primary" onclick={ppStartNew}>Empezar</button>
        {:else}
          <div class="hints-list">
            {#each ppWord.hints.slice(0, ppHintIndex + 1) as hint, i}
              <div class="hint-pill bg-sky-100 dark:bg-sky-900/40 text-sky-700 dark:text-sky-300">
                Pista {i + 1}: {hint}
              </div>
            {/each}
          </div>
          {#if !ppWon}
            <div class="input-row">
              <input type="text" bind:value={ppGuess} placeholder="Tu guess..." class="game-input bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100"
                onkeydown={(e) => e.key === 'Enter' && ppGuessWord()} />
              <button type="button" class="btn btn-primary" onclick={ppGuessWord}>Adivinar</button>
            </div>
          {/if}
          {#if ppMessage}
            <div class="game-message" class:success={ppWon}>{ppMessage}</div>
          {/if}
          {#if ppHistory.length > 0}
            <div class="history text-slate-500 dark:text-slate-400">
              {#each ppHistory as h, i}
                <span class="history-item" class:wrong={true}>#{i + 1} {h.guess} (pista {h.hint})</span>
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
        <p class="game-desc text-slate-500 dark:text-slate-400">Cambia UNA letra por paso para llegar de "{ccPair?.start}" a "{ccPair?.end}".</p>
        {#if ccPair}
          <div class="ladder">
            {#each ccUserPath as word, i}
              <div class="ladder-step" class:step-first={i === 0} class:step-current={i === ccUserPath.length - 1 && !ccWon}>
                <span class="step-num text-slate-400 dark:text-slate-500">{i}.</span>
                <span class="step-word text-slate-900 dark:text-white">{word}</span>
              </div>
            {/each}
          </div>
          {#if !ccWon}
            <div class="input-row">
              <input type="text" bind:value={ccInput} placeholder="Siguiente palabra..." class="game-input bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100"
                onkeydown={(e) => e.key === 'Enter' && ccStep()} />
              <button type="button" class="btn btn-primary" onclick={ccStep}>Paso</button>
            </div>
          {/if}
          {#if ccMessage}
            <div class="game-message" class:success={ccWon}>{ccMessage}</div>
          {/if}
          <button type="button" class="btn btn-secondary mt-3" onclick={ccStartNew}>Nueva escalera</button>
        {/if}
      </div>

    <!-- QUEENS -->
    {:else if activeGame === 'queens'}
      <div class="game-content">
        <h2 class="game-title text-slate-900 dark:text-white">♛ Queens</h2>
        <p class="game-desc text-slate-500 dark:text-slate-400">Coloca 1 reina por fila, columna y región de color. No pueden tocarse (ni en diagonal).</p>
        <div class="queens-grid" style="grid-template-columns: repeat({qSize}, 1fr);">
          {#each qGrid as cell, i}
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
          <span class="legend-item">♛ = reina</span>
          <span class="legend-item">Rojo = atacada</span>
          <span class="legend-item">{qQueens.length}/{qSize} reinas</span>
        </div>
        {#if qMessage}
          <div class="game-message" class:success={qWon}>{qMessage}</div>
        {/if}
        <button type="button" class="btn btn-secondary mt-3" onclick={qInit}>Nuevo tablero</button>
      </div>

    <!-- TANGO -->
    {:else if activeGame === 'tango'}
      <div class="game-content">
        <h2 class="game-title text-slate-900 dark:text-white">💃 Tango</h2>
        <p class="game-desc text-slate-500 dark:text-slate-400">No puede haber 3+ celdas seguidas del mismo color en fila o columna.</p>
        <div class="tango-grid" style="grid-template-columns: repeat({tSize}, 1fr);">
          {#each tGrid as cell, i}
            <button type="button"
              class="tango-cell"
              class:cell-a={cell === 1}
              class:cell-b={cell === 2}
              onclick={() => tToggleCell(i)}>
              {#if cell === 1}●{:else if cell === 2}○{/if}
            </button>
          {/each}
        </div>
        <div class="legend text-slate-500 dark:text-slate-400">
          <span class="legend-item">● Azul | ○ Naranja | Vacío</span>
          <span class="legend-item">Clic para cambiar</span>
        </div>
        {#if tMessage}
          <div class="game-message" class:success={tWon}>{tMessage}</div>
        {/if}
        <button type="button" class="btn btn-secondary mt-3" onclick={tInit}>Nuevo tablero</button>
      </div>

    <!-- ZIP -->
    {:else if activeGame === 'zip'}
      <div class="game-content">
        <h2 class="game-title text-slate-900 dark:text-white">📦 Zip</h2>
        <p class="game-desc text-slate-500 dark:text-slate-400">Cada fila y columna debe tener exactamente 2 de cada color (4 colores).</p>
        <div class="zip-grid" style="grid-template-columns: repeat({zSize}, 1fr);">
          {#each zGrid as cell, i}
            <button type="button"
              class="zip-cell"
              class:z-red={cell === 0}
              class:z-blue={cell === 1}
              class:z-green={cell === 2}
              class:z-yellow={cell === 3}
              onclick={() => zCycleColor(i)}>
              {#if cell >= 0}{['🔴', '🔵', '🟢'][cell]}{:else}?{/if}
            </button>
          {/each}
        </div>
        <div class="legend text-slate-500 dark:text-slate-400">
          <span class="legend-item">🔴 🔵 🟢 (2 de cada por fila/columna)</span>
          <span class="legend-item">Clic para cambiar color</span>
        </div>
        {#if zMessage}
          <div class="game-message" class:success={zWon}>{zMessage}</div>
        {/if}
        <button type="button" class="btn btn-secondary mt-3" onclick={zInit}>Nuevo tablero</button>
      </div>
    {/if}
  </div>
</div>

<style>
  .juegos-wrapper { max-width: 700px; margin: 0 auto; font-family: system-ui, sans-serif; }
  .tabs-navigation { display: flex; gap: 4px; padding: 4px; border-radius: 8px; margin-bottom: 16px; flex-wrap: wrap; }
  .tab-btn { flex: 1; min-width: 80px; border: none; background: transparent; padding: 10px 6px; font-weight: 600; font-size: 0.8rem; cursor: pointer; border-radius: 6px; transition: all 0.15s; }
  .tab-btn.active { background: #ffffff; color: #1e293b !important; box-shadow: 0 2px 6px rgba(0,0,0,0.05); }
  :global(.dark) .tab-btn.active { background: #1e293b; color: #ffffff !important; }
  .game-card { border-radius: 12px; }
  .game-content { display: flex; flex-direction: column; gap: 14px; }
  .game-title { font-size: 1.3rem; font-weight: 800; margin: 0; }
  .game-desc { font-size: 0.9rem; margin: 0; }

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

  /* PINPOINT */
  .hints-list { display: flex; flex-wrap: wrap; gap: 6px; }
  .hint-pill { padding: 4px 12px; border-radius: 20px; font-size: 0.82rem; font-weight: 600; }
  .history { display: flex; flex-wrap: wrap; gap: 6px; font-size: 0.8rem; }
  .history-item { padding: 2px 8px; background: #fee2e2; color: #991b1b; border-radius: 4px; }
  :global(.dark) .history-item { background: #451a1a; color: #fca5a5; }

  /* CROSSCLIMB */
  .ladder { display: flex; flex-direction: column; gap: 4px; }
  .ladder-step { display: flex; align-items: center; gap: 10px; padding: 8px 12px; border-radius: 6px; background: #f8fafc; border: 1px solid #e2e8f0; }
  :global(.dark) .ladder-step { background: #1e293b; border-color: #334155; }
  .step-first { border-left: 3px solid #22c55e; }
  .step-current { border-left: 3px solid #3498db; }
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
  .z-yellow { background: #fef9c3 !important; }
</style>
