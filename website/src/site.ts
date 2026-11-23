// Single place for every value that must be filled in before launch.
// Role-based addresses only — never personal contact details.
export const site = {
  name: "Open Source Engineering Lab",
  short: "OSEL",
  tagline: "Reliable, reproducible tools for developers and researchers.",
  github: "https://github.com/[osel-org]",
  repo: "https://github.com/[osel-org]/osel",
  // The docs site is built into /docs/ of this website (see .github/workflows/pages.yml).
  docs: "/docs/",
  email: {
    hello: "hello@[osel-domain]",
    security: "security@[osel-domain]",
    conduct: "conduct@[osel-domain]",
    privacy: "privacy@[osel-domain]",
  },
  status: "alpha",
  version: "0.1.0.dev0",
  lastUpdated: "11 November 2026",
};

/** Prefix an internal path with the deploy base (e.g. "/osel/" on GitHub Pages). Idempotent. */
export function url(path: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, "");
  if (!path.startsWith("/") || (base && path.startsWith(base + "/"))) return path;
  return base + path;
}

export const nav = [
  { href: "/docs/", label: "Docs" },
  { href: "/projects", label: "Projects" },
  { href: "/roadmap", label: "Roadmap" },
  { href: "/community", label: "Community" },
  { href: "/blog", label: "Blog" },
  { href: "/about", label: "About" },
];
