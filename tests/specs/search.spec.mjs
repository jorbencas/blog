import { test, expect } from "@playwright/test";

test.describe("Pagefind search", () => {
  test("Search input is present and interactive", async ({ page }) => {
    await page.goto("/", { waitUntil: "networkidle" });

    const input = page.locator("#search-input");
    await expect(input).toBeVisible();
    await expect(input).toHaveAttribute("placeholder", /BUSCAR/i);

    const results = page.locator("#search-results");
    await expect(results).toHaveCount(1);
  });

  test("Search returns results after typing a query", async ({ page }) => {
    await page.goto("/", { waitUntil: "networkidle" });

    await page.waitForTimeout(3000);

    const input = page.locator("#search-input");
    await input.fill("docker");

    const resultLink = page.locator("#search-results a").first();
    await expect(resultLink).toBeVisible({ timeout: 15000 });

    const count = await page.locator("#search-results a").count();
    expect(count).toBeGreaterThan(0);
  });

  test("Search hides results when input is cleared", async ({ page }) => {
    await page.goto("/", { waitUntil: "networkidle" });

    await page.waitForTimeout(3000);

    const input = page.locator("#search-input");
    const results = page.locator("#search-results");

    await input.fill("docker");
    await expect(results.locator("a").first()).toBeVisible({ timeout: 15000 });

    await input.fill("");
    await expect(results).toHaveClass(/hidden/);
  });

  test("Ctrl+K focuses the search input", async ({ page }) => {
    await page.goto("/", { waitUntil: "networkidle" });

    await page.waitForTimeout(2000);

    await page.keyboard.press("Control+k");

    const input = page.locator("#search-input");
    await expect(input).toBeFocused();
  });
});
