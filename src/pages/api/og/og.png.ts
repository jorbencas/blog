import type { APIRoute } from 'astro';
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import fs from 'fs';
import path from 'path';
import { SITE_NAME } from 'src/consts.js';

export const prerender = false;

const SECTION_STICKERS: Record<string, { header: string; stickers: string[] }> = {
  home:         { header: "Blog",              stickers: ["blog", "code", "github"] },
  blog:         { header: "Blog",              stickers: ["js", "python", "ts"] },
  posts:        { header: "Blog",              stickers: ["js", "python", "ts"] },
  retos:        { header: "Retos",             stickers: ["python", "js", "java", "ts"] },
  proyectos:    { header: "Proyectos",         stickers: ["github", "docker", "ts"] },
  herramientas: { header: "Herramientas",      stickers: ["docker", "nodejs", "python"] },
  weekly:       { header: "Weekly",            stickers: ["rss", "github", "email"] },
  tags:         { header: "Etiquetas",         stickers: ["github", "code", "blog"] },
};

const SECTION_COLORS: Record<string, { from: string; to: string }> = {
  home:         { from: "#075985", to: "#06b6d4" },
  blog:         { from: "#075985", to: "#06b6d4" },
  posts:        { from: "#075985", to: "#06b6d4" },
  retos:        { from: "#b45309", to: "#f59e0b" },
  proyectos:    { from: "#6b21a8", to: "#a855f7" },
  herramientas: { from: "#065f46", to: "#10b981" },
  weekly:       { from: "#075985", to: "#06b6d4" },
  tags:         { from: "#075985", to: "#06b6d4" },
};

const SIZES: Record<string, { width: number; height: number }> = {
  og:     { width: 1200, height: 630 },
  square: { width: 800,  height: 800 },
  small:  { width: 600,  height: 315 },
};

function getSvgAsBase64(tagName: string): string | null {
  try {
    const svgPath = path.join(process.cwd(), `public/icons/${tagName}.svg`);
    if (!fs.existsSync(svgPath)) return null;
    const svgContent = fs.readFileSync(svgPath, 'utf8');
    const base64 = Buffer.from(svgContent).toString('base64');
    return `data:image/svg+xml;base64,${base64}`;
  } catch (e) {
    console.error(`Error al convertir SVG a Base64 para [${tagName}]:`, e);
    return null;
  }
}

function getFaviconAsBase64(): string | null {
  try {
    const faviconPath = path.join(process.cwd(), 'public/favicon-96x96.png');
    if (!fs.existsSync(faviconPath)) return null;
    const fileBuffer = fs.readFileSync(faviconPath);
    const base64 = Buffer.from(fileBuffer).toString('base64');
    return `data:image/png;base64,${base64}`;
  } catch (e) {
    console.error("Error al convertir Favicon a Base64:", e);
    return null;
  }
}

function loadFont(weight: string): Uint8Array | null {
  try {
    const fontPath = path.join(process.cwd(), `public/fonts/static/SpaceGrotesk-${weight}.ttf`);
    if (!fs.existsSync(fontPath)) return null;
    return new Uint8Array(fs.readFileSync(fontPath));
  } catch {
    return null;
  }
}

function getTitleFontSize(title: string): number {
  const len = title.length;
  if (len <= 30) return 52;
  if (len <= 50) return 44;
  if (len <= 80) return 36;
  return 28;
}

function truncate(str: string, max: number): string {
  if (str.length <= max) return str;
  const truncated = str.substring(0, max);
  const lastSpace = truncated.lastIndexOf(" ");
  return `${truncated.substring(0, lastSpace > 0 ? lastSpace : max)}...`;
}

