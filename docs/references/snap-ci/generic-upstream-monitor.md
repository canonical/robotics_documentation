(references-snap-ci-generic-upstream-monitor)=

# generic-upstream-monitor

The `generic-upstream-monitor` workflow monitors upstream
for new versions of the packaged software.
It is meant to be used when the `snapcraft.yaml` file
lives outside the upstream source code
and should be kept in sync with upstream releases.

When a newer version is found upstream,
the workflow opens a GitHub issue titled
`[CI] Found version '<version>' upstream`
suggesting to update the snap.
If such an issue is already open, no new issue is created.

The workflow is "generic" in that it expects
two caller-provided bash scripts:

- `script-get-upstream-version` retrieves the latest upstream version.
  It must print the version, and solely the version, to stdout.
- `script-compare-versions` compares the version read from the
  `snapcraft.yaml` to the upstream version.
  It is called with both versions as arguments:
  `compare-versions <upstream-version> <snap-version>`.
  It is expected to print `1` to stdout
  when the upstream version is greater than the snap version.
  Any other value is ignored.

## Usage

```yaml
jobs:
  monitor:
    permissions:
      contents: read
      issues: write
    uses: canonical/robotics-actions-workflows/.github/workflows/generic-upstream-monitor.yaml@main
    with:
      script-get-upstream-version: |
        curl -s https://example.com/latest-version.txt
      script-compare-versions: |
        if [ "${1}" -gt "${2}" ]; then
          echo 1
        fi
```

## Inputs

<!-- Table rows exceed the 85-character line-length rule (MD013) and tables
     cannot be wrapped. The pinned pymarkdownlnt 0.9.35 has no table exemption;
     TODO: switch to the 'tables' option once pymarkdownlnt is updated to 0.9.38
     or later, which added 'tables'/'table_line_length' support. -->
<!-- pyml disable-num-lines 10 line-length -->

| Input | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `git-ref` | string | `${{ github.ref }}` | no | The branch to checkout. |
| `issue-assignee` | string | `''` | no | Whom to assign the issue to, in the form `@name`. |
| `script-compare-versions` | string | — | yes | A bash script to compare versions. |
| `script-get-upstream-version` | string | — | yes | A bash script to retrieve the upstream version. |
| `snapcraft-source-subdir` | string | `.` | no | The directory of the Snapcraft project. |

## Secrets

This workflow takes no secrets.
The `GITHUB_TOKEN` is used to open issues
and is available to the `script-get-upstream-version` script
as the `GH_TOKEN` environment variable.

## Outputs

The workflow declares no workflow outputs and uploads no artifacts.
Its outcome is a GitHub issue opened
when a newer upstream version is detected.

## Permissions

- `contents: read`
- `issues: write`
