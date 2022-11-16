import rss from '@astrojs/rss';

export const get = () => rss({
  title: 'Problesmas de un desarollador Web',
  description: 'Blog con articulos sobre programación y ejercicios',
  site: import.meta.env.SITE,
  items: import.meta.glob("./posts/*.md"),
});