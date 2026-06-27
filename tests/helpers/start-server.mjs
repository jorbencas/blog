import { createStaticServer } from "./server.mjs";
import { fileURLToPath } from "node:url";

const PORT = parseInt(process.argv[2] || "3457", 10);
const DIST = fileURLToPath(new URL("../../dist/client", import.meta.url));

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
