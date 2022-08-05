import rss from "@astrojs/rss";
const postImportResult = import.meta.glob("./posts/*.md", { eager: true });
const posts = Object.values(postImportResult);
export const get = () =>
  rss({
    title: "Problema de un deramado",
    description: "A humble Astronaut’s guide to the stars",
    site: import.meta.env.SITE,
    items: posts.map((post) => ({
      link: post.frontmatter.slug,
      title: post.frontmatter.title,
      pubDate: post.frontmatter.date,
    })),
    customData: `<language>es-ES</language>`,
    stylesheet: "/rss/styles.xsl",
  });
