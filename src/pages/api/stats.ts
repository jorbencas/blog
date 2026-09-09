import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { getSortedPosts } from 'src/utils';

export const prerender = true;

export const GET: APIRoute = async () => {
  const allPosts = await getCollection('posts');
  const sortedPosts = await getSortedPosts(allPosts);

  const allTools = await getCollection('tools');
  const sortedTools = await getSortedPosts(allTools);

  const allWeekly = await getCollection('weeklyPosts');
  const sortedWeekly = await getSortedPosts(allWeekly);

  const allTags = new Set<string>();
  sortedPosts.forEach(p => (p.data.tags || []).forEach(t => allTags.add(t)));
  sortedTools.forEach(p => (p.data.tags || []).forEach(t => allTags.add(t)));

  const stats = {
    posts: sortedPosts.length,
    herramientas: sortedTools.length,
    weekly: sortedWeekly.length,
    total: sortedPosts.length + sortedTools.length + sortedWeekly.length,
    tags: allTags.size,
    lastUpdated: new Date().toISOString(),
  };

  return new Response(JSON.stringify(stats, null, 2), {
    headers: { 'Content-Type': 'application/json; charset=utf-8' },
  });
};
