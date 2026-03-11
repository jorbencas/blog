// src/content/config.ts
import { defineCollection, z } from 'astro:content';

const postsCollection = defineCollection({
  type: 'content', // indica que son archivos .md o .mdx
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.string().or(z.date()), // Acepta texto o fecha
    image: z.string().optional(),
    tags: z.array(z.string()).default([]),
    draft: z.boolean().optional().default(false),
    autor: z.string()
    slug: z.string()
  }),
});

export const collections = {
  'posts': postsCollection,
};