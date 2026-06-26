import { test, expect } from "@playwright/test";

const PAGES = [
  { path: "/", name: "homepage", maxDiffPixelRatio: 0.12 },
  { path: "/posts/conexion_ssh_mediante_clave_publica_privada/", name: "post-ssh" },
  { path: "/posts/plan_de_verano/", name: "post-plan-verano" },
  { path: "/posts/linea_temporal_blog/", name: "post-timeline" },
  { path: "/proyectos/1", name: "proyectos" },
  { path: "/retos/1", name: "retos" },
  { path: "/herramientas/1", name: "herramientas-list" },
  { path: "/herramientas/extractor-frames/", name: "herramientas-extractor" },
  { path: "/404.html", name: "404" },
];

test.describe("Visual regression", () => {
  for (const pageConfig of PAGES) {
    const { path, name } = pageConfig;
    test(`Screenshot: ${name}`, async ({ page }) => {
      await page.goto(path, { waitUntil: "networkidle" });
      await page.waitForTimeout(2000);

      await expect(page).toHaveScreenshot(`${name}.png`, {
        fullPage: true,
        maxDiffPixelRatio: pageConfig.maxDiffPixelRatio || 0.05,
        animations: "disabled",
      });
    });
  }
});
