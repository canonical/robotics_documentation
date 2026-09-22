(how-to-guides-packaging-test-a-snap-in-ci)=

# Test a snap in CI

Building a snap in CI is only half the story:
before it reaches the Snap Store,
you want to verify that the built snap actually installs and runs.
The {ref}`test <references-snap-ci-test>` reusable workflow does exactly that:
it installs the snap(s) built during the run
and optionally executes a custom test script.

## Prerequisites

- A GitHub repository containing a snap project.
- A workflow that builds your snap,
  for example the one from the
  {ref}`snap CI tutorial <tutorials-snap-ci-with-github-actions>`.
  The `test` workflow expects the snap artifacts
  produced by the {ref}`build <references-snap-ci-build>` workflow
  to be present in the same run.

## Test with the snap workflow

The {ref}`snap <references-snap-ci-snap>` workflow
already runs the `test` workflow between the build and the publish steps.
By default, it only verifies that the snap installs
and calls `snap info` on it.

Add a custom test script with the `snap-test-script` input.
The script runs with `bash -euxo pipefail`,
so any failing command fails the pipeline:

```yaml
jobs:
  snap:
    permissions:
      contents: read
    uses: canonical/robotics-actions-workflows/.github/workflows/snap.yaml@main
    with:
      snap-test-script: |
        #!/bin/sh
        set -euxo pipefail
        hello-snap | grep "Hello World"
    secrets:
      snapstore-login: ${{ secrets.SNAPSTORE_LOGIN }}
```

Adapt the script to exercise the actual commands your snap ships.

```{note}
The `test` workflow installs every `*.snap` file
it finds in the run artifacts
that matches the architecture of the runner.
When your repository builds several snaps,
for example with a list in `snapcraft-source-subdir`,
the same test job installs them all
and runs the test script against the whole deployment.
This is convenient for intricate multi-snap setups.
```

## Test inside an LXD container

GitHub-hosted runners only offer a limited set of operating systems.
To test your snap on an image that is not available as a runner,
for example Ubuntu 20.04 LTS, set the `lxd-image` input.
The workflow then launches an [LXD container](https://canonical.com/lxd),
installs `snapd` and your snap inside it,
and executes the test script inside the container:

```yaml
jobs:
  snap:
    permissions:
      contents: read
    uses: canonical/robotics-actions-workflows/.github/workflows/snap.yaml@main
    with:
      lxd-image: "ubuntu:20.04"
      snap-test-script: |
        #!/bin/sh
        set -euxo pipefail
        hello-snap | grep "Hello World"
    secrets:
      snapstore-login: ${{ secrets.SNAPSTORE_LOGIN }}
```

The value must be an image alias from an LXD remote,
For example one listed by `lxc image list ubuntu:`.

## Tune the installation

Use `snap-install-args` to control how the snap is installed.
The default is `--dangerous`,
which allows installing the unsigned, locally built snap.
Add further flags when needed, for example:

```yaml
    with:
      snap-install-args: "--dangerous --jailmode"
```

See the {ref}`test workflow reference <references-snap-ci-test>`
for the full list of inputs.
