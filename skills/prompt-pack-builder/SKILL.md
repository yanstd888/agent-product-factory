---
name: prompt-pack-builder
description: Create a structured prompt pack with declared variables and tested examples. Use when a user asks for reusable prompts, a prompt library, or a prompt pack.
license: MIT
---

# Prompt-pack builder

1. Read the requested language pack from `packs/<language>/STYLE.md`.
2. Create `README.md`, `product.json`, and `prompts.json` in one product directory.
3. Use this `prompts.json` shape:

```json
{"prompts":[{"id":"short-name","template":"Write for {{audience}}.","variables":["audience"],"example":{"input":{"audience":"creators"},"output":"Example output."}}]}
```

4. Every declared variable must appear in its template exactly as `{{name}}`; every template variable must be declared.
5. Include one complete input/output example for each prompt.
6. Run the installed `product-qa` skill. Fix blockers before delivery. Retry a failed build or QA run at most three times; then report the blocker and never declare completion.
