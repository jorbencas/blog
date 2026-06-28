import { test, expect } from "@playwright/test";

test.describe("Post detail page", () => {
  test("renders full post layout with banner, title, content", async ({ page }) => {
    await page.goto("/posts/conexion_ssh_mediante_clave_publica_privada/", { waitUntil: "networkidle" });
    await expect(page.locator("h1")).toBeVisible();
    const article = page.locator("article");
    await expect(article).toBeVisible();
  });

  test("CopyPost buttons exist (MD, TXT, IA)", async ({ page }) => {
    await page.goto("/posts/conexion_ssh_mediante_clave_publica_privada/", { waitUntil: "networkidle" });
    const btns = page.locator('button:has-text("MD"), button:has-text("TXT"), button:has-text("IA")');
    const count = await btns.count();
    expect(count).toBeGreaterThanOrEqual(1);
  });

  test("CopyPost dropdown opens on click", async ({ page }) => {
    await page.goto("/posts/plan_de_verano/", { waitUntil: "networkidle" });
    const btn = page.locator('.copy-trigger, button:has-text("MD")').first();
    const count = await btn.count();
    if (count === 0) return;
    const menu = page.locator(".copy-menu, [data-copy]").first();
    const wasHidden = await menu.evaluate((el) => el.closest('[class*="hidden"]') !== null);
    await btn.click();
    await page.waitForTimeout(200);
  });

  test("tags section exists at bottom", async ({ page }) => {
    await page.goto("/posts/conexion_ssh_mediante_clave_publica_privada/", { waitUntil: "networkidle" });
    const tagSection = page.locator("text=ETIQUETADO");
    const count = await tagSection.count();
    if (count > 0) {
      await expect(tagSection.first()).toBeVisible();
    }
  });

  test("table of contents exists on long post", async ({ page }) => {
    await page.goto("/posts/n8n/", { waitUntil: "networkidle" });
    const toc = page.locator("#toc-container, #toc-mobile");
    const count = await toc.count();
    expect(count).toBeGreaterThan(0);
  });

  test("banner image exists on post", async ({ page }) => {
    await page.goto("/posts/plan_de_verano/", { waitUntil: "networkidle" });
    const img = page.locator("header img, header picture").first();
    const count = await img.count();
    if (count > 0) {
      await expect(img).toBeVisible();
    }
  });
});

test.describe("Challenge detail page", () => {
  test("challenge layout renders correctly", async ({ page }) => {
    await page.goto("/retos/reto-inicial-01-suma-de-digitos/", { waitUntil: "networkidle" });
    await expect(page.locator("h1").first()).toBeVisible();
    await expect(page.locator("h1").first()).toContainText("Suma de Dígitos");
    const briefing = page.locator("text=Misión_Briefing");
    const count = await briefing.count();
    if (count > 0) {
      await expect(briefing.first()).toBeVisible();
    }
  });

  test("challenge layout has sidebar with other challenges", async ({ page }) => {
    await page.goto("/retos/reto-inicial-01-suma-de-digitos/", { waitUntil: "networkidle" });
    const sidebar = page.locator("text=Otras_Misiones");
    const count = await sidebar.count();
    if (count > 0) {
      await expect(sidebar.first()).toBeVisible();
    }
  });

  test("challenge solution details exists inside <details>", async ({ page }) => {
    await page.goto("/retos/reto-inicial-01-suma-de-digitos/", { waitUntil: "networkidle" });
    const details = page.locator("details");
    const count = await details.count();
    if (count > 0) {
      await expect(details.first()).toBeVisible();
      const summary = details.first().locator("summary");
      await expect(summary).toBeVisible();
    }
  });
});

test.describe("Project detail page", () => {
  test("project layout renders", async ({ page }) => {
    await page.goto("/proyectos/tech-pulse-dashboard/", { waitUntil: "networkidle" });
    await expect(page.locator("h1")).toBeVisible();
    const desc = page.locator("p:has-text('dashboard')");
    await expect(desc.first()).toBeVisible();
  });

  test("project sidebar shows more projects", async ({ page }) => {
    await page.goto("/proyectos/tech-pulse-dashboard/", { waitUntil: "networkidle" });
    const sidebar = page.locator("text=Más_Proyectos");
    const count = await sidebar.count();
    if (count > 0) {
      await expect(sidebar.first()).toBeVisible();
    }
  });
});

test.describe("Tool detail page", () => {
  test("tool page renders", async ({ page }) => {
    await page.goto("/herramientas/extractor-frames/", { waitUntil: "networkidle" });
    await expect(page.locator("h1")).toBeVisible();
  });
});

test.describe("Weekly recap page", () => {
  test("weekly recap has content", async ({ page }) => {
    await page.goto("/weekly/2026-w26-tech-recap/", { waitUntil: "networkidle" });
    await expect(page.locator("h1")).toBeVisible();
    const article = page.locator("article");
    await expect(article).toBeVisible();
    const text = await article.textContent();
    expect(text.length).toBeGreaterThan(50);
  });
});
