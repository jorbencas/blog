<script>
  let mode = $state("ai");
  let difficulty = $state("medium");
  let playerPiece = $state("X");
  let board = $state(Array(9).fill(null));
  let currentPlayer = $state("X");
  let gameActive = $state(false);
  let player1Name = $state("Jugador 1");
  let player2Name = $state("IA");
  let player1Wins = $state(0);
  let player2Wins = $state(0);
  let ties = $state(0);
  let rounds = $state(3);
  let currentRound = $state(0);
  let showSummary = $state(false);
  let announcement = $state("");
  let announcementColor = $state("");
  let showAnnouncement = $state(false);
  let roundHistory = $state([]);

  const WIN_LINES = [
    [0,1,2],[3,4,5],[6,7,8],
    [0,3,6],[1,4,7],[2,5,8],
    [0,4,8],[2,4,6]
  ];

  function changeMode(val) {
    mode = val;
    player2Name = val === "ai" ? "IA" : "Jugador 2";
  }

  function selectPiece(piece) {
    playerPiece = piece;
  }

  function startGame() {
    player1Wins = 0;
    player2Wins = 0;
    ties = 0;
    currentRound = 0;
    roundHistory = [];
    showSummary = false;
    nextRound();
  }

  function nextRound() {
    currentRound++;
    if (currentRound > rounds) {
      showSummary = true;
      return;
    }
    board = Array(9).fill(null);
    currentPlayer = playerPiece;
    gameActive = true;
    showAnnouncement = false;
  }

  function stopSeries() {
    gameActive = false;
    showSummary = true;
    showAnnouncement = false;
  }

  function play(idx) {
    if (!gameActive || board[idx] !== null) return;
    board[idx] = currentPlayer;
    board = [...board];

    const win = checkWin(currentPlayer);
    if (win) {
      const isPlayer1Turn = (mode === "ai" && currentPlayer === playerPiece) ||
                            (mode === "multi" && currentPlayer === "X");
      handleEnd(isPlayer1Turn ? "win" : "lose");
      return;
    }
    if (board.every(c => c !== null)) {
      handleEnd("tie");
      return;
    }

    toggleTurn();

    if (mode === "ai" && currentPlayer !== playerPiece && gameActive) {
      setTimeout(aiMove, 400);
    }
  }

  function aiMove() {
    if (!gameActive) return;
    const move = getSmartMove();
    if (move !== -1) {
      play(move);
    }
  }

  function getSmartMove() {
    const ai = playerPiece === "X" ? "O" : "X";
    const human = playerPiece;

    // Fácil: solo bloques y jugadas aleatorias
    if (difficulty === "easy") {
      // Bloquear si el humano va a ganar
      for (const line of WIN_LINES) {
        const vals = line.map(i => board[i]);
        if (vals.filter(v => v === human).length === 2 && vals.includes(null)) {
          return line[vals.indexOf(null)];
        }
      }
      const empty = board.map((v,i) => v === null ? i : -1).filter(i => i !== -1);
      return empty.length > 0 ? empty[Math.floor(Math.random() * empty.length)] : -1;
    }

    // Medio: ofensiva + defensa
    if (difficulty === "medium") {
      // Ganar si puede
      for (const line of WIN_LINES) {
        const vals = line.map(i => board[i]);
        if (vals.filter(v => v === ai).length === 2 && vals.includes(null)) {
          return line[vals.indexOf(null)];
        }
      }
      // Bloquear
      for (const line of WIN_LINES) {
        const vals = line.map(i => board[i]);
        if (vals.filter(v => v === human).length === 2 && vals.includes(null)) {
          return line[vals.indexOf(null)];
        }
      }
      if (board[4] === null) return 4;
      const corners = [0,2,6,8].filter(i => board[i] === null);
      if (corners.length > 0) return corners[Math.floor(Math.random() * corners.length)];
      const empty = board.map((v,i) => v === null ? i : -1).filter(i => i !== -1);
      return empty.length > 0 ? empty[0] : -1;
    }

    // Difícil: minimax
    return getBestMoveMinimax();
  }

  function getBestMoveMinimax() {
    const ai = playerPiece === "X" ? "O" : "X";
    let bestScore = -Infinity;
    let bestMove = -1;

    for (let i = 0; i < 9; i++) {
      if (board[i] === null) {
        board[i] = ai;
        const score = minimax(board, 0, false, ai, playerPiece);
        board[i] = null;
        if (score > bestScore) {
          bestScore = score;
          bestMove = i;
        }
      }
    }
    return bestMove;
  }

  function minimax(b, depth, isMaximizing, ai, human) {
    const winner = getWinner(b);
    if (winner === ai) return 10 - depth;
    if (winner === human) return depth - 10;
    if (b.every(c => c !== null)) return 0;

    if (isMaximizing) {
      let best = -Infinity;
      for (let i = 0; i < 9; i++) {
        if (b[i] === null) {
          b[i] = ai;
          best = Math.max(best, minimax(b, depth + 1, false, ai, human));
          b[i] = null;
        }
      }
      return best;
    } else {
      let best = Infinity;
      for (let i = 0; i < 9; i++) {
        if (b[i] === null) {
          b[i] = human;
          best = Math.min(best, minimax(b, depth + 1, true, ai, human));
          b[i] = null;
        }
      }
      return best;
    }
  }

  function getWinner(b) {
    for (const line of WIN_LINES) {
      const [a, bb, c] = line;
      if (b[a] && b[a] === b[bb] && b[a] === b[c]) return b[a];
    }
    return null;
  }

  function toggleTurn() {
    currentPlayer = currentPlayer === "X" ? "O" : "X";
  }

  function checkWin(piece) {
    for (const line of WIN_LINES) {
      if (line.every(i => board[i] === piece)) return line;
    }
    return null;
  }

  function handleEnd(result) {
    gameActive = false;

    if (result === "win") {
      player1Wins++;
      roundHistory.push("win");
      announcement = `¡${player1Name} gana!`;
      announcementColor = "#00c853";
    } else if (result === "lose") {
      player2Wins++;
      roundHistory.push("lose");
      const winner = mode === "ai" ? "La IA" : player2Name;
      announcement = `${winner} gana`;
      announcementColor = "#ff1744";
    } else {
      ties++;
      roundHistory.push("tie");
      announcement = "Empate";
      announcementColor = "#455a64";
    }

    showAnnouncement = true;
    setTimeout(() => {
      showAnnouncement = false;
      nextRound();
    }, 1500);
  }

  function resetAll() {
    mode = "ai";
    difficulty = "medium";
    playerPiece = "X";
    player1Name = "Jugador 1";
    player2Name = "IA";
    player1Wins = 0;
    player2Wins = 0;
    ties = 0;
    currentRound = 0;
    gameActive = false;
    showSummary = false;
    showAnnouncement = false;
    roundHistory = [];
    board = Array(9).fill(null);
  }

  function getSymbolSvg(piece) {
    if (piece === "X") {
      return `<svg viewBox="0 0 460.775 460.775" fill="none" stroke="currentColor" stroke-width="40"><line x1="60" y1="60" x2="400" y2="400"/><line x1="400" y1="60" x2="60" y2="400"/></svg>`;
    }
    return `<svg viewBox="0 0 200 200" fill="none" stroke="currentColor" stroke-width="8"><circle cx="100" cy="100" r="80"/></svg>`;
  }

  function getWinLine() {
    for (const piece of ["X", "O"]) {
      const win = checkWin(piece);
      if (win) return win;
    }
    return null;
  }
