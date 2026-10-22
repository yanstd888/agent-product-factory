# Implementation Plan: Digital Product Factory v0.1

Status: local product implementation complete through T7; all three examples pass real QA locally; T8/T9 remain publication/release-evidence gates · 2026-10-20

## Approach

Build the shared QA contract first. Then add each product type as a thin vertical slice that produces a real example and verifies it through the public CLI. Keep external validators as explicitly detected local prerequisites rather than adding network or opaque dependencies.

## Architecture decisions

- Python standard library core: smallest portable path for deterministic file inspection and CLI exit codes.
- Versioned QA JSON schema: builders, CI, and future MCP integrations consume one contract.
- External tools are adapters: `doctor` discovers them; missing required tools yield explicit blocker findings.
- Language packs are markdown/data only: product logic stays centralized and locale contributions do not alter safety semantics.

## Task list

### Phase 1 — shared foundation

1. Repository contract and Python CLI skeleton.
2. QA report schema, universal file/placeholder/metadata checks, JSON and human renderers.
3. `doctor` and external-tool adapter contract.

### Checkpoint — QA core

- Public CLI returns documented exit codes.
- Deterministic fixtures prove a passing report and a blocker report.

### Phase 2 — product slices

4. Prompt-pack builder and prompt-pack QA; passing example.
5. XLSX template builder and structural XLSX QA; passing example on LibreOffice-equipped environment.
6. Ebook builder and EPUB/PDF QA; passing example on Pandoc/EPUBCheck-equipped environment.

### Checkpoint — product proof

- Three examples run through the same CLI and exit `0`.
- Missing prerequisite tools produce blockers, not false passes.

### Phase 3 — distribution and release gate

7. `id` and `en` packs plus contributor template.
8. Installable skill metadata, README files, license, security policy, and contribution docs.
9. CI: Agent Skills validation, SKILL lint, unit/functional tests, and offline/no-secret checks.
10. Release evidence: clean-install rehearsal, trigger set, comparative QA run, and beta checklist.

### Checkpoint — release candidate

- PRD layers 1–6 have reproducible evidence.
- No blocker remains in examples or security checks.

## Risks and mitigations

| Risk | Mitigation |
|---|---|
| Spreadsheet formulas cannot be evaluated by Python stdlib | Require LibreOffice for formula-evaluation QA; block when unavailable. |
| Ebook validation depends on local tooling | `doctor` names the missing tool and check; builder never declares completion without it. |
| Install command differs between agent clients | Validate package layout against the official Agent Skills tooling before documenting the one-liner. |
| Scope creep into publishing/live models | Keep every non-v0.1 feature outside task list. |

## Explicitly deferred

DOCX, `--live`, MCP, Notion, Google Sheets, external source verification automation, and marketplace/distribution beyond the skill package.
