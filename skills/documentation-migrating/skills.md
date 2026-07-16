# SKILLS.md — Maintainer playbook learned from migration PRs

This file captures the practical rules and pitfalls we had to go through while migrating and maintaining this repository.

It is intended for maintainers and automation agents working on this repo.

---

## 1) Branching and worktree policy

- Use **git worktrees** for repository work.
- Start migration/fix PRs from the requested base branch (often `main`) in a fresh worktree.
- For follow-up requests that should not change an existing PR scope, open a **separate PR**.
- Do not reuse one branch name for unrelated PR scopes.

### Canonical pattern

```bash
git fetch origin
git worktree add ../robotics_documentation-<topic> -b <type>/<topic> origin/main
cd ../robotics_documentation-<topic>
```

---

## 2) Commit and GitHub message conventions

### Commits

- Do **not** prefix commit subjects with `[hermes-agent]`.
- Set git identity:
  - `Guillaume beuzeboc <guillaume.beuzeboc@gmail.com>`
- Commit body must include:
  - `Model: <actual model used>`
  - `Co-authored-by: hermes <hermes@beuzeboc.com>`

### GitHub-facing text

- Prefix PR titles/comments/reviews with `[hermes-agent]`.
- For Markdown comments/bodies, use:

```md
[hermes-agent]

<message>
```

- Use `--body-file` with `gh` for multiline Markdown to avoid shell quoting/backtick corruption.

---

## 3) Collaboration safety rules

- **No force-push** unless explicitly requested.
- Ask before major design trade-offs.
- If the user asks a question/proposal (not an instruction), treat it as **proposal-only** until explicitly approved.
- If a push/action was done without explicit approval, revert promptly and transparently.
- Keep wording precise (grammar/pluralization) in commit/PR text.

---

## 4) Template migration discipline (Sphinx stack)

- For stack migrations, prioritize **upstream template parity**.
- If user requests “redo from main”, do a **clean-room redo**:
  - fresh branch/worktree from `origin/main`
  - reapply only approved divergences
  - do not import/cherry-pick previous migration branch work
- Avoid "nice-to-have" formatting drift in template-owned files.

### Divergence policy

- Keep repository-specific divergences explicit and documented.
- If a file is mostly template-owned but needs local policy:
  - keep template base file
  - keep project overrides in a separate local file
  - merge at runtime (build/lint step) where practical
- This prevents future template sync from deleting local policy.

---

## 5) GitHub auth scope vs Actions token permissions

These are different systems and are easy to confuse.

### Local CLI token (`gh auth`)

- Controls what maintainers/agents can push/change from terminal.
- Workflow file changes under `.github/workflows/*` require `workflow` scope.

Useful commands:

```bash
gh auth refresh -h github.com -s repo -s workflow -s read:org
gh auth status -h github.com
```

### Actions runtime token (`GITHUB_TOKEN`)

- Controls what workflows can do during CI.
- `gh auth` changes do **not** change workflow runtime permissions.

For PR API access in workflows (e.g., "List commits on a pull request"):

```yaml
permissions:
  contents: read
  pull-requests: read
```

If CI shows `Resource not accessible by integration`, check workflow `permissions:` first.

---

## 6) PR and CI execution discipline

- Do not declare PR done until checks reach terminal state.
- `gh pr checks` showing "no checks reported" is not success; continue watching runs.
- If push is blocked by permissions/scope, report exact blocker immediately and do not claim completion.
- For docs/migration PRs, run local validation before push (as applicable):
  - `make clean-doc`
  - `make lint-md`
  - `make html`

---

## 7) Review-loop behavior

- Address review comments with follow-up commits (avoid history rewrite unless asked).
- When scope changes, update PR summary/body accordingly.
- Include direct commit links in review-response comments when relevant.

---

## 8) Scope management learned here

When concurrent asks appear (migration PR, workflow migration, CLA fix, docs policy fix):

- keep concerns split into focused PRs when requested
- avoid bundling unrelated fixes into one PR without explicit approval
- verify branch base/head before opening additional PRs

---

## 9) Recommended file strategy for this repository

For future maintainability:

- Keep this `SKILLS.md` as the human maintainer/agent playbook.
- `AGENTS.md` is optional; only add it if a toolchain specifically consumes it.
- If both are used, keep `SKILLS.md` as source-of-truth and keep `AGENTS.md` as a thin pointer.

---

## 10) Minimal checklist before pushing

- [ ] Correct branch/worktree and base branch
- [ ] Scope matches explicit user request
- [ ] No force-push unless explicitly approved
- [ ] Commit metadata conventions applied
- [ ] Required local checks run
- [ ] If touching workflows, verify `gh auth` includes `workflow`
- [ ] If CI uses PR APIs, set explicit workflow `permissions`
- [ ] PR/comment formatting follows `[hermes-agent]` rules
