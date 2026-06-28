import { test, expect } from "@playwright/test";

const PAGES = [
  { path: "/", name: "homepage" },
  { path: "/posts/conexion_ssh_mediante_clave_publica_privada/", name: "post-ssh" },
  { path: "/posts/plan_de_verano/", name: "post-plan-verano" },
  { path: "/posts/linea_temporal_blog/", name: "post-timeline" },
  { path: "/posts/1", name: "blog-listing" },
  { path: "/proyectos/1", name: "proyectos" },
  { path: "/proyectos/tech-pulse-dashboard/", name: "proyecto-detail" },
  { path: "/retos/1", name: "retos" },
  { path: "/retos/reto-inicial-01-suma-de-digitos/", name: "reto-detail" },
  { path: "/herramientas/1", name: "herramientas-list" },
  { path: "/herramientas/extractor-frames/", name: "herramientas-detail" },
  { path: "/tags", name: "tags-index" },
  { path: "/tags/web/1", name: "tags-web" },
  { path: "/weekly/1", name: "weekly-listing" },
  { path: "/weekly/2026-w26-tech-recap/", name: "weekly-detail" },
  { path: "/404.html", name: "404" },
];

test.describe("Visual regression desktop light", () => {
  for (const { path, name } of PAGES) {
    test(`screenshot: ${name}`, async ({ page }) => {
      await page.setViewportSize({ width: 1280, height: 800 });
      await page.goto(path, { waitUntil: "networkidle" });
      await page.waitForTimeout(2000);
      await expect(page).toHaveScreenshot(`${name}-desktop-light.png`, {
        fullPage: true,
        maxDiffPixelRatio: 0.08,
        animations: "disabled",
      });
    });
  }
});

test.describe("Visual regression desktop dark", () => {
  for (const { path, name } of PAGES) {
    test(`screenshot dark: ${name}`, async ({ page }) => {
      await page.setViewportSize({ width: 1280, height: 800 });
      await page.goto(path, { waitUntil: "networkidle" });
      await page.locator("#theme-toggle").click();
      await page.waitForTimeout(2000);
      await expect(page).toHaveScreenshot(`${name}-desktop-dark.png`, {
        fullPage: true,
        maxDiffPixelRatio: 0.08,
        animations: "disabled",
      });
    });
  }
});

test.describe("Visual regression mobile", () => {
  const MOBILE_PAGES = [
    { path: "/", name: "homepage" },
    { path: "/posts/1", name: "blog-listing" },
    { path: "/retos/reto-inicial-01-suma-de-digitos/", name: "reto-detail" },
    { path: "/proyectos/1", name: "proyectos" },
  ];

  for (const { path, name } of MOBILE_PAGES) {
    test(`screenshot mobile: ${name}`, async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 812 });
      await page.goto(path, { waitUntil: "networkidle" });
      await page.waitForTimeout(2000);
      await expect(page).toHaveScreenshot(`${name}-mobile-light.png`, {
        fullPage: true,
        maxDiffPixelRatio: 0.08,
        animations: "disabled",
      });
    });
  }
});

test.describe("Visual regression mobile dark", () => {
  const MOBILE_PAGES = [
    { path: "/", name: "homepage" },
    { path: "/posts/1", name: "blog-listing" },
    { path: "/retos/reto-inicial-01-suma-de-digitos/", name: "reto-detail" },
  ];

  for (const { path, name } of MOBILE_PAGES) {
    test(`screenshot mobile dark: ${name}`, async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 812 });
      await page.goto(path, { waitUntil: "networkidle" });
      await page.locator("#theme-toggle").click();
      await page.waitForTimeout(2000);
      await expect(page).toHaveScreenshot(`${name}-mobile-dark.png`, {
        fullPage: true,
        maxDiffPixelRatio: 0.08,
        animations: "disabled",
      });
    });
  }
});
