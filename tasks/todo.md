# Digital Product Factory v0.1 tasks

## Phase 1 — shared foundation

- [x] **T1: Bootstrap repository contract and product-qa CLI**
  - Acceptance: package layout, `python -m product_qa --help`, and standard-library test command exist.
  - Verify: `python -m product_qa --help && python -m unittest discover -s tests -v`.
  - Depends on: none.
  - Scope: S.

- [x] **T2: Implement report contract and universal checks**
  - Acceptance: versioned JSON/human report; placeholders and unreadable/missing files are blockers; metadata is warning-only.
  - Verify: focused `unittest` fixtures prove exit `0` and exit `1`.
  - Depends on: T1.
  - Scope: M.

- [x] **T3: Add doctor and external-tool detection**
  - Acceptance: detects Python, Pandoc, EPUBCheck, and LibreOffice without network access; relevant absent tool reports blocker.
  - Verify: fixture/mocked PATH test plus local `doctor` output.
  - Depends on: T1, T2.
  - Scope: S.

## Checkpoint — QA core

- [x] CLI exit and JSON schema are stable.
- [x] Tests pass without network access.

## Phase 2 — product slices

- [x] **T4: Prompt-pack builder, QA, and example**
  - Acceptance: markdown+JSON manifest validates prompt structure, declared variables, and example input/output.
  - Verify: pass fixture, dangling-variable blocker fixture, `examples/prompt-pack` exits `0`.
  - Depends on: T2, T3.
  - Scope: M.

- [x] **T5: XLSX template builder, QA, and example**
  - Verified: example exits `0` after LibreOffice recalculation.
  - Acceptance: structural checks detect instructions/sample-data/input markers; LibreOffice formula errors are blockers.
  - Verify: valid example exits `0` with LibreOffice; unavailable LibreOffice blocks.
  - Depends on: T2, T3.
  - Scope: M.

- [x] **T6: Ebook builder, QA, and example**
  - Verified: example exits `0` after EPUBCheck validation.
  - Acceptance: builds EPUB/PDF; EPUBCheck, table of contents, and internal-link failures are blockers.
  - Verify: valid example exits `0` with Pandoc/EPUBCheck; unavailable required tool blocks.
  - Depends on: T2, T3.
  - Scope: M.

## Checkpoint — product proof

- [x] Every example uses the public QA CLI and has a saved report.
- [x] Required-tool absence never returns success.

## Phase 3 — distribution and release evidence

- [x] **T7: Add language packs and contributor template**
  - Verified: `id`/`en` packs and builder references are present.
  - Acceptance: `id`/`en` packs provide writing/format rules without duplicating executable checks.
  - Verify: both builder skill docs reference selected pack.
  - Depends on: T4–T6.
  - Scope: S.

- [ ] **T8: Package skills and publish docs**
  - Acceptance: skill metadata validates; README/README.id, MIT, SECURITY, CONTRIBUTING, and examples are present.
  - Verify: official skill validator and a clean local install rehearsal.
  - Depends on: T7.
  - Scope: M.

- [ ] **T9: Add CI and release evidence checklist**
  - State: workflow and local CI-equivalent commands are implemented; remote CI awaits T8 publication/install rehearsal.
  - Acceptance: format, skill lint, tests, no-secret/offline checks are automated; release checklist maps to PRD layers 1–6.
  - Verify: CI-equivalent commands pass locally before provider setup.
  - Depends on: T8.
  - Scope: M.
