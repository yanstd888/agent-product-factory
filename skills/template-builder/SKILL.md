---
name: template-builder
description: Create a practical XLSX template with instructions, sample data, and marked input cells. Use when a user asks for a spreadsheet template, calculator, tracker, budget, or planning workbook.
license: MIT
---

# XLSX template builder

1. Read the requested language pack from `packs/<language>/STYLE.md`.
2. Create one `.xlsx` file, `product.json`, an `Instructions` sheet, and sample data.
3. Put input-cell markers in `product.json`, for example `"input_cells": ["Budget!B2"]`.
4. Use formulas that do not leave `#REF!`, `#NAME?`, or `#DIV/0!` errors.
5. Run `product-qa doctor`; LibreOffice is required for formula evaluation.
6. Run the installed `product-qa` skill and fix blockers before delivery. Retry a failed build or QA run at most three times; then report the blocker and never declare completion.
