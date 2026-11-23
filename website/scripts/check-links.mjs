// Checks that every internal link (href/src) in the built site (dist/) points to an existing file.
// Honors the deploy base path (OSEL_BASE, e.g. "/osel/"): an absolute link that ignores the base
// would 404 on GitHub Pages, so it is reported as broken.
import { readdirSync, readFileSync, statSync, existsSync } from "node:fs";
import { join, dirname, posix } from "node:path";

const dist = new URL("../dist/", import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, "$1");
const base = ("/" + (process.env.OSEL_BASE || "/").replace(/^\/+|\/+$/g, "") + "/").replace("//", "/");

const files = [];
(function walk(dir) {
  for (const name of readdirSync(dir)) {
    const p = join(dir, name);
    statSync(p).isDirectory() ? walk(p) : p.endsWith(".html") && files.push(p);
  }
})(dist);

const existsInDist = (rel) => {
  const clean = decodeURIComponent(rel.split("#")[0].split("?")[0]).replace(/^\/+/, "");
  if (clean === "") return existsSync(join(dist, "index.html"));
  const p = join(dist, clean);
  return existsSync(p) || existsSync(join(p, "index.html")) || existsSync(p + ".html");
};

let broken = 0;
let checked = 0;
for (const file of files) {
  const html = readFileSync(file, "utf8");
  // Directory of this page as a URL path relative to the site root.
  const pageDir = dirname(file).slice(dist.length).split(/[\\/]/).filter(Boolean).join("/");
  for (const [, href] of html.matchAll(/(?:href|src)="([^"]+)"/g)) {
    if (/^(https?:|mailto:|data:|javascript:|#)/.test(href)) continue;
    checked++;
    let rel;
    if (href.startsWith("/")) {
      if (!href.startsWith(base) && href + "/" !== base) {
        console.log(`BROKEN (ignores base ${base}) ${file.slice(dist.length)} -> ${href}`);
        broken++;
        continue;
      }
      rel = href.slice(base.length);
    } else {
      rel = posix.normalize(posix.join(pageDir, href.split("#")[0]));
    }
    if (!existsInDist(rel)) {
      console.log(`BROKEN ${file.slice(dist.length)} -> ${href}`);
      broken++;
    }
  }
}
console.log(`${files.length} pages, ${checked} internal links checked (base ${base}), ${broken} broken`);
process.exit(broken ? 1 : 0);
