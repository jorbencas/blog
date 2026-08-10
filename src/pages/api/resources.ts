import type { APIRoute } from "astro";
import fs from "fs";
import path from "path";

export const prerender = false;

export const GET: APIRoute = async ({ url }) => {
  const page = parseInt(url.searchParams.get("page") || "1");
  const limit = parseInt(url.searchParams.get("limit") || "50");
  const category = url.searchParams.get("category") || "";
  const pricing = url.searchParams.get("pricing") || "";
  const search = url.searchParams.get("search") || "";

  const mapPath = path.resolve(process.cwd(), "src/data/resources.json");
  const allResources = JSON.parse(fs.readFileSync(mapPath, "utf-8"));

  let filtered = allResources;

  if (category && category !== "all") {
    filtered = filtered.filter((r) => r.category === category);
  }

  if (pricing && pricing !== "all") {
    filtered = filtered.filter((r) => r.pricing === pricing);
  }

  if (search) {
    const q = search.toLowerCase();
    filtered = filtered.filter(
      (r) =>
        r.title.toLowerCase().includes(q) ||
        r.description.toLowerCase().includes(q) ||
        r.category.toLowerCase().includes(q)
    );
  }

  const total = filtered.length;
  const totalPages = Math.ceil(total / limit);
  const start = (page - 1) * limit;
  const items = filtered.slice(start, start + limit);

  return new Response(
    JSON.stringify({ items, page, totalPages, total, hasMore: page < totalPages }),
    {
      headers: { "Content-Type": "application/json" },
    }
  );
};
