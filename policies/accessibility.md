# Accessibility policy

**Owner:** Founder · **Review:** every website release · **Channel:** issue labelled `accessibility` or `orridian.contact@gmail.com` · **Enforcement:** accessibility regressions are treated as bugs and block a website release.

- **Target:** WCAG 2.2 AA for the website and docs.
- **Keyboard:** every interactive element is reachable and usable by keyboard, with a visible focus indicator and a skip link.
- **Contrast:** text meets 4.5:1 (3:1 for large text) in both light and dark themes.
- **Structure:** one `h1` per page, logical heading order, landmarks, and descriptive link text.
- **Media:** images have alt text. Videos have captions or transcripts where feasible.
- **Docs and examples:** short, copy-pasteable, readable code examples. Meaning is never conveyed by colour alone in CLI output (status words accompany colours).
- **Testing:** keyboard pass and an automated check before each website release ([website checklist](../operations/website-launch-checklist.md)).
