import type { APIRoute } from 'astro';
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import fs from 'fs';
import path from 'path';

export const prerender = false;

// Función para transformar los logos a Base64
function getSvgAsBase64(tagName: string): string | null {
  try {
    const svgPath = path.join(process.cwd(), `public/icons/${tagName}.svg`);
    if (!fs.existsSync(svgPath)) return null;
    const svgContent = fs.readFileSync(svgPath, 'utf8');
    const base64 = Buffer.from(svgContent).toString('base64');
    return `data:image/svg+xml;base64,${base64}`;
  } catch (e) {
    console.error(`❌ Error al convertir SVG a Base64 para [${tagName}]:`, e);
    return null;
  }
}

// 🌟 SOLUCIÓN DEFINITIVA PARA EL FAVICON: Carga local instantánea sin peticiones HTTP
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
    const rawTitle = searchParams.get("title")?.trim() || "Problemas de un desarrollador Web";
    const title = rawTitle
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/&/g, "&amp;");
    
    const tagsParam = searchParams.get("tags")?.trim() ?? "";
    let tags = tagsParam.length > 0 
      ? tagsParam.split(",").filter(Boolean).map((t) => t.trim().toLowerCase())
      : [];

    if (tags.length === 0) {
      tags = ["default"]; 
    }

    // 🌟 Obtenemos el favicon en Base64 de forma local y segura
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

    const stickersJSX = [];
    
    // Posiciones asimétricas y desenfadadas que te gustaban
    const posiciones = [
      { top: "60px", right: "220px", rotate: "6deg" },    
      { top: "140px", right: "50px", rotate: "-8deg" },   
      { top: "250px", right: "240px", rotate: "-4deg" },  
      { top: "330px", right: "70px", rotate: "10deg" },   
      { top: "450px", right: "200px", rotate: "-6deg" }   
    ];

    let stickerContador = 0;

    for (let i = 0; i < tags.length; i++) {
      if (stickerContador >= 5) break; 

      const tag = tags[i];
      const svgBase64 = getSvgAsBase64(tag);

      if (!svgBase64) continue;

      const pos = posiciones[stickerContador];
      stickerContador++; 

      stickersJSX.push({
        type: "div",
        props: {
          style: {
            position: "absolute",
            top: pos.top,
            right: pos.right,
            transform: `rotate(${pos.rotate})`, 
            display: "flex"
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
                  padding: "20px"
                },
                children: {
                  type: "img",
                  props: {
                    src: svgBase64,
                    style: {
                      width: "64px",
                      height: "64px",
                      objectFit: "contain"
                    }
                  }
                }
              }
            }
          ]
        }
      });
    }

    const fontSize = title.length > 50 ? "52px" : "66px";

    const satoriOptions: any = {
      width: 1200,
      height: 630,
    };

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
            fontFamily: fontData ? '"Space Grotesk", sans-serif' : 'sans-serif',
            backgroundColor: "#131926" 
          },
          children: [
            // Malla de micro-líneas de fondo
            {
              type: "div",
              props: {
                style: {
                  position: "absolute",
                  top: 0, left: 0, right: 0, bottom: 0,
                  display: "flex",
                  backgroundImage: "linear-gradient(to right, rgba(255, 255, 255, 0.03) 1px, transparent 1px), linear-gradient(to bottom, rgba(255, 255, 255, 0.03) 1px, transparent 1px)",
                  backgroundSize: "50px 50px"
                }
              }
            },

            // Contenedor de contenido principal (Izquierda)
            {
              type: "div",
              props: {
                style: {
                  position: "absolute",
                  top: "130px",
                  left: "80px",
                  maxWidth: "640px", 
                  display: "flex",
                  flexDirection: "column"
                },
                children: [
                  // Cabecera con Favicon
                  {
                    type: "div",
                    props: {
                      style: {
                        display: "flex",
                        alignItems: "center",
                        marginBottom: "32px"
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
                              marginRight: "20px"
                            },
                            children: {
                              type: "img",
                              props: {
                                src: faviconBase64, // 🌟 Usamos la imagen local mapeada en Base64
                                style: {
                                  width: "72px",
                                  height: "72px",
                                  objectFit: "contain"
                                }
                              }
                            }
                          }
                        },
                        {
                          type: "span",
                          props: {
                            style: {
                              fontSize: "15px",
                              fontWeight: 700,
                              color: "#9CA3AF", 
                              fontFamily: "monospace",
                              letterSpacing: "2px"
                            },
                            children: "jorbencas // blog-jorbencas.vercel.app"
                          }
                        }
                      ]
                    }
                  },

                  // Línea de degradado corporativa
                  {
                    type: "div",
                    props: {
                      style: {
                        width: "120px",
                        height: "3px",
                        backgroundImage: "linear-gradient(to right, #075985, #06b6d4)",
                        borderRadius: "2px",
                        marginBottom: "36px"
                      }
                    }
                  },
                ]
              }
            },

            // Renderizado de los stickers asimétricos flotantes
            ...stickersJSX,

            // Branding inferior izquierdo
            {
              type: "div",
              props: {
                style: {
                  position: "absolute",
                  bottom: "48px",
                  left: "80px",
                  display: "flex",
                  alignItems: "center"
                },
                children: [
                  {
                    type: "div",
                    props: {
                      style: {
                        width: "6px",
                        height: "6px",
                        borderRadius: "3px",
                        backgroundImage: "linear-gradient(to right, #075985, #06b6d4)",
                        marginRight: "12px"
                      }
                    }
                  },
                  {
                    type: "span",
                    props: {
                      style: {
                        fontSize: "14px",
                        fontWeight: 700,
                        color: "#9CA3AF",
                        fontFamily: "monospace"
                      },
                      children: "blog-jorbencas.vercel.app"
                    }
                  }
                ]
              }
            }
          ]
        }
      },
      satoriOptions
    );

    const resvg = new Resvg(svg);
    const pngData = resvg.render();
    const pngBuffer = pngData.asPng();

    return new Response(new Uint8Array(pngBuffer), {
      status: 200,
      headers: {
        "Content-Type": "image/png",
        "Cache-Control": "public, max-age=31536000, immutable"
      }
    });
  } catch (error) {
    console.error("❌ Error crítico en el generador de imágenes OG:", error);
    return new Response("Error interno al generar la imagen", { status: 500 });
  }
};