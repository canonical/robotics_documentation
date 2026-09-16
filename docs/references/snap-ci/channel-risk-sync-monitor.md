(references-snap-ci-channel-risk-sync-monitor)=

# channel-risk-sync-monitor

The `channel-risk-sync-monitor` workflow monitors a snap
waiting for promotion from one channel risk to another.

It compares the revision published on the aspirant channel
(for example `latest/candidate`)
to the revision published on the target channel
(for example `latest/stable`).
If the aspirant revision is newer,
it compares the publication date of that revision to the current date.
When the revision has been waiting for a number of days
greater than or equal to `threshold`,
the workflow opens a GitHub issue titled
`[CI] Consider promoting '<aspirant-channel>' to '<target-channel>'.`.
If such an issue is already open, no new issue is created.

If the `snap-name` input is not provided,
the snap name is inferred from the `snapcraft.yaml` file
found in `snapcraft-source-subdir` on the `git-ref` branch.

## Usage

```yaml
jobs:
  monitor:
    permissions:
      contents: read
      issues: write
    uses: canonical/robotics-actions-workflows/.github/workflows/channel-risk-sync-monitor.yaml@main
    with:
      snap-name: my-snap
      threshold: 14
```

## Inputs

<!-- Table rows exceed the 85-character line-length rule (MD013) and tables
     cannot be wrapped. The pinned pymarkdownlnt 0.9.35 has no table exemption;
     TODO: switch to the 'tables' option once pymarkdownlnt is updated to 0.9.38
     or later, which added 'tables'/'table_line_length' support. -->
<!-- pyml disable-num-lines 13 line-length -->

| Input | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `git-ref` | string | `${{ github.ref }}` | no | The branch to checkout. |
| `issue-assignee` | string | `''` | no | Whom to assign the issue to, in the form `@name`. |
| `snap-name` | string | `''` | no | The snap name. If not provided, it is inferred from the local `snapcraft.yaml`. |
| `snap-risk-aspirant` | string | `candidate` | no | Snap Store channel risk used as aspirant. |
| `snap-risk-target` | string | `stable` | no | Snap Store channel risk used as reference. |
| `snap-track` | string | `latest` | no | Snap Store channel track to monitor. |
| `snapcraft-source-subdir` | string | `.` | no | The directory of the Snapcraft project. |
| `threshold` | number | `10` | no | The threshold to trigger the issue, in days. |

## Secrets

This workflow takes no secrets.
The `GITHUB_TOKEN` is used to open issues.

## Outputs

The workflow declares no workflow outputs and uploads no artifacts.
Its outcome is a GitHub issue opened
when a snap revision has been waiting for promotion
for at least the threshold.

## Permissions

- `contents: read`
- `issues: write`
