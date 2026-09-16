(references-snap-ci)=

# Snap CI workflows

% Include start summary

**Reusable GitHub workflows** to build, test, release
and monitor snaps in CI,
maintained in the
[canonical/robotics-actions-workflows](https://github.com/canonical/robotics-actions-workflows)
repository.

% Include stop summary

These workflows implement an opinionated pipeline
to build, test and release snaps.
They are meant to be called from other repositories
with the GitHub Actions
[reusable workflows](https://docs.github.com/en/actions/using-workflows/reusing-workflows)
mechanism:

```yaml
jobs:
  snap:
    permissions:
      contents: read
    uses: canonical/robotics-actions-workflows/.github/workflows/snap.yaml@main
    secrets:
      snapstore-login: ${{ secrets.SNAPSTORE_LOGIN }}
```

## Workflows

<!-- Table rows exceed the 85-character line-length rule (MD013) and tables
     cannot be wrapped. The pinned pymarkdownlnt 0.9.35 has no table exemption;
     TODO: switch to the 'tables' option once pymarkdownlnt is updated to 0.9.38
     or later, which added 'tables'/'table_line_length' support. -->
<!-- pyml disable-num-lines 14 line-length -->

| Workflow | Description |
| --- | --- |
| {ref}`snap <references-snap-ci-snap>` | Build, test and publish a snap in a single pipeline. |
| {ref}`build <references-snap-ci-build>` | Build the snap and upload it as a workflow artifact. |
| {ref}`test <references-snap-ci-test>` | Install and test the built snap. |
| {ref}`publish <references-snap-ci-publish>` | Publish the built snap to the Snap Store. |
| {ref}`promote <references-snap-ci-promote>` | Promote a snap from one channel to another. |
| {ref}`generic-upstream-monitor <references-snap-ci-generic-upstream-monitor>` | Monitor upstream for new versions with custom scripts. |
| {ref}`upstream-gh-tag-monitor <references-snap-ci-upstream-gh-tag-monitor>` | Monitor an upstream GitHub repository for new tags. |
| {ref}`bump-snap-version <references-snap-ci-bump-snap-version>` | Open a pull request that bumps the snap version. |
| {ref}`channel-risk-sync-monitor <references-snap-ci-channel-risk-sync-monitor>` | Monitor snaps waiting for channel promotion. |

## Permissions

Each reusable workflow follows the principle of least privilege.
It declares a minimal set of
[`GITHUB_TOKEN` permissions](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#modifying-the-permissions-for-the-github_token)
and elevates them only on the jobs that need more.

A called reusable workflow cannot be granted more permissions than its caller.
The caller job must therefore grant at least the permissions listed below.
Keep a restrictive default at the top of your workflow
and grant the rest per job:

```yaml
# Restrictive default for the whole workflow.
permissions: {}

jobs:
  snap:
    permissions:
      contents: read
    uses: canonical/robotics-actions-workflows/.github/workflows/snap.yaml@main
    secrets:
      snapstore-login: ${{ secrets.SNAPSTORE_LOGIN }}
```

<!-- pyml disable-num-lines 14 line-length -->

| Workflow | contents | issues | pull-requests | actions |
| --- | --- | --- | --- | --- |
| `snap` | read | — | — | write [^cleanup] |
| `build` | read | — | — | — |
| `test` | read | — | — | — |
| `publish` | read | — | — | — |
| `promote` | read | — | — | — |
| `generic-upstream-monitor` | read | write | — | — |
| `upstream-gh-tag-monitor` | read | write | — | — |
| `channel-risk-sync-monitor` | read | write | — | — |
| `bump-snap-version` | write | read | write | — |

[^cleanup]: `actions: write` is only required when the `cleanup` option
of the `snap` workflow is enabled,
so that the workflow can delete the build artifacts.
Without `cleanup`, `contents: read` is sufficient.

```{note}
The `bump-snap-version` workflow needs `contents: write`
and `pull-requests: write` to push the version-bump branch
and open the pull request.
Pull requests created with the default `GITHUB_TOKEN`
do not trigger further workflow runs.
Use a
[Personal Access Token or GitHub App token](https://docs.github.com/en/actions/security-guides/automatic-token-authentication#granting-additional-permissions)
if you expect the bump pull request to start your build and test CI.
```

```{toctree}
:maxdepth: 1
:hidden:

snap
build
test
publish
promote
generic-upstream-monitor
upstream-gh-tag-monitor
bump-snap-version
channel-risk-sync-monitor
```
