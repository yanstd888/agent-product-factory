---
name: product-qa
description: Validate a local prompt pack, XLSX template, or EPUB/PDF ebook and produce an offline QA report. Use when an agent has created or changed a digital product and must prove it is ready before delivery.
license: MIT
---

# Product QA Gate

1. Run `python scripts/run_qa.py doctor` before XLSX or ebook checks.
2. Run `python scripts/run_qa.py check <product-path> --type prompt-pack|xlsx|ebook --json-out <report-path>`.
3. Keep the report path outside the product path; the command will reject overwrites and report paths inside the product.
4. If blockers exist, fix the product and rerun at most three times.
5. Deliver the product only with a zero-exit QA report. Otherwise name the remaining blockers plainly.

## Result rules

- Exit `0`: no blockers.
- Exit `1`: product or environment blocker.
- Exit `2`: invalid report-output path or report write failure.
- Warnings do not block delivery, but must be included in the handoff.

## Product metadata

Each product directory needs `product.json` with `title`, `author`, `version`, and `license`.
