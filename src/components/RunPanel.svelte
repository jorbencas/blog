<script>
  let { code = '', language = 'javascript' } = $props();
  let output = $state([]);
  let running = $state(false);
  let pyodide = $state(null);
  let pyodideLoading = $state(false);
  let expanded = $state(false);

  function getLangKey(raw) {
    return (raw || '').toLowerCase();
  }

  async function loadPyodide() {
    if (pyodide) return pyodide;
    pyodideLoading = true;
    try {
      if (!window.loadPyodide) {
        const script = document.createElement('script');
        script.src = 'https://cdn.jsdelivr.net/pyodide/v0.25.1/full/pyodide.js';
        document.head.appendChild(script);
        await new Promise((resolve, reject) => {
          script.onload = resolve;
          script.onerror = reject;
        });
      }
      pyodide = await window.loadPyodide({
        indexURL: 'https://cdn.jsdelivr.net/pyodide/v0.25.1/full/',
      });
      return pyodide;
    } finally {
      pyodideLoading = false;
    }
  }

  async function runCode() {
    if (running) return;
    running = true;
    output = [];
    expanded = true;
    const lang = getLangKey(language);

    try {
      if (lang === 'python' || lang === 'py') {
        await runPython();
      } else if (lang === 'javascript' || lang === 'js') {
        await runJavaScript();
      } else {
        output = [{ type: 'error', text: `Ejecución no disponible para "${language}". Solo Python y JavaScript.` }];
      }
    } catch (err) {
      output = [{ type: 'error', text: err.message || String(err) }];
    } finally {
      running = false;
    }
  }

  async function runPython() {
    const py = await loadPyodide();
    let logs = [];
    py.setStdout({ batched: (msg) => logs.push(msg) });
    py.setStderr({ batched: (msg) => logs.push({ type: 'error', text: msg }) });
    try {
      py.runPython(code);
      output = logs.map(l => typeof l === 'string' ? { type: 'log', text: l } : l);
      if (output.length === 0) {
        output = [{ type: 'log', text: '(sin salida)' }];
      }
    } catch (err) {
      output = [...logs.map(l => typeof l === 'string' ? { type: 'log', text: l } : l), { type: 'error', text: err.message }];
    }
  }

  async function runJavaScript() {
    let logs = [];
    const origLog = console.log;
    const origError = console.error;
    const origWarn = console.warn;

    console.log = (...args) => logs.push({ type: 'log', text: args.map(a => typeof a === 'object' ? JSON.stringify(a, null, 2) : String(a)).join(' ') });
    console.error = (...args) => logs.push({ type: 'error', text: args.map(String).join(' ') });
    console.warn = (...args) => logs.push({ type: 'warn', text: args.map(String).join(' ') });

    try {
      const AsyncFunction = Object.getPrototypeOf(async function(){}).constructor;
      const fn = new AsyncFunction(code);
      await fn();
      output = logs.length > 0 ? logs : [{ type: 'log', text: '(sin salida)' }];
    } catch (err) {
      output = [...logs, { type: 'error', text: err.message || String(err) }];
    } finally {
      console.log = origLog;
      console.error = origError;
      console.warn = origWarn;
    }
  }
</script>

<div class="run-panel">
  <button
    type="button"
    class="run-btn"
    onclick={runCode}
    disabled={running || pyodideLoading}
  >
    {#if running || pyodideLoading}
      <svg class="w-3.5 h-3.5 animate-spin" fill="none" viewBox="0 0 24 24">
        <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"/>
        <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"/>
      </svg>
      <span>{pyodideLoading ? 'Cargando Python...' : 'Ejecutando...'}</span>
    {:else}
      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <polygon points="5 3 19 12 5 21 5 3"/>
      </svg>
      <span>EJECUTAR</span>
    {/if}
  </button>

  {#if expanded && (output.length > 0 || running)}
    <div class="output-panel">
      <div class="output-header">
        <span class="output-title">Salida</span>
        <button type="button" class="output-close" onclick={() => { expanded = false; output = []; }}>×</button>
      </div>
      <div class="output-content">
        {#each output as line}
          <div class="output-line" class:error={line.type === 'error'} class:warn={line.type === 'warn'}>
            {#if line.type === 'error'}<span class="prefix">✗ </span>{:else if line.type === 'warn'}<span class="prefix">⚠ </span>{:else}<span class="prefix">› </span>{/if}{line.text}
          </div>
        {/each}
        {#if running}
          <div class="output-line running">Ejecutando...</div>
        {/if}
      </div>
    </div>
  {/if}
</div>

<style>
  .run-panel {
    display: flex;
    flex-direction: column;
  }

  .run-btn {
    margin-left: 0.5rem;
    padding: 0.35rem 0.75rem;
    display: flex;
    align-items: center;
    gap: 0.35rem;
    font-size: 0.65rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: rgb(34 197 94);
    background: transparent;
    border: none;
    border-radius: 0.375rem;
    cursor: pointer;
    transition: color 0.15s ease, background 0.15s ease;
    white-space: nowrap;
    flex-shrink: 0;
  }

  .run-btn:hover:not(:disabled) {
    color: rgb(22 163 74);
    background: rgb(34 197 94 / 0.1);
  }

  .run-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
  }

  :global(.dark) .run-btn {
    color: rgb(74 222 128);
  }

  :global(.dark) .run-btn:hover:not(:disabled) {
    color: rgb(34 197 94);
    background: rgb(74 222 128 / 0.1);
  }

  .animate-spin {
    animation: spin 1s linear infinite;
  }

  @keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  .output-panel {
    border-top: 1px solid rgb(148 163 184 / 0.2);
    background: rgb(15 23 42);
    border-radius: 0 0 0.5rem 0.5rem;
    overflow: hidden;
  }

  .output-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.35rem 0.75rem;
    border-bottom: 1px solid rgb(148 163 184 / 0.1);
  }

  .output-title {
    font-size: 0.6rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    color: rgb(148 163 184);
  }

  .output-close {
    background: none;
    border: none;
    color: rgb(148 163 184);
    cursor: pointer;
    font-size: 1rem;
    padding: 0;
    line-height: 1;
  }

  .output-close:hover {
    color: rgb(248 250 252);
  }

  .output-content {
    padding: 0.75rem;
    max-height: 300px;
    overflow-y: auto;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    font-size: 0.8rem;
    line-height: 1.6;
  }

  .output-line {
    color: rgb(226 232 240);
    white-space: pre-wrap;
    word-break: break-all;
  }

  .output-line .prefix {
    color: rgb(100 116 139);
    user-select: none;
  }

  .output-line.error {
    color: rgb(248 113 113);
  }

  .output-line.error .prefix {
    color: rgb(239 68 68);
  }

  .output-line.warn {
    color: rgb(250 204 21);
  }

  .output-line.warn .prefix {
    color: rgb(234 179 8);
  }

  .output-line.running {
    color: rgb(148 163 184);
    font-style: italic;
  }
</style>
