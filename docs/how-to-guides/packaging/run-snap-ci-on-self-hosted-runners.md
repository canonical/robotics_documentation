(how-to-guides-packaging-run-snap-ci-on-self-hosted-runners)=

# Run the snap CI on self-hosted runners

GitHub-hosted runners only cover a few operating systems and architectures.
To build or test your snap on your own hardware,
for example on an ARM board or inside your infrastructure,
run the snap CI on
[self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners).
The reusable workflows support this through the `runs-on` input.

## Prerequisites

- A GitHub repository containing a snap project
  with a snap CI workflow set up,
  for example from the
  {ref}`snap CI tutorial <tutorials-snap-ci-with-github-actions>`.
- A self-hosted runner
  [registered with your repository](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/adding-self-hosted-runners).
  The build action installs snapd, LXD and Snapcraft on the runner,
  so it needs an Ubuntu host with passwordless `sudo`
  for the runner user and the ability to run LXD.

## Build and test on a self-hosted runner

Set the `runs-on` input to a label matching your self-hosted runner:

```yaml
jobs:
  snap:
    permissions:
      contents: read
    uses: canonical/robotics-actions-workflows/.github/workflows/snap.yaml@main
    with:
      runs-on: '[["self-hosted", "linux", "arm64"]]'
    secrets:
      snapstore-login: ${{ secrets.SNAPSTORE_LOGIN }}
```

The value is converted to a JSON list of labels
and used as the `runs-on` of the build and test jobs.
All listed labels must match for a runner to be selected.

## Build and test on multiple runners

To run the pipeline on several runners in parallel,
pass several label sets.
Both the `build` and the `test` workflows expand the value into a matrix,
so each runner gets its own build and test job:

```yaml
    with:
      runs-on: '["ubuntu-latest", ["self-hosted", "linux", "arm64"]]'
```

```{note}
When testing on multiple architectures,
the test job only installs the snap(s)
matching the architecture of the runner it executes on.
```

See the {ref}`build <references-snap-ci-build>`
and {ref}`test <references-snap-ci-test>` workflow references
for the details of the `runs-on` input.
