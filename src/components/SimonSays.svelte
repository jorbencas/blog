<script>
  let difficulty = $state("medium");
  let gameActive = $state(false);
  let showingSequence = $state(false);
  let level = $state(1);
  let maxLevel = $state(20);
  let score = $state(0);
  let highScore = $state(0);
  let sequence = $state([]);
  let playerSequence = $state([]);
  let colors = $state(["red", "blue", "green", "yellow"]);
  let activeColor = $state("");
  let announcement = $state("");
  let announcementColor = $state("");
  let showAnnouncement = $state(false);
  let gameOver = $state(false);
  let roundHistory = $state([]);

  const COLOR_MAP = {
    red: { bg: "#ef4444", glow: "rgba(239,68,68,0.6)" },
    blue: { bg: "#3b82f6", glow: "rgba(59,130,246,0.6)" },
    green: { bg: "#22c55e", glow: "rgba(34,197,94,0.6)" },
    yellow: { bg: "#eab308", glow: "rgba(234,179,8,0.6)" },
    purple: { bg: "#a855f7", glow: "rgba(168,85,247,0.6)" },
    orange: { bg: "#f97316", glow: "rgba(249,115,22,0.6)" },
  };

  const SPEED_MAP = { easy: 800, medium: 500, hard: 300 };

  function getSpeed() {
    const base = SPEED_MAP[difficulty];
    const reduction = Math.min(level * 15, base - 150);
    return base - reduction;
  }

  function startGame() {
    level = 1;
    score = 0;
    sequence = [];
    playerSequence = [];
    gameOver = false;
    roundHistory = [];
    gameActive = true;
    nextRound();
  }

  function nextRound() {
    playerSequence = [];
    showingSequence = true;
    gameActive = true;

    if (level === 5 && colors.length === 4) {
      colors = [...colors, "purple"];
    }
    if (level === 10 && colors.length === 5) {
      colors = [...colors, "orange"];
    }

    const randomColor = colors[Math.floor(Math.random() * colors.length)];
    sequence = [...sequence, randomColor];

    playSequence();
  }

  async function playSequence() {
    showingSequence = true;
    await waitFor(600);

    for (let i = 0; i < sequence.length; i++) {
      if (!gameActive) return;
      const c = sequence[i];
      activeColor = c;
      await waitFor(getSpeed() * 0.7);
      activeColor = "";
      await waitFor(getSpeed() * 0.4);
    }

    showingSequence = false;
  }

  function handleColorClick(color) {
    if (!gameActive || showingSequence) return;

    playerSequence = [...playerSequence, color];
    const idx = playerSequence.length - 1;

    if (playerSequence[idx] !== sequence[idx]) {
      handleWrong();
      return;
    }

    activeColor = color;
    setTimeout(() => { activeColor = ""; }, 200);

    if (playerSequence.length === sequence.length) {
      score += level * 10;
      roundHistory.push("win");
      level++;

      if (level > maxLevel) {
        handleWin();
        return;
      }

      setTimeout(nextRound, 800);
    }
  }

  function handleWrong() {
    gameActive = false;
    gameOver = true;
    roundHistory.push("lose");
    if (score > highScore) highScore = score;

    announcement = `¡Error! Nivel ${level}`;
    announcementColor = "#ef4444";
    showAnnouncement = true;
    setTimeout(() => { showAnnouncement = false; }, 2000);
  }

  function handleWin() {
    gameActive = false;
    gameOver = true;
    score += 500;
    roundHistory.push("win");
    if (score > highScore) highScore = score;

    announcement = "¡Completaste todos los niveles!";
    announcementColor = "#22c55e";
    showAnnouncement = true;
  }

  function resetAll() {
    resetGame();
  }

  async function repeatSequence() {
    if (!gameActive || showingSequence || difficulty !== "easy") return;
    showingSequence = true;
    await waitFor(400);
    for (let i = 0; i < sequence.length; i++) {
      if (!gameActive) return;
      const c = sequence[i];
      activeColor = c;
      await waitFor(getSpeed() * 0.7);
      activeColor = "";
      await waitFor(getSpeed() * 0.4);
    }
    showingSequence = false;
  }

  function resetGame() {
    level = 1;
    score = 0;
    sequence = [];
    playerSequence = [];
    colors = ["red", "blue", "green", "yellow"];
    gameActive = false;
    gameOver = false;
    showingSequence = false;
    showAnnouncement = false;
    roundHistory = [];
  }

  function waitFor(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
  }

  function getColorStyle(color) {
    const c = COLOR_MAP[color];
    if (!c) return "";
    const isActive = activeColor === color;
    if (isActive) {
      return `background-color: ${c.bg}; box-shadow: 0 0 40px ${c.glow}, 0 0 80px ${c.glow}, inset 0 0 30px rgba(255,255,255,0.3); transform: scale(1.08); border: 3px solid rgba(255,255,255,0.6); filter: brightness(1.3);`;
    }
    return `background-color: ${c.bg}; box-shadow: 0 4px 15px rgba(0,0,0,0.3); border: 3px solid transparent;`;
  }
