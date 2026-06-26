import { createStaticServer } from "./server.mjs";

const PORT = parseInt(process.argv[2] || "3457", 10);
const DIST = new URL("../../dist/client", import.meta.url).pathname;

const server = createStaticServer(DIST, PORT);
await server.start();
console.log(`Server running on ${server.url}`);

// Keep running until killed
process.on("SIGINT", async () => {
  await server.stop();
  process.exit(0);
});
process.on("SIGTERM", async () => {
  await server.stop();
  process.exit(0);
});
