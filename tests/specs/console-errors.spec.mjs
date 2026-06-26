import { test, expect } from "@playwright/test";

const PAGES = [
  "/",
  "/posts/conexion_ssh_mediante_clave_publica_privada/",
  "/posts/plan_de_verano/",
  "/posts/linea_temporal_blog/",
  "/posts/guia-0-100-python/",
  "/proyectos/1",
  "/retos/1",
  "/herramientas/1",
  "/herramientas/extractor-frames/",
  "/tags/web/1",
  "/weekly/2026-w26-tech-recap/",
];

test.describe("Console errors on key pages", () => {
  for (const url of PAGES) {
    test(`No JS errors: ${url}`, async ({ page }) => {
      const jsErrors = [];
      page.on("console", (msg) => {
        if (msg.type() === "error") {
          const text = msg.text();
          if (text.includes("robots.txt")) return;
          if (text.includes("favicon")) return;
          if (text.includes("ERR_SOCKET_NOT_CONNECTED")) return;
          if (text.includes("Failed to load resource")) return;
          jsErrors.push(text);
        }
      });
      page.on("pageerror", (err) => {
        jsErrors.push(err.message);
      });

      await page.goto(url, { waitUntil: "networkidle" });
      await page.waitForTimeout(500);

      expect(jsErrors, `JS errors on ${url}`).toEqual([]);
    });
  }
});
