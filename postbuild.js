const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

console.log("--- Listando contenido del directorio raíz ---");
console.log(fs.readdirSync(".")); // Esto nos dirá qué carpetas existen realmente

// Si ves una carpeta como 'output', '.vercel' o similar, la añadiremos a la lista
const possiblePaths = [
  "dist",
  ".vercel/output/static",
  ".vercel/output",
  "build",
];
const foundPath = possiblePaths.find((p) => fs.existsSync(p));

if (foundPath) {
  console.log(`Carpeta encontrada: ${foundPath}. Iniciando Pagefind...`);
  execSync(`npx pagefind --site ${foundPath}`, { stdio: "inherit" });
} else {
  console.error("¡ALERTA! Ninguna de las rutas esperadas existe.");
  process.exit(1);
}
