import { createServer } from "node:http";
import { readFileSync, statSync } from "node:fs";
import { join, extname } from "node:path";

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".js": "application/javascript",
  ".css": "text/css",
  ".webp": "image/webp",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".json": "application/json",
  ".xml": "application/xml",
  ".woff2": "font/woff2",
  ".woff": "font/woff",
  ".ico": "image/x-icon",
};

export function createStaticServer(distDir, port) {
  const server = createServer((req, res) => {
    let path = req.url.split("?")[0];
    if (path === "/") path = "/index.html";

    const send = (filePath) => {
      const content = readFileSync(filePath);
      res.writeHead(200, {
        "Content-Type": MIME[extname(filePath)] || "application/octet-stream",
      });
      res.end(content);
    };

    const filePath = join(distDir, path);
    try {
      statSync(filePath);
      send(filePath);
    } catch {
      // Try with index.html (directory route)
      const alt = join(filePath, "index.html");
      try {
        statSync(alt);
        send(alt);
      } catch {
        res.writeHead(404);
        res.end("Not found");
      }
    }
  });

  const start = () =>
    new Promise((resolve) => server.listen(port, resolve));
  const stop = () =>
    new Promise((resolve) => server.close(resolve));

  return { server, start, stop, url: `http://localhost:${port}` };
}
