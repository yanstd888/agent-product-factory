---
name: ebook-builder
description: Create an EPUB and PDF ebook with working navigation and offline QA evidence. Use when a user asks for an ebook, guide, handbook, or downloadable PDF/EPUB publication.
license: MIT
---

# Ebook builder

1. Read the requested language pack from `packs/<language>/STYLE.md`.
2. Create a product directory containing exactly one `.epub`, one `.pdf`, and `product.json`.
3. Build navigation with a valid EPUB nav document and working internal links.
4. Run `product-qa doctor`; Pandoc and EPUBCheck are required.
5. Run the installed `product-qa` skill. Fix blockers before delivery. Retry a failed build or QA run at most three times; then report the blocker and never declare completion.
