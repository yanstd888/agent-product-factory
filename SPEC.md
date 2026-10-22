# Spec: Digital Product Factory v0.1

Status: approved baseline · 2026-10-20

## Objective

Provide installable Agent Skills that let an AI agent create a prompt pack, XLSX template, or EPUB/PDF ebook, then prove the resulting product passes an offline QA gate before the agent calls it complete.

Success means a clean machine can install the skills, create each example product, and receive a deterministic QA JSON report plus readable summary. Exit code `0` means no blockers; `1` means at least one blocker.

## v0.1 decisions

- Working repository name: `digital-product-factory`; final public-name availability is a release prerequisite.
- Python 3.10+ is the only required runtime. Core product-qa checks use the standard library.
- Prompt-pack QA is fully implemented by the repository.
- XLSX formula evaluation requires local LibreOffice; ebook builds/validation require local Pandoc and EPUBCheck. `doctor` reports availability. Required-tool absence blocks the relevant product QA.
- Supported template format is XLSX only.
- DOCX, `--live`, MCP, Notion, Google Sheets, and any default network access are out of scope.

## Commands

```text
python -m product_qa check <product-path> --type prompt-pack|xlsx|ebook --json-out <path>
python -m product_qa doctor
python -m unittest discover -s tests -v
```

The final package command and `npx skills add` metadata are defined by the distribution module after the repository satisfies Agent Skills validation.

## Project structure

```text
skills/                  installable Agent Skills
  product-qa/
  ebook-builder/
  prompt-pack-builder/
  template-builder/
packs/id/ packs/en/      locale-only guidance
product_qa/              Python CLI and checks
tests/                   standard-library functional tests
examples/                one passing product per type
tasks/                   approved implementation plan and checklist
```

## Code style

- Python standard library first; no dependency without explicit approval.
- Validate at the CLI/file boundary; checks return structured findings instead of raising user-facing tracebacks.
- One report schema owned by `product-qa`; builders invoke it rather than copying checks.
- Non-trivial branches, parsers, and report aggregation receive one small `unittest` regression check.
- Deliberate ceilings use a `# ponytail:` comment with an upgrade path.

```python
finding = Finding("placeholder", "blocker", "Found '{{title}}' in README.md")
return Report([finding]).exit_code
```

## Testing strategy

- `unittest` only for v0.1.
- Fixture products cover passing and blocker cases for placeholders, prompt variables/examples, workbook instructions/sample data, and missing external tools.
- Each product example runs through the CLI and exits `0`.
- Skill format validation and existing SKILL.md linting run in CI once the chosen tools are pinned.

## Boundaries

- Always: deterministic offline checks; JSON + human output; no hidden network access; preserve user files; verify every example through the same public CLI.
- Ask first: add a Python dependency; add/alter CI provider; change product report schema; enable network or `--live`; add formats or product types.
- Never: claim success after a blocker; silently skip missing validation tooling; store API keys; include copyrighted/unattributed example assets; commit or push without explicit user request.

## Success criteria

1. Four installable skills exist: `product-qa`, `ebook-builder`, `prompt-pack-builder`, `template-builder`.
2. QA emits versioned JSON and readable output; `0` has no blockers and `1` has one or more.
3. Each builder requires QA before declaring its product complete and retries at most three times.
4. `id` and `en` packs are isolated from executable checks.
5. Three examples pass their applicable QA gates on a prepared local environment.
6. Core checks run without network access and give the same report for the same input.
7. Project docs, security policy, MIT license, and CI complete the release checklist.

## Open release questions

- Final public repository/package name after GitHub, npm, and PyPI checks.
- License label for generated example products (proposed: CC0-1.0 for text/data authored in-repo, with no third-party assets).
- Creator-owned promotion channels for the launch plan.
