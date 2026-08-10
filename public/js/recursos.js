(() => {
const BATCH_SIZE = 30;
let currentPage = 1;
let activeCategory = "all";
let activePricing = "all";
let activeSearch = "";
let isLoading = false;
let hasMore = true;
let debounceTimer = null;

const grid = document.getElementById("resources-grid");
const skeleton = document.getElementById("loading-skeleton");
const emptyState = document.getElementById("empty-state");
const endMessage = document.getElementById("end-message");
const visibleCount = document.getElementById("visible-count");
const searchInput = document.getElementById("resource-search");
const chips = document.querySelectorAll(".chip");
const pricingChips = document.querySelectorAll(".pricing-chip");

function updateCount() {
  const visible = grid.querySelectorAll(".resource-item:not([style*='display: none'])").length;
  if (visibleCount) visibleCount.textContent = visible;
}

const totalCount = parseInt(visibleCount?.getAttribute("data-total") || "0");

const categoryLabels = {"administración de sistemas":"🖥️ Sistemas","algoritmos y práctica":"🧮 Algoritmos","apis":"🔌 APIs","aprendizaje":"📚 Aprendizaje","backend as a service":"⚡ BaaS","blogs":"📝 Blogs","canales de youtube":"📺 YouTube","certificaciones informáticas":"🎓 Certificaciones","cms":"📰 CMS","componentes ui":"🎨 UI","comunidad":"👥 Comunidad","conversión de archivos":"🔄 Archivos","diseño gráfico / figma":"✏️ Diseño","documentación":"📖 Docs","dominios":"🌐 Dominios","editores con ia / editores multimedia":"🎬 Editores","extensiones":"🧩 Extensiones","extracción de información de imágenes/vídeos":"🖼️ Extracción","frameworks":"🏗️ Frameworks","gaming / vr / ar":"🎮 Gaming","git / control de versiones":"🔀 Git","hacking / ciberseguridad":"🛡️ Seguridad","herramientas dev":"🛠️ Dev Tools","hosting / nube":"☁️ Hosting","iconos":"🔷 Iconos","inteligencia artificial":"🤖 IA","multimedia":"🎵 Multimedia","noticias de tecnología":"📰 Noticias","nuevas herramientas descubiertas":"🆕 Nuevas","nuevas-herramientas":"🆕 Nuevas","productividad":"⚡ Productividad","redes / wifi / ethernet":"📶 Redes","rendimiento":"🚀 Rendimiento","repositorios destacados github":"⭐ GitHub","retos de programación":"🎯 Retos","state management":"📦 State","terminal":"💻 Terminal","testing":"🧪 Testing","utilidades dev":"🔧 Utilidades","general":"📌 General"};

let lastCategory = "";

function renderItems(items) {
  const pricingConfig = {
    free: { label: "Gratis", class: "bg-gradient-to-r from-emerald-800 to-emerald-500 text-white" },
    freemium: { label: "Plan gratuito", class: "bg-gradient-to-r from-amber-800 to-amber-500 text-white" },
    paid: { label: "De pago", class: "bg-gradient-to-r from-orange-800 to-orange-500 text-white" },
  };

  const categoryCounts = {};

  items.forEach((r) => {
    const cat = r.category || "general";

    if (cat !== lastCategory) {
      const existingGroup = grid.querySelector(`.category-group[data-category="${cat}"]`);
      if (!existingGroup) {
        const group = document.createElement("div");
        group.className = "category-group";
        group.dataset.category = cat;
        const count = items.filter((i) => i.category === cat).length;
        group.innerHTML = `
          <div class="flex items-center gap-3 mb-4 mt-2">
            <h2 class="text-lg font-bold text-slate-900 dark:text-white">${categoryLabels[cat] || cat}</h2>
            <span class="bg-gradient-to-r from-sky-800 to-cyan-500 px-2 py-0.5 text-[10px] sm:text-xs font-bold uppercase tracking-wider text-white">${count}</span>
            <div class="flex-1 h-px bg-slate-200 dark:bg-slate-700"></div>
          </div>
          <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4"></div>
        `;
        grid.appendChild(group);
      }
      lastCategory = cat;
    }

    const group = grid.querySelector(`.category-group[data-category="${cat}"] .grid`);
    if (!group) return;

    const div = document.createElement("div");
    div.className = "resource-item h-full";
    div.dataset.category = r.category;
    div.dataset.title = r.title.toLowerCase();
    div.dataset.description = r.description.toLowerCase();
    const badge = r.pricing ? pricingConfig[r.pricing] : null;
    const badgeHtml = badge ? `<span class="bg-gradient-to-r ${badge.class} px-2 py-0.5 text-[10px] sm:text-xs font-bold uppercase tracking-wider text-white">${badge.label}</span>` : "";
    div.innerHTML = `
      <a href="${r.href}" class="flex flex-col h-full gap-4 p-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 hover:border-orange-400 dark:hover:border-orange-400 hover:shadow-xl hover:-translate-y-1 transition-all no-underline group" target="_blank" rel="noopener noreferrer">
        <img src="https://www.google.com/s2/favicons?domain=${new URL(r.href).hostname}&sz=32" width="20" height="20" class="mt-1 shrink-0 rounded bg-slate-100 dark:bg-slate-800 p-0.5" alt="${r.title}" loading="lazy" onerror="this.style.display='none'" />
        <div class="flex-1 min-w-0">
          <div class="flex items-center gap-2 flex-wrap">
            <span class="font-bold text-slate-900 dark:text-white group-hover:text-orange-600 dark:group-hover:text-orange-400 transition-colors">${r.title}</span>
            ${badgeHtml}
          </div>
          ${r.rating ? `<p class="text-xs text-amber-500 dark:text-amber-400 mt-1 font-semibold">${r.rating}</p>` : ""}
          <p class="text-sm text-slate-500 dark:text-slate-400 mt-0.5 leading-snug">${r.description}</p>
          ${r.features && r.features.length > 0 ? `<ul class="mt-1 space-y-0.5">${r.features.map(f => `<li class="text-xs text-cyan-600 dark:text-cyan-400 flex items-center gap-1"><span>✓</span><span>${f}</span></li>`).join("")}</ul>` : ""}
          ${r.useCases ? `<p class="text-xs text-slate-400 dark:text-slate-500 mt-1 italic">${r.useCases}</p>` : ""}
        </div>
      </a>
    `;
    group.appendChild(div);
  });
  updateCount();
}

async function loadMore() {
  if (isLoading || !hasMore) return;
  isLoading = true;
  skeleton.classList.remove("hidden");

  try {
    const params = new URLSearchParams({
      page: currentPage.toString(),
      limit: BATCH_SIZE.toString(),
      category: activeCategory,
      pricing: activePricing,
      search: activeSearch,
    });
    const res = await fetch(`/api/resources?${params}`);
    const data = await res.json();

    if (data.items.length > 0) {
      renderItems(data.items);
      currentPage++;
      hasMore = data.hasMore;
    } else {
      hasMore = false;
    }
  } catch (e) {
    console.error("Error loading resources:", e);
  }

  isLoading = false;
  skeleton.classList.add("hidden");

  if (!hasMore && grid.querySelectorAll(".resource-item").length > 0) {
    endMessage.classList.remove("hidden");
  }

  const totalVisible = grid.querySelectorAll(".resource-item:not([style*='display: none'])").length;
  emptyState.classList.toggle("hidden", totalVisible > 0);

  if (hasMore && sentinel.parentNode) {
    observer.unobserve(sentinel);
    observer.observe(sentinel);
  }
}

function resetAndLoad() {
  observer.disconnect();
  grid.innerHTML = "";
  currentPage = 1;
  hasMore = true;
  isLoading = false;
  lastCategory = "";
  endMessage.classList.add("hidden");
  emptyState.classList.add("hidden");
  if (sentinel.parentNode) sentinel.parentNode.removeChild(sentinel);
  grid.parentNode.appendChild(sentinel);
  observer.observe(sentinel);
  loadMore();
}

function filterExisting() {
  const query = activeSearch.toLowerCase();
  const groups = grid.querySelectorAll(".category-group");
  let totalVisible = 0;

  groups.forEach((group) => {
    const items = group.querySelectorAll(".resource-item");
    let groupVisible = 0;
    items.forEach((item) => {
      const cat = item.dataset.category || "";
      const title = item.dataset.title || "";
      const desc = item.dataset.description || "";
      const matchesChip = activeCategory === "all" || cat === activeCategory;
      const matchesSearch = !query || title.includes(query) || desc.includes(query) || cat.includes(query);
      if (matchesChip && matchesSearch) {
        item.style.display = "";
        groupVisible++;
      } else {
        item.style.display = "none";
      }
    });
    group.style.display = groupVisible === 0 ? "none" : "";
    totalVisible += groupVisible;
  });

  updateCount();
  emptyState.classList.toggle("hidden", totalVisible > 0);
}

// Chip clicks
chips.forEach((chip) => {
  chip.addEventListener("click", () => {
    activeCategory = chip.dataset.chip || "all";
    chips.forEach((c) => {
      const isActive = c.dataset.chip === activeCategory;
      c.classList.toggle("bg-orange-500", isActive);
      c.classList.toggle("text-white", isActive);
      c.classList.toggle("border-orange-500", isActive);
      c.classList.toggle("bg-white", !isActive);
      c.classList.toggle("dark:bg-slate-800", !isActive);
      c.classList.toggle("text-slate-600", !isActive);
      c.classList.toggle("dark:text-slate-300", !isActive);
      c.classList.toggle("border-slate-200", !isActive);
      c.classList.toggle("dark:border-slate-700", !isActive);
    });
    resetAndLoad();
  });
});

// Pricing chip clicks
pricingChips.forEach((chip) => {
  chip.addEventListener("click", () => {
    activePricing = chip.dataset.pricing || "all";
    pricingChips.forEach((c) => {
      const isActive = c.dataset.pricing === activePricing;
      c.classList.toggle("bg-orange-500", isActive);
      c.classList.toggle("text-white", isActive);
      c.classList.toggle("border-orange-500", isActive);
      c.classList.toggle("bg-white", !isActive);
      c.classList.toggle("dark:bg-slate-800", !isActive);
      c.classList.toggle("text-slate-600", !isActive);
      c.classList.toggle("dark:text-slate-300", !isActive);
      c.classList.toggle("border-slate-200", !isActive);
      c.classList.toggle("dark:border-slate-700", !isActive);
    });
    resetAndLoad();
  });
});

// Search with debounce
searchInput?.addEventListener("input", (e) => {
  clearTimeout(debounceTimer);
  debounceTimer = setTimeout(() => {
    activeSearch = e.target.value;
    resetAndLoad();
  }, 300);
});

// Infinite scroll
const observer = new IntersectionObserver(
  (entries) => {
    if (entries[0].isIntersecting && hasMore && !isLoading) {
      loadMore();
    }
  },
  { rootMargin: "200px" }
);

// Observe a sentinel element at the bottom
const sentinel = document.createElement("div");
sentinel.id = "scroll-sentinel";
grid.parentNode.appendChild(sentinel);
observer.observe(sentinel);

// Initial load status
const totalItems = grid.querySelectorAll(".resource-item").length;
if (totalItems >= totalCount) {
  hasMore = false;
  skeleton.classList.add("hidden");
  endMessage.classList.remove("hidden");
}
})();
