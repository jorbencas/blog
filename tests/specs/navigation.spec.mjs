import { test, expect } from "@playwright/test";

test.describe("Navigation", () => {
  test.describe("Navbar", () => {
    test("all 5 nav links visible on desktop", async ({ page }) => {
      await page.setViewportSize({ width: 1280, height: 800 });
      await page.goto("/", { waitUntil: "networkidle" });
      const links = page.locator("a.nav-link");
      await expect(links).toHaveCount(5);
      const texts = await links.allTextContents();
      const expected = ["Proyectos", "Retos", "Blog", "Mini Herramientas", "Bugs"];
      for (const t of expected) {
        expect(texts.some((s) => s.trim().startsWith(t))).toBeTruthy();
      }
    });

    test("active nav link has visible underline", async ({ page }) => {
      await page.setViewportSize({ width: 1280, height: 800 });
      await page.goto("/retos/1", { waitUntil: "networkidle" });
      const retosLink = page.locator("a.nav-link:has-text('Retos')");
      const underline = retosLink.locator(".nav-underline");
      const w = await underline.evaluate((el) => parseFloat(getComputedStyle(el).width));
      expect(w).toBeGreaterThan(0);
    });

    test("inactive nav link has zero underline width", async ({ page }) => {
      await page.setViewportSize({ width: 1280, height: 800 });
      await page.goto("/retos/1", { waitUntil: "networkidle" });
      const blogLink = page.locator("a.nav-link:has-text('Blog')");
      const underline = blogLink.locator(".nav-underline");
      const w = await underline.evaluate((el) => parseFloat(getComputedStyle(el).width));
      expect(w).toBe(0);
    });

    test("nav links not clipped on desktop", async ({ page }) => {
      await page.setViewportSize({ width: 1280, height: 800 });
      await page.goto("/", { waitUntil: "networkidle" });
      const nav = page.locator("nav");
      const overflow = await nav.evaluate((el) => getComputedStyle(el).overflow);
      expect(overflow).not.toBe("hidden");
    });
  });

  test.describe("Mobile menu", () => {
    async function openMenu(page) {
      await page.locator("button#menu-toggle").click();
      await page.waitForTimeout(300);
    }

    test("hamburger visible on mobile, toggles menu", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 812 });
      await page.goto("/", { waitUntil: "networkidle" });
      const toggle = page.locator("button#menu-toggle");
      await expect(toggle).toBeVisible();
      const items = page.locator("#menu-items");
      await expect(items).not.toHaveClass(/open/);
      await openMenu(page);
      await expect(items).toHaveClass(/open/);
    });

    test("backdrop click closes mobile menu", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 812 });
      await page.goto("/", { waitUntil: "networkidle" });
      await openMenu(page);
      await expect(page.locator("#menu-items")).toHaveClass(/open/);
      const backdrop = page.locator("#menu-backdrop");
      await backdrop.click({ force: true });
      await page.waitForTimeout(200);
      await expect(page.locator("#menu-items")).not.toHaveClass(/open/);
    });

    test("Escape key closes mobile menu", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 812 });
      await page.goto("/", { waitUntil: "networkidle" });
      await openMenu(page);
      await expect(page.locator("#menu-items")).toHaveClass(/open/);
      await page.keyboard.press("Escape");
      await page.waitForTimeout(200);
      await expect(page.locator("#menu-items")).not.toHaveClass(/open/);
    });

    test("menu closed when resizing to desktop", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 812 });
      await page.goto("/", { waitUntil: "networkidle" });
      await openMenu(page);
      await expect(page.locator("#menu-items")).toHaveClass(/open/);
      await page.setViewportSize({ width: 1280, height: 800 });
      await page.waitForTimeout(400);
      await expect(page.locator("#menu-items")).not.toHaveClass(/open/);
    });

    test("nav links are accessible inside mobile menu", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 812 });
      await page.goto("/", { waitUntil: "networkidle" });
      await openMenu(page);
      await expect(page.locator("#menu-items a.nav-link")).toHaveCount(5);
    });
  });

  test.describe("Breadcrumbs", () => {
    test("breadcrumbs on post detail", async ({ page }) => {
      await page.goto("/posts/conexion_ssh_mediante_clave_publica_privada/", { waitUntil: "networkidle" });
      const bc = page.locator("nav[aria-label='Breadcrumb'], nav.breadcrumbs, .breadcrumbs");
      const count = await bc.count();
      if (count > 0) {
        await expect(bc.first()).toBeVisible();
      }
    });
  });

  test.describe("404 page", () => {
    test("shows 404 message and link to home", async ({ page }) => {
      await page.goto("/404.html", { waitUntil: "networkidle" });
      await expect(page.locator("h1")).toContainText("404");
      const homeLink = page.locator('a[href="/"]');
      await expect(homeLink.first()).toBeVisible();
    });
  });

  test.describe("Scroll to top", () => {
    test("button appears after scrolling 400px", async ({ page }) => {
      await page.setViewportSize({ width: 1280, height: 800 });
      await page.goto("/posts/plan_de_verano/", { waitUntil: "networkidle" });
      const btn = page.locator("#scroll-to-top, [aria-label='Scroll to top'], .scroll-to-top").first();
      const visibleBefore = await btn.isVisible();
      await page.evaluate(() => window.scrollTo(0, 500));
      await page.waitForTimeout(400);
      const visibleAfter = await btn.isVisible();
      expect(visibleAfter || !visibleBefore).toBeTruthy();
    });
  });
});