</script>

<div class="simon-wrapper">
  <h2 class="simon-title">SIMON DICE</h2>

  <div class="simon-layout">
    <!-- Panel lateral -->
    <div class="side-panel">
      {#if !gameActive && !gameOver}
        <div class="setup-section">
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

          <button type="button" class="start-btn bg-slate-900 dark:bg-white text-white dark:text-black hover:bg-slate-800 dark:hover:bg-slate-200" onclick={startGame}>EMPEZAR</button>
        </div>
      {/if}

      {#if gameActive || gameOver}
        <div class="stats-card bg-white dark:bg-[#141414] border border-slate-200 dark:border-white/[0.06]">
          <div class="stat-row">
            <span class="stat-label">Nivel</span>
            <span class="stat-value">{level} / {maxLevel}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Puntos</span>
            <span class="stat-value score">{score}</span>
          </div>
          <div class="stat-row">
            <span class="stat-label">Récord</span>
            <span class="stat-value high">{highScore}</span>
          </div>
        </div>

        <div class="progress-bar">
          <div class="progress-fill" style="width: {(level / maxLevel) * 100}%"></div>
        </div>

        {#if showingSequence}
          <div class="status-badge showing">👁 Observa la secuencia</div>
        {:else if gameActive}
          <div class="status-badge your-turn">🎯 Tu turno</div>
        {/if}

        {#if gameActive && !showingSequence && difficulty === 'easy'}
          <button type="button" class="repeat-btn" onclick={repeatSequence}>🔄 Repetir secuencia</button>
        {/if}

        {#if gameActive}
          <button type="button" class="stop-btn" onclick={resetGame}>⏹ DETENER</button>
        {/if}

        {#if gameOver}
          <button type="button" class="start-btn bg-slate-900 dark:bg-white text-white dark:text-black hover:bg-slate-800 dark:hover:bg-slate-200" onclick={resetAll}>VOLVER A EMPEZAR</button>
        {/if}
      {/if}

      {#if roundHistory.length > 0}
        <div class="badge-container">
          {#each roundHistory as result}
            <div class="badge" class:badge-win={result === 'win'} class:badge-lose={result === 'lose'}>
              {result === 'win' ? '✓' : '✗'}
            </div>
          {/each}
        </div>
      {/if}
    </div>

    <!-- Tablero de colores -->
    <div class="board-wrapper">
      <div class="simon-board">
        {#each colors as color}
          <button
            type="button"
            class="color-btn"
            style={getColorStyle(color)}
            disabled={!gameActive || showingSequence}
            onclick={() => handleColorClick(color)}
          >
            <span class="color-label">{color}</span>
          </button>
        {/each}
      </div>
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
  .simon-wrapper { max-width: 900px; margin: 0 auto; text-align: center; }
  .simon-title { font-size: 0.85rem; letter-spacing: 0.4rem; font-weight: 300; opacity: 0.6; margin-bottom: 30px; }

  .simon-layout { display: flex; gap: 50px; align-items: flex-start; justify-content: center; }
  @media (max-width: 700px) { .simon-layout { flex-direction: column; align-items: center; gap: 24px; } }

  .side-panel { flex: 0 0 240px; display: flex; flex-direction: column; gap: 14px; }
  @media (max-width: 700px) { .side-panel { flex: none; width: 100%; max-width: 320px; } }

  .setup-section { display: flex; flex-direction: column; gap: 16px; }

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

  .piece-label { font-size: 0.82rem; opacity: 0.7; }

  .start-btn {
    width: 100%; padding: 12px; font-weight: 700; font-size: 0.78rem;
    letter-spacing: 1px; cursor: pointer; border-radius: 6px; transition: all 0.15s;
    font-family: inherit; border: none;
  }

  .stop-btn {
    width: 100%; padding: 10px; font-weight: 700; font-size: 0.75rem;
    letter-spacing: 0.5px; cursor: pointer; border-radius: 6px; transition: all 0.15s;
    font-family: inherit; border: 2px solid #ef4444; color: #ef4444;
    background: transparent; margin-top: 4px;
  }
  .stop-btn:hover { background: rgba(239,68,68,0.1); }

  .stats-card {
    padding: 16px; border-radius: 8px; display: flex; flex-direction: column; gap: 10px;
  }
  .stat-row { display: flex; justify-content: space-between; align-items: center; }
  .stat-label { font-size: 0.78rem; opacity: 0.6; }
  .stat-value { font-size: 1rem; font-weight: 700; }
  .stat-value.score { color: #00e5ff; }
  .stat-value.high { color: #ff9100; }

  .progress-bar {
    width: 100%; height: 6px; background: #e2e8f0; border-radius: 3px; overflow: hidden;
  }
  :global(.dark) .progress-bar { background: rgba(255,255,255,0.1); }
  .progress-fill {
    height: 100%; background: linear-gradient(90deg, #00e5ff, #22c55e);
    border-radius: 3px; transition: width 0.4s ease;
  }

  .status-badge {
    padding: 8px 16px; border-radius: 20px; font-size: 0.78rem; font-weight: 600;
    text-align: center;
  }
  .status-badge.showing { background: rgba(234,179,8,0.15); color: #eab308; border: 1px solid rgba(234,179,8,0.3); }
  .status-badge.your-turn { background: rgba(34,197,94,0.15); color: #22c55e; border: 1px solid rgba(34,197,94,0.3); }

  .repeat-btn {
    width: 100%; padding: 10px; font-weight: 700; font-size: 0.75rem;
    letter-spacing: 0.5px; cursor: pointer; border-radius: 6px; transition: all 0.15s;
    font-family: inherit; border: 2px solid #00e5ff; color: #00e5ff;
    background: rgba(0,229,255,0.08);
  }
  .repeat-btn:hover { background: rgba(0,229,255,0.18); }

  .board-wrapper { display: flex; justify-content: center; }
  .simon-board {
    display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px;
    width: 340px; height: 340px;
  }
  @media (max-width: 400px) { .simon-board { width: 280px; height: 280px; } }

  .color-btn {
    border-radius: 12px; border: 3px solid transparent; cursor: pointer;
    transition: all 0.15s ease;
    display: flex; align-items: center; justify-content: center;
    font-family: inherit; color: white; font-weight: 700; font-size: 0.85rem;
    letter-spacing: 0.5px; text-transform: uppercase;
  }
  .color-btn:not(:disabled):hover { transform: scale(1.03); }
  .color-btn:not(:disabled):active { transform: scale(0.97); }
  .color-btn:disabled { cursor: not-allowed; opacity: 0.7; }
  .color-label { text-shadow: 0 1px 3px rgba(0,0,0,0.4); pointer-events: none; }

  .badge-container { display: flex; gap: 6px; justify-content: center; flex-wrap: wrap; margin-top: 8px; }
  .badge {
    width: 28px; height: 28px; border-radius: 50%; display: flex; align-items: center;
    justify-content: center; font-size: 0.7rem; font-weight: 700; border: 1px solid;
  }
  .badge-win { border-color: #22c55e; color: #22c55e; }
  .badge-lose { border-color: #ef4444; color: #ef4444; }

  .announcement-overlay {
    position: fixed; top: 0; left: 0; right: 0; bottom: 0;
    display: flex; align-items: center; justify-content: center;
    background: rgba(0,0,0,0.6); backdrop-filter: blur(4px); z-index: 50;
    animation: fadeIn 0.2s ease;
  }
  .announcement-box {
    font-size: 1.5rem; font-weight: 800; padding: 24px 48px;
    border: 2px solid; border-radius: 12px; background: white;
    animation: popIn 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
  }
  :global(.dark) .announcement-box { background: #141414; }

  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
  @keyframes popIn { from { opacity: 0; transform: scale(0.8); } to { opacity: 1; transform: scale(1); } }
</style>
