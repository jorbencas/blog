<script>
  let { items = [] } = $props();
</script>

{#if items.length > 0}
  <div class="space-y-3 mt-4">
    <span class="text-base font-bold uppercase tracking-[0.3em] text-slate-500 dark:text-slate-400 block pb-2 w-fit">
      Retos Relacionados
    </span>
    <div class="space-y-3">
      {#each items as item}
        <a
          href={item.href}
          class="block p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 transition-colors no-underline group hover:border-amber-500/50"
        >
          <p class="text-sm font-black uppercase tracking-wider text-slate-900 dark:text-white transition-colors line-clamp-2 leading-tight group-hover:text-amber-600 dark:group-hover:text-amber-400">
            {item.title}
          </p>
        </a>
      {/each}
    </div>
  </div>
{/if}
