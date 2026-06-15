import { defineConfig } from "astro/config";
import { remarkReadingTime } from "./remark-reading-time.mjs";
import tailwind from "@astrojs/tailwind";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
import vercel from "@astrojs/vercel"; // 1. Se añade la importación del adaptador
export default defineConfig({
  output: "static", // o 'server' dependiendo de tu configuración
  adapter: vercel(),
  integrations: [tailwind(), mdx(), sitemap()],
  image: {
    domains: ["images.unsplash.com"], // 🌟 Permet a Astro optimitzar les fotos d'Unsplash
  },
  site: "https://blog-jorbencas.vercel.app/",
  markdown: {
    remarkPlugins: [remarkReadingTime],
    shikiConfig: {
      // Usamos un tema para Light y otro para Dark
      themes: {
        light: "one-light",
        dark: "one-dark-pro",
      },
    },
    wrap: true,
    smartypants: true, // Mejora tipografía (comillas, guiones)
    gfm: true, // Habilita GitHub Flavored Markdown (por defecto es true)
  },
});
