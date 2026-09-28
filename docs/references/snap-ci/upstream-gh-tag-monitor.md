(references-snap-ci-upstream-gh-tag-monitor)=

# upstream-gh-tag-monitor

The `upstream-gh-tag-monitor` workflow is a specialization of the
{ref}`generic-upstream-monitor <references-snap-ci-generic-upstream-monitor>`
workflow.
It provides the two scripts the generic workflow expects:

- `script-get-upstream-version` retrieves the tag of the latest release
  of a given upstream GitHub repository;
- `script-compare-versions` compares two semver versions.

When a newer version is found upstream,
the workflow opens a GitHub issue titled
`[CI] Found version '<version>' upstream`
suggesting to update the snap.

## Usage

```yaml
jobs:
  monitor:
    permissions:
      contents: read
      issues: write
    uses: canonical/robotics-actions-workflows/.github/workflows/upstream-gh-tag-monitor.yaml@main
    with:
      source-repo: my-org/my-upstream-project
```

## Inputs

<!-- Table rows exceed the 85-character line-length rule (MD013) and tables
     cannot be wrapped. The pinned pymarkdownlnt 0.9.35 has no table exemption;
     TODO: switch to the 'tables' option once pymarkdownlnt is updated to 0.9.38
     or later, which added 'tables'/'table_line_length' support. -->
<!-- pyml disable-num-lines 9 line-length -->

| Input | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `git-ref` | string | `${{ github.ref }}` | no | The branch to checkout. |
| `issue-assignee` | string | `''` | no | Whom to assign the issue to, in the form `@name`. |
| `snapcraft-source-subdir` | string | `.` | no | The directory of the Snapcraft project. |
| `source-repo` | string | — | yes | The upstream repository to monitor, in `org/repo` form. |

## Secrets

This workflow takes no secrets.
The `GITHUB_TOKEN` is used to query the upstream repository
and to open issues.

## Outputs

The workflow declares no workflow outputs and uploads no artifacts.
Its outcome is a GitHub issue opened
when a newer upstream version is detected.

## Permissions

- `contents: read`
- `issues: write`
