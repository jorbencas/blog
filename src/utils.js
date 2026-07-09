import { existsSync } from "node:fs";
import { join } from "node:path";

export const resolveImagePath = (image) => {
  if (!image) return null;
  if (image.startsWith("http")) return image;
  if (image.startsWith("/")) {
    return existsSync(join(process.cwd(), "public", image.slice(1)))
      ? image
      : null;
  }
  return existsSync(join(process.cwd(), "public", image)) ? `/${image}` : null;
};

export const formatDatePost = (date) => {
  return new Intl.DateTimeFormat("es-ES", {
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  }).format(new Date(date));
};

export const getSortedPosts = (allPosts) => {
  return allPosts
    .filter((post) => !post.data.draft && post.data.draft === false)
    .sort(
      (a, b) =>
        new Date(b.data.pubDate).getTime() - new Date(a.data.pubDate).getTime()
    );
};

export const getRelatedPosts = (currentPost, allPosts, limit = 3) => {
  const currentTags = new Set(currentPost.data.tags || []);
  if (currentTags.size === 0) return [];

  return allPosts
    .filter((p) => p.id !== currentPost.id && !p.data.draft)
    .map((p) => {
      const postTags = p.data.tags || [];
      const shared = postTags.filter((t) => currentTags.has(t)).length;
      return { post: p, score: shared };
    })
    .filter((item) => item.score > 0)
    .sort((a, b) => b.score - a.score)
    .slice(0, limit)
    .map((item) => item.post);
};
