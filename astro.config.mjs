import { defineConfig } from "astro/config";
import { remarkReadingTime } from "./remark-reading-time.mjs";
import tailwind from "@astrojs/tailwind";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
//import vercel from '@astrojs/vercel'
export default defineConfig({
  output: "static", // <-- Asegúrate de que sea static o borra la línea
  // adapter: vercel(),
  build: {
    format: "directory", // Fuerza a crear carpetas con index.html
    outDir: "./dist", // Fuerza a crear la carpeta dist en la raíz
  },
  integrations: [tailwind(), mdx(), sitemap()],
  site: "https://blog-jorbencas.vercel.app/",
  markdown: {
    remarkPlugins: [remarkReadingTime],
    smartypants: true, // Mejora tipografía (comillas, guiones)
    gfm: true, // Habilita GitHub Flavored Markdown (por defecto es true)
  },
});
