import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import { getSortedPosts } from "src/utils";

export async function GET(context) {
  const posts = await getCollection("posts");
  const sortedPosts = await getSortedPosts(posts);

  const listaItems = sortedPosts.map((post) => {
    const item = {
      title: post.data.title,
      description: post.data.description,
      pubDate: post.data.pubDate,
      author: post.data.author,
      link: new URL(`/posts/${post.id}`, context.site).toString(),
      categories: post.data.tags || [],
    };
    if (post.data.audioSrc) {
      item.enclosure = {
        url: new URL(post.data.audioSrc, context.site).href,
        type: "audio/mpeg",
        length: 0, // Las apps de podcast modernos lo calculan al leer el archivo
      };
    }

    return item;
  });

  return rss({
    title: "Problemas de un desarrollador Web",
    description: "Blog con artículos sobre programación y ejercicios",
    site: context.site,
    items: listaItems,
  });
}
