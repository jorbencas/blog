// remark-reading-time.mjs
import getReadingTime from "reading-time";
import { toString } from "mdast-util-to-string";

export function remarkReadingTime() {
  return function (tree, { data }) {
    const textOnPage = toString(tree);
    const readingTime = getReadingTime(textOnPage);

    // Inicializamos la variable formattedText
    let formattedText;

    // Personalización avanzada para mostrar el tiempo de lectura
    if (readingTime.minutes >= 60) {
      const hours = Math.floor(readingTime.minutes / 60);
      const minutes = readingTime.minutes % 60;
      formattedText = `Aproximadamente ${hours} hora${
        hours > 1 ? "s" : ""
      } y ${minutes} minuto${minutes > 1 ? "s" : ""} de lectura`;
    } else if (readingTime.minutes === 1) {
      formattedText = `Aproximadamente 1 minuto de lectura`; // Singular
    } else if (readingTime.minutes > 1 && readingTime.minutes < 5) {
      formattedText = `Aproximadamente ${readingTime.minutes} minutos de lectura`; // Entre 2 y 4 minutos
    } else if (readingTime.minutes >= 5 && readingTime.minutes < 10) {
      formattedText = `Lectura corta (~${readingTime.minutes} min)`; // Lectura de corta duración
    } else if (readingTime.minutes >= 10 && readingTime.minutes < 20) {
      formattedText = `Lectura media (~${readingTime.minutes} min)`; // Lectura de duración media
    } else {
      formattedText = `Lectura larga (~${readingTime.minutes} min)`; // Lectura larga
    }

    // En caso de ser menos de 1 minuto
    if (readingTime.minutes < 1) {
      formattedText = `Menos de 1 minuto de lectura`;
    }

    // Asignamos el texto personalizado al frontmatter de Astro
    data.astro.frontmatter.minutesRead = formattedText;
  };
}
