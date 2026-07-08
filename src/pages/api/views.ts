import type { APIRoute } from "astro";
import { readFileSync, writeFileSync, existsSync, mkdirSync } from "node:fs";
import { join } from "node:path";

const DATA_DIR = join(process.cwd(), "data");
const VIEWS_FILE = join(DATA_DIR, "views.json");

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
  writeFileSync(VIEWS_FILE, JSON.stringify(views, null, 2));
}

export const POST: APIRoute = async ({ request }) => {
  const body = await request.json();
  const { slug } = body;

  if (!slug || typeof slug !== "string") {
    return new Response(JSON.stringify({ error: "slug required" }), {
      status: 400,
    });
  }

  const views = getViews();
  views[slug] = (views[slug] || 0) + 1;
  saveViews(views);

  return new Response(JSON.stringify({ slug, views: views[slug] }), {
    headers: { "Content-Type": "application/json" },
  });
};

export const GET: APIRoute = async ({ url }) => {
  const slug = url.searchParams.get("slug");
  const views = getViews();

  if (slug) {
    return new Response(
      JSON.stringify({ slug, views: views[slug] || 0 }),
      { headers: { "Content-Type": "application/json" } }
    );
  }

  const top = Object.entries(views)
    .sort(([, a], [, b]) => b - a)
    .slice(0, 5)
    .map(([slug, views]) => ({ slug, views }));

  return new Response(JSON.stringify(top), {
    headers: { "Content-Type": "application/json" },
  });
};
