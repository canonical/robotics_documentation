# Documentation migration skill

## Purpose

Use this skill when migrating a documentation repository to a newer upstream template/version while preserving project-specific behavior.

This skill is intentionally **migration-focused**.

## Source of truth and upgrade origin

- Target documentation repository: https://github.com/canonical/robotics_documentation
- Upstream template to migrate from: https://github.com/canonical/sphinx-stack

**Rule:** run documentation-template upgrades from `canonical/sphinx-stack` as the upstream source of truth (not from ad-hoc local copies).

---

## When to use

- Upgrading to a new docs template release (for example a Sphinx stack update)
- Re-syncing repository files with upstream template state
- Recovering project-specific config lost during a template sync
- Splitting migration work into follow-up PRs (workflow fix, CI fix, policy fix)

---

## Core principles

1. **Template parity first**
   - Keep template-owned files identical to upstream unless a divergence is explicitly approved.

2. **Local policy survives upgrades**
   - Repository-specific rules must live outside template-owned files where possible.

3. **Small scoped PRs**
   - Keep migration, CI fixes, and unrelated cleanup in separate PRs.

4. **No assumed completion**
   - Validate locally and watch CI to terminal state before declaring done.

---

## Recommended migration workflow

### 1) Prepare clean branch

- Start from the requested base branch (usually `main`).
- Use a fresh worktree/branch for each migration scope.

### 2) Sync template files

- Copy/update template-owned files from `https://github.com/canonical/sphinx-stack` upstream.
- Avoid opportunistic formatting or refactors in those files.

### 3) Re-apply approved project divergences

- Re-introduce only intentional, documented differences.
- Keep each divergence explicit and easy to review.

### 4) Run local validation

Typical docs checks:

```bash
make clean-doc
make lint-md
make html
```

### 5) Open PR and monitor CI

- Open a focused PR with a clear scope statement.
- Watch checks/runs until final state (pass/fail/skipped as expected).
- Fix failures or report external blockers clearly.

---

## Pattern: track intentional divergence with `patches/`

When this repository intentionally diverges from upstream template files, record the divergence in a dedicated patch note so future migrations can reapply it safely.

### Recommended approach

1. Keep template-owned files as close to upstream as possible during the migration.
2. For each intentional local deviation, add a concise note in `patches/` that includes:
   - file path(s)
   - reason for divergence
   - minimal diff or exact change summary
   - reapply instructions for next migration
3. During template upgrades, review `patches/` first to identify candidate divergences.
4. Apply `patches/` changes **only at the very end of the migration and only after explicit user approval**.

This prevents accidental loss of project policy, avoids undocumented drift, and keeps review focused on template parity before local divergences are reintroduced.

## Pattern: handle any intentional divergence from template files

Use this pattern for **any** file that intentionally differs from the upstream template.

1. Keep upstream template-owned files unchanged by default.
2. If a local divergence is required, isolate it in a project-owned layer when practical (override file, merge step, wrapper, or post-sync patch).
3. Record the divergence in `patches/` with:
   - file path(s)
   - reason
   - exact change or minimal diff
   - reapply instructions
4. Reapply approved divergence patches only at the very end of migration, after user approval.

### Untracked divergence rule

If the agent finds a divergence from template state that is **not** recorded in `patches/`, it must ask:

- Is this divergence intentional?
- Should it be tracked in `patches/` for future migrations?

Do not silently keep or remove untracked divergences.

---

## GitHub permission pitfalls to verify during migration

### A) Pushing workflow file changes

If PR changes files under `.github/workflows/`, push can fail unless your GitHub CLI auth token includes `workflow` scope.

Check and refresh as needed:

```bash
gh auth status -h github.com
gh auth refresh -h github.com -s repo -s workflow -s read:org
```

### B) Workflow runtime API access

If CI errors with `Resource not accessible by integration` when calling Pull Request APIs, set explicit workflow permissions (this is independent from your local `gh auth` scopes):

```yaml
permissions:
  contents: read
  pull-requests: read
```

---

## Scope control rules

- Do not bundle unrelated fixes into a migration PR without explicit approval.
- If asked to add another change “on top”, use a separate stacked PR.
- If a request is phrased as a question/proposal, confirm before implementing.

---

## Reusable migration checklist

- [ ] Correct base branch and isolated worktree/branch
- [ ] Template-owned files synced with minimal drift
- [ ] Project-specific divergences explicitly reapplied
- [ ] Local docs checks pass (`clean-doc`, `lint-md`, `html`)
- [ ] Workflow/auth requirements verified when touching CI
- [ ] PR scope is focused and reviewable
- [ ] CI watched until terminal state