</script>

<div class="ttt-wrapper">
  <h2 class="ttt-title">3 EN RAYA</h2>

  <div class="ttt-layout">
    <!-- Panel lateral -->
    <div class="side-panel">
      <select class="ttt-select bg-white dark:bg-[#141414] border border-slate-300 dark:border-white/[0.08] text-slate-900 dark:text-white" onchange={(e) => changeMode(e.target.value)} disabled={gameActive}>
        <option value="ai">VS IA</option>
        <option value="multi">MULTIPLAYER</option>
      </select>

      {#if mode === 'ai' && !gameActive && !showSummary}
        <div class="difficulty-selector">
          <span class="piece-label">Dificultad:</span>
          <div class="diff-buttons">
            <button type="button" class="diff-btn" class:active={difficulty === 'easy'} onclick={() => difficulty = 'easy'}>
              <span class="diff-icon">😊</span>
              <span class="diff-text">Fácil</span>
            </button>
            <button type="button" class="diff-btn" class:active={difficulty === 'medium'} onclick={() => difficulty = 'medium'}>
              <span class="diff-icon">😐</span>
              <span class="diff-text">Medio</span>
            </button>
            <button type="button" class="diff-btn" class:active={difficulty === 'hard'} onclick={() => difficulty = 'hard'}>
              <span class="diff-icon">😈</span>
              <span class="diff-text">Difícil</span>
            </button>
          </div>
        </div>
      {/if}

      {#if !gameActive && !showSummary}
        <div class="setup-section">
          <div class="piece-selector">
            <span class="piece-label">Elige tu pieza:</span>
            <div class="piece-buttons">
              <button type="button" class="piece-btn bg-white dark:bg-[#141414] border-2 border-slate-300 dark:border-white/10 hover:border-slate-400 dark:hover:border-white/30" class:active={playerPiece === 'X'} onclick={() => selectPiece('X')}>
                <span class="piece-x">X</span>
              </button>
              <button type="button" class="piece-btn bg-white dark:bg-[#141414] border-2 border-slate-300 dark:border-white/10 hover:border-slate-400 dark:hover:border-white/30" class:active={playerPiece === 'O'} onclick={() => selectPiece('O')}>
                <span class="piece-o">O</span>
              </button>
            </div>
          </div>

          {#if mode === 'multi'}
            <input type="text" class="ttt-input bg-white dark:bg-[#141414] border border-slate-300 dark:border-white/[0.08] text-slate-900 dark:text-white" placeholder="Nombre Jugador 1" bind:value={player1Name} />
            <input type="text" class="ttt-input bg-white dark:bg-[#141414] border border-slate-300 dark:border-white/[0.08] text-slate-900 dark:text-white" placeholder="Nombre Jugador 2" bind:value={player2Name} />
          {/if}

          <button type="button" class="start-btn bg-slate-900 dark:bg-white text-white dark:text-black hover:bg-slate-800 dark:hover:bg-slate-200" onclick={startGame}>INICIAR PARTIDA</button>
        </div>
      {/if}

      {#if gameActive || showSummary}
        <div class="player-card bg-white dark:bg-[#141414] border border-slate-200 dark:border-white/[0.06]" class:active={gameActive && currentPlayer === 'X'}>
          <div class="player-header">
            <span class="piece-icon" class:icon-x={playerPiece === 'X'} class:icon-o={playerPiece !== 'X'}>{playerPiece}</span>
            <span class="player-name">{player1Name}</span>
          </div>
          {#if mode === 'ai' && !showSummary}
            <span class="your-piece">Tu pieza: <strong class:piece-x={playerPiece === 'X'} class:piece-o={playerPiece !== 'X'}>{playerPiece}</strong></span>
          {/if}
          <div class="score-badge">VICTORIAS: {player1Wins}</div>
        </div>

        <div class="divider">VS</div>

        <div class="player-card bg-white dark:bg-[#141414] border border-slate-200 dark:border-white/[0.06]" class:active={gameActive && currentPlayer !== 'X'}>
          <div class="player-header">
            <span class="piece-icon" class:icon-x={playerPiece !== 'X'} class:icon-o={playerPiece === 'X'}>{playerPiece === 'X' ? 'O' : 'X'}</span>
            <span class="player-name">{player2Name}</span>
          </div>
          {#if mode === 'ai' && !showSummary}
            <span class="your-piece">Pieza IA: <strong class:piece-x={playerPiece !== 'X'} class:piece-o={playerPiece === 'X'}>{playerPiece === 'X' ? 'O' : 'X'}</strong></span>
          {/if}
          <div class="score-badge">VICTORIAS: {player2Wins}</div>
        </div>

        {#if currentRound > 0}
          <div class="round-info">Ronda {Math.min(currentRound, rounds)} / {rounds}</div>
        {/if}

        {#if gameActive}
          <button type="button" class="stop-btn" onclick={stopSeries}>⏹ DETENER SERIE</button>
        {/if}
      {/if}
    </div>

    <!-- Tablero -->
    <div class="board-wrapper">
      {#if !showSummary}
        <div class="board">
          {#each board as cell, i}
            <button
              type="button"
              class="cell bg-white dark:bg-[#141414] border-slate-200 dark:border-white/[0.06] hover:bg-slate-100 dark:hover:bg-white/[0.04] hover:border-slate-300 dark:hover:border-white/[0.12] text-slate-900 dark:text-white"
              class:cell-x={cell === 'X'}
              class:cell-o={cell === 'O'}
              class:cell-win={getWinLine()?.includes(i)}
              disabled={!gameActive || cell !== null}
              onclick={() => play(i)}
            >
              {#if cell}
                <span class="cell-symbol">{cell}</span>
              {/if}
            </button>
          {/each}
        </div>
      {:else}
        <div class="summary-view">
          <h3 class="summary-title">
            {#if player1Wins > player2Wins}
              🏆 ¡{player1Name} gana la serie!
            {:else if player2Wins > player1Wins}
              {mode === 'ai' ? '🤖 La IA gana la serie' : `🏆 ${player2Name} gana la serie`}
            {:else}
              🤝 Empate en la serie
            {/if}
          </h3>

          <div class="summary-scores">
            <div class="summary-score">
              <span class="summary-name">{player1Name}</span>
              <span class="summary-wins">{player1Wins}</span>
            </div>
            <div class="summary-divider">-</div>
            <div class="summary-score">
              <span class="summary-name">{player2Name}</span>
              <span class="summary-wins">{player2Wins}</span>
            </div>
          </div>

          <div class="badge-container">
            {#each roundHistory as result}
              <div class="badge" class:badge-win={result === 'win'} class:badge-lose={result === 'lose'} class:badge-tie={result === 'tie'}>
                {result === 'win' ? '✓' : result === 'lose' ? '✗' : '='}
              </div>
            {/each}
          </div>

          <button type="button" class="start-btn bg-slate-900 dark:bg-white text-white dark:text-black hover:bg-slate-800 dark:hover:bg-slate-200" onclick={resetAll} style="margin-top: 24px;">VOLVER A EMPEZAR</button>
        </div>
      {/if}
    </div>
  </div>

  <!-- Anuncio -->
  {#if showAnnouncement}
    <div class="announcement-overlay" class:show={showAnnouncement}>
      <div class="announcement-box" style="border-color: {announcementColor}; color: {announcementColor};">
        {announcement}
      </div>
    </div>
  {/if}
</div>

<style>
  .ttt-wrapper { max-width: 900px; margin: 0 auto; text-align: center; }
  .ttt-title { font-size: 0.85rem; letter-spacing: 0.4rem; font-weight: 300; opacity: 0.6; margin-bottom: 30px; }

  .ttt-layout { display: flex; gap: 50px; align-items: flex-start; justify-content: center; }
  @media (max-width: 700px) { .ttt-layout { flex-direction: column; align-items: center; gap: 24px; } }

  .side-panel { flex: 0 0 240px; display: flex; flex-direction: column; gap: 14px; }
  @media (max-width: 700px) { .side-panel { flex: none; width: 100%; max-width: 320px; } }

  .ttt-select, .ttt-input {
    width: 100%; padding: 10px 12px;
    font-size: 0.82rem; border-radius: 6px; outline: none; font-family: inherit;
  }
  .ttt-select:focus, .ttt-input:focus { border-color: #00e5ff; }

  .difficulty-selector { display: flex; flex-direction: column; gap: 8px; align-items: center; }
  .diff-buttons { display: flex; gap: 6px; }
  .diff-btn {
    display: flex; flex-direction: column; align-items: center; gap: 2px;
    padding: 8px 12px; border-radius: 8px; cursor: pointer; transition: all 0.15s;
    background: white; border: 2px solid #e2e8f0; font-family: inherit;
  }
  .diff-btn.active { border-color: #00e5ff; background: #00e5ff10; }
  :global(.dark) .diff-btn { background: #141414; border-color: rgba(255,255,255,0.1); }
  :global(.dark) .diff-btn.active { border-color: #00e5ff; background: rgba(0,229,255,0.1); }
  .diff-icon { font-size: 1.1rem; }
  .diff-text { font-size: 0.7rem; font-weight: 600; opacity: 0.7; }

  .setup-section { display: flex; flex-direction: column; gap: 12px; }
  .piece-selector { display: flex; flex-direction: column; gap: 8px; align-items: center; }
  .piece-label { font-size: 0.82rem; opacity: 0.7; }
  .piece-buttons { display: flex; gap: 10px; }
  .piece-btn {
    width: 52px; height: 52px; border-radius: 8px; cursor: pointer; transition: all 0.15s;
    display: flex; align-items: center; justify-content: center;
  }
  .piece-btn.active { border-color: #00e5ff; box-shadow: 0 0 0 2px #00e5ff; }
  :global(.dark) .piece-btn.active { border-color: #00e5ff; box-shadow: 0 0 0 2px #00e5ff; }
  .piece-x { color: #00e5ff; font-size: 1.4rem; font-weight: 800; }
  .piece-o { color: #ff9100; font-size: 1.4rem; font-weight: 800; }

  .player-header { display: flex; align-items: center; gap: 10px; margin-bottom: 6px; }
  .piece-icon { font-weight: 800; font-size: 1.1rem; }
  .icon-x { color: #00e5ff; }
  .icon-o { color: #ff9100; }
  .your-piece { font-size: 0.72rem; opacity: 0.6; display: block; margin-bottom: 4px; }

  .board-wrapper { display: flex; justify-content: center; }
  .board {
    display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px;
    width: 420px; height: 420px; flex-shrink: 0;
  }
  @media (max-width: 400px) { .board { width: 300px; height: 300px; } }

  .cell {
    border-radius: 6px; display: flex; justify-content: center; align-items: center;
    cursor: pointer; transition: all 0.15s; font-size: 2.2rem; font-weight: 800;
    overflow: hidden; border: 3px solid; aspect-ratio: 1;
  }
  .cell-x .cell-symbol { color: #00e5ff; }
  .cell-o .cell-symbol { color: #ff9100; }
  .cell-win { border-color: #00c853 !important; }
  .cell-symbol { line-height: 1; display: flex; align-items: center; justify-content: center; width: 100%; height: 100%; }

  .start-btn {
    width: 100%; padding: 12px; font-weight: 700; font-size: 0.78rem;
    letter-spacing: 1px; cursor: pointer; border-radius: 6px; transition: all 0.15s;
    font-family: inherit; border: none;
  }

  .stop-btn {
    width: 100%; padding: 10px; font-weight: 700; font-size: 0.75rem;
    letter-spacing: 0.5px; cursor: pointer; border-radius: 6px; transition: all 0.15s;
    font-family: inherit; border: 2px solid #ff1744; color: #ff1744;
    background: transparent; margin-top: 4px;
  }
  .stop-btn:hover { background: #ff174410; }

  .summary-view { text-align: center; animation: fadeIn 0.4s ease; }
  .summary-title { font-size: 1.1rem; font-weight: 700; margin-bottom: 20px; }
  .summary-scores { display: flex; align-items: center; justify-content: center; gap: 20px; margin-bottom: 16px; }
  .summary-score { display: flex; flex-direction: column; align-items: center; gap: 4px; }
  .summary-wins { font-size: 2rem; font-weight: 800; }
  .summary-divider { font-size: 1.5rem; opacity: 0.3; }

  .badge-container { display: flex; gap: 8px; justify-content: center; margin-top: 12px; }
  .badge {
    width: 32px; height: 32px; border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-size: 0.75rem; font-weight: 700; border: 1px solid;
  }
  .badge-win { border-color: #00c853; color: #00c853; }
  .badge-lose { border-color: #ff1744; color: #ff1744; }
  .badge-tie { border-color: #455a64; color: #455a64; }

  .announcement-overlay {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    display: flex; align-items: center; justify-content: center;
    background: rgba(0,0,0,0.6); backdrop-filter: blur(4px); z-index: 50;
    animation: fadeIn 0.2s ease;
  }
  .announcement-box {
    font-size: 1.8rem; font-weight: 800; padding: 24px 48px;
    border: 2px solid; border-radius: 12px;
    animation: popIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  }

  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  @keyframes popIn { from { opacity: 0; transform: scale(0.8); } to { opacity: 1; transform: scale(1); } }
</style>
