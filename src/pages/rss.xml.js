import rss from "@astrojs/rss";
import { getCollection } from "astro:content";

export async function GET(context) {
  const posts = await getCollection("posts");

  return rss({
    title: "Problemas de un desarrollador Web",
    description: "Blog con artículos sobre programación y ejercicios",
    site: context.site,
    items: posts.flatMap((post) => ({
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      author: post.data.author,
      link: `/posts/${post.slug}`,
      categories: post.data.tags || [],
    })),
  });
}
