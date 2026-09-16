(references-snap-ci-publish)=

# publish

The `publish` workflow publishes the snap(s) built during the run
to the Snap Store,
using the [canonical/action-publish](https://github.com/canonical/action-publish)
action.
Each `*.snap` file found in the run artifacts is published.

The target channel is resolved as follows,
in increasing precedence order:

1. by default, the snap is published to `<track>/edge`;
2. if the git ref is a tag, the snap is published to `<track>/candidate`;
3. if the `snap-risk` input is set, it takes precedence over both.

All snaps built from the `git-ref` branch
are published to the same track defined by `snap-track`.

## Usage

```yaml
jobs:
  publish:
    permissions:
      contents: read
    uses: canonical/robotics-actions-workflows/.github/workflows/publish.yaml@main
    secrets:
      snapstore-login: ${{ secrets.SNAPSTORE_LOGIN }}
```

```{note}
This workflow expects the snap artifacts produced by the
{ref}`build <references-snap-ci-build>` workflow
to be present in the same run.
```

## Inputs

<!-- Table rows exceed the 85-character line-length rule (MD013) and tables
     cannot be wrapped. The pinned pymarkdownlnt 0.9.35 has no table exemption;
     TODO: switch to the 'tables' option once pymarkdownlnt is updated to 0.9.38
     or later, which added 'tables'/'table_line_length' support. -->
<!-- pyml disable-num-lines 8 line-length -->

| Input | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `git-ref` | string | `${{ github.ref }}` | no | The branch that published the artifacts. |
| `snap-risk` | string | `''` | no | Snap Store channel risk used for publication. Defaults to `edge`, or to `candidate` when the git ref is a tag. |
| `snap-track` | string | `latest` | no | Snap Store channel track used for publication. |

## Secrets

<!-- pyml disable-num-lines 6 line-length -->

| Secret | Required | Description |
| --- | --- | --- |
| `snapstore-login` | yes | Snap Store credential (see `snapcraft export-login`). |

## Outputs

The workflow declares no workflow outputs and uploads no artifacts.
Its outcome is the published snap revision(s) on the resolved channel.

## Permissions

- `contents: read`
