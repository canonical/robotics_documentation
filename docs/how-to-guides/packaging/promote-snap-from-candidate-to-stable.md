(how-to-guides-packaging-promote-snap-from-candidate-to-stable)=

# Promote a snap from candidate to stable

When triggered by a tag,
the {ref}`snap <references-snap-ci-snap>` workflow
publishes the snap to the `candidate` channel
instead of `edge`.
Promotion from `candidate` to `stable` is a deliberate decision
that should happen only after thorough testing.
The {ref}`promote <references-snap-ci-promote>` workflow
facilitates this promotion
while keeping it under manual control through a `workflow_dispatch` trigger.

## Prerequisites

- A GitHub repository containing a snap project
  whose snap is already published on the `latest/candidate` channel.
- A `SNAPSTORE_LOGIN` repository secret holding your store credential,
  as set up in the
  {ref}`snap CI tutorial <tutorials-snap-ci-with-github-actions>`.
  The credential must include the `package_release` ACL and,
  if restricted with `--channels`, must allow the target channel.

## Create the promotion workflow

Create the file `.github/workflows/promote.yaml` in your repository
with the following content:

```yaml
name: promote

on:
  workflow_dispatch:

# Restrictive default for the whole workflow.
permissions: {}

jobs:
  promote:
    permissions:
      contents: read
    uses: canonical/robotics-actions-workflows/.github/workflows/promote.yaml@main
    secrets:
      snapstore-login: ${{ secrets.SNAPSTORE_LOGIN }}
```

The workflow promotes the snap named in your `snapcraft.yaml`
from `latest/candidate` to `latest/stable`,
which are the defaults of the `from-channel` and `to-channel` inputs.

## Trigger the promotion

1. On GitHub, open your repository and go to the **Actions** tab.
2. Select the **promote** workflow in the sidebar.
3. Select **Run workflow**, pick the branch and confirm.

The workflow resolves the snap name from the `snapcraft.yaml`
and runs `snapcraft promote` with your store credential.
The Snapcraft logs of the run are uploaded as a workflow artifact,
which is useful for auditing.

Verify the promotion once the run completes:

```bash
snap info <your-snap-name>
```

The output now lists the promoted revision
on the `latest/stable` channel.

## Promote a different snap or channels

When the snap is not defined in the repository,
or when you want to promote between other channels,
override the inputs:

```yaml
    with:
      snap: my-snap
      from-channel: latest/beta
      to-channel: latest/stable
```

See the {ref}`promote workflow reference <references-snap-ci-promote>`
for the full list of inputs.
