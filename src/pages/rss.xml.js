import rss from '@astrojs/rss';

const postImportResult = import.meta.glob('./posts/*.md', { eager: true });
const posts = Object.values(postImportResult);

export const get = () => rss({
  title: 'Problesmas de un desarollador Web',
  description: 'Blog con articulos sobre programación y ejercicios',
  site: import.meta.env.SITE,
  items: posts.map((post) => ({
    link: post.url,
    title: post.frontmatter.tittle,
    description: post.frontmatter.description,
    date: post.frontmatter.date,
    image: import.meta.env.SITE + post.frontmatter.image,
    author: post.frontmatter.author,

  }))
});


rss({
    // ex. use your stylesheet from "public/rss/styles.xsl"
    stylesheet: '/rss/styles.xsl',
    // ...
  });