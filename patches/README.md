# Migration divergence patches

This directory tracks repository-specific divergences from the upstream docs template.

## When to use these patches

Whenever you do an upstream migration or sync (template refresh, stack migration, or baseline sync), apply all patches in this directory after syncing upstream changes.

## Rule

After each migration/sync from upstream:

1. Apply all patches in `patches/`.
2. Run checks/lint as usual.
3. Keep these patches up to date when intentional divergences change.

## Current patch set

- `0001-reapply-pymarkdown-divergence.patch`
  - Re-applies project-specific `pymarkdown` rules.
  - Target path: `docs/_dev/.pymarkdown.json`

## How to apply

From the repository root:

```bash
git apply patches/*.patch
```
