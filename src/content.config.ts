// src/content/config.ts
import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const posts = defineCollection({
  loader: glob({ pattern: '**/[^_]*.(md|mdx)', base: "./content/posts" }),
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

export const collections = { posts };
