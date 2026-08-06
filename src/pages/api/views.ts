import type { APIRoute } from "astro";
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const DATA_DIR = join(process.cwd(), "data");
const VIEWS_FILE = join(DATA_DIR, "views.json");
const MAX_ENTRIES = 5000;
const SLUG_MAX_LEN = 200;
const SLUG_REGEX = /^[a-zA-Z0-9\-_]+$/;

const rateMap = new Map<string, { count: number; resetAt: number }>();
const RATE_WINDOW_MS = 60_000;
const RATE_MAX = 30;

function checkRate(ip: string): boolean {
  const now = Date.now();
  const entry = rateMap.get(ip);
  if (!entry || now > entry.resetAt) {
    rateMap.set(ip, { count: 1, resetAt: now + RATE_WINDOW_MS });
    return true;
  }
  if (entry.count >= RATE_MAX) return false;
  entry.count++;
  return true;
}

function sanitizeSlug(slug: string): string | null {
  if (typeof slug !== "string") return null;
  const trimmed = slug.trim();
  if (trimmed.length === 0 || trimmed.length > SLUG_MAX_LEN) return null;
  if (!SLUG_REGEX.test(trimmed)) return null;
  return trimmed;
}

function ensureDataDir() {
  if (!existsSync(DATA_DIR)) {
    mkdirSync(DATA_DIR, { recursive: true });
  }
}

function getViews(): Record<string, number> {
  ensureDataDir();
  if (existsSync(VIEWS_FILE)) {
    try {
      return JSON.parse(readFileSync(VIEWS_FILE, "utf-8"));
    } catch {
      return {};
    }
  }
  return {};
}

function saveViews(views: Record<string, number>) {
  ensureDataDir();
  const entries = Object.entries(views);
  if (entries.length > MAX_ENTRIES) {
    const sorted = entries.sort(([, a], [, b]) => a - b);
    const pruned = Object.fromEntries(sorted.slice(-MAX_ENTRIES));
    writeFileSync(VIEWS_FILE, JSON.stringify(pruned, null, 2));
  } else {
    writeFileSync(VIEWS_FILE, JSON.stringify(views, null, 2));
  }
}

function getClientIP(request: Request): string {
  const xfwd = request.headers.get("x-forwarded-for");
  if (xfwd) return xfwd.split(",")[0].trim();
  return "unknown";
}

const JSON_HEADERS = { "Content-Type": "application/json" };

export const POST: APIRoute = async ({ request }) => {
  const ip = getClientIP(request);

  if (!checkRate(ip)) {
    return new Response(JSON.stringify({ error: "rate limit exceeded" }), {
      status: 429,
      headers: { ...JSON_HEADERS, "Retry-After": "60" },
    });
  }

  let body: unknown;
  try {
    body = await request.json();
  } catch {
    return new Response(JSON.stringify({ error: "invalid json" }), {
      status: 400,
      headers: JSON_HEADERS,
    });
  }

  const { slug: rawSlug } = body as { slug?: unknown };
  const slug = sanitizeSlug(rawSlug as string);

  if (!slug) {
    return new Response(JSON.stringify({ error: "slug required (alphanumeric, hyphens, underscores, max 200 chars)" }), {
      status: 400,
      headers: JSON_HEADERS,
    });
  }

  const views = getViews();
  views[slug] = (views[slug] || 0) + 1;
  saveViews(views);

  return new Response(JSON.stringify({ slug, views: views[slug] }), {
    headers: JSON_HEADERS,
  });
};

export const GET: APIRoute = async ({ url }) => {
  const slug = url.searchParams.get("slug");
  const views = getViews();

  if (slug) {
    const clean = sanitizeSlug(slug);
    if (!clean) {
      return new Response(JSON.stringify({ error: "invalid slug" }), {
        status: 400,
        headers: JSON_HEADERS,
      });
    }
    return new Response(
      JSON.stringify({ slug: clean, views: views[clean] || 0 }),
      { headers: JSON_HEADERS }
    );
  }

  const top = Object.entries(views)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 5)
    .map(([slug, views]) => ({ slug, views }));

  return new Response(JSON.stringify(top), {
    headers: JSON_HEADERS,
  });
};
