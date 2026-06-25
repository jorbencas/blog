import { defineCollection } from "astro:content";
import { glob } from "astro/loaders";
import { z } from "astro/zod";

const posts = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "./src/content/posts" }),
  schema: z.object({
    draft: z.boolean().optional().default(false),
    title: z.string(),
    description: z.string(),
    pubDate: z.string().or(z.date()).transform((v) => new Date(v)),
    tags: z.array(z.string()).default([]),
    author: z.string().default("Jorge Beneyto Castelló"),
    image: z.string().optional(),
  }),
});

const autoNews = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "./src/content/auto-news" }),
  schema: z.object({
    draft: z.boolean().optional().default(false),
    title: z.string(),
    description: z.string(),
    pubDate: z.string().or(z.date()).transform((v) => new Date(v)),
    tags: z.array(z.string()).default([]),
    image: z.string().optional(),
    author: z.string().default("Jorge Beneyto Castelló"),
  }),
});

const weeklyPosts = defineCollection({
  loader: glob({ pattern: "**/*.md", base: "./src/content/auto-news" }),
  schema: z.object({
    draft: z.boolean().optional().default(false),
    title: z.string(),
    description: z.string(),
    pubDate: z.string().or(z.date()).transform((v) => new Date(v)),
    tags: z.array(z.string()).default([]),
    image: z.string().optional(),
    slug: z.string().optional(),
    author: z.string().default("Jorge Beneyto Castelló"),
  }),
});

const autoChallenges = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "./src/content/auto-challenges" }),
  schema: z.object({
    draft: z.boolean().optional().default(false),
    title: z.string(),
    description: z.string(),
    pubDate: z.string().or(z.date()).transform((v) => new Date(v)),
    tags: z.array(z.string()).default([]),
    slug: z.string().optional(),
    image: z.string().optional(),
    author: z.string().default("Jorge Beneyto Castelló"),
    difficulty: z.string().optional(),
  }),
});

const myprojects = defineCollection({
  loader: glob({ pattern: "**/*.mdx", base: "./src/content/myprojects" }),
  schema: z.object({
    draft: z.boolean().optional().default(false),
    title: z.string(),
    description: z.string(),
    pubDate: z.string().or(z.date()).transform((v) => new Date(v)),
    tags: z.array(z.string()).default([]),
    image: z.string().optional(),
    repository: z.string().optional(),
    url: z.string().optional(),
    author: z.string().default("Jorge Beneyto Castelló"),
  }),
});

export const collections = { posts, "auto-news": autoNews, "weeklyPosts": weeklyPosts, "auto-challenges": autoChallenges, myprojects };
