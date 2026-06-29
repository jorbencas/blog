import { test, expect } from "@playwright/test";

test.describe("Navbar underline", () => {
  test("active link shows underline on desktop", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/retos/1", { waitUntil: "networkidle" });

    const retosLink = page.locator("a.nav-link:has-text('Retos')");
    await expect(retosLink).toBeVisible();

    const underline = retosLink.locator(".nav-underline");
    await expect(underline).toBeVisible();

    const ancho = await underline.evaluate((el) => {
      const style = getComputedStyle(el);
      return parseFloat(style.width);
    });
    expect(ancho).toBeGreaterThan(0);
  });

  test("inactive link has zero-width underline", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/retos/1", { waitUntil: "networkidle" });

    const blogLink = page.locator("a.nav-link:has-text('Blog')");
    await expect(blogLink).toBeVisible();

    const underline = blogLink.locator(".nav-underline");
    const cls = await underline.getAttribute("class");
    expect(cls).toContain("w-0");
  });

  test("all nav links are visible without overflow clipping on desktop", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/retos/1", { waitUntil: "networkidle" });

    const links = page.locator("a.nav-link");
    const count = await links.count();
    expect(count).toBeGreaterThanOrEqual(4);

    for (let i = 0; i < count; i++) {
      const link = links.nth(i);
      const underline = link.locator(".nav-underline");
      const visible = await underline.evaluate((el) => {
        const style = getComputedStyle(el);
        return style.visibility !== "hidden" && style.display !== "none" && parseFloat(style.opacity) > 0;
      });
      expect(visible).toBe(true);
    }
  });
});
