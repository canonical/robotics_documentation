(how-to-guides-packaging-monitor-upstream-github-repository-for-new-releases)=

# Monitor an upstream GitHub repository for new releases

When the `snapcraft.yaml` file lives outside the upstream source code,
the snap version must be updated every time upstream publishes a release.
The {ref}`upstream-gh-tag-monitor <references-snap-ci-upstream-gh-tag-monitor>`
workflow watches the releases of an upstream GitHub repository
and opens an issue when it finds a release tag
newer than the one in your `snapcraft.yaml`.

## Prerequisites

- A GitHub repository containing the snap project.
  The `snapcraft.yaml` must declare the packaged version,
  typically through a `version` field
  or a `source-tag` on the relevant part.
- The upstream project must publish its releases
  as [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases)
  in a public repository.
  Pre-releases and drafts are ignored.

## Create the monitoring workflow

Create the file `.github/workflows/upstream-monitor.yaml` in your repository
with the following content:

```yaml
name: upstream-monitor

on:
  schedule:
    - cron: '0 6 * * *'
  workflow_dispatch:

# Restrictive default for the whole workflow.
permissions: {}

jobs:
  monitor:
    permissions:
      contents: read
      issues: write
    uses: canonical/robotics-actions-workflows/.github/workflows/upstream-gh-tag-monitor.yaml@main
    with:
      source-repo: some-org/the-upstream-project
```

Replace `some-org/the-upstream-project`
with the upstream repository to monitor.
The `schedule` trigger runs the check every day at 06:00 UTC;
adapt the cron expression to your needs.
The `workflow_dispatch` trigger lets you run the check manually
from the **Actions** tab.

```{note}
The calling job must grant `issues: write`,
otherwise the workflow cannot open the monitoring issue.
```

## Verify the monitoring

Run the workflow manually once:

1. On GitHub, open your repository and go to the **Actions** tab.
2. Select the **upstream-monitor** workflow in the sidebar.
3. Select **Run workflow** and confirm.

If the latest upstream release is newer than the snap version,
a new issue appears in your repository,
titled `[CI] Found version '<version>' upstream`.
Running the workflow again does not create a duplicate
while that issue is still open.

## Act on new releases

Once a monitoring issue is open,
the {ref}`bump-snap-version <references-snap-ci-bump-snap-version>` workflow
can automatically create a pull request
that updates the `snapcraft.yaml` to the new version.
Follow the
{ref}`version-bump guide <how-to-guides-packaging-automate-version-bump-pull-requests>`
to set it up and trigger it after each monitoring issue.

If the upstream project does not publish releases on GitHub,
use the {ref}`generic-upstream-monitor <references-snap-ci-generic-upstream-monitor>`
workflow with your own version-retrieval and comparison scripts instead.
