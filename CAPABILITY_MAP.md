# Capability Map: Digital Product Factory

Status: approved baseline · 2026-10-20

| Module ID | Responsibility | Depends on |
|---|---|---|
| `product-qa` | Deterministic offline QA CLI, JSON/human reports, exit status | — |
| `language-packs` | `id`/`en` language policy and product metadata conventions | — |
| `prompt-pack` | Build and validate prompt packs | `product-qa`, `language-packs` |
| `spreadsheet-template` | Build XLSX templates and run local spreadsheet QA | `product-qa`, `language-packs` |
| `ebook` | Build EPUB/PDF ebooks and run local ebook QA | `product-qa`, `language-packs` |
| `distribution` | Skill packaging, examples, CI, docs, install flow | all modules |

Build order: `product-qa` + `language-packs` → `prompt-pack` → `spreadsheet-template` → `ebook` → `distribution`.

## Boundaries

- `product-qa` owns report schema and blocker semantics. Builders call it; they do not duplicate validation rules.
- `language-packs` contains locale guidance only. It has no executable product logic.
- Spreadsheet and ebook adapters may require locally installed tools. A missing required tool is a blocker, never a silent skip.
- `--live`, DOCX, MCP, network calls, and remote API keys are outside v0.1.
