import { defineConfig } from "astro/config";
import { remarkReadingTime } from "./remark-reading-time.mjs";
import { unified } from "@astrojs/markdown-remark";
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
    domains: ["images.unsplash.com"],
  },
  site: "https://blog-jorbencas.vercel.app/",
  markdown: {
    processor: unified({
      remarkPlugins: [remarkReadingTime],
      gfm: true,
      smartypants: true,
    }),
    shikiConfig: {
      themes: {
        light: "github-light",
        dark: "github-dark",
      },
    },
    wrap: true,
  },
});
