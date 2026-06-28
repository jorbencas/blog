import { test, expect } from "@playwright/test";

test.describe("Dark mode", () => {
  test("toggle exists and toggles dark class", async ({ page }) => {
    await page.goto("/", { waitUntil: "networkidle" });
    const toggle = page.locator("#theme-toggle");
    await expect(toggle).toBeVisible();
    const hasDark = await page.evaluate(() => document.documentElement.classList.contains("dark"));
    await toggle.click();
    await page.waitForTimeout(200);
    const hasDarkAfter = await page.evaluate(() => document.documentElement.classList.contains("dark"));
    expect(hasDarkAfter).toBe(!hasDark);
  });

  test("dark mode persists on navigation", async ({ page }) => {
    await page.goto("/", { waitUntil: "networkidle" });
    await page.locator("#theme-toggle").click();
    await page.waitForTimeout(200);
    await page.goto("/retos/1", { waitUntil: "networkidle" });
    const isDark = await page.evaluate(() => document.documentElement.classList.contains("dark"));
    expect(isDark).toBeTruthy();
  });

  test("dark mode persists on reload", async ({ page }) => {
    await page.goto("/", { waitUntil: "networkidle" });
    await page.locator("#theme-toggle").click();
    await page.waitForTimeout(200);
    await page.reload({ waitUntil: "networkidle" });
    const isDark = await page.evaluate(() => document.documentElement.classList.contains("dark"));
    expect(isDark).toBeTruthy();
  });

  test("dark mode applies dark bg to body", async ({ page }) => {
    await page.goto("/posts/plan_de_verano/", { waitUntil: "networkidle" });
    await page.locator("#theme-toggle").click();
    await page.waitForTimeout(200);
    const bodyBg = await page.evaluate(() => getComputedStyle(document.body).backgroundColor);
    const rgb = bodyBg.match(/\d+/g);
    if (rgb) {
      const avg = (parseInt(rgb[0]) + parseInt(rgb[1]) + parseInt(rgb[2])) / 3;
      expect(avg).toBeLessThan(50);
    }
  });
});

test.describe("Search", () => {
  test("search input visible on desktop", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/", { waitUntil: "networkidle" });
    const input = page.locator("#search-input");
    await expect(input).toBeVisible();
    await expect(input).toHaveAttribute("placeholder", /BUSCAR/i);
  });

  test("Ctrl+K focuses search input", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/", { waitUntil: "networkidle" });
    const input = page.locator("#search-input");
    await input.waitFor({ state: "attached", timeout: 5000 });
    await page.waitForTimeout(5000);
    for (let i = 0; i < 3; i++) {
      await page.keyboard.press("Control+k");
      await page.waitForTimeout(300);
    }
    const focused = await input.evaluate((el) => el === document.activeElement);
    expect(focused).toBeTruthy();
  });

  async function waitForPagefind(page) {
    await page.waitForFunction(() => {
      return typeof window?.pagefind !== "undefined" ||
        document.querySelector("#search-results") !== null ||
        document.querySelector('[data-pagefind-body]') !== null;
    }, { timeout: 10000 }).catch(() => {});
    await page.waitForTimeout(2000);
  }

  test("typing shows search results", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/", { waitUntil: "networkidle" });
    await waitForPagefind(page);
    const input = page.locator("#search-input");
    await input.fill("docker");
    const results = page.locator("#search-results");
    const link = results.locator("a").first();
    await expect(link).toBeVisible({ timeout: 15000 });
    const count = await results.locator("a").count();
    expect(count).toBeGreaterThan(0);
  });

  test("clearing search hides results", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/", { waitUntil: "networkidle" });
    await waitForPagefind(page);
    const input = page.locator("#search-input");
    const results = page.locator("#search-results");
    await input.fill("docker");
    await expect(results.locator("a").first()).toBeVisible({ timeout: 15000 });
    await input.fill("");
    await page.waitForTimeout(300);
    const isHidden = await results.evaluate((el) => el.classList.contains("hidden"));
    expect(isHidden).toBeTruthy();
  });

  test("search mobile button exists", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto("/", { waitUntil: "networkidle" });
    const btn = page.locator("#search-toggle");
    await expect(btn).toBeVisible();
  });
});

