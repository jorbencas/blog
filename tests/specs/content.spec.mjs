import { test, expect } from "@playwright/test";

test.describe("Content elements", () => {
  test("CopyPost buttons exist (MD, TXT, IA)", async ({ page }) => {
    await page.goto("/posts/conexion_ssh_mediante_clave_publica_privada/", {
      waitUntil: "networkidle",
    });

    const btns = page.locator('.copy-post button[data-copy]');
    await expect(btns).toHaveCount(3);
    await expect(btns.nth(0)).toContainText("MD");
    await expect(btns.nth(1)).toContainText("TXT");
    await expect(btns.nth(2)).toContainText("IA");
  });

  test("Navbar hamburger menu opens on mobile", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto("/", { waitUntil: "networkidle" });

    const toggle = page.locator("button#menu-toggle");
    await expect(toggle).toBeVisible();

    const items = page.locator("#menu-items");
    await expect(items).not.toHaveClass(/open/);

    await toggle.click();
    await page.waitForTimeout(300);

    await expect(items).toHaveClass(/open/);
  });

  test("Dark mode toggle exists", async ({ page }) => {
    await page.goto("/", { waitUntil: "networkidle" });

    const toggle = page.locator("#theme-toggle");
    await expect(toggle).toBeVisible();
  });

  test("Table of Contents exists on long post", async ({ page }) => {
    await page.goto("/posts/plan_de_verano/", { waitUntil: "networkidle" });

    const toc = page.locator("#toc-container");
    await expect(toc).toBeVisible();
    const links = await toc.locator("a").count();
    expect(links).toBeGreaterThan(5);
  });

  test("Post has a banner image", async ({ page }) => {
    await page.goto("/posts/plan_de_verano/", { waitUntil: "networkidle" });

    // Banner image is in the header area, inside a <picture> element
    const picture = page.locator("header picture, header img").first();
    await expect(picture).toBeVisible();
  });

  test("Weekly Recap page has content", async ({ page }) => {
    await page.goto("/weekly/2026-w26-tech-recap/", { waitUntil: "networkidle" });

    await expect(page.locator("h1")).toBeVisible();
    const text = await page.locator("article").textContent();
    expect(text.length).toBeGreaterThan(100);
  });

  test("Post listing page has cards", async ({ page }) => {
    await page.goto("/posts/1", { waitUntil: "networkidle" });

    // Cards are inside a grid; look for article or section elements with post content
    const articles = page.locator("article");
    const count = await articles.count();
    // The listing page may not use <article> tags; check for any post preview
    const postLinks = page.locator('a[href*="/posts/"]');
    const linkCount = await postLinks.count();
    expect(Math.max(count, linkCount)).toBeGreaterThan(0);
  });
});
