# Release checklist — v0.1 local candidate

## Verified locally

- [ ] `python -m product_qa doctor` exits `0` on the release machine.
- [ ] `examples/prompt-pack` exits `0` and writes a JSON report outside the product directory.
- [ ] `examples/xlsx` exits `0` after LibreOffice recalculation and writes a JSON report outside the product directory.
- [ ] `examples/ebook` exits `0` after EPUBCheck validation and writes a JSON report outside the product directory.
- [ ] `python -m unittest discover -s tests -v` passes.
- [ ] All four skills pass `skills-ref validate`; SKILL lint has no errors.
- [ ] Generated XLSX and EPUB examples are byte-stable across two runs.
- [ ] No secret, network, or destructive runtime dependency was added to `product_qa`.

## External publication gates — intentionally not performed locally

- [ ] Clean-machine install through `npx skills add` completes in under five minutes.
- [ ] Trigger evaluation: 10 positive and 10 negative prompts per skill on two agents reaches at least 90% accuracy.
- [ ] Blind comparison demonstrates the skills improve product output over the no-skill baseline.
- [ ] Three to five beta users complete their intended task; at least three succeed.
- [ ] Final public name availability, repository creation, changelog, and publication are explicitly approved by the owner.

No GitHub, remote repository, or publication action is authorized by this checklist.
