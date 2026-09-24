(references-snap-ci-promote)=

# promote

The `promote` workflow promotes a given snap
from one Snap Store channel to another,
using `snapcraft promote`.

If the `snap` input is not provided,
the snap name is inferred from the `snapcraft.yaml` file
found in `snapcraft-source-subdir` on the `git-ref` branch.

The Snapcraft logs of the run are always uploaded
as a workflow artifact named `snapcraft_logs_<snap-name>`.

## Usage

```yaml
jobs:
  promote:
    permissions:
      contents: read
    uses: canonical/robotics-actions-workflows/.github/workflows/promote.yaml@main
    with:
      from-channel: latest/candidate
      to-channel: latest/stable
    secrets:
      snapstore-login: ${{ secrets.SNAPSTORE_LOGIN }}
```

## Inputs

<!-- Table rows exceed the 85-character line-length rule (MD013) and tables
     cannot be wrapped. The pinned pymarkdownlnt 0.9.35 has no table exemption;
     TODO: switch to the 'tables' option once pymarkdownlnt is updated to 0.9.38
     or later, which added 'tables'/'table_line_length' support. -->
<!-- pyml disable-num-lines 10 line-length -->

| Input | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `snap` | string | `''` | no | The snap to promote. If not provided, the name is inferred from the local `snapcraft.yaml`. |
| `from-channel` | string | `latest/candidate` | no | The channel from which to promote. |
| `to-channel` | string | `latest/stable` | no | The channel to which to promote. |
| `snapcraft-source-subdir` | string | `.` | no | The directory of the Snapcraft project. Used to infer the snap name when the `snap` input is not provided. |
| `git-ref` | string | `${{ github.ref }}` | no | The branch to checkout. Used to infer the snap name when the `snap` input is not provided. |

## Secrets

<!-- pyml disable-num-lines 6 line-length -->

| Secret | Required | Description |
| --- | --- | --- |
| `snapstore-login` | yes | Snap Store credential (see `snapcraft export-login`). |

## Outputs

The workflow declares no workflow outputs.
Its outcomes are the promoted snap revision on the Snap Store
and the uploaded `snapcraft_logs_<snap-name>` artifact.

## Permissions

- `contents: read`
