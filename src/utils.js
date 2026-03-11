import mounths from "./layouts/months.json";
import days from "./layouts/days.json";
import { init } from "@pagefind/core";

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
    .filter((post) => !post.frontmatter.draft)
    .sort(
      (a, b) =>
        new Date(b.frontmatter.pubDate).valueOf() -
        new Date(a.frontmatter.pubDate).valueOf()
    );
};

export const makeUrl = (urlParam, Astro) => {
  let url = urlParam !== undefined ? "" + urlParam : "";
  let site = Astro.request.url.includes("localhost")
    ? Astro.request.url
    : Astro.site;
  return new URL(url, site);
};

const search = init({
  input: "#search-input",
  results: "#search-results",
  render: (results) => {
    const container = document.querySelector("#search-results");
    container.innerHTML = ""; // limpiar resultados
    if (results.length === 0) {
      container.innerHTML =
        '<p class="p-4 text-gray-500">No se encontraron resultados</p>';
    } else {
      results.forEach((item) => {
        const div = document.createElement("div");
        div.className =
          "p-4 border-b last:border-b-0 hover:bg-indigo-50 cursor-pointer transition";
        div.innerHTML = `
          <a href="${item.url}" class="block">
            <h3 class="font-semibold text-indigo-700 mb-1">${item.title}</h3>
            <p class="text-gray-600 text-sm">${item.snippet}</p>
          </a>
        `;
        container.appendChild(div);
      });
    }
    container.classList.toggle("hidden", results.length === 0);
  },
});

export const doSomething = () => {
  console.log("doSomething");
};
