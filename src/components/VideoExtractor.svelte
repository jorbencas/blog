<script>
  import { onMount } from 'svelte';
  let currentFile = $state(null);
  let activeTab = $state("cutter"); 
  
  let isExtracting = $state(false);
  let progress = $state(0);
  let statusText = $state("Procesando...");
  let videoPreviewSrc = $state("");

  // PESTAÑA 1: FRAMES & SLIDESHOW
  let imagesDataURLs = $state([]);
  let timestamps = $state([]);
  let extractMode = $state("total"); 
  let numFrames = $state(10);
  let intervalMs = $state(500);
  let activeLightboxIndex = $state(null);

  // PESTAÑA 2: CORTADOR DE VÍDEO
  let savedCuts = $state([]); 
  let cropStart = $state(0);
  let cropEnd = $state(10);
  let maxDuration = $state(0);
  let cropMode = $state("keep"); 
  let cropStartStr = $state("00:00:00");
  let cropEndStr = $state("00:00:00");

  let visibleVideoElement = $state(null);

  let fileInput = null;
  let cancelRequested = false;
  let videoElement = null;
  let canvas = null;
  let ctx = null;

  onMount(() => {
    videoElement = document.createElement("video");
    videoElement.muted = true;
    videoElement.className = "hidden-video-decoder";
    document.body.appendChild(videoElement);
    
    canvas = document.createElement("canvas");
    ctx = canvas.getContext("2d");

    // Manejo de teclado para el visor (Esc, Flechas)
    const handleKeyDown = (e) => {
      if (activeLightboxIndex === null) return;
      if (e.key === "Escape") activeLightboxIndex = null;
      if (e.key === "ArrowRight") navigateLightbox(1);
      if (e.key === "ArrowLeft") navigateLightbox(-1);
    };

    window.addEventListener("keydown", handleKeyDown);
    return () => { 
      if (videoElement) videoElement.remove(); 
      window.removeEventListener("keydown", handleKeyDown);
    };
  });

  // --- HELPERS DE TIEMPO ---
  function secondsToHHMMSS(totalSeconds) {
    if (isNaN(totalSeconds) || totalSeconds < 0) return "00:00:00";
    const hrs = Math.floor(totalSeconds / 3600);
    const mins = Math.floor((totalSeconds % 3600) / 60);
    const secs = Math.floor(totalSeconds % 60);
    return `${String(hrs).padStart(2, "0")}:${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}`;
  }

  function hhmmssToSeconds(str) {
    const parts = str.trim().split(':');
    if (parts.length !== 3) return 0;
    const hrs = parseInt(parts[0], 10) || 0;
    const mins = parseInt(parts[1], 10) || 0;
    const secs = parseFloat(parts[2]) || 0;
    return (hrs * 3600) + (mins * 60) + secs;
  }

  function formatTimeWithMs(seconds) {
    const hrs = Math.floor(seconds / 3600);
    const mins = Math.floor((seconds % 3600) / 60);
    const secs = Math.floor(seconds % 60);
    const ms = Math.floor((seconds - Math.floor(seconds)) * 1000);
    return `${String(hrs).padStart(2, "0")}:${String(mins).padStart(2, "0")}:${String(secs).padStart(2, "0")}.${String(ms).padStart(3, "0")}`;
  }

  function updateInputsFromSeconds() {
    cropStartStr = secondsToHHMMSS(cropStart);
    cropEndStr = secondsToHHMMSS(cropEnd);
  }

  // --- LÓGICA DE AJUSTE DE SEGUNDOS ---
  function tweakTime(type, amount) {
    if (type === 'start') {
      cropStart = Math.max(0, Math.min(cropStart + amount, cropEnd));
      syncVideoCurrentTime(cropStart);
    } else {
      cropEnd = Math.max(cropStart, Math.min(cropEnd + amount, maxDuration));
      syncVideoCurrentTime(cropEnd);
    }
    updateInputsFromSeconds();
  }

  function handleTextInputChange(type) {
    if (type === 'start') {
      const secs = hhmmssToSeconds(cropStartStr);
      cropStart = Math.max(0, Math.min(secs, cropEnd));
      syncVideoCurrentTime(cropStart);
    } else {
      const secs = hhmmssToSeconds(cropEndStr);
      cropEnd = Math.max(cropStart, Math.min(secs, maxDuration));
      syncVideoCurrentTime(cropEnd);
    }
    updateInputsFromSeconds();
  }

  // --- LÓGICA DEL SLIDESHOW / VISOR ---
  function openLightbox(index) {
    activeLightboxIndex = index;
  }

  function navigateLightbox(direction) {
    if (activeLightboxIndex === null) return;
    let newIndex = activeLightboxIndex + direction;
    if (newIndex < 0) newIndex = imagesDataURLs.length - 1;
    if (newIndex >= imagesDataURLs.length) newIndex = 0;
    activeLightboxIndex = newIndex;
  }

  function syncVideoCurrentTime(timeInSec) {
    if (visibleVideoElement && !isNaN(timeInSec)) {
      visibleVideoElement.currentTime = timeInSec;
    }
  }

  // --- MOTOR EXTRACCIÓN DE FRAMES ---
  function yieldToMain() {
    return new Promise(resolve => setTimeout(resolve, 0));
  }

  async function extractFrames() {
    if (!currentFile) return;
    imagesDataURLs = [];
    timestamps = [];
    cancelRequested = false;
    progress = 0;
    statusText = "Preparando decodificador...";
    isExtracting = true;

    const duration = maxDuration;

    if (extractMode === "total") {
      const total = Math.max(2, parseInt(numFrames) || 10);
      for (let i = 0; i < total; i++) { 
        timestamps.push((i / (total - 1)) * duration); 
      }
    } else {
      const step = (parseInt(intervalMs) || 500) / 1000;
      for (let t = 0; t <= duration; t += step) { 
        timestamps.push(t); 
      }
    }

    const BATCH_SIZE = 5;
    for (let i = 0; i < timestamps.length; i++) {
      if (cancelRequested) break;
      try {
        await seekVideoTo(timestamps[i]);
        canvas.width = videoElement.videoWidth || 640;
        canvas.height = videoElement.videoHeight || 360;
        ctx.drawImage(videoElement, 0, 0, canvas.width, canvas.height);
        imagesDataURLs.push(canvas.toDataURL("image/jpeg", 0.85));
      } catch (err) {
        // Fallo silencioso
      }
      if (i % BATCH_SIZE === 0) {
        statusText = `Procesando: ${imagesDataURLs.length} / ${timestamps.length} imágenes`;
        progress = Math.round(((i + 1) / timestamps.length) * 100);
        await yieldToMain();
      }
    }
    statusText = cancelRequested ? "Extracción cancelada" : `¡${imagesDataURLs.length} fotogramas extraídos!`;
    isExtracting = false;
  }

  // --- GESTIÓN DE CORTES ---
  function addCurrentCut() {
    if (cropEnd <= cropStart) return;
    savedCuts.push({
      id: crypto.randomUUID(),
      start: cropStart,
      end: cropEnd,
      mode: cropMode,
      startStr: secondsToHHMMSS(cropStart),
      endStr: secondsToHHMMSS(cropEnd)
    });
  }

  function removeCut(id) {
    savedCuts = savedCuts.filter(c => c.id !== id);
  }

  function getSupportedMimeType() {
    const types = [
      'video/webm;codecs=vp9,opus',
      'video/webm;codecs=vp8,opus',
      'video/webm;codecs=vp9',
      'video/webm;codecs=vp8',
      'video/webm',
      'video/mp4;codecs=h264,aac',
      'video/mp4',
    ];
    for (const t of types) {
      if (MediaRecorder.isTypeSupported(t)) return t;
    }
    return '';
  }

  async function processSingleCut(cut) {
    return new Promise((resolve) => {
      let resolved = false;
      const doResolve = () => {
        if (!resolved) { resolved = true; cleanup(); resolve(); }
      };
      const onSeeked = () => {
        visibleVideoElement.removeEventListener('seeked', onSeeked);
        const stream = visibleVideoElement.captureStream();
        const mimeType = getSupportedMimeType();
        const recorder = new MediaRecorder(stream, mimeType ? { mimeType } : {});
        const chunks = [];
        recorder.ondataavailable = (e) => chunks.push(e.data);
        recorder.onstop = () => {
          visibleVideoElement.pause();
          const blob = new Blob(chunks, { type: recorder.mimeType || 'video/webm' });
          const ext = recorder.mimeType.includes('mp4') ? 'mp4' : 'webm';
          const url = URL.createObjectURL(blob);
          const a = document.createElement('a');
          a.href = url;
          a.download = `recorte_${(currentFile?.name || 'video').replace(/\.[^.]+$/, '')}_${cut.startStr.replace(/:/g, '-')}_${cut.endStr.replace(/:/g, '-')}.${ext}`;
          a.click();
          URL.revokeObjectURL(url);
          doResolve();
        };
        recorder.onerror = () => {
          visibleVideoElement.pause();
          doResolve();
        };
        const durationMs = Math.max(100, (cut.end - cut.start) * 1000);
        recorder.start();
        visibleVideoElement.play();
        setTimeout(() => recorder.stop(), durationMs);
      };
      const cleanup = () => {
        visibleVideoElement.removeEventListener('seeked', onSeeked);
      };
      visibleVideoElement.addEventListener('seeked', onSeeked, { once: true });
      visibleVideoElement.currentTime = cut.start;
      setTimeout(doResolve, 10000);
    });
  }

  async function processVideoCuts() {
    if (savedCuts.length === 0) return;
    const keepCuts = savedCuts.filter(c => c.mode === 'keep');
    if (keepCuts.length === 0) {
      alert('No hay tramos en modo "Conservar". Cambia el modo o añade tramos.');
      return;
    }
    if (!HTMLVideoElement.prototype.captureStream) {
      alert('Tu navegador no soporta captureStream. Usa Chrome o Edge.');
      return;
    }
    const isFirefox = navigator.userAgent.includes('Firefox');
    const totalSeconds = keepCuts.reduce((sum, c) => sum + (c.end - c.start), 0);
    const maxSegment = Math.max(...keepCuts.map(c => c.end - c.start));

    if (isFirefox) {
      alert('Firefox no captura audio con captureStream. Los segmentos se descargarán sin sonido.');
    }

    if (maxSegment > 300) {
      const ok = confirm(
        `El tramo más largo es de ${Math.round(maxSegment)}s (${Math.round(maxSegment / 60)} min).\n\n` +
        `La grabación es en TIEMPO REAL: tardará al menos ese tiempo.\n\n` +
        `¿Continuar?`
      );
      if (!ok) return;
    } else if (totalSeconds > 30) {
      const ok = confirm(
        `Duración total: ${Math.round(totalSeconds)}s. ` +
        `La grabación tardará al menos ese tiempo. ¿Continuar?`
      );
      if (!ok) return;
    }

    cancelRequested = false;
    progress = 0;
    isExtracting = true;
    const startTime = Date.now();

    for (let i = 0; i < keepCuts.length; i++) {
      if (cancelRequested) break;
      const cut = keepCuts[i];
      const cutDuration = cut.end - cut.start;
      statusText = `Tramo ${i + 1}/${keepCuts.length}: ${cut.startStr} → ${cut.endStr} (${Math.round(cutDuration)}s)`;
      try { await processSingleCut(cut); } catch (e) { console.error(e); }
      progress = Math.round(((i + 1) / keepCuts.length) * 100);
      await yieldToMain();
    }

    const elapsed = Math.round((Date.now() - startTime) / 1000);
    statusText = cancelRequested
      ? `Cancelado tras ${elapsed}s`
      : `¡${keepCuts.length} tramo(s) descargado(s)! (${elapsed}s de procesamiento)`;
    isExtracting = false;
  }

  // --- MANEJO DE ARCHIVOS ---
  async function handleFile(file) {
    if (!file || !file.type.startsWith("video/")) return;
    if (videoPreviewSrc) URL.revokeObjectURL(videoPreviewSrc);

    currentFile = file;
    imagesDataURLs = [];
    savedCuts = [];
    activeLightboxIndex = null;
    
    videoPreviewSrc = URL.createObjectURL(file);
    videoElement.src = videoPreviewSrc;
    videoElement.load();

    await new Promise((resolve) => {
      videoElement.onloadedmetadata = () => {
        maxDuration = videoElement.duration || 0;
        cropStart = 0;
        cropEnd = maxDuration;
        updateInputsFromSeconds();
        resolve();
      };
    });
  }

  function seekVideoTo(timeInSec) {
    return new Promise((resolve) => {
      const target = Math.min(timeInSec, videoElement.duration || 0);
      let resolved = false;
      const timeout = setTimeout(() => {
        if (!resolved) { resolved = true; resolve(); }
      }, 3000);
      const onSeeked = () => {
        if (!resolved) {
          resolved = true;
          clearTimeout(timeout);
          videoElement.removeEventListener("seeked", onSeeked);
          resolve();
        }
      };
      videoElement.addEventListener("seeked", onSeeked);
      videoElement.currentTime = target;
    });
  }

  function downloadSingleFrame(e, data, index) {
    e.stopPropagation(); 
    const a = document.createElement("a");
    a.href = data;
    a.download = `frame_${index + 1}.jpg`;
    document.body.appendChild(a);
    a.click();
    a.remove();
  }

  function reset() {
    if (videoPreviewSrc) URL.revokeObjectURL(videoPreviewSrc);
    cancelRequested = true;
    currentFile = null; 
    savedCuts = []; 
    imagesDataURLs = []; 
    timestamps = [];
    videoPreviewSrc = ""; 
    activeLightboxIndex = null;
    isExtracting = false;
    progress = 0;
    cropStart = 0;
    cropEnd = 0;
    cropStartStr = "00:00:00";
    cropEndStr = "00:00:00";
    maxDuration = 0;
    if (fileInput) fileInput.value = "";
  }
