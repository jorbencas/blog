const { execSync } = require("child_process");
const fs = require("fs");
const path = require("path");

function findDir(dir) {
  if (!fs.existsSync(dir)) return null;
  const files = fs.readdirSync(dir, { withFileTypes: true });
  for (const file of files) {
    if (file.isDirectory()) {
      // Buscamos carpetas que suelen contener los HTML finales
      if (
        file.name === "dist" ||
        file.name === "static" ||
        file.name === "out"
      ) {
        return path.join(dir, file.name);
      }
      // Evitamos entrar en node_modules o carpetas ocultas para ser más rápidos
      if (file.name === "node_modules" || file.name.startsWith(".")) continue;

      const found = findDir(path.join(dir, file.name));
      if (found) return found;
    }
  }
  return null;
}

console.log("--- Buscando carpeta de salida automáticamente ---");
const foundPath = findDir(".");

if (foundPath) {
  console.log(`¡Encontrado! Carpeta: ${foundPath}. Iniciando Pagefind...`);
  execSync(`npx pagefind --site ${foundPath}`, { stdio: "inherit" });
} else {
  console.error(
    "--- ERROR: No se encontró ninguna carpeta de salida con HTML ---"
  );
  console.error("Contenido del directorio actual:", fs.readdirSync("."));
  process.exit(1);
}
