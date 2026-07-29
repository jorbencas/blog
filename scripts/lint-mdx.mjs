import { readFileSync, readdirSync, statSync, writeFileSync } from "fs";
import { join, extname } from "path";

const CONTENT_DIR = "src/content";
const FIX_MODE = process.argv.includes("--fix");

const errors = [];
let totalFixed = 0;

function lintFile(filePath) {
  let content = readFileSync(filePath, "utf-8");
  let lines = content.split("\n");
  let fixed = 0;
  let inCodeBlock = false;
  let codeBlockStart = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNum = i + 1;

    if (line.match(/^`{3,}/)) {
      const hasInfoString = line.match(/^`{3,}\s*\S/);
      if (!inCodeBlock) {
        inCodeBlock = true;
        codeBlockStart = lineNum;
      } else if (!hasInfoString) {
        inCodeBlock = false;
      }
      continue;
    }

    if (inCodeBlock) continue;

    // Fix: //> → />
    if (line.match(/^\/\/>/)) {
      if (FIX_MODE) {
        lines[i] = line.replace(/^\/\//, "");
        fixed++;
      } else {
        errors.push({
          file: filePath,
          line: lineNum,
          message: "JSX tag cerrado con '//' en vez de '/>'. Ejemplo correcto: <Component />",
        });
      }
    }

    // Fix: missing > after / in tags like description="
    if (line.match(/^\s*\/[ \t]*$/) && !line.match(/^(import |export )/)) {
      const prevLine = lines[i - 1] || "";
      if (prevLine.match(/description="/)) {
        if (FIX_MODE) {
          lines[i] = "/>";
          fixed++;
        } else {
          errors.push({
            file: filePath,
            line: lineNum,
            message: "Tag JSX sin cerrar. Falta '>' después de '/'. Debería ser: />",
          });
        }
      }
    }

    // Fix: unclosed <ResourceCard> with only / on last line → add />
    if (line.match(/<ResourceCard\s*$/) && !inCodeBlock) {
      const nextLine = lines[i + 1]?.trim();
      if (nextLine === "/" || nextLine === "") {
        if (FIX_MODE) {
          if (nextLine === "/") {
            lines[i + 1] = " />";
          }
          fixed++;
        } else {
          errors.push({
            file: filePath,
            line: lineNum,
            message: "Posible <ResourceCard> sin cerrar. Verifica que tenga '/>' al final.",
          });
        }
      }
    }

    // Check for unclosed tags (report only, too complex to auto-fix)
    const openTagMatch = line.match(/^<(\w+)/);
    if (openTagMatch && !line.match(/\/>$/) && !line.match(/>/) && !openTagMatch[1].match(/^(import|export)$/)) {
      const tagName = openTagMatch[1];
      let found = false;
      for (let j = i + 1; j < Math.min(i + 10, lines.length); j++) {
        if (lines[j].match(new RegExp(`</${tagName}>`)) || lines[j].match(new RegExp(`<${tagName}[^>]*>`))) {
          found = true;
          break;
        }
        if (lines[j].match(/\/>/)) {
          found = true;
          break;
        }
      }
      if (!found) {
        errors.push({
          file: filePath,
          line: lineNum,
          message: `Posible tag <${tagName}> sin cerrar.`,
        });
      }
    }
  }

  if (inCodeBlock) {
    errors.push({
      file: filePath,
      line: codeBlockStart,
      message: "Code block sin cerrar (``` sin pareja).",
    });
  }

  const categoryOpens = (content.match(/<ResourceCategory[\s>]/g) || []).length;
  const categoryCloses = (content.match(/<\/ResourceCategory>/g) || []).length;
  if (categoryOpens !== categoryCloses) {
    errors.push({
      file: filePath,
      line: 0,
      message: `<ResourceCategory> desbalanceado: ${categoryOpens} aperturas, ${categoryCloses} cierres.`,
    });
  }

  if (FIX_MODE && fixed > 0) {
    writeFileSync(filePath, lines.join("\n"));
    totalFixed += fixed;
    console.log(`  🔧 ${filePath}: ${fixed} fix(es) aplicado(s)`);
  }
}

function walkDir(dir) {
  for (const entry of readdirSync(dir)) {
    const full = join(dir, entry);
    if (statSync(full).isDirectory()) {
      walkDir(full);
    } else if (extname(full) === ".mdx") {
      lintFile(full);
    }
  }
}

walkDir(CONTENT_DIR);

if (errors.length > 0) {
  console.error(`\n❌ ${errors.length} error(es) de sintaxis MDX:\n`);
  for (const err of errors) {
    const loc = err.line > 0 ? `:${err.line}` : "";
    console.error(`  ${err.file}${loc} — ${err.message}`);
  }
  process.exit(1);
} else {
  if (FIX_MODE && totalFixed > 0) {
    console.log(`\n✅ ${totalFixed} fix(es) aplicado(s)`);
  } else {
    console.log("✅ MDX syntax OK");
  }
}
