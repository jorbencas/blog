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
});
