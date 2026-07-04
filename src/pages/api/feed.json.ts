import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { getSortedPosts } from 'src/utils';
import { SITE_NAME, SITE_DESCRIPTION, SITE_URL, AUTHOR_NAME } from 'src/consts';

export const prerender = true;

export const GET: APIRoute = async () => {
  const allPosts = await getCollection('posts');
  const sortedPosts = await getSortedPosts(allPosts);

  const allChallenges = await getCollection('auto-challenges');
  const sortedChallenges = await getSortedPosts(allChallenges);

  const allTools = await getCollection('tools');
  const sortedTools = await getSortedPosts(allTools);

  const allWeekly = await getCollection('weeklyPosts');
  const sortedWeekly = await getSortedPosts(allWeekly);

  const allItems = [
    ...sortedPosts.map(p => ({
      id: `${SITE_URL.replace(/\/$/, '')}/posts/${p.id}`,
      url: `${SITE_URL.replace(/\/$/, '')}/posts/${p.id}`,
      title: p.data.title || '',
      content_text: p.data.description || '',
      date_published: p.data.pubDate ? new Date(p.data.pubDate).toISOString() : undefined,
      tags: p.data.tags || [],
      _section: 'posts',
    })),
    ...sortedChallenges.map(p => ({
      id: `${SITE_URL.replace(/\/$/, '')}/retos/${p.id.replace(/\.[^/.]+$/, '')}`,
      url: `${SITE_URL.replace(/\/$/, '')}/retos/${p.id.replace(/\.[^/.]+$/, '')}`,
      title: p.data.title || '',
      content_text: p.data.description || '',
      date_published: p.data.pubDate ? new Date(p.data.pubDate).toISOString() : undefined,
      tags: p.data.tags || [],
      _section: 'retos',
    })),
    ...sortedTools.map(p => ({
      id: `${SITE_URL.replace(/\/$/, '')}/herramientas/${p.id.replace(/\.[^/.]+$/, '')}`,
      url: `${SITE_URL.replace(/\/$/, '')}/herramientas/${p.id.replace(/\.[^/.]+$/, '')}`,
      title: p.data.name || p.data.title || '',
      content_text: p.data.description || '',
      tags: p.data.tags || [],
      _section: 'herramientas',
    })),
    ...sortedWeekly.map(p => ({
      id: `${SITE_URL.replace(/\/$/, '')}/weekly/${p.id}`,
      url: `${SITE_URL.replace(/\/$/, '')}/weekly/${p.id}`,
      title: p.data.title || '',
      content_text: p.data.description || '',
      date_published: p.data.date ? new Date(p.data.date).toISOString() : undefined,
      tags: [],
      _section: 'weekly',
    })),
  ].sort((a, b) => {
    const da = a.date_published ? new Date(a.date_published).getTime() : 0;
    const db = b.date_published ? new Date(b.date_published).getTime() : 0;
    return db - da;
  });

  const feed = {
    version: 'https://jsonfeed.org/version/1.1',
    title: SITE_NAME,
    home_page_url: SITE_URL,
    feed_url: `${SITE_URL}api/feed.json`,
    description: SITE_DESCRIPTION,
    language: 'es',
    authors: [{ name: AUTHOR_NAME }],
    items: allItems.map(({ _section, ...item }) => ({
      ...item,
      date_published: item.date_published || new Date().toISOString(),
    })),
  };

  return new Response(JSON.stringify(feed, null, 2), {
    headers: { 'Content-Type': 'application/feed+json; charset=utf-8' },
  });
};
