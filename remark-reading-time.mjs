// remark-reading-time.mjs
import getReadingTime from "reading-time";
import { toString } from "mdast-util-to-string";

export function remarkReadingTime() {
  return function (tree, { data }) {
    const textOnPage = toString(tree);
    const readingTime = getReadingTime(textOnPage);
    const minutes = Math.ceil(readingTime.minutes);
    const formattedText = `${minutes} minuto${minutes === 1 ? '' : 's'} de lectura`;
    data.astro.frontmatter.minutesRead = formattedText;
  };
}
