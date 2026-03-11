import { defineConfig } from "astro/config";
import { remarkReadingTime } from "./remark-reading-time.mjs";
import tailwind from "@astrojs/tailwind";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";

// https://astro.build/config
export default defineConfig({
  output: "static", // <-- Asegúrate de que sea static o borra la línea
  integrations: [tailwind(), mdx(), sitemap()],
  site: "https://blog-jorbencas.vercel.app/",
  markdown: {
    remarkPlugins: [remarkReadingTime],
    smartypants: true, // Mejora tipografía (comillas, guiones)
    gfm: true, // Habilita GitHub Flavored Markdown (por defecto es true)
  },
});
