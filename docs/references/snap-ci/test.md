(references-snap-ci-test)=

# test

The `test` workflow tests the snap(s) built during the run.
It downloads all the `*.snap` files found in the run artifacts
and installs those matching the architecture of the runner.
This allows testing multiple snaps at once,
which is convenient for multi-snap deployments.

By default, the workflow makes sure the snap(s) install
and calls `snap info` on them.
A caller can provide an additional custom test
as a bash script through the `snap-test-script` input.

The entire test can also run inside an
[LXD container](https://canonical.com/lxd),
allowing testing on images that are not available as GitHub runners,
through the `lxd-image` input.

## Usage

```yaml
jobs:
  test:
    needs: [build]
    permissions:
      contents: read
    uses: canonical/robotics-actions-workflows/.github/workflows/test.yaml@main
    with:
      snap-test-script: |
        #!/bin/sh
        set -euxo pipefail
        hello-snap | grep "Hello World"
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
<!-- pyml disable-num-lines 10 line-length -->

| Input | Type | Default | Required | Description |
| --- | --- | --- | --- | --- |
| `lxd-image` | string | `''` | no | The LXD image to run the snap tests in, for example `ubuntu:20.04`. When empty, tests run directly on the runner. |
| `runs-on` | string | `ubuntu-latest` | no | The runner(s) to use. Accepts a JSON list. Only snaps matching the runner architecture are installed. |
| `git-ref` | string | `${{ github.ref }}` | no | The branch used to build the snap. |
| `snap-install-args` | string | `--dangerous` | no | The argument to pass to `snap install`. |
| `snap-test-script` | string | `''` | no | A bash test script to run against the snap. |

## Secrets

This workflow takes no secrets.

## Outputs

The workflow declares no workflow outputs and uploads no artifacts.
Its outcome is the success or failure of the install,
of `snap info` and of the optional test script.

## Permissions

- `contents: read`
