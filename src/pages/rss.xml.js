import rss from "@astrojs/rss";
import { getCollection } from "astro:content";

export async function GET(context) {
  const posts = await getCollection("blog");

  return rss({
    title: "Problemas de un desarrollador Web",
    description: "Blog con artículos sobre programación y ejercicios",
    site: context.site,
    items: posts.map((post) => ({
      title: post.data.title,
      pubDate: post.data.pubDate,
      link: `/posts/${post.slug}`,
    })),
  });
}