import type { APIRoute } from 'astro';
import { getCollection } from 'astro:content';
import { getSortedPosts } from 'src/utils';
import { SITE_NAME, SITE_DESCRIPTION, SITE_URL, AUTHOR_NAME } from 'src/consts';

export const prerender = true;

function escapeXml(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

function buildRssItem(title: string, link: string, description: string, pubDate: Date, tags: string[], section: string): string {
  return `  <item>
    <title>${escapeXml(title)}</title>
    <link>${link}</link>
    <guid isPermaLink="true">${link}</guid>
    <pubDate>${pubDate.toUTCString()}</pubDate>
    <description>${escapeXml(description)}</description>
    <category>${escapeXml(section)}</category>
    ${tags.map(t => `<category>${escapeXml(t)}</category>`).join('\n    ')}
  </item>`;
}

export const GET: APIRoute = async () => {
  const allPosts = (await getCollection('posts'));
  const sortedPosts = await getSortedPosts(allPosts);

  const allChallenges = await getCollection('auto-challenges');
  const sortedChallenges = await getSortedPosts(allChallenges);

  const allTools = await getCollection('tools');
  const sortedTools = await getSortedPosts(allTools);

  const allWeekly = await getCollection('weeklyPosts');
  const sortedWeekly = await getSortedPosts(allWeekly);

  const allItems = [
    ...sortedPosts.map(p => ({ ...p, _section: 'posts', _link: `/posts/${p.id}` })),
    ...sortedChallenges.map(p => ({ ...p, _section: 'retos', _link: `/retos/${p.id.replace(/\.[^/.]+$/, '')}` })),
    ...sortedTools.map(p => ({ ...p, _section: 'herramientas', _link: `/herramientas/${p.id.replace(/\.[^/.]+$/, '')}` })),
    ...sortedWeekly.map(p => ({ ...p, _section: 'weekly', _link: `/weekly/${p.id}` })),
  ].sort((a, b) => new Date(b.data.pubDate || b.data.date || 0).getTime() - new Date(a.data.pubDate || a.data.date || 0).getTime());

  const now = new Date();
  const items = allItems.map(p => buildRssItem(
    p.data.title || p.data.name || '',
    `${SITE_URL.replace(/\/$/, '')}${p._link}`,
    p.data.description || '',
    new Date(p.data.pubDate || p.data.date || now),
    p.data.tags || [],
    p._section,
  )).join('\n');

  const rss = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
  <channel>
    <title>${escapeXml(SITE_NAME)}</title>
    <link>${SITE_URL}</link>
    <description>${escapeXml(SITE_DESCRIPTION)}</description>
    <language>es</language>
    <lastBuildDate>${now.toUTCString()}</lastBuildDate>
    <atom:link href="${SITE_URL}rss.xml" rel="self" type="application/rss+xml"/>
    <image>
      <url>${SITE_URL}favicon.ico</url>
      <title>${escapeXml(SITE_NAME)}</title>
      <link>${SITE_URL}</link>
    </image>
${items}
  </channel>
</rss>`;

  return new Response(rss, {
    headers: { 'Content-Type': 'application/rss+xml; charset=utf-8' },
  });
};
