import type { APIRoute } from 'astro';
import satori from 'satori';
import { Resvg } from '@resvg/resvg-js';
import fs from 'fs';
import path from 'path';

export const prerender = false; // Se ejecuta en el servidor bajo demanda

export const GET: APIRoute = async ({ request }) => {
  try {
    // 1. Extraer título y tags de la URL
    const { searchParams } = new URL(request.url);
    const title = searchParams.get('title') ?? 'Problemas de un desarrollador Web';
    const tagsParam = searchParams.get('tags') ?? '';
    const tags = tagsParam.split(',').filter(Boolean).map(t => t.trim().toLowerCase());

    // 2. Cargar la fuente tipográfica (.woff) obligatoria para Satori
    const fontPath = path.join(process.cwd(), 'public/fonts/space-grotesk-bold.woff');
    const fontData = fs.readFileSync(fontPath).buffer as ArrayBuffer;

    // 3. 🌟 MAGIA: Cargar los archivos SVG de los logos locales dinámicamente
    // Buscaremos en tu carpeta public/logos/ nombres como php.svg, astro.svg, etc.
    const stickersJSX = [];
    
    // Coordenadas fijas en el lienzo para que los stickers queden flotando con estilo de "colage"
    const posiciones = [
      { top: '90px', right: '120px', rotate: '6deg' },   // Sticker 1 (Arriba)
      { top: '330px', right: '240px', rotate: '-8deg' }, // Sticker 2 (Centro-Izquierda)
      { top: '280px', right: '50px', rotate: '12deg' }    // Sticker 3 (Abajo-Derecha)
    ];

    for (let i = 0; i < Math.min(tags.length, 3); i++) {
      const tag = tags[i];
      const svgPath = path.join(process.cwd(), `public/logos/${tag}.svg`);
      
      if (fs.existsSync(svgPath)) {
        let svgContent = fs.readFileSync(svgPath, 'utf8');
        
        // Limpieza rápida del SVG para que Satori lo procese sin romper las dimensiones
        svgContent = svgContent
          .replace(/<svg[^>]*>/, '<svg width="110" height="110" viewBox="0 0 128 128" fill="none">')
          .replace(/<\?xml.*\?>/g, '');

        const pos = posiciones[i];

        // Construimos la estructura del Sticker Neobrutalista (Contenedor + Sombra + SVG)
        stickersJSX.push({
          type: 'div',
          props: {
            style: {
              position: 'absolute',
              top: pos.top,
              right: pos.right,
              transform: `rotate(${pos.rotate})`,
              display: 'flex',
            },
            children: [
              // Capa de Sombra Sólida Negra (Detrás)
              {
                type: 'div',
                props: {
                  style: {
                    position: 'absolute',
                    top: '8px',
                    left: '8px',
                    width: '150px',
                    height: '150px',
                    backgroundColor: '#1a1a1a',
                    borderRadius: '8px',
                  }
                }
              },
              // Capa de la Tarjeta Blanca del Sticker (Delante)
              {
                type: 'div',
                props: {
                  style: {
                    position: 'relative',
                    width: '150px',
                    height: '150px',
                    backgroundColor: '#FFFFFF',
                    border: '4px solid #1a1a1a',
                    borderRadius: '8px',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    padding: '16px',
                  },
                  // Inyectamos el código SVG en bruto dentro de las propiedades de Satori
                  children: {
                    type: 'div',
                    props: {
                      style: { display: 'flex' },
                      dangerouslySetInnerHTML: { __html: svgContent }
                    }
                  }
                }
              }
            ]
          }
        });
      }
    }

    // 4. Calcular tamaño de fuente adaptativo para el título
    const fontSize = title.length > 50 ? '54px' : '68px';

    // 5. Estructura Completa del Lienzo Abstrato Open Graph (1200x630)
    const svg = await satori(
      {
        type: 'div',
        props: {
          style: {
            width: '1200px',
            height: '630px',
            position: 'relative',
            display: 'flex',
            flexDirection: 'column',
            fontFamily: '"Space Grotesk", sans-serif',
            backgroundColor: '#FAFAFA', // Fondo Gris Neobrutalista muy claro
          },
          children: [
            // 📐 FONDO: Cuadrícula Técnica de Ingeniería (Grid CSS simulado)
            {
              type: 'div',
              props: {
                style: {
                  position: 'absolute',
                  top: 0, left: 0, right: 0, bottom: 0,
                  display: 'flex',
                  flexWrap: 'wrap',
                  backgroundImage: 'linear-gradient(to right, #EEEEEE 1px, transparent 1px), linear-gradient(to bottom, #EEEEEE 1px, transparent 1px)',
                  backgroundSize: '40px 40px',
                }
              }
            },
            
            // 📝 ÁREA DEL TEXTO (Izquierda)
            {
              type: 'div',
              props: {
                style: {
                  position: 'absolute',
                  top: '140px',
                  left: '72px',
                  maxWidth: '640px',
                  display: 'flex',
                  flexDirection: 'column',
                },
                children: [
                  // Barra de acento Amarilla
                  {
                    type: 'div',
                    props: {
                      style: {
                        width: '64px',
                        height: '12px',
                        background: '#FFCC00',
                        border: '3px solid #1a1a1a',
                        marginBottom: '28px',
                      }
                    }
                  },
                  // Título principal
                  {
                    type: 'div',
                    props: {
                      style: {
                        fontSize,
                        fontWeight: 700,
                        color: '#1a1a1a',
                        lineHeight: 1.15,
                        letterSpacing: '-1.5px',
                      },
                      children: title
                    }
                  }
                ]
              }
            },

            // 🌟 INYECCIÓN DE LOS STICKERS COMPILADOS ARRIBA
            ...stickersJSX,

            // 🏷️ BRANDING: Botón Neobrutalista Inferior Derecho (Tu Dominio)
            {
              type: 'div',
              props: {
                style: {
                  position: 'absolute',
                  bottom: '48px',
                  right: '56px',
                  background: '#FFCC00',
                  border: '3px solid #1a1a1a',
                  borderRadius: '4px',
                  padding: '10px 20px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  boxShadow: '5px 5px 0px #1a1a1a'
                },
                children: {
                  type: 'span',
                  props: {
                    style: {
                      fontSize: '16px',
                      fontWeight: 700,
                      color: '#1a1a1a',
                      fontFamily: 'monospace'
                    },
                    children: 'blog-jorbencas.vercel.app'
                  }
                }
              }
            }
          ]
        }
      },
      {
        width: 1200,
        height: 630,
        fonts: [{ name: 'Space Grotesk', data: fontData, weight: 700, style: 'normal' }],
      }
    );

    // 6. Transformar el SVG a un buffer binario PNG usando resvg
    const resvg = new Resvg(svg);
    const pngData = resvg.render();
    const pngBuffer = pngData.asPng();

    // 7. Enviar la imagen resultante con caché optimizada para Redes Sociales
    return new Response(pngBuffer, {
      status: 200,
      headers: {
        'Content-Type': 'image/png',
        'Cache-Control': 'public, max-age=31536000, immutable'
      },
    });

  } catch (error) {
    console.error('❌ Error en el generador de imágenes OG:', error);
    return new Response('Error interno al generar la imagen', { status: 500 });
  }
};