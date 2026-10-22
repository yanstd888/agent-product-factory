# Contributing

1. Keep v0.1 scope to prompt packs, XLSX templates, and EPUB/PDF ebooks.
2. Do not add a runtime dependency or network call without an issue and maintainer approval.
3. Run `python -m unittest discover -s tests -v` before opening a pull request.
4. Add or update a passing example for every product-QA behavior change.

## Add a language pack

1. Copy `packs/en/STYLE.md` to `packs/<language>/STYLE.md`.
2. State dates, currency, terminology, and writing style.
3. Do not copy executable checks into a language pack.

## Add a skill

- Directory name, frontmatter `name`, and skill identifier must match.
- Use lowercase letters, digits, and hyphens only.
- Keep `SKILL.md` below 500 lines and make its description say both what it does and when to use it.
