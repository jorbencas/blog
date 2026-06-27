import { defineConfig } from "@playwright/test";

export default defineConfig({
  testDir: "./tests/specs",
  timeout: 30000,
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  workers: 1,
  reporter: [["list"], ["html", { outputFolder: "tests/report" }]],
  use: {
    baseURL: "http://localhost:3457",
    trace: "on-first-retry",
    screenshot: "only-on-failure",
  },
  webServer: {
    command: "node tests/helpers/start-server.mjs 3457",
    port: 3457,
    reuseExistingServer: false,
    timeout: 10000,
  },
});
