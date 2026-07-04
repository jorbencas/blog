import type { APIRoute } from 'astro';
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import fs from 'fs';
import path from 'path';
import { SITE_NAME } from 'src/consts.js';

export const prerender = false;

// ── Section → header text + predefined sticker icons ──

const SECTION_STICKERS: Record<string, { header: string; stickers: string[] }> = {
  home:         { header: "Blog",              stickers: ["blog", "code", "github"] },
  blog:         { header: "Blog",              stickers: ["js", "python", "ts"] },
  retos:        { header: "Retos",             stickers: ["python", "js", "java", "ts"] },
  proyectos:    { header: "Proyectos",         stickers: ["github", "docker", "ts"] },
  herramientas: { header: "Herramientas",      stickers: ["docker", "nodejs", "python"] },
  weekly:       { header: "Weekly",            stickers: ["rss", "github", "email"] },
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
    console.error("❌ Error al convertir Favicon a Base64:", e);
    return null;
  }
}

export const GET: APIRoute = async ({ request }) => {
  try {
    const { searchParams } = new URL(request.url);

    // ── Params ──
    const rawTitle = searchParams.get("title")?.trim() || SITE_NAME;
    const title = rawTitle
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/&/g, "&amp;");

    const sectionParam = searchParams.get("section")?.trim()?.toLowerCase() || "";
    const tagsParam = searchParams.get("tags")?.trim() ?? "";

    // ── Resolve section vs tags ──
    let headerText = "jorbencas // blog-jorbencas.vercel.app";
    let tags: string[] = [];

    if (sectionParam && SECTION_STICKERS[sectionParam]) {
      const sec = SECTION_STICKERS[sectionParam];
      headerText = `jorbencas // ${sec.header}`;
      tags = sec.stickers;
    } else {
      // Fallback: use tags param (existing behavior for detail pages)
      tags = tagsParam.length > 0
        ? tagsParam.split(",").filter(Boolean).map((t) => t.trim().toLowerCase())
        : [];
      if (tags.length === 0) tags = ["default"];
    }

    // ── Assets ──
    const faviconBase64 = getFaviconAsBase64() || "";

    let fontData: Uint8Array | null = null;
    try {
      const fontPath = path.join(process.cwd(), "public/fonts/static/SpaceGrotesk-Bold.ttf");
      if (fs.existsSync(fontPath)) {
        const fileBuffer = fs.readFileSync(fontPath);
        fontData = new Uint8Array(fileBuffer);
      }
    } catch (fontError) {
      console.warn("⚠️ No se pudo cargar la fuente personalizada:", fontError);
    }

    // ── Sticker positions (asymmetric floating layout) ──
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
          children: [
            {
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
            },
          ],
        },
      });
    }

    // ── Satori render ──
    const satoriOptions: any = { width: 1200, height: 630 };
    if (fontData) {
      satoriOptions.fonts = [{ name: "Space Grotesk", data: fontData, weight: 700, style: "normal" }];
    }

    const svg = await satori(
      {
        type: "div",
        props: {
          style: {
            width: "1200px",
            height: "630px",
            position: "relative",
            display: "flex",
            flexDirection: "column",
            fontFamily: fontData ? '"Space Grotesk", sans-serif' : "sans-serif",
            backgroundColor: "#131926",
          },
          children: [
            // Background micro-grid
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

            // Left content area
            {
              type: "div",
              props: {
                style: {
                  position: "absolute",
                  top: "130px",
                  left: "80px",
                  maxWidth: "640px",
                  display: "flex",
                  flexDirection: "column",
                },
                children: [
                  // Header: favicon + section text
                  {
                    type: "div",
                    props: {
                      style: {
                        display: "flex",
                        alignItems: "center",
                        marginBottom: "32px",
                      },
                      children: [
                        // Favicon container
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
                        // Section header text
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

                  // Gradient accent line
                  {
                    type: "div",
                    props: {
                      style: {
                        width: "120px",
                        height: "3px",
                        backgroundImage: "linear-gradient(to right, #075985, #06b6d4)",
                        borderRadius: "2px",
                        marginBottom: "36px",
                      },
                    },
                  },
                ],
              },
            },

            // Floating stickers
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
    console.error("❌ Error crítico en el generador de imágenes OG:", error);
    return new Response("Error interno al generar la imagen", { status: 500 });
  }
};
