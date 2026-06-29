import { defineConfig } from "astro/config";
import { remarkReadingTime } from "./remark-reading-time.mjs";
import tailwindcss from "@tailwindcss/vite";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import vercel from "@astrojs/vercel";
import svelte from "@astrojs/svelte";
export default defineConfig({
  output: "static",
  adapter: vercel(),
  integrations: [mdx(), sitemap(), svelte()],
  vite: {
    plugins: [tailwindcss()],
    build: {
      rollupOptions: {
        external: (id) => id === "/pagefind/pagefind.js",
      },
    },
  },
  image: {
    domains: ["images.unsplash.com"], // 🌟 Permet a Astro optimitzar les fotos d'Unsplash
  },
  site: "https://blog-jorbencas.vercel.app/",
  markdown: {
    gfm: true,
    remarkPlugins: [remarkReadingTime],
    shikiConfig: {
      // Usamos un tema para Light y otro para Dark
      themes: {
        light: "github-light",
        dark: "github-dark",
      },
    },
    wrap: true,
    smartypants: true, // Mejora tipografía (comillas, guiones)
  },
});
