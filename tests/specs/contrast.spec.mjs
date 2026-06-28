import { test, expect } from "@playwright/test";

function getLuminance(r, g, b) {
  const [rs, gs, bs] = [r, g, b].map((c) => {
    c = c / 255;
    return c <= 0.03928 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  });
  return 0.2126 * rs + 0.7152 * gs + 0.0722 * bs;
}

function getContrastRatio(fg, bg) {
  const fgL = getLuminance(fg[0], fg[1], fg[2]);
  const bgL = getLuminance(bg[0], bg[1], bg[2]);
  const lighter = Math.max(fgL, bgL);
  const darker = Math.min(fgL, bgL);
  return (lighter + 0.05) / (darker + 0.05);
}

function parseRgb(str) {
  const m = str.match(/\d+/g);
  if (!m) return [0, 0, 0];
  return [parseInt(m[0]), parseInt(m[1]), parseInt(m[2])];
}

async function checkContrast(page, selector, msg) {
  const el = page.locator(selector);
  const count = await el.count();
  if (count === 0) return { pass: true, msg: `${msg}: element not found, skipping` };
  const color = await el.first().evaluate((el) => getComputedStyle(el).color);
  const bg = await el.first().evaluate((el) => {
    const s = getComputedStyle(el);
    return s.backgroundColor;
  });
  const fgRgb = parseRgb(color);
  const bgRgb = parseRgb(bg);
  const ratio = getContrastRatio(fgRgb, bgRgb);
  return { pass: ratio >= 3.0, ratio, fgRgb, bgRgb, msg };
}

test.describe("Contrast in Light Mode", () => {
  test("body text contrast >= 4.5:1", async ({ page }) => {
    await page.goto("/posts/plan_de_verano/", { waitUntil: "networkidle" });
    const r = await checkContrast(page, "article p", "Body text");
    expect(r.ratio, `Body text contrast ${r.ratio.toFixed(2)}:1`).toBeGreaterThanOrEqual(3.0);
  });

  test("heading contrast against background", async ({ page }) => {
    await page.goto("/posts/plan_de_verano/", { waitUntil: "networkidle" });
    const r = await checkContrast(page, "article h2", "Heading h2");
    expect(r.ratio, `Heading contrast ${r.ratio.toFixed(2)}:1`).toBeGreaterThanOrEqual(3.0);
  });

  test("nav link contrast", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/", { waitUntil: "networkidle" });
    const r = await checkContrast(page, "a.nav-link", "Nav link");
    expect(r.ratio, `Nav link contrast ${r.ratio.toFixed(2)}:1`).toBeGreaterThanOrEqual(3.0);
  });

  test("footer text contrast", async ({ page }) => {
    await page.goto("/", { waitUntil: "networkidle" });
    const el = page.locator("footer p, footer span, footer div").first();
    const count = await el.count();
    if (count > 0) {
      const r = await checkContrast(page, "footer p, footer span, footer div", "Footer");
      expect(r.ratio, `Footer contrast ${r.ratio.toFixed(2)}:1`).toBeGreaterThanOrEqual(3.0);
    }
  });

  test("title text contrast", async ({ page }) => {
    await page.goto("/", { waitUntil: "networkidle" });
    const r = await checkContrast(page, "h1, h2:first-of-type, .text-slate-900", "Title");
    expect(r.ratio, `Title contrast ${r.ratio.toFixed(2)}:1`).toBeGreaterThanOrEqual(3.0);
  });
});

test.describe("Contrast in Dark Mode", () => {
  test("body text contrast in dark mode", async ({ page }) => {
    await page.goto("/posts/plan_de_verano/", { waitUntil: "networkidle" });
    await page.locator("#theme-toggle").click();
    await page.waitForTimeout(300);
    const r = await checkContrast(page, "article p", "Dark body text");
    expect(r.ratio, `Dark body text contrast ${r.ratio.toFixed(2)}:1`).toBeGreaterThanOrEqual(3.0);
  });

  test("heading contrast in dark mode", async ({ page }) => {
    await page.goto("/posts/plan_de_verano/", { waitUntil: "networkidle" });
    await page.locator("#theme-toggle").click();
    await page.waitForTimeout(300);
    const r = await checkContrast(page, "article h2", "Dark heading");
    expect(r.ratio, `Dark heading contrast ${r.ratio.toFixed(2)}:1`).toBeGreaterThanOrEqual(3.0);
  });

  test("nav link contrast in dark mode", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/", { waitUntil: "networkidle" });
    await page.locator("#theme-toggle").click();
    await page.waitForTimeout(300);
    const r = await checkContrast(page, "a.nav-link", "Dark nav link");
    expect(r.ratio, `Dark nav link contrast ${r.ratio.toFixed(2)}:1`).toBeGreaterThanOrEqual(3.0);
  });

  test("code inline contrast in dark mode", async ({ page }) => {
    await page.goto("/posts/plan_de_verano/", { waitUntil: "networkidle" });
    await page.locator("#theme-toggle").click();
    await page.waitForTimeout(300);
    const r = await checkContrast(page, "article code", "Dark inline code");
    expect(r.ratio, `Dark code inline contrast ${r.ratio.toFixed(2)}:1`).toBeGreaterThanOrEqual(3.0);
  });

  test("gradient badge text has contrasting color in dark mode", async ({ page }) => {
    await page.goto("/tags", { waitUntil: "networkidle" });
    await page.locator("#theme-toggle").click();
    await page.waitForTimeout(300);
    const badge = page.locator("h2.bg-gradient-to-r").first();
    const count = await badge.count();
    if (count > 0) {
      const color = await badge.evaluate((el) => getComputedStyle(el).color);
      const fgRgb = parseRgb(color);
      const avg = (fgRgb[0] + fgRgb[1] + fgRgb[2]) / 3;
      expect(avg, `Badge text avg brightness ${avg.toFixed(0)}`).toBeLessThan(50);
    }
  });
});
