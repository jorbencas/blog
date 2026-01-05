import rss from '@astrojs/rss';

export const get = () => rss({
  title: 'Problemas de un desarrollador Web',
  description: 'Blog con artículos sobre programación y ejercicios',
  site: import.meta.env.SITE,
  items: import.meta.glob("./posts/*.md"),
});