import { readFileSync, readdirSync, statSync } from "fs";
import { join, extname } from "path";

const CONTENT_DIR = "src/content";

const errors = [];

function lintFile(filePath) {
  const content = readFileSync(filePath, "utf-8");
  const lines = content.split("\n");
  let inCodeBlock = false;
  let codeBlockStart = 0;

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];
    const lineNum = i + 1;

    if (line.match(/^```/)) {
      const hasInfoString = line.match(/^```\w/);
      const shouldToggle = !inCodeBlock || (inCodeBlock && !hasInfoString);
      if (shouldToggle) {
        if (!inCodeBlock) {
          inCodeBlock = true;
          codeBlockStart = lineNum;
        } else {
          inCodeBlock = false;
        }
        continue;
      }
    }

    if (inCodeBlock) continue;

    if (line.match(/^\/\/>/)) {
      errors.push({
        file: filePath,
        line: lineNum,
        message: "JSX tag cerrado con '//' en vez de '/>'. Ejemplo correcto: <Component />",
      });
    }

    if (line.match(/^\/$/) && !line.match(/^(import |export )/)) {
      const prevLine = lines[i - 1] || "";
      if (prevLine.match(/description="/)) {
        errors.push({
          file: filePath,
          line: lineNum,
          message: "Tag JSX sin cerrar. Falta '>' después de '/'. Debería ser: />",
        });
      }
    }

    if (line.match(/<ResourceCard[^/]*$/) && !line.match(/\/>$/) && !line.match(/>$/)) {
      const nextLines = lines.slice(i + 1, i + 5).join(" ");
      if (!nextLines.match(/\/>/) && !nextLines.match(/>/)) {
        errors.push({
          file: filePath,
          line: lineNum,
          message: "Posible <ResourceCard> sin cerrar. Verifica que tenga '/>' al final.",
        });
      }
    }

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
  console.log("✅ MDX syntax OK");
}
