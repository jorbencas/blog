import { test, expect } from "@playwright/test";

test.describe("CodeEnhancer", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto("/posts/n8n/", { waitUntil: "networkidle" });
    await page.waitForSelector(".bloque-codigo-wrapper", { timeout: 10000 });
  });

  test("code block pre has transparent background (removes Shiki theme bg)", async ({ page }) => {
    const pre = page.locator(".bloque-codigo-wrapper pre.astro-code").first();
    await expect(pre).toBeVisible();

    const bg = await pre.evaluate((el) => getComputedStyle(el).backgroundColor);
    expect(["rgba(0, 0, 0, 0)", "transparent"]).toContain(bg);
  });

  test("code block wrapper provides rounded corners, not the pre", async ({ page }) => {
    const pre = page.locator(".bloque-codigo-wrapper pre.astro-code").first();
    await expect(pre).toBeVisible();

    const borderRadius = await pre.evaluate((el) => getComputedStyle(el).borderRadius);
    expect(borderRadius).toBe("0px");
  });

  test("code block header shows language name", async ({ page }) => {
    const header = page.locator(".bloque-codigo-wrapper > div:first-child").first();
    await expect(header).toBeVisible();
    const text = await header.textContent();
    expect(text.length).toBeGreaterThan(0);
  });

  test("pre has no margin from prose-pre", async ({ page }) => {
    const pre = page.locator(".bloque-codigo-wrapper pre.astro-code").first();
    await expect(pre).toBeVisible();

    const mt = await pre.evaluate((el) => getComputedStyle(el).marginTop);
    const mb = await pre.evaluate((el) => getComputedStyle(el).marginBottom);
    expect(mt).toBe("0px");
    expect(mb).toBe("0px");
  });

  test("pre has no padding from astro-code global style", async ({ page }) => {
    const pre = page.locator(".bloque-codigo-wrapper pre.astro-code").first();
    await expect(pre).toBeVisible();

    const pt = await pre.evaluate((el) => getComputedStyle(el).paddingTop);
    const pb = await pre.evaluate((el) => getComputedStyle(el).paddingBottom);
    expect(pt).toBe("0px");
    expect(pb).toBe("0px");
  });
});