export const GET: APIRoute = async ({ request }) => {
  try {
    const { searchParams } = new URL(request.url);

    const rawTitle = searchParams.get("title")?.trim() || SITE_NAME;
    const title = rawTitle
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/&/g, "&amp;");

    const sectionParam = searchParams.get("section")?.trim()?.toLowerCase() || "";
    const tagsParam = searchParams.get("tags")?.trim() ?? "";
    const descParam = searchParams.get("desc")?.trim() ?? "";
    const sizeParam = (searchParams.get("size")?.trim()?.toLowerCase() || "og") as keyof typeof SIZES;
    const size = SIZES[sizeParam] || SIZES.og;

    let headerText = "jorbencas // blog-jorbencas.vercel.app";
    let tags: string[] = [];

    if (sectionParam && SECTION_STICKERS[sectionParam]) {
      const sec = SECTION_STICKERS[sectionParam];
      headerText = `jorbencas // ${sec.header}`;
      tags = sec.stickers;
    } else {
      tags = tagsParam.length > 0
        ? tagsParam.split(",").filter(Boolean).map((t) => t.trim().toLowerCase())
        : [];
      if (tags.length === 0) tags = ["default"];
    }

    const accent = SECTION_COLORS[sectionParam] || SECTION_COLORS.home;
    const faviconBase64 = getFaviconAsBase64() || "";
    const fontBold = loadFont("Bold");
    const fontRegular = loadFont("Regular");

    const satoriFonts: any[] = [];
    if (fontBold) satoriFonts.push({ name: "Space Grotesk", data: fontBold, weight: 700, style: "normal" });
    if (fontRegular) satoriFonts.push({ name: "Space Grotesk", data: fontRegular, weight: 400, style: "normal" });

    const fontFamily = fontBold ? '"Space Grotesk", sans-serif' : "sans-serif";

    const posiciones = [
      { top: "60px",  right: "220px", rotate: "6deg" },
      { top: "140px", right: "50px",  rotate: "-8deg" },
      { top: "250px", right: "240px", rotate: "-4deg" },
      { top: "330px", right: "70px",  rotate: "10deg" },
      { top: "450px", right: "200px", rotate: "-6deg" },
    ];

    const stickersJSX: any[] = [];
    let stickerCount = 0;

    for (let i = 0; i < tags.length; i++) {
      if (stickerCount >= 5) break;
      const svgBase64 = getSvgAsBase64(tags[i]);
      if (!svgBase64) continue;

      const pos = posiciones[stickerCount];
      stickerCount++;

      stickersJSX.push({
        type: "div",
        props: {
          style: {
            position: "absolute",
            top: pos.top,
            right: pos.right,
            transform: `rotate(${pos.rotate})`,
            display: "flex",
          },
          children: [{
            type: "div",
            props: {
              style: {
                width: "110px",
                height: "110px",
                backgroundColor: "#1E293B",
                border: "1px solid #06b6d4",
                borderRadius: "16px",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                padding: "20px",
              },
              children: {
                type: "img",
                props: {
                  src: svgBase64,
                  style: { width: "64px", height: "64px", objectFit: "contain" },
                },
              },
            },
          }],
        },
      });
    }

    const titleFontSize = getTitleFontSize(title);
    const showTitle = title && title !== SITE_NAME;

    const leftColumnChildren: any[] = [
      {
        type: "div",
        props: {
          style: {
            display: "flex",
            alignItems: "center",
            marginBottom: "32px",
          },
          children: [
            {
              type: "div",
              props: {
                style: {
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  backgroundColor: "#1E293B",
                  border: "1px solid #06b6d4",
                  borderRadius: "14px",
                  width: "54px",
                  height: "54px",
                  padding: "10px",
                  marginRight: "20px",
                },
                children: {
                  type: "img",
                  props: {
                    src: faviconBase64,
                    style: { width: "72px", height: "72px", objectFit: "contain" },
                  },
                },
              },
            },
            {
              type: "span",
              props: {
                style: {
                  fontSize: "15px",
                  fontWeight: 700,
                  color: "#9CA3AF",
                  fontFamily: "monospace",
                  letterSpacing: "2px",
                },
                children: headerText,
              },
            },
          ],
        },
      },
      {
        type: "div",
        props: {
          style: {
            width: "120px",
            height: "3px",
            backgroundImage: `linear-gradient(to right, ${accent.from}, ${accent.to})`,
            borderRadius: "2px",
            marginBottom: showTitle ? "28px" : "0",
          },
        },
      },
    ];

    if (showTitle) {
      leftColumnChildren.push({
        type: "div",
        props: {
          style: {
            fontSize: `${titleFontSize}px`,
            fontWeight: 700,
            color: "#F1F5F9",
            lineHeight: 1.2,
            fontFamily,
            display: "-webkit-box",
            WebkitLineClamp: size.height >= 630 ? 4 : 3,
            WebkitBoxOrient: "vertical",
            overflow: "hidden",
            textOverflow: "ellipsis",
          },
          children: truncate(title, size.height >= 630 ? 180 : 120),
        },
      });
    }

    if (descParam) {
      leftColumnChildren.push({
        type: "div",
        props: {
          style: {
            fontSize: "18px",
            fontWeight: 400,
            color: "#94A3B8",
            fontFamily,
            marginTop: "16px",
            lineHeight: 1.5,
            display: "-webkit-box",
            WebkitLineClamp: 2,
            WebkitBoxOrient: "vertical",
            overflow: "hidden",
            textOverflow: "ellipsis",
            maxWidth: "600px",
          },
          children: truncate(descParam, 120),
        },
      });
    }

    const satoriOptions: any = { width: size.width, height: size.height };
    if (satoriFonts.length > 0) {
      satoriOptions.fonts = satoriFonts;
    }

    const svg = await satori(
      {
        type: "div",
        props: {
          style: {
            width: `${size.width}px`,
            height: `${size.height}px`,
            position: "relative",
            display: "flex",
            flexDirection: "column",
            fontFamily,
            backgroundColor: "#131926",
          },
          children: [
            {
              type: "div",
              props: {
                style: {
                  position: "absolute",
                  top: 0, left: 0, right: 0, bottom: 0,
                  display: "flex",
                  backgroundImage:
                    "linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px)",
                  backgroundSize: "50px 50px",
                },
              },
            },
            {
              type: "div",
              props: {
                style: {
                  position: "absolute",
                  top: size.height >= 630 ? "130px" : "60px",
                  left: size.width >= 800 ? "80px" : "40px",
                  maxWidth: size.width >= 800 ? "640px" : "480px",
                  display: "flex",
                  flexDirection: "column",
                },
                children: leftColumnChildren,
              },
            },
            ...stickersJSX,
          ],
        },
      },
      satoriOptions,
    );

    const resvg = new Resvg(svg);
    const pngData = resvg.render();
    const pngBuffer = pngData.asPng();

    return new Response(new Uint8Array(pngBuffer), {
      status: 200,
      headers: {
        "Content-Type": "image/png",
        "Cache-Control": "public, max-age=31536000, immutable",
      },
    });
  } catch (error) {
    console.error("Error crítico en el generador de imágenes OG:", error);
    return new Response("Error interno al generar la imagen", { status: 500 });
  }
};
