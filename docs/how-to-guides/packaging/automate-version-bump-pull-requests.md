(how-to-guides-packaging-automate-version-bump-pull-requests)=

# Update snaps automatically

The
{ref}`upstream monitoring guide <how-to-guides-packaging-monitor-upstream-github-repository-for-new-releases>`
opens an issue when a new version is available upstream.
The {ref}`bump-snap-version <references-snap-ci-bump-snap-version>` workflow
goes one step further:
it reads the latest monitoring issue
and opens a pull request that updates the `snapcraft.yaml`
to the new version, closing the issue.

## Prerequisites

- A GitHub repository containing the snap project.
  The `snapcraft.yaml` must declare the packaged version
  through a top-level `version` field
  and a `source-tag` on the relevant part,
  or use `adopt-info` with a `source-tag`.
- The
  {ref}`upstream monitoring <how-to-guides-packaging-monitor-upstream-github-repository-for-new-releases>`
  workflow set up in the same repository,
  so that monitoring issues exist for the workflow to act on.

## Create the version bump workflow

Create the file `.github/workflows/bump-snap-version.yaml`
in your repository with the following content:

```yaml
name: bump-snap-version

on:
  workflow_dispatch:
    inputs:
      new-version:
        description: The new version tag (e.g., 'v0.27.0'). Leave empty to use the latest monitoring issue.
        required: false
        type: string
      issue-to-close:
        description: The issue number that this PR will resolve (e.g., '108'). Leave empty to use the latest monitoring issue.
        required: false
        type: string

# Restrictive default for the whole workflow.
permissions: {}

jobs:
  bump:
    permissions:
      contents: write
      pull-requests: write
      issues: read
    uses: canonical/robotics-actions-workflows/.github/workflows/bump-snap-version.yaml@main
    with:
      new-version: ${{ inputs.new-version }}
      issue-to-close: ${{ inputs.issue-to-close }}
```

The `workflow_dispatch` trigger keeps the bump under manual control:
you run it from the **Actions** tab
after reviewing the monitoring issue.
The two `workflow_dispatch` inputs appear as form fields
in the **Run workflow** dialog,
and are forwarded to the reusable workflow.
Leaving both empty triggers the automatic mode described below.

```{note}
The calling job must grant `contents: write` and `pull-requests: write`
so that the workflow can push the version-bump branch
and open the pull request.
Pull requests created with the default `GITHUB_TOKEN`
do not trigger further workflow runs;
use a Personal Access Token or GitHub App token
if you expect the bump pull request to start your build and test CI.
```

## Bump to the detected version

Run the workflow without inputs:

1. On GitHub, open your repository and go to the **Actions** tab.
2. Select the **bump-snap-version** workflow in the sidebar.
3. Select **Run workflow** and confirm.

The workflow finds the latest open monitoring issue,
for example `[CI] Found version 'v0.27.0' upstream`,
extracts the version and creates a branch
named after it, for example `feat/bump-v0.27.0`.
It updates the `snapcraft.yaml`,
pushes the branch and opens a pull request
that closes the monitoring issue
and any older open monitoring issues.

If no monitoring issue is open,
or a pull request closing the issue already exists,
the workflow exits without making changes.

```{note}
If several parts of your `snapcraft.yaml` declare a `source-tag`,
set the `source-tag-part` input to the name of the part to update.
```

## Bump to a specific version

In automatic mode, the workflow derives everything
from the latest monitoring issue —
the issue titled `[CI] Found version '<version>' upstream`
opened by the upstream monitor workflow.
To bypass this lookup,
fill in both fields of the **Run workflow** dialog:

- **new-version**: the new version tag, for example `v0.27.0`.
- **issue-to-close**: the issue number that the pull request resolves,
  for example `108`.

The workflow then uses those values directly
instead of looking up the latest monitoring issue.
Fill in both fields or neither:
providing only one of the two fails the workflow.

See the
{ref}`bump-snap-version workflow reference <references-snap-ci-bump-snap-version>`
for the full list of inputs and the exact update rules.
