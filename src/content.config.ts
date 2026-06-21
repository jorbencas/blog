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
    pubDate: z.coerce.string().or(z.coerce.date()),
    tags: z.array(z.string()).default([]),
    image: z.string().optional(),
    author: z.string(),
    audioSrc: z.string().optional()
  }),
});

const weeklyPosts = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: "./src/content/auto-news" }),
  schema: z.object({
    draft: z.boolean().optional().default(false),
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.string().or(z.coerce.date()),
    tags: z.array(z.string()).default([]),
    image: z.string().optional(),
    author: z.string(),
    audioSrc: z.string().optional()
  }),
});

const challenges = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: "./src/content/auto-challenges" }),
  schema: z.object({
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.string().or(z.coerce.date()),
    image: z.string(),
    tags: z.array(z.string()),
    difficulty: z.enum(['Iniciación', 'Intermedio', 'Avanzado']),
  }),
});

const myprojects = defineCollection({
  loader: glob({ pattern: '**/*.{md,mdx}', base: "./src/content/myprojects" }),
  schema: z.object({
    draft: z.boolean().optional().default(false),
    title: z.string(),
    description: z.string(),
    pubDate: z.coerce.string().or(z.coerce.date()),
    image: z.string(),
    repository: z.string().url().optional(), // Enlace a GitHub
    url: z.string().url().optional(),        // Enlace al proyecto en vivo
    tags: z.array(z.string()).optional(),               // Tecnologías (React, Astro, etc.)
    featured: z.boolean().default(false),    // Por si quieres destacar alguno
  }),
});

export const collections = { posts, weeklyPosts, challenges, myprojects };
