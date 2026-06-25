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
  return existsSync(join(process.cwd(), "public", image))
    ? `/${image}`
    : null;
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
    .filter((post) => !post.data.draft)
    .sort(
      (a, b) =>
        new Date(b.data.pubDate).getTime() - new Date(a.data.pubDate).getTime()
    );
};
