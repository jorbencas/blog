import { defineConfig } from "astro/config";
import { remarkReadingTime } from "./remark-reading-time.mjs";
import tailwind from "@astrojs/tailwind";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
//import vercel from '@astrojs/vercel'
export default defineConfig({
  // adapter: vercel(),
  integrations: [tailwind(), mdx(), sitemap()],
  site: "https://blog-jorbencas.vercel.app/",
  markdown: {
    remarkPlugins: [remarkReadingTime],
    smartypants: true, // Mejora tipografía (comillas, guiones)
    gfm: true, // Habilita GitHub Flavored Markdown (por defecto es true)
  },
});
