# Newsletter Setup Guide

## What is a Newsletter?

A newsletter is a list of subscribers who receive periodic emails with your content. You write articles, summaries, or updates, and they arrive directly in the subscriber's inbox.

For this blog, a newsletter would let readers subscribe to receive:
- Weekly tech recaps (resúmenes semanales)
- New blog posts
- Curated tool discoveries
- Challenge announcements

---

## Recommended Services (Free Tier)

### 1. Buttondown (Recommended)

- **Free tier**: 100 subscribers, 100 emails/month
- **Best for**: Developers, minimal UI, Markdown-based
- **Pricing**: Free → $9/mo (1,000 subs) → $29/mo (10,000 subs)

**Setup:**
1. Go to [buttondown.com](https://buttondown.com/) and create an account
2. Create a newsletter (name it, add description)
3. Get your API key from Settings → API
4. The embed form URL is: `https://buttondown.com/yourname`

**Pros:**
- Clean, developer-friendly UI
- Markdown emails
- Simple API for programmatic subscriptions
- No branding forced on your emails

**Cons:**
- Small free tier
- Limited templates

---

### 2. Substack

- **Free tier**: Unlimited subscribers, unlimited emails
- **Best for**: Writers who want built-in discovery
- **Pricing**: Free (they take 10% of paid subscriptions if you monetize)

**Setup:**
1. Go to [substack.com](https://substack.com/) and create an account
2. Create your publication
3. Customize the page
4. Share the URL

**Pros:**
- Completely free
- Built-in reader network
- Easy to use

**Cons:**
- Your content is public by default (SEO-indexed)
- Less control over branding
- Substack-owned audience (you can export, but they own the distribution)

---

### 3. Resend

- **Free tier**: 3,000 emails/month, 100 contacts
- **Best for**: Developers who want full control
- **Pricing**: Free → $20/mo (50,000 emails/mo)

**Setup:**
1. Go to [resend.com](https://resend.com/) and create an account
2. Verify your domain (DNS records)
3. Use their API or React Email for templates
4. Build a custom signup form

**Pros:**
- Developer-first (API, webhooks)
- Beautiful React Email templates
- Full control over everything
- No vendor lock-in

**Cons:**
- Requires more setup (domain verification, custom form)
- No built-in subscriber management UI (use their API or build one)

---

### 4. Mailchimp

- **Free tier**: 500 subscribers, 500 emails/month
- **Best for**: Non-technical users
- **Pricing**: Free → $13/mo (500 subs) → scales up

**Setup:**
1. Go to [mailchimp.com](https://mailchimp.com/) and create an account
2. Create an audience
3. Create a signup form
4. Embed or link to it

**Pros:**
- Drag-and-drop email builder
- Well-known, lots of integrations

**Cons:**
- Aggressive upsell emails
- Complex UI
- Free tier is very limited

---

### 5. Beehiiv

- **Free tier**: 2,500 subscribers, unlimited emails
- **Best for**: Growth-focused newsletters
- **Pricing**: Free → $39/mo (custom domain, ad network)

**Setup:**
1. Go to [beehiiv.com](https://www.beehiiv.com/) and create an account
2. Create a publication
3. Use their built-in signup forms
4. Embed via JavaScript widget

**Pros:**
- Generous free tier
- Built-in analytics and growth tools
- Ad network for monetization

**Cons:**
- Less known
- Some features locked behind paid tiers

---

## Integration with This Blog

### Option A: Link-based CTA (Simplest)

No backend needed. Just add a CTA section in `index.astro`:

```astro
<section class="...">
  <div class="bg-gradient-to-r from-sky-800 to-cyan-500 p-8 rounded-xl">
    <h2>Suscríbete al Newsletter</h2>
    <p>Recibe resúmenes semanales de novedades tech en tu inbox.</p>
    <a href="https://your-service.com/subscribe" target="_blank">
      Suscribirse →
    </a>
  </div>
</section>
```

### Option B: Embed Form (Buttondown/Substack)

Buttondown and Substack provide embeddable forms:

```html
<!-- Buttondown embed -->
<iframe
  src="https://buttondown.com/yourname/embed"
  width="480"
  height="320"
  frameborder="0"
  scrolling="no"
></iframe>
```

### Option C: Custom Form + API (Resend/Mailchimp)

Build a custom form that POSTs to the service API:

```astro
<form id="newsletter-form" class="flex gap-2">
  <input
    type="email"
    name="email"
    placeholder="tu@email.com"
    required
    class="px-4 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800"
  />
  <button
    type="submit"
    class="px-6 py-2 bg-gradient-to-r from-sky-800 to-cyan-500 text-white font-bold rounded-lg"
  >
    Suscribirse
  </button>
</form>

<script>
  document.getElementById("newsletter-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target as HTMLFormElement;
    const email = new FormData(form).get("email");

    await fetch("https://api.resend.com/subscribers", {
      method: "POST",
      headers: {
        Authorization: "Bearer re_your_api_key",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        audience_id: "your_audience_id",
      }),
    });

    alert("¡Suscrito!");
    form.reset();
  });
</script>
```

---

## Recommendation for This Blog

**Start with Buttondown** because:
1. Free up to 100 subscribers (enough to validate the idea)
2. Markdown-based (matches the blog's developer aesthetic)
3. Simple embed form (no custom code needed)
4. Can migrate later (export subscriber list as CSV)

**Steps:**
1. Create Buttondown account
2. Set up newsletter name and description
3. Copy the embed URL
4. Add the CTA section in `index.astro` with the embed link
5. Share the newsletter link in weekly posts and the footer

---

## Adding the Newsletter CTA to index.astro

Once you have a service, add this section after the Stats Bar:

```astro
<!-- NEWSLETTER CTA -->
<section class="relative overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-gradient-to-br from-sky-900 via-cyan-800 to-sky-900 p-8 sm:p-12">
  <div class="absolute inset-0 opacity-10" style="background-image: url('/img/circuit-bg.svg'); background-size: 200px;"></div>
  <div class="relative z-10 max-w-xl">
    <h2 class="text-2xl sm:text-3xl font-black uppercase italic tracking-tighter text-white mb-3">
      📬 Newsletter
    </h2>
    <p class="text-cyan-100/80 text-sm sm:text-base leading-relaxed mb-6">
      Recibe en tu inbox los resúmenes semanales, nuevos artículos y las mejores herramientas descubiertas.
    </p>
    <a
      href="https://your-buttondown-url.subscribe"
      target="_blank"
      rel="noopener noreferrer"
      class="inline-flex items-center gap-2 px-6 py-3 bg-white text-sky-900 font-black uppercase tracking-wider text-sm rounded-lg hover:bg-cyan-100 transition-colors"
    >
      Suscribirse →
    </a>
  </div>
</section>
```

---

## Tracking Views for "Lo más leído"

To show "most read" posts, you need view tracking. Options:

### Simple: JSON file on Vercel

Create `src/pages/api/views.ts` that reads/writes a JSON file:

```typescript
import type { APIRoute } from 'astro';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const VIEWS_FILE = join(process.cwd(), 'data/views.json');

export const POST: APIRoute = async ({ request }) => {
  const { slug } = await request.json();

  let views: Record<string, number> = {};
  if (existsSync(VIEWS_FILE)) {
    views = JSON.parse(readFileSync(VIEWS_FILE, 'utf-8'));
  }

  views[slug] = (views[slug] || 0) + 1;
  writeFileSync(VIEWS_FILE, JSON.stringify(views, null, 2));

  return new Response(JSON.stringify({ views: views[slug] }));
};

export const GET: APIRoute = async ({ url }) => {
  const slug = url.searchParams.get('slug');

  let views: Record<string, number> = {};
  if (existsSync(VIEWS_FILE)) {
    views = JSON.parse(readFileSync(VIEWS_FILE, 'utf-8'));
  }

  if (slug) {
    return new Response(JSON.stringify({ slug, views: views[slug] || 0 }));
  }

  // Return top 5 most viewed
  const top = Object.entries(views)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 5)
    .map(([slug, views]) => ({ slug, views }));

  return new Response(JSON.stringify(top));
};
```

**Note:** This approach has a caveat — Vercel serverless functions are ephemeral, so the JSON file won't persist across deployments. For production, use:
- **Vercel KV** (Redis) — free tier: 30,000 requests/month
- **Upstash Redis** — free tier: 10,000 requests/day
- **PlanetScale** — free tier: 1 billion reads/month

### Better: Upstash Redis

```typescript
import { Redis } from '@upstash/redis';

const redis = new Redis({
  url: process.env.UPSTASH_REDIS_REST_URL!,
  token: process.env.UPSTASH_REDIS_REST_TOKEN!,
});

export const POST: APIRoute = async ({ request }) => {
  const { slug } = await request.json();
  const views = await redis.incr(`views:${slug}`);
  return new Response(JSON.stringify({ views }));
};

export const GET: APIRoute = async ({ url }) => {
  const slug = url.searchParams.get('slug');
  if (slug) {
    const views = await redis.get<number>(`views:${slug}`) || 0;
    return new Response(JSON.stringify({ slug, views }));
  }
  // Top 5
  const keys = await redis.keys('views:*');
  const top = await Promise.all(
    keys.slice(0, 5).map(async (key) => ({
      slug: key.replace('views:', ''),
      views: (await redis.get<number>(key)) || 0,
    }))
  );
  top.sort((a, b) => b.views - a.views);
  return new Response(JSON.stringify(top));
};
```

---

## Summary

| Step | Action |
|------|--------|
| 1 | Choose a newsletter service (Buttondown recommended) |
| 2 | Create account and set up newsletter |
| 3 | Copy embed URL or API key |
| 4 | Add CTA section in `index.astro` |
| 5 | Add newsletter link to weekly posts and footer |
| 6 | For "lo más leído", set up view tracking (Upstash Redis recommended) |
| 7 | Add "lo más leído" section using the tracking API |
