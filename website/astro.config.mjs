import { defineConfig } from "astro/config";
import sitemap from "@astrojs/sitemap";

// OSEL_SITE / OSEL_BASE are set by the Pages workflow (e.g. https://org.github.io + /osel/).
// For a custom domain, OSEL_BASE is "/" (the default).
export default defineConfig({
  site: process.env.OSEL_SITE || "https://osel.example",
  base: process.env.OSEL_BASE || "/",
  integrations: [sitemap()],
  trailingSlash: "ignore",
});
