(references-snap-ci-bump-snap-version)=

# bump-snap-version

The `bump-snap-version` workflow automates the creation
of a version-bump pull request.
It is designed to work together with the
{ref}`upstream-gh-tag-monitor <references-snap-ci-upstream-gh-tag-monitor>`
workflow:
when a new version is detected upstream and an issue is opened,
this workflow can be triggered to create a pull request
that updates the `snapcraft.yaml` file with the new version.

The workflow operates in two modes:

- **Automatic mode**: when called without `new-version` and
  `issue-to-close`, the workflow finds the latest open monitoring issue
  (for example `[CI] Found version 'v0.27.0' upstream`),
  extracts the version from it and proceeds with the bump.
  If no monitoring issue is found,
  the workflow exits successfully without making changes.
- **Manual mode**: when `new-version` and `issue-to-close`
  are both provided, the workflow uses those values directly.
  Providing only one of the two fails the workflow.

In both modes, the workflow:

1. Checks out the repository at `git-ref`.
2. Skips if a pull request closing the issue already exists.
3. Creates a new branch named after the version,
   for example `feat/bump-v0.27.0`.
4. Updates the `snapcraft.yaml` file:
   - if `adopt-info` is used, only the `source-tag` field
     of the referenced part is updated;
   - otherwise, the top-level `version` field is updated
     (with the `v` prefix removed)
     and the `source-tag` field of the parts is updated;
   - if several parts declare a `source-tag`,
     the `source-tag-part` input must specify which part to update.
5. Commits, pushes the branch and opens a pull request
   that closes the monitoring issue,
   as well as any older open monitoring issues.

## Usage

```yaml
jobs:
  bump:
    permissions:
      contents: write
      pull-requests: write
      issues: read
    uses: canonical/robotics-actions-workflows/.github/workflows/bump-snap-version.yaml@main
```

## Inputs

<!-- Table rows exceed the 85-character line-length rule (MD013) and tables
     cannot be wrapped. The pinned pymarkdownlnt 0.9.35 has no table exemption;
     TODO: switch to the 'tables' option once pymarkdownlnt is updated to 0.9.38
     or later, which added 'tables'/'table_line_length' support. -->
<!-- pyml disable-num-lines 11 line-length -->

| Input | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `new-version` | string | `''` | no | The new version tag, for example `v0.27.0`. If not provided, the version is extracted from the latest monitoring issue. |
| `issue-to-close` | string | `''` | no | The issue number that this pull request resolves, for example `108`. If not provided, the latest monitoring issue is used. |
| `snapcraft-source-subdir` | string | `.` | no | The directory of the Snapcraft project. |
| `pr-reviewer` | string | `''` | no | The pull request reviewer, in the form `@name`. |
| `source-tag-part` | string | `''` | no | The part name to update the `source-tag` for. Required when multiple parts declare a `source-tag`. |
| `git-ref` | string | `${{ github.ref }}` | no | The branch to checkout. |

## Secrets

This workflow takes no secrets.
The `GITHUB_TOKEN` is used to list issues,
push the branch and open the pull request.

```{note}
Pull requests created with the default `GITHUB_TOKEN`
do not trigger further workflow runs.
One must thus manually trigger it.
```

## Outputs

The workflow declares no workflow outputs and uploads no artifacts.
Its outcome is a pull request that bumps the snap version,
or no change when no monitoring issue is open
or when a matching pull request already exists.

## Permissions

- `contents: write`
- `pull-requests: write`
- `issues: read`
