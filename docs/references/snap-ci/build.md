(references-snap-ci-build)=

# build

The `build` workflow builds the snap found in the repository
using the [canonical/action-build](https://github.com/canonical/action-build)
action,
and uploads the result as a workflow artifact.

The workflow builds a matrix
over the `snapcraft-source-subdir` and `runs-on` inputs,
so a caller can build several snaps,
or the same snap on several runners, in a single run.

## Usage

```yaml
jobs:
  build:
    permissions:
      contents: read
    uses: canonical/robotics-actions-workflows/.github/workflows/build.yaml@main
```

## Inputs

<!-- Table rows exceed the 85-character line-length rule (MD013) and tables
     cannot be wrapped. The pinned pymarkdownlnt 0.9.35 has no table exemption;
     TODO: switch to the 'tables' option once pymarkdownlnt is updated to 0.9.38
     or later, which added 'tables'/'table_line_length' support. -->
<!-- pyml disable-num-lines 11 line-length -->

| Input | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `git-ref` | string | `${{ github.ref }}` | no | The branch to checkout. |
| `runs-on` | string | `ubuntu-latest` | no | The runner(s) to use. Accepts a JSON list, for example `'["ubuntu-latest", "self-hosted"]'`. |
| `snapcraft-args` | string | `''` | no | The arguments to pass to `snapcraft` (pack). |
| `snapcraft-channel` | string | `latest/stable` | no | The channel from which to install Snapcraft. |
| `snapcraft-enable-experimental-extensions` | boolean | `false` | no | Whether to enable Snapcraft experimental extensions. |
| `snapcraft-source-subdir` | string | `.` | no | The path where to execute Snapcraft. Accepts a JSON list to build multiple snaps, for example `'["bar", "foo"]'`. |

## Secrets

This workflow takes no secrets.

## Outputs

The workflow declares no workflow outputs.
Each built snap is uploaded as a workflow artifact named
`workflow-build-snap-<snap-file-name>-<branch>`,
with a retention of 10 days.
The run fails if no snap file is produced.

## Permissions

- `contents: read`
