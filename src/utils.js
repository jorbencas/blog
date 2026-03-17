import mounths from "./layouts/months.json";
import days from "./layouts/days.json";

export const formatDatePost = (date) => {
  let fullDate = new Date(date);
  let day = days[fullDate.getDay()];
  let month = mounths[fullDate.getMonth()];
  let year = fullDate.getFullYear();
  let numday = fullDate.getDate();
  return day + ", " + numday + " de " + month + " del " + year;
};

export const getSortedPosts = (allPosts) => {
  return allPosts
    .filter((post) => !post.data.draft)
    .sort((a, b) => {
      let dateA = new Date(a.data.pubDate).getTime();
      let dateB = new Date(b.data.pubDate).getTime();
      // Si la fecha es inválida, getTime() devuelve NaN.
      // Esto asegura que el build no se rompa silenciosamente.
      return dateB - dateA;
    });
};

export const makeUrl = (urlParam, Astro) => {
  let url = urlParam !== undefined ? "" + urlParam : "";
  let site = Astro.request.url.includes("localhost")
    ? Astro.request.url
    : Astro.site;
  return new URL(url, site);
};

export const doSomething = () => {
  console.log("doSomething");
};
