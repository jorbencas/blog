<script>
  import { onMount } from 'svelte';

  let { children } = $props();
  let container;
  let tabs = $state([]);
  let activeIndex = $state(0);
  let ready = $state(false);

  const languageMap = {
    python: 'Python',
    javascript: 'JavaScript',
    java: 'Java',
    typescript: 'TypeScript'
  };

  function getDisplayName(raw) {
    const lower = raw.toLowerCase();
    return languageMap[lower] || raw.charAt(0).toUpperCase() + raw.slice(1);
  }

  onMount(() => {
    if (!container) return;
    const preElements = Array.from(container.querySelectorAll(':scope > .code-panels > pre'));
    if (preElements.length === 0) return;

    tabs = preElements.map((pre, i) => {
      const codeEl = pre.querySelector('code');
      let lang = 'Code';
      if (codeEl) {
        const match = codeEl.className.match(/language-(\w+)/);
        if (match) lang = getDisplayName(match[1]);
      }
      if (i !== 0) pre.style.display = 'none';
      return { name: lang };
    });
    ready = true;
  });

  function switchTab(index) {
    if (!container) return;
    activeIndex = index;
    const preElements = Array.from(container.querySelectorAll(':scope > .code-panels > pre'));
    preElements.forEach((pre, i) => {
      pre.style.display = i === index ? '' : 'none';
    });
  }
</script>

<div bind:this={container} class="code-tabs-wrapper" class:ready>
  {#if ready}
    <div class="tab-bar" role="tablist">
      {#each tabs as tab, i}
        <button
          type="button"
          role="tab"
          aria-selected={i === activeIndex}
          class="tab-btn"
          class:active={i === activeIndex}
          onclick={() => switchTab(i)}
        >
          {tab.name}
        </button>
      {/each}
    </div>
  {/if}
  <div class="code-panels">
    {@render children()}
  </div>
</div>

<style>
  .code-tabs-wrapper:not(.ready) {
    display: none;
  }

  .tab-bar {
    display: flex;
    border-bottom: 1px solid rgb(148 163 184 / 0.2);
    overflow-x: auto;
  }

  .tab-btn {
    padding: 0.5rem 1rem;
    font-size: 0.75rem;
    font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: rgb(100 116 139);
    transition: color 0.15s ease, border-color 0.15s ease;
    border: none;
    border-bottom: 2px solid transparent;
    background: transparent;
    cursor: pointer;
    white-space: nowrap;
  }

  :global(.dark) .tab-btn {
    color: rgb(148 163 184);
  }

  .tab-btn:hover {
    color: rgb(8 145 178);
  }

  :global(.dark) .tab-btn:hover {
    color: rgb(34 211 238);
  }

  .tab-btn.active {
    color: rgb(8 145 178);
    border-bottom-color: rgb(6 182 212);
  }

  :global(.dark) .tab-btn.active {
    color: rgb(34 211 238);
  }

  .code-panels {
    background: #f8fafc;
    border-radius: 0 0 0.5rem 0.5rem;
    overflow: hidden;
  }

  :global(.dark) .code-panels {
    background: #0f172a;
  }

  .code-panels :global(pre) {
    margin: 0;
    border-radius: 0;
  }
</style>
