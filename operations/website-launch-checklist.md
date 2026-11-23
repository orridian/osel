# Website launch checklist

- [ ] Name and domain availability and trademark conflicts checked **before** branding spend (decision log)
- [ ] Domain registered, with adult help if provider terms require it
- [ ] Logo readable at 16px; contrast checked in light and dark themes
- [ ] Only pages with accurate content are launched. Remove or hide any page that would overstate
- [ ] `website/src/site.ts` placeholders replaced (domain, emails, GitHub URLs); `astro.config.mjs` `site` set; `public/robots.txt` sitemap URL updated
- [ ] HTTPS enforced; `www` → apex redirect (or the reverse); old URLs redirected
- [ ] Metadata, canonical URLs, sitemap (`/sitemap-index.xml`), robots rules
- [ ] Keyboard pass: skip link, focus visible, every link and button reachable
- [ ] Mobile layout at 375px: no horizontal scroll
- [ ] Page speed: Lighthouse performance and accessibility ≥ 90
- [ ] Broken links: `npm run check-links` passes; external links spot-checked
- [ ] Forms: none exist. If one is added, update the privacy page **first**
- [ ] Product status and canonical repository links are correct
- [ ] Privacy and security pages match the systems actually in use (host logs, email provider named)
- [ ] Role addresses (hello@, security@, conduct@, privacy@) forward and have been tested
- [ ] Update process agreed: the website is updated in the same PR as any release, policy or status change
