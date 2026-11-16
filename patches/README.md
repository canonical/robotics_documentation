# Migration divergence patches

This directory tracks repository-specific divergences from the upstream docs template.

## When to use these patches

Whenever you do an upstream migration or sync (template refresh, stack migration, or baseline sync), apply all patches in this directory after syncing upstream changes.

## How to apply

From the repository root:

```bash
git apply patches/*.patch
```

Apply the patches to the freshly synced upstream files, before you copy the project
settings (names, URLs, link check exceptions) into `docs/conf.py`. The patches were
generated against the Sphinx Stack 3.0 files and are independent of each other.

If a patch no longer applies because upstream changed the surrounding lines, make
the change by hand and regenerate the patch from the resulting diff.

## Tracked divergences

### `0001-reapply-pymarkdown-divergence.patch`

- File: `docs/_dev/.pymarkdown.json`
- Change: enables extra Markdown lint rules, such as the 85-character line length.
- Reason: the project enforces a stricter Markdown style than the template.

### `0002-reapply-redirects-divergence.patch`

- Files: `docs/conf.py`, `docs/requirements.txt`
- Change: keeps `sphinx-reredirects` and the inline `redirects` mapping in place of
  the template's `sphinx-rerediraffe` and `redirects.txt`.
- Reason: the existing redirects predate the template's switch to
  `sphinx-rerediraffe` and haven't been migrated. Moving them to `redirects.txt`
  is a separate change that needs each redirect to be checked.

### `0003-reapply-mermaid-divergence.patch`

- Files: `docs/conf.py`, `docs/requirements.txt`
- Change: adds the `sphinxcontrib-mermaid` extension.
- Reason: some pages contain Mermaid diagrams, and the template doesn't ship
  this extension.