</script>

<div class="extractor-wrapper text-slate-800 dark:text-slate-100">
  
  <div class="dropzone border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-900/50" class:drop-ready={currentFile} onclick={() => fileInput.click()} role="button" tabindex="0" onkeydown={(e) => e.key === 'Enter' && fileInput.click()}>
    <div class="dropzone-title font-semibold">{currentFile ? '✓ Vídeo listo' : 'Selecciona o arrastra tu vídeo aquí'}</div>
    {#if currentFile}
      <span class="filename text-slate-500 dark:text-slate-400">{currentFile.name}</span>
    {/if}
  </div>
  <input type="file" bind:this={fileInput} onchange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])} accept="video/*" class="hidden-input" />

  {#if currentFile}
    <div class="video-preview-wrapper">
      <video src={videoPreviewSrc} bind:this={visibleVideoElement} class="video-preview" controls></video>
    </div>

    <div class="tabs-navigation bg-slate-100 dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
      <button type="button" class="tab-btn text-slate-600 dark:text-slate-400" class:active={activeTab === 'frames'} onclick={() => activeTab = 'frames'}>📸 Extraer Frames</button>
      <button type="button" class="tab-btn text-slate-600 dark:text-slate-400" class:active={activeTab === 'cutter'} onclick={() => activeTab = 'cutter'}>✂️ Cortar Vídeo</button>
    </div>

    <div class="tab-content-card bg-white dark:bg-slate-900/60 border border-slate-200 dark:border-slate-800">
      {#if activeTab === 'frames'}
        <div class="frames-tab-layout">
          <div class="settings-row">
            <div class="control-group">
              <label for="extractMode" class="text-slate-700 dark:text-slate-300">Frecuencia de muestreo:</label>
              <select id="extractMode" bind:value={extractMode} class="bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-800 dark:text-slate-100">
                <option value="total">Número fijo total de imágenes</option>
                <option value="interval">Por intervalo de tiempo</option>
              </select>
            </div>
            
            {#if extractMode === 'total'}
              <div class="control-group group-range-picker">
                <div class="label-with-value">
                  <label for="numFrames" class="text-slate-700 dark:text-slate-300">Cantidad de imágenes:</label>
                  <span class="range-badge">{numFrames} uds</span>
                </div>
                <div class="slider-input-combination">
                  <input id="numFrames" type="range" min="2" max="100" step="1" bind:value={numFrames} class="modern-slider bg-slate-200 dark:bg-slate-700" />
                  <input type="number" min="2" max="500" bind:value={numFrames} class="compact-numeric-input bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-800 dark:text-slate-100" />
                </div>
              </div>
            {:else}
              <div class="control-group">
                <label for="interval" class="text-slate-700 dark:text-slate-300">Extraer una captura cada (ms):</label>
                <input id="interval" type="number" min="10" bind:value={intervalMs} class="bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-800 dark:text-slate-100" />
              </div>
            {/if}
          </div>

          <div class="tab-actions border-slate-100 dark:border-slate-800">
            <button type="button" class="btn btn-secondary bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300" onclick={reset}>Quitar Vídeo</button>
            <button type="button" class="btn btn-primary" onclick={extractFrames}>📸 Iniciar Extracción</button>
          </div>
        </div>

        {#if imagesDataURLs.length > 0}
          <div class="results-header border-slate-300 dark:border-slate-700">
            <h3 class="text-slate-800 dark:text-slate-200">Fotogramas Obtenidos ({imagesDataURLs.length})</h3>
          </div>
          <div class="images-slider-container">
            <div class="images-grid">
              {#each imagesDataURLs as data, i}
                <div 
                  class="thumb-card interactive-thumb bg-slate-50 dark:bg-slate-800 border-slate-200 dark:border-slate-700"
                  onclick={() => openLightbox(i)}
                  title="Haga clic para expandir en el visor"
                  role="button"
                  tabindex="0"
                  onkeydown={(e) => e.key === 'Enter' && openLightbox(i)}
                >
                  <img src={data} alt="Frame {i + 1}" />
                  <div class="meta text-slate-500 dark:text-slate-400">#{i + 1} — {formatTimeWithMs(timestamps[i] || 0)}</div>
                  <button type="button" class="download-icon-btn bg-white dark:bg-slate-700 border-slate-300 dark:border-slate-600 text-slate-800 dark:text-slate-100" onclick={(e) => downloadSingleFrame(e, data, i)}>↓</button>
                </div>
              {/each}
            </div>
          </div>
        {/if}

      {:else}
        <div class="cutter-tab-layout">
          <div class="realtime-warning bg-amber-50 dark:bg-amber-950/40 border border-amber-200 dark:border-amber-800 rounded-lg p-3 text-sm text-amber-800 dark:text-amber-200">
            <strong>Tiempo real:</strong> La grabación dura lo mismo que el tramo seleccionado. Un clip de 5 min tarda 5 min. Para vídeos largos, corta en tramos pequeños.
          </div>
          <div class="cutter-header-mode">
            <span class="section-instruction text-slate-500 dark:text-slate-400">Ajusta y afina al segundo los límites del tramo utilizando los controles numéricos:</span>
            <div class="mode-selector bg-slate-100 dark:bg-slate-800 border-slate-200 dark:border-slate-700">
              <button type="button" class="mode-btn mode-keep text-slate-600 dark:text-slate-400" class:active={cropMode === 'keep'} onclick={() => cropMode = 'keep'}>🔒 Conservar</button>
              <button type="button" class="mode-btn mode-remove text-slate-600 dark:text-slate-400" class:active={cropMode === 'remove'} onclick={() => cropMode = 'remove'}>✂️ Descartar</button>
            </div>
          </div>

          <div class="precision-controls-panel-v2 bg-slate-50 dark:bg-slate-900 border-slate-200 dark:border-slate-800">
            
            <div class="precision-column">
              <span class="block-label text-slate-800 dark:text-slate-200">Inicio</span>
              <div class="input-tweak-row">
                <button type="button" class="btn-step bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300" onclick={() => tweakTime('start', -1.0)}>[-1s]</button>
                <input type="text" placeholder="00:00:00" bind:value={cropStartStr} onchange={() => handleTextInputChange('start')} class="precise-input-v2 bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100" />
                <button type="button" class="btn-step bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300" onclick={() => tweakTime('start', 1.0)}>[+1s]</button>
              </div>
            </div>

            <div class="central-action-wrapper">
              <button type="button" class="btn-add-cut-central-v2 bg-sky-50 dark:bg-sky-950/40 border-sky-200 dark:border-sky-900 text-sky-700 dark:text-sky-300" onclick={addCurrentCut}>
                + Añadir tramo seleccionado
              </button>
            </div>

            <div class="precision-column">
              <span class="block-label text-slate-800 dark:text-slate-200">Fin</span>
              <div class="input-tweak-row">
                <button type="button" class="btn-step bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300" onclick={() => tweakTime('end', -1.0)}>[-1s]</button>
                <input type="text" placeholder="00:00:00" bind:value={cropEndStr} onchange={() => handleTextInputChange('end')} class="precise-input-v2 bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-900 dark:text-slate-100" />
                <button type="button" class="btn-step bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-700 dark:text-slate-300" onclick={() => tweakTime('end', 1.0)}>[+1s]</button>
              </div>
            </div>

          </div>

          <div class="saved-cuts-container bg-slate-100 dark:bg-slate-950 border border-slate-200 dark:border-slate-800">
            <div class="saved-cuts-title text-slate-800 dark:text-slate-200">Tramos guardados (En cola)</div>
            {#if savedCuts.length > 0}
              <div class="cuts-tags-list">
                {#each savedCuts as cut, idx}
                  <div class="cut-tag bg-white dark:bg-slate-800 border-slate-300 dark:border-slate-700 text-slate-800 dark:text-slate-200" class:tag-remove={cut.mode === 'remove'}>
                    <span>#{idx + 1} ({cut.mode === 'keep' ? 'OK' : 'OUT'}): {cut.startStr} a {cut.endStr}</span>
                    <button type="button" class="btn-delete-tag text-slate-400 dark:text-slate-500" onclick={() => removeCut(cut.id)}>×</button>
                  </div>
                {/each}
              </div>
            {:else}
              <div class="no-cuts-placeholder text-slate-500 dark:text-slate-400">Sin tramos preparados</div>
            {/if}
          </div>

          <div class="tab-actions border-slate-100 dark:border-slate-800">
            <button type="button" class="btn btn-secondary bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300" onclick={reset}>Quitar Vídeo</button>
            <button type="button" class="btn btn-success" disabled={savedCuts.length === 0 || isExtracting} onclick={processVideoCuts}>
              💾 Guardar Vídeo Cortado
            </button>
          </div>
        </div>
      {/if}
    </div>
  {/if}
</div>

{#if activeLightboxIndex !== null}
  <div class="lightbox-overlay" onclick={() => activeLightboxIndex = null} role="presentation">
    <button type="button" class="lightbox-close" onclick={() => activeLightboxIndex = null}>&times;</button>
    
    <button type="button" class="lightbox-nav lightbox-prev" onclick={(e) => { e.stopPropagation(); navigateLightbox(-1); }}>&#8592;</button>
    
    <div class="lightbox-content bg-slate-900/90 border border-slate-800 rounded-xl" onclick={(e) => e.stopPropagation()} role="presentation">
      <img src={imagesDataURLs[activeLightboxIndex]} alt="Slide frame actual" class="lightbox-main-img" />
      <div class="lightbox-caption text-slate-200">
        <span>Fotograma #{activeLightboxIndex + 1} de {imagesDataURLs.length}</span>
        <span class="caption-time text-slate-400 font-mono">Tiempo: {formatTimeWithMs(timestamps[activeLightboxIndex] || 0)}</span>
      </div>
    </div>
    
    <button type="button" class="lightbox-nav lightbox-next" onclick={(e) => { e.stopPropagation(); navigateLightbox(1); }}>&#8594;</button>
  </div>
{/if}

{#if isExtracting}
  <div class="modal-overlay bg-black/60 backdrop-blur-xs">
    <div class="modal-content bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800">
      <div class="status-text text-slate-800 dark:text-slate-100">{statusText}</div>
      <div class="progress-container bg-slate-200 dark:bg-slate-800">
        <div class="progress-bar bg-green-500" style="width: {progress}%"></div>
      </div>
      <button type="button" class="btn btn-danger" onclick={() => cancelRequested = true}>Cancelar</button>
    </div>
  </div>
{/if}

<style>
  .extractor-wrapper { max-width: 860px; margin: 0 auto; font-family: system-ui, -apple-system, sans-serif; }
  .hidden-input { display: none !important; }
  :global(.hidden-video-decoder) { position: absolute; width: 1px; height: 1px; opacity: 0.01; pointer-events: none; top: 0; left: 0; }

  /* Dropzone & Preview */
  .dropzone { border: 2px dashed; padding: 24px; text-align: center; cursor: pointer; border-radius: 12px; margin-bottom: 20px; transition: background 0.15s, border-color 0.15s; }
  .drop-ready { border-color: #27ae60 !important; background: rgba(39, 174, 96, 0.06) !important; color: #27ae60; }
  .filename { font-size: 0.8rem; display: block; margin-top: 4px; word-break: break-all; }
  .video-preview-wrapper { width: 100%; display: flex; justify-content: center; margin-bottom: 20px; border-radius: 12px; padding: 10px; }
  .video-preview { width: 100%; max-width: 500px; aspect-ratio: 16 / 9; background: #000; border-radius: 6px; display: block; }

  /* Tabs */
  .tabs-navigation { display: flex; gap: 4px; padding: 4px; border-radius: 8px; margin-bottom: 16px; }
  .tab-btn { flex: 1; border: none; background: transparent; padding: 10px; font-weight: 600; font-size: 0.9rem; cursor: pointer; border-radius: 6px; transition: all 0.15s; }
  .tab-btn.active { background: #ffffff; color: #1e293b !important; box-shadow: 0 2px 6px rgba(0,0,0,0.05); }
  :global(.dark) .tab-btn.active { background: #1e293b; color: #ffffff !important; box-shadow: 0 2px 6px rgba(0,0,0,0.3); }
  .tab-content-card { border-radius: 12px; padding: 20px; }

  /* Layout Pestaña 1 */
  .realtime-warning { margin-bottom: 12px; }
  .frames-tab-layout { display: flex; flex-direction: column; gap: 16px; }
  .settings-row { display: flex; flex-wrap: wrap; gap: 16px; }
  .control-group { display: flex; flex-direction: column; gap: 6px; flex: 1; min-width: 200px; }
  .control-group label { font-size: 0.85rem; font-weight: 700; }
  .control-group select, .control-group input[type="number"] { padding: 10px; border: 1px solid; border-radius: 6px; font-size: 0.9rem; outline: none; }

  /* Slider fotogramas */
  .group-range-picker { flex: 2; min-width: 280px; }
  .label-with-value { display: flex; justify-content: space-between; align-items: center; }
  .range-badge { background: #3498db; color: white; font-size: 0.75rem; font-weight: bold; padding: 2px 8px; border-radius: 20px; }
  .slider-input-combination { display: flex; align-items: center; gap: 12px; margin-top: 4px; }
  .modern-slider { flex: 1; height: 6px; border-radius: 4px; appearance: none; outline: none; cursor: pointer; }
  .modern-slider::-webkit-slider-thumb { appearance: none; width: 18px; height: 18px; border-radius: 50%; background: #3498db; border: 2px solid white; box-shadow: 0 1px 3px rgba(0,0,0,0.2); }
  .compact-numeric-input { width: 65px; text-align: center; padding: 6px !important; border: 1px solid; border-radius: 6px; }

  /* Mode Selector Cortador */
  .cutter-header-mode { display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px; flex-wrap: wrap; gap: 12px; }
  .section-instruction { font-size: 0.85rem; font-weight: 500; }
  .mode-selector { display: flex; padding: 3px; border-radius: 6px; border: 1px solid; }
  .mode-btn { padding: 6px 12px; border: none; background: transparent; border-radius: 4px; font-size: 0.8rem; font-weight: 600; cursor: pointer; transition: all 0.15s ease; }
  
  .mode-btn.mode-keep.active { background: #3498db; color: #ffffff !important; box-shadow: 0 2px 4px rgba(52, 152, 219, 0.2); }
  .mode-btn.mode-remove.active { background: #ef4444; color: #ffffff !important; box-shadow: 0 2px 4px rgba(239, 68, 68, 0.2); }

  /* PANEL DE PRECISIÓN */
  .precision-controls-panel-v2 { display: flex; justify-content: space-between; align-items: center; padding: 16px; border-radius: 8px; border: 1px solid; gap: 10px; flex-wrap: wrap; margin-top: 8px; }
  .precision-column { display: flex; flex-direction: column; align-items: center; gap: 4px; flex: 1; min-width: 160px; }
  .block-label { font-size: 0.85rem; font-weight: 600; }
  .input-tweak-row { display: flex; align-items: center; gap: 8px; margin: 4px 0; }
  
  .btn-step { border: 1px solid; border-radius: 6px; padding: 6px 12px; font-size: 0.85rem; font-weight: 500; cursor: pointer; transition: all 0.1s; }
  .btn-step:hover { background: rgba(0,0,0,0.05); }
  :global(.dark) .btn-step:hover { background: rgba(255,255,255,0.05); }
  
  .precise-input-v2 { width: 110px; height: 34px; border: 1px solid; border-radius: 6px; text-align: center; font-family: monospace; font-weight: bold; font-size: 0.95rem; letter-spacing: 0.5px; outline: none; }

  /* Botón Añadir central */
  .central-action-wrapper { display: flex; align-items: center; justify-content: center; padding: 0 10px; min-width: 200px; }
  .btn-add-cut-central-v2 { border: 1px solid; padding: 8px 16px; border-radius: 6px; font-weight: 700; font-size: 0.85rem; cursor: pointer; transition: all 0.1s; }
  .btn-add-cut-central-v2:hover { background: rgba(14, 165, 233, 0.15); box-shadow: 0 2px 4px rgba(14, 165, 233, 0.15); }

  /* Slider Horizontal Fotogramas */
  .results-header { margin-top: 24px; border-top: 1px dashed; padding-top: 16px; text-align: left; }
  .results-header h3 { font-size: 1rem; margin: 0; font-weight: 700; }
  
  .images-slider-container { width: 100%; overflow-x: auto; margin-top: 12px; padding-bottom: 8px; }
  .images-grid { display: flex; flex-direction: row; gap: 12px; width: max-content; }
  
  .thumb-card { border: 1px solid; padding: 6px; border-radius: 8px; position: relative; text-align: center; width: 160px; flex-shrink: 0; outline: none; }
.interactive-thumb { 
  cursor: pointer; 
  transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1); 
}
  .interactive-thumb:hover { transform: translateY(-3px); filter: brightness(1.06); box-shadow: 0 4px 12px rgba(0,0,0,0.12); }
  :global(.dark) .interactive-thumb:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.4); }
  
  .thumb-card img { width: 100%; height: 100px; object-fit: cover; border-radius: 6px; background: #000; }
  .meta { font-size: 0.7rem; margin-top: 6px; font-family: monospace; }
  .download-icon-btn { position: absolute; top: 12px; right: 12px; width: 24px; height: 24px; border-radius: 50%; border: 1px solid; cursor: pointer; font-size: 0.85rem; display: flex; align-items: center; justify-content: center; font-weight: bold; box-shadow: 0 1px 3px rgba(0,0,0,0.1); z-index: 2; }
  .download-icon-btn:hover { color: #3498db !important; border-color: #3498db !important; }

  .images-slider-container::-webkit-scrollbar { height: 8px; }
  .images-slider-container::-webkit-scrollbar-track { background: transparent; }
  .images-slider-container::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
  :global(.dark) .images-slider-container::-webkit-scrollbar-thumb { background: #475569; }

  /* Listado de Cortes */
  .saved-cuts-container { padding: 14px; border-radius: 8px; margin-top: 16px; width: 100%; text-align: left; box-sizing: border-box; }
  .saved-cuts-title { font-size: 0.85rem; font-weight: 700; margin-bottom: 8px; }
  .no-cuts-placeholder { font-size: 0.85rem; text-align: center; padding: 8px 0; font-style: italic; }
  .cuts-tags-list { display: flex; flex-wrap: wrap; gap: 6px; }
  .cut-tag { display: flex; align-items: center; gap: 6px; padding: 4px 12px; border-radius: 6px; font-size: 0.8rem; font-weight: 600; border: 1px solid; }
  .cut-tag.tag-remove { border-color: #fca5a5 !important; background: rgba(239, 68, 68, 0.08) !important; color: #ef4444 !important; }
  .btn-delete-tag { background: none; border: none; cursor: pointer; font-weight: bold; font-size: 1rem; margin-left: 4px; line-height: 1; transition: color 0.1s; }
  .btn-delete-tag:hover { color: #ef4444 !important; }

  /* Acciones generales */
  .tab-actions { display: flex; justify-content: space-between; margin-top: 20px; border-top: 1px solid; padding-top: 16px; gap: 10px; flex-wrap: wrap; }
  .btn { padding: 10px 18px; border: none; border-radius: 6px; cursor: pointer; font-weight: 600; font-size: 0.88rem; transition: background 0.15s ease, opacity 0.15s; }
  .btn-primary { background: #3498db; color: white; }
  .btn-primary:hover { background: #2980b9; }
  .btn-danger { background: #ef4444; color: white; }
  
  .btn-success { background: #22c55e; color: white; }
  .btn-success:hover:not(:disabled) { background: #16a34a; }
  .btn-success:disabled { background: #cbd5e1; color: #94a3b8; cursor: not-allowed; }
  :global(.dark) .btn-success:disabled { background: #334155; color: #64748b; }

  /* LIGHTBOX MODAL */
  .lightbox-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(15, 23, 42, 0.9); backdrop-filter: blur(4px); display: flex; align-items: center; justify-content: center; z-index: 200; animation: fadeIn 0.15s ease-out; }
  .lightbox-content { position: relative; max-width: 90%; max-height: 85%; display: flex; flex-direction: column; align-items: center; box-shadow: 0 25px 50px -12px rgba(0,0,0,0.5); padding: 8px; }
  .lightbox-main-img { max-width: 100%; max-height: 72vh; object-fit: contain; border-radius: 6px; }
  .lightbox-caption { width: 100%; display: flex; justify-content: space-between; align-items: center; padding: 12px 6px 4px 6px; font-size: 0.9rem; font-weight: 500; }
  .caption-time { font-size: 0.85rem; }
  
  .lightbox-close { position: absolute; top: 20px; right: 20px; background: none; border: none; color: #94a3b8; font-size: 2.5rem; cursor: pointer; line-height: 1; transition: color 0.1s; }
  .lightbox-close:hover { color: #ffffff; }
  .lightbox-nav { position: absolute; top: 50%; transform: translateY(-50%); background: rgba(30, 41, 59, 0.6); border: 1px solid rgba(255,255,255,0.05); color: #f1f5f9; border-radius: 50%; width: 44px; height: 44px; font-size: 1.2rem; cursor: pointer; display: flex; align-items: center; justify-content: center; font-weight: bold; transition: background 0.15s, color 0.15s; z-index: 210; }
  .lightbox-nav:hover { background: #3498db; color: #ffffff; }
  .lightbox-prev { left: 24px; }
  .lightbox-next { right: 24px; }

  /* MODAL DE CARGA */
  .modal-overlay { position: fixed; top: 0; left: 0; right: 0; bottom: 0; display: flex; align-items: center; justify-content: center; z-index: 100; }
  .modal-content { padding: 24px; border-radius: 12px; width: 85%; max-width: 320px; text-align: center; box-shadow: 0 20px 25px -5px rgba(0,0,0,0.15); }
  .status-text { font-weight: 600; margin-bottom: 12px; font-size: 0.95rem; }
  .progress-container { height: 8px; border-radius: 4px; overflow: hidden; margin-bottom: 16px; }
  .progress-bar { height: 100%; transition: width 0.1s linear; }

  /* Responsive: móvil */
  @media (max-width: 640px) {
    .precision-controls-panel-v2 { flex-direction: column; align-items: stretch; }
    .central-action-wrapper { min-width: unset; padding: 8px 0; }
    .control-group { min-width: unset; }
    .group-range-picker { min-width: unset; }
    .tab-content-card { padding: 12px; }
    .dropzone { padding: 16px; }
    .lightbox-caption { flex-direction: column; gap: 4px; align-items: flex-start; }
    .lightbox-nav { width: 36px; height: 36px; font-size: 1rem; }
    .lightbox-prev { left: 8px; }
    .lightbox-next { right: 8px; }
    .btn { font-size: 0.82rem; padding: 8px 14px; }
    .btn-add-cut-central-v2 { font-size: 0.78rem; padding: 6px 12px; }
    .precise-input-v2 { width: 90px; }
  }

  @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
</style>