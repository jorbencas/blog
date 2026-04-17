import { defineConfig } from "astro/config";
import { remarkReadingTime } from "./remark-reading-time.mjs";
import tailwind from "@astrojs/tailwind";
import mdx from "@astrojs/mdx";
import sitemap from "@astrojs/sitemap";
//import vercel from '@astrojs/vercel'
export default defineConfig({
  // adapter: vercel(),
  integrations: [tailwind(), mdx(), sitemap()],
  //integrations: [tailwind()],
  site: "https://blog-jorbencas.vercel.app/",
  markdown: {
    remarkPlugins: [remarkReadingTime],
    shikiConfig: {
      // Usamos un tema para Light y otro para Dark
      themes: {
        light: "one-light",
         "one-dark-pro",
      },
    },
    // Esto envuelve el código para que no se rompa la línea
    wrap: true,
    smartypants: true, // Mejora tipografía (comillas, guiones)
    gfm: true, // Habilita GitHub Flavored Markdown (por defecto es true)
  },
});