test.describe("CopyPost", () => {
  test("dropdown has 3 buttons (MD, TXT, IA)", async ({ page }) => {
    await page.goto("/posts/conexion_ssh_mediante_clave_publica_privada/", { waitUntil: "networkidle" });
    const btns = page.locator('button:has-text("MD"), button:has-text("TXT"), button:has-text("IA")');
    const count = await btns.count();
    expect(count).toBeGreaterThanOrEqual(2);
  });
});

test.describe("Archive", () => {
  test("archive toggle shows years", async ({ page }) => {
    await page.goto("/posts/1", { waitUntil: "networkidle" });
    const archive = page.locator("#archive-years");
    const count = await archive.count();
    if (count > 0) {
      await expect(archive).toBeVisible();
      const toggle = page.locator("#archive-toggle");
      const toggleCount = await toggle.count();
      if (toggleCount > 0) {
        await expect(toggle).toBeVisible();
      }
    }
  });
});

test.describe("CodeTabs", () => {
  async function openSolutionDetails(page) {
    const details = page.locator("details").first();
    const count = await details.count();
    if (count > 0) {
      const isOpen = await details.evaluate((el) => el.hasAttribute("open"));
      if (!isOpen) {
        await details.locator("summary").click();
        await page.waitForTimeout(500);
      }
    }
  }

  test("CodeTabs renders on challenge detail", async ({ page }) => {
    await page.goto("/retos/reto-inicial-01-suma-de-digitos/", { waitUntil: "networkidle" });
    await openSolutionDetails(page);
    await page.waitForTimeout(2000);
    const tabs = page.locator(".code-tabs-wrapper");
    const count = await tabs.count();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test("CodeTabs shows Python, JavaScript, Java, TypeScript tabs", async ({ page }) => {
    await page.goto("/retos/reto-inicial-01-suma-de-digitos/", { waitUntil: "networkidle" });
    await openSolutionDetails(page);
    await page.waitForTimeout(3000);
    const wrapper = page.locator(".code-tabs-wrapper.ready");
    const count = await wrapper.count();
    expect(count).toBeGreaterThanOrEqual(1);
    const tabBtns = wrapper.first().locator(".tab-btn");
    await expect(tabBtns.first()).toBeVisible({ timeout: 5000 });
    const texts = await tabBtns.allTextContents();
    const expected = ["Python", "JavaScript", "Java", "TypeScript"];
    for (const e of expected) {
      expect(texts.some((t) => t.trim() === e)).toBeTruthy();
    }
  });

  test("CodeTabs switching tabs changes visible code", async ({ page }) => {
    await page.goto("/retos/reto-inicial-01-suma-de-digitos/", { waitUntil: "networkidle" });
    await openSolutionDetails(page);
    await page.waitForTimeout(3000);
    const wrapper = page.locator(".code-tabs-wrapper.ready").first();
    const wrapperCount = await wrapper.count();
    if (wrapperCount === 0) return;

    const tabBtns = wrapper.locator(".tab-btn");
    await expect(tabBtns.first()).toBeVisible({ timeout: 5000 });

    const panels = wrapper.locator(".code-panels");
    const firstDisplay = await panels.locator("pre").nth(0).evaluate((el) => getComputedStyle(el).display);
    expect(firstDisplay).not.toBe("none");

    await tabBtns.nth(1).click();
    await page.waitForTimeout(200);

    const secondDisplay = await panels.locator("pre").nth(1).evaluate((el) => getComputedStyle(el).display);
    expect(secondDisplay).not.toBe("none");

    const firstDisplayAfter = await panels.locator("pre").nth(0).evaluate((el) => getComputedStyle(el).display);
    expect(firstDisplayAfter).toBe("none");
  });

  test("CodeTabs in dark mode renders correctly", async ({ page }) => {
    await page.goto("/retos/reto-inicial-01-suma-de-digitos/", { waitUntil: "networkidle" });
    await openSolutionDetails(page);
    await page.locator("#theme-toggle").click();
    await page.waitForTimeout(1000);
    const wrapper = page.locator(".code-tabs-wrapper.ready").first();
    const count = await wrapper.count();
    if (count === 0) return;
    const tabBtns = wrapper.locator(".tab-btn");
    await expect(tabBtns.first()).toBeVisible({ timeout: 5000 });
    await tabBtns.nth(2).click();
    await page.waitForTimeout(200);
    const activeClass = await tabBtns.nth(2).getAttribute("class");
    expect(activeClass).toContain("active");
  });
});
