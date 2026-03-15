// src/content/config.ts
import { defineCollection } from 'astro:content';
import { z } from 'astro/zod';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: "./src/content/posts" }),
  schema: z.object({
    draft: z.boolean().optional().default(false),
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.string().or(z.coerce.date()), // Acepta texto o fecha
    tags: z.array(z.string()).default([]),
    slug: z.string().optional(),
    image: z.string().optional(),
    author: z.string(),
    layout: z.string().optional(),
  }),
});

const autoNews = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: "./src/content/auto-news" }),
  schema: z.object({
    draft: z.boolean().optional().default(false),
    title: z.string(),
    description: z.string(),
    pubDate: z.string().or(z.date()), // Acepta texto o fecha
    tags: z.array(z.string()).default([]),
    slug: z.string().optional(),
    image: z.string().optional(),
    author: z.string(),
    layout: z.string().optional(),
  }),
});
export const collections = { posts, autoNews };
