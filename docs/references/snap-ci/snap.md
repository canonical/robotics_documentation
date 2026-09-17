(references-snap-ci-snap)=

# snap

The `snap` workflow is the main entry point of the snap CI.
It calls the {ref}`build <references-snap-ci-build>`,
{ref}`test <references-snap-ci-test>`
and {ref}`publish <references-snap-ci-publish>` workflows
as an integrated and coherent sequence.

By default it:

- builds the snap,
- installs it and calls `snap info` on it,
- publishes it to the Snap Store, either to `latest/edge` on pushes
  or to `latest/candidate` on tags.

The publish step only runs on `push`, `workflow_dispatch` and `schedule` events,
and only when the `snapstore-login` secret is defined.
On pull requests, the workflow only builds and tests the snap.

## Usage

```yaml
jobs:
  snap:
    permissions:
      contents: read
    uses: canonical/robotics-actions-workflows/.github/workflows/snap.yaml@main
    secrets:
      snapstore-login: ${{ secrets.SNAPSTORE_LOGIN }}
```

## Inputs

<!-- Table rows exceed the 85-character line-length rule (MD013) and tables
     cannot be wrapped. The pinned pymarkdownlnt 0.9.35 has no table exemption;
     TODO: switch to the 'tables' option once pymarkdownlnt is updated to 0.9.38
     or later, which added 'tables'/'table_line_length' support. -->
<!-- pyml disable-num-lines 17 line-length -->

| Input | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `cleanup` | boolean | `false` | no | Whether to delete the build artifacts after the run. Requires `actions: write` permission. |
| `git-ref` | string | `${{ github.ref }}` | no | The branch to checkout. |
| `lxd-image` | string | `''` | no | The LXD image to run the snap tests in, for example `ubuntu:20.04`. |
| `runs-on` | string | `ubuntu-latest` | no | The runner(s) to use. Accepts a JSON list, for example `'["ubuntu-latest", "self-hosted"]'`. |
| `snap-install-args` | string | `--dangerous` | no | The argument to pass to `snap install`. |
| `snap-test-script` | string | `''` | no | A bash test script to run against the snap. |
| `snap-risk` | string | `''` | no | Snap Store channel risk used for publication. Defaults to `edge`, or to `candidate` when the git ref is a tag. |
| `snap-track` | string | `latest` | no | Snap Store channel track used for publication. |
| `snapcraft-args` | string | `''` | no | The arguments to pass to `snapcraft` (pack). |
| `snapcraft-channel` | string | `latest/stable` | no | The channel from which to install Snapcraft. |
| `snapcraft-enable-experimental-extensions` | boolean | `false` | no | Whether to enable Snapcraft experimental extensions. |
| `snapcraft-source-subdir` | string | `.` | no | The path where to execute Snapcraft. Accepts a JSON list to build multiple snaps, for example `'["bar", "foo"]'`. |

## Secrets

<!-- pyml disable-num-lines 6 line-length -->

| Secret | Required | Description |
| --- | --- | --- |
| `snapstore-login` | no | Snap Store credential (see `snapcraft export-login`). When not defined, the publish step is skipped. |

## Outputs

The workflow declares no workflow outputs.
Its outcomes are:

- a workflow artifact per built snap,
  named `workflow-build-snap-<snap-file-name>-<branch>`,
  retained for 10 days unless `cleanup` is enabled;
- a published snap revision on the configured channel
  when the publish step runs.

## Permissions

- `contents: read`
- `actions: write` on the cleanup job, only when `cleanup` is enabled.
