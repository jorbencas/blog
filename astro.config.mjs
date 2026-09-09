import { defineConfig } from "astro/config";
import { remarkReadingTime } from "./remark-reading-time.mjs";
import { unified } from "@astrojs/markdown-remark";
import tailwindcss from "@tailwindcss/vite";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import vercel from "@astrojs/vercel";
import svelte from "@astrojs/svelte";
import rehypeTableWrapper from "./rehype-table-wrapper.mjs";
import remarkGfm from "remark-gfm";
export default defineConfig({
  output: "static",
  adapter: vercel(),
  integrations: [mdx({ remarkPlugins: [remarkGfm], rehypePlugins: [rehypeTableWrapper] }), sitemap({
    serialize(item) {
      if (item.url === "https://blog-jorbencas.vercel.app/") {
        item.priority = 1.0;
        item.changefreq = "daily";
      } else if (item.url.includes("/herramientas/")) {
        item.priority = 0.8;
        item.changefreq = "monthly";
      } else if (item.url.includes("/posts/")) {
        item.priority = 0.7;
        item.changefreq = "weekly";
      } else if (item.url.includes("/retos/")) {
        item.priority = 0.6;
        item.changefreq = "monthly";
      } else if (item.url.includes("/tags/")) {
        item.priority = 0.5;
        item.changefreq = "weekly";
      } else if (item.url.includes("/proyectos/")) {
        item.priority = 0.8;
        item.changefreq = "monthly";
      }
      return item;
    },
  }), svelte()],
  vite: {
    plugins: [tailwindcss()],
    build: {
      rollupOptions: {
        external: ["/pagefind/pagefind.js"],
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
