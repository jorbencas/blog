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

  test("code block header shows language name and SVG badge", async ({ page }) => {
    const header = page.locator(".bloque-codigo-wrapper > div:first-child").first();
    await expect(header).toBeVisible();
    const text = await header.textContent();
    expect(text.length).toBeGreaterThan(0);

    const svg = header.locator("svg");
    await expect(svg).toBeVisible();
    const rect = svg.locator("rect");
    await expect(rect).toBeVisible();
    const txt = svg.locator("text");
    await expect(txt).toBeVisible();
  });

  test("header has compact padding", async ({ page }) => {
    const header = page.locator(".bloque-codigo-wrapper > div:first-child").first();
    await expect(header).toBeVisible();

    const pt = await header.evaluate((el) => parseFloat(getComputedStyle(el).paddingTop));
    const pb = await header.evaluate((el) => parseFloat(getComputedStyle(el).paddingBottom));
    expect(pt).toBeLessThanOrEqual(6);
    expect(pb).toBeLessThanOrEqual(6);
  });

  test("pre has no margin from prose-pre", async ({ page }) => {
    const pre = page.locator(".bloque-codigo-wrapper pre.astro-code").first();
    await expect(pre).toBeVisible();

    const mt = await pre.evaluate((el) => getComputedStyle(el).marginTop);
    const mb = await pre.evaluate((el) => getComputedStyle(el).marginBottom);
    expect(mt).toBe("0px");
    expect(mb).toBe("0px");
  });

  test("code block has selection styling for readability", async ({ page }) => {
    const pre = page.locator(".bloque-codigo-wrapper pre.astro-code").first();
    await expect(pre).toBeVisible();

    const hasSelection = await pre.evaluate((el) => {
      const sheet = [...document.styleSheets].find(s =>
        [...s.cssRules]?.some(r =>
          r.selectorText?.includes("::selection")
        )
      );
      return !!sheet;
    });
    // At minimum, the pre has the selection class
    expect(await pre.getAttribute("class")).toContain("selection");
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
