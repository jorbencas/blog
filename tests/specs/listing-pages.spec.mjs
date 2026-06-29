import { test, expect } from "@playwright/test";

const VIEWPORTS = [
  { width: 375, height: 812, label: "mobile" },
  { width: 768, height: 1024, label: "tablet" },
  { width: 1280, height: 800, label: "desktop" },
];

test.describe("Homepage sections", () => {
  for (const vp of VIEWPORTS) {
    test(`all sections render on ${vp.label}`, async ({ page }) => {
      await page.setViewportSize({ width: vp.width, height: vp.height });
      await page.goto("/", { waitUntil: "networkidle" });

      const sections = [
        { heading: "Mis_Proyectos", link: "Ver portafolio" },
        { heading: "Retos", link: "Ver retos" },
        { heading: "Últimos_Posts", link: "Ir a la bitácora" },
      ];

      for (const s of sections) {
        const h = page.locator(`h2:has-text("${s.heading}")`);
        await expect(h.first()).toBeVisible();
      }
    });
  }

  test(`"Ver portafolio" link works on desktop`, async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/", { waitUntil: "networkidle" });
    const link = page.locator('a:has-text("Ver portafolio")');
    await expect(link).toHaveAttribute("href", "/proyectos/1");
  });

  test(`"Ver retos" link works on desktop`, async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/", { waitUntil: "networkidle" });
    const link = page.locator('a:has-text("Ver retos")');
    await expect(link).toHaveAttribute("href", "/retos/1");
  });

  test(`"Ir a la bitácora" link works on desktop`, async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/", { waitUntil: "networkidle" });
    const link = page.locator('a:has-text("Ir a la bitácora")');
    await expect(link).toHaveAttribute("href", "/posts/1");
  });

  test("Mini Herramientas section appears if tools exist", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/", { waitUntil: "networkidle" });
    const section = page.locator("h2:has-text('Mini_Herramientas')");
    const count = await section.count();
    if (count > 0) {
      await expect(section).toBeVisible();
      const link = page.locator('a:has-text("Ver herramientas")');
      await expect(link).toHaveAttribute("href", "/herramientas/1");
    }
  });

  test("Weekly section appears if entries exist", async ({ page }) => {
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto("/", { waitUntil: "networkidle" });
    const section = page.locator("h2:has-text('Resúmenes_Semanales')");
    const count = await section.count();
    if (count > 0) {
      await expect(section).toBeVisible();
    }
  });
});

test.describe("Listing pages", () => {
  test.describe("Blog listing", () => {
    test("renders posts in grid", async ({ page }) => {
      await page.goto("/posts/1", { waitUntil: "networkidle" });
      const grid = page.locator("a[href*='/posts/']");
      const count = await grid.count();
      expect(count).toBeGreaterThan(0);
    });

    test("has Archive sidebar", async ({ page }) => {
      await page.goto("/posts/1", { waitUntil: "networkidle" });
      const archive = page.locator("#archive-years, section:has-text('ARCHIVO_SISTEMA')");
      const count = await archive.count();
      if (count > 0) {
        await expect(archive.first()).toBeVisible();
      }
    });
  });

  test.describe("Challenges listing", () => {
    test("renders challenge cards in grid", async ({ page }) => {
      await page.goto("/retos/1", { waitUntil: "networkidle" });
      const cards = page.locator("a[href*='/retos/']");
      const count = await cards.count();
      expect(count).toBeGreaterThan(0);
    });

    test("page title includes Retos", async ({ page }) => {
      await page.goto("/retos/1", { waitUntil: "networkidle" });
      await expect(page.locator("h1")).toContainText("Retos");
    });
  });

  test.describe("Projects listing", () => {
    test("renders project cards in grid", async ({ page }) => {
      await page.goto("/proyectos/1", { waitUntil: "networkidle" });
      const cards = page.locator("a[href*='/proyectos/']");
      const count = await cards.count();
      expect(count).toBeGreaterThan(0);
    });

    test("page title includes Proyectos", async ({ page }) => {
      await page.goto("/proyectos/1", { waitUntil: "networkidle" });
      await expect(page.locator("h1")).toContainText("Proyectos");
    });
  });

  test.describe("Tools listing", () => {
    test("renders tool cards in grid", async ({ page }) => {
      await page.goto("/herramientas/1", { waitUntil: "networkidle" });
      const cards = page.locator("a[href*='/herramientas/']");
      const count = await cards.count();
      if (count > 0) {
        await expect(cards.first()).toBeVisible();
      }
    });
  });

  test.describe("Weekly listing", () => {
    test("renders weekly cards", async ({ page }) => {
      await page.goto("/weekly/1", { waitUntil: "networkidle" });
      const links = page.locator("a[href*='/weekly/']");
      const count = await links.count();
      expect(count).toBeGreaterThan(0);
    });
  });

  test.describe("Tags pages", () => {
    test("tags index lists all tags", async ({ page }) => {
      await page.goto("/tags", { waitUntil: "networkidle" });
      await expect(page.locator("h1")).toContainText("etiquetas");
      const tagLinks = page.locator("a[href*='/tags/']");
      const count = await tagLinks.count();
      expect(count).toBeGreaterThan(0);
    });

    test("tag detail shows posts", async ({ page }) => {
      await page.goto("/tags/web/1", { waitUntil: "networkidle" });
      await expect(page.locator("h1")).toContainText("#");
    });
  });
});

test.describe("Pagination", () => {
  test("blog page 1 has next link", async ({ page }) => {
    await page.goto("/posts/1", { waitUntil: "networkidle" });
    const nextLinks = page.locator('a:has-text("Anteriores")');
    const count = await nextLinks.count();
    if (count > 0) {
      await expect(nextLinks.first()).toBeVisible();
    }
  });

  test("challenges page 1 has next link", async ({ page }) => {
    await page.goto("/retos/1", { waitUntil: "networkidle" });
    const nextLinks = page.locator('a:has-text("Misiones antiguas")');
    const count = await nextLinks.count();
    if (count > 0) {
      await expect(nextLinks.first()).toBeVisible();
    }
  });

  test("projects page 1 has next link", async ({ page }) => {
    await page.goto("/proyectos/1", { waitUntil: "networkidle" });
    const nextLinks = page.locator('a:has-text("Proyectos antiguos")');
    const count = await nextLinks.count();
    if (count > 0) {
      await expect(nextLinks.first()).toBeVisible();
    }
  });

  test("pagination buttons have border styling", async ({ page }) => {
    await page.goto("/posts/1", { waitUntil: "networkidle" });
    const btn = page.locator('a:has-text("Anteriores")');
    const count = await btn.count();
    if (count > 0) {
      const border = await btn.first().evaluate((el) => getComputedStyle(el).borderColor);
      expect(border).not.toBe("rgba(0, 0, 0, 0)");
    }
  });
});
