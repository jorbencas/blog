const { execSync } = require("child_process");
const fs = require("fs");

console.log("--- Iniciando proceso de búsqueda de archivos ---");

// Vercel suele usar esta ruta cuando el adaptador está activo
const paths = [".vercel/output/static", "dist"];
let foundPath = paths.find((p) => fs.existsSync(p));

if (foundPath) {
  console.log(`Carpeta encontrada: ${foundPath}. Iniciando Pagefind...`);
  execSync(`npx pagefind --site ${foundPath}`, { stdio: "inherit" });
} else {
  console.error(
    "Error: No se encontró la carpeta de salida (dist o .vercel/output/static)"
  );
  process.exit(1);
}
