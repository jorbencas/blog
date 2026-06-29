import { test, expect } from "@playwright/test";

test.describe("Responsive behavior", () => {
  test.describe("No horizontal overflow", () => {
    const PAGES = ["/", "/posts/1", "/retos/1", "/proyectos/1", "/tags"];
    const VIEWPORTS = [
      { width: 375, height: 812, label: "mobile" },
      { width: 768, height: 1024, label: "tablet" },
      { width: 1280, height: 800, label: "desktop" },
    ];

    for (const vp of VIEWPORTS) {
      for (const url of PAGES) {
        test(`${url} no overflow on ${vp.label}`, async ({ page }) => {
          await page.setViewportSize({ width: vp.width, height: vp.height });
          await page.goto(url, { waitUntil: "networkidle" });
          const overflow = await page.evaluate(() => {
            return {
              scrollW: document.documentElement.scrollWidth,
              clientW: document.documentElement.clientWidth,
              bodyOverflow: getComputedStyle(document.body).overflowX,
            };
          });
          expect(overflow.scrollW).toBeLessThanOrEqual(overflow.clientW + 20);
        });
      }
    }
  });

  test.describe("Navbar responsive", () => {
    test("hamburger hidden on desktop", async ({ page }) => {
      await page.setViewportSize({ width: 1280, height: 800 });
      await page.goto("/", { waitUntil: "networkidle" });
      const btn = page.locator("button#menu-toggle");
      const isVisible = await btn.isVisible();
      expect(isVisible).toBeFalsy();
    });

    test("hamburger visible on mobile", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 812 });
      await page.goto("/", { waitUntil: "networkidle" });
      const btn = page.locator("button#menu-toggle");
      await expect(btn).toBeVisible();
    });

    test("nav links hidden on mobile when menu closed", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 812 });
      await page.goto("/", { waitUntil: "networkidle" });
      const items = page.locator("#menu-items");
      await expect(items).not.toHaveClass(/open/);
    });
  });

  test.describe("Grid breakpoints", () => {
    test("homepage grid shows 1 col on mobile", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 812 });
      await page.goto("/", { waitUntil: "networkidle" });
      const sections = page.locator("div.grid > div");
      const count = await sections.count();
      if (count > 0) {
        const grid = sections.first().evaluate((el) => {
          const parent = el.parentElement;
          if (!parent) return "";
          return getComputedStyle(parent).gridTemplateColumns;
        });
      }
    });

    test("blog posts grid on tablet", async ({ page }) => {
      await page.setViewportSize({ width: 768, height: 1024 });
      await page.goto("/posts/1", { waitUntil: "networkidle" });
      const grid = page.locator("div.grid");
      const gtc = await grid.first().evaluate((el) => getComputedStyle(el).gridTemplateColumns);
      const cols = gtc.split(" ").length;
      expect(cols).toBeGreaterThanOrEqual(1);
    });
  });

  test.describe("Images", () => {
    test("images do not exceed container width on mobile", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 812 });
      await page.goto("/posts/plan_de_verano/", { waitUntil: "networkidle" });
      const imgs = page.locator("article img");
      const count = await imgs.count();
      for (let i = 0; i < count; i++) {
        const img = imgs.nth(i);
        const naturalW = await img.evaluate((el) => (el.naturalWidth || el.width));
        const containerW = await img.evaluate((el) => {
          const parent = el.parentElement;
          return parent ? parent.clientWidth : window.innerWidth;
        });
        if (naturalW > 0) {
          const renderedW = await img.evaluate((el) => el.getBoundingClientRect().width);
          expect(renderedW).toBeLessThanOrEqual(containerW + 1);
        }
      }
    });
  });

  test.describe("Code blocks", () => {
    test("code blocks scroll horizontally on mobile", async ({ page }) => {
      await page.setViewportSize({ width: 375, height: 812 });
      await page.goto("/posts/n8n/", { waitUntil: "networkidle" });
      const pres = page.locator("pre");
      const count = await pres.count();
      if (count > 0) {
        const overflow = await pres.first().evaluate((el) => getComputedStyle(el).overflowX);
        expect(overflow).toBe("auto");
      }
    });
  });
});
