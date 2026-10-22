# Agent Product Factory

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Offline QA](https://img.shields.io/badge/QA_Engine-100%25_Deterministic-success.svg)](#deterministic-offline-qa-gates)
[![No AI Slop](https://img.shields.io/badge/Quality-Zero_Slop_Guarantee-emerald.svg)](#why-agent-product-factory)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **Autonomous AI Agent Skills to generate, verify, and package commercial digital products (financial spreadsheets, verified EPUB/PDF ebooks, and prompt packs) with zero-tolerance offline QA gates.**

---

## ⚡ Why Agent Product Factory?

Large language models can write text and draft tables, but 95% of AI-generated digital products sold today are **broken slop**:
- Excel sheets with hidden `#VALUE!`, `#REF!`, or `#DIV/0!` errors.
- Unfilled placeholders like `{{company_name}}` or `[INSERT_PRICE_HERE]`.
- EPUB and PDF files with broken internal anchor links, missing metadata, or unstyled walls of text.

**Agent Product Factory fixes this.** It pairs AI generation skills with an **unforgiving, deterministic offline QA engine**. If a single formula breaks or a hyperlink fails, the build **exits code 1** and blocks the release.

---

## 🧩 The 4 Agent Skills

Compatible with [Hermes Agent](https://hermes-agent.nousresearch.com/), Claude Code, Codex, and any Agent Skills-compliant runtime.

| Skill | Directory | Primary Role | Output Formats |
| :--- | :--- | :--- | :--- |
| **`product-qa`** | `skills/product-qa/` | Universal deterministic QA scanner & gatekeeper | Versioned JSON reports |
| **`template-builder`** | `skills/template-builder/` | Financial models, calculators, and operating systems | Multi-sheet `.xlsx` |
| **`ebook-builder`** | `skills/ebook-builder/` | Longform playbooks, SOPs, and technical guides | Standard `.epub` & `.pdf` |
| **`prompt-pack-builder`** | `skills/prompt-pack-builder/` | Structured prompt playbooks with strict schemas | Validated `prompts.json` |

---

## 📦 Showcase Product: Clothing Brand Starter Kit v1.0

Included out-of-the-box as a complete commercial showcase (`products/`):

1. **Financial & Production Operating System (`.xlsx`)**:
   - **5 Sheets**: `Instructions` (SOP & Glossary), `Dashboard` (6 KPI cards + 4-scenario stress test), `HPP_Calculator` (5 real garment archetypes), `Batch_Planner` (330-piece drop simulation & BEP analysis), and `Vendor_Database` (fabric, CMT, print, and trims catalog).
   - Recalculated and verified headless via LibreOffice Calc engine.
2. **Editorial Blueprint Guidebook (`.pdf` & `.epub`)**:
   - 18 pages covering brand archetypes, fabric grammage encyclopedia (Combed 16s/24s/30s, Fleece 330 gsm, Canvas), tech-packs, screenprint chemistry (Plastisol vs Discharge), unboxing trims, 10-point QC SOP table, and the 4-week Drop Launch strategy.
   - Validated against official **W3C EPUBCheck 5.4.0** (0 errors, 0 warnings).
3. **Fashion Brand AI Prompt Playbook (`.json` + `.md`)**:
   - 6 structured marketing prompts with declared variables and runnable examples.

---

## 🛡️ Deterministic Offline QA Gates

The factory operates **100% offline without network calls or external API dependencies**:

```
[Agent Generation]
        │
        ▼
[Product Directory] ──► [Universal File & Path Check] (Symlink / UTF BOM / Hidden file rejection)
        │
        ├──► [Placeholder Scanner] (Blocks {{...}}, [TBD], <insert_...>, lorem ipsum)
        ├──► [XLSX Formula Engine] (Headless Calc recalculation + regex #VALUE!, #REF!, #DIV/0!)
        ├──► [EPUB Validation Engine] (W3C EPUBCheck + all XHTML internal hyperlink resolution)
        └──► [PDF Inspection Engine] (Minimum byte budget + layout render integrity)
        │
        ▼
[Exit Code 0: Certified Pass] OR [Exit Code 1: Hard Blocker]
```

---

## 🚀 Quickstart

### 1. Check System Dependencies
```bash
python -m product_qa doctor
```
Checks for local runtimes: Python 3.10+, Pandoc, LibreOffice (`soffice`), and Java/EPUBCheck.

### 2. Run Test Suite
```bash
python -m unittest discover -s tests -v
```
All 24 unit and regression tests pass deterministically.

### 3. Run QA on Any Product
```bash
# Validate a spreadsheet product
python -m product_qa check products/kalkulator-hpp-clothing --type xlsx --json-out reports/xlsx-report.json

# Validate an ebook product
python -m product_qa check products/ebook-clothing-brand --type ebook --json-out reports/ebook-report.json

# Validate a prompt pack
python -m product_qa check products/prompts-fashion-brand --type prompt-pack --json-out reports/prompts-report.json
```

---

## 🔒 Security & Safe Defaults

- **Zero Network Ingestion**: No outbound telemetry, analytics, or network calls during QA verification.
- **No In-Tree Contamination**: QA reports are strictly forbidden from writing inside product target folders.
- **Symlink Jail**: Refuses to follow symlinks to protect host filesystem boundaries.
- **Secret & API Key Immune**: Zero persistent credentials required.

---

## 📄 License

- **Engine & Skills**: [MIT License](LICENSE)
- **Sample & Product Content**: CC0-1.0 (Public Domain Dedication)

