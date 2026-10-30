(how-to-guides-packaging-monitor-snaps-pending-promotion-to-stable)=

# Monitor snaps pending promotion to stable

Revisions published to `candidate` should be promoted to `stable`
once they have been tested.
When this step depends on someone remembering to do it,
revisions can linger on `candidate` for weeks.
The {ref}`channel-risk-sync-monitor <references-snap-ci-channel-risk-sync-monitor>`
workflow opens an issue
whenever a revision has been waiting on the aspirant channel
longer than a threshold,
reminding you to promote it.

## Prerequisites

- A GitHub repository containing the snap project.
- The snap must be published on the Snap Store
  on the channels to compare,
  by default `latest/candidate` and `latest/stable`.

## Create the monitoring workflow

Create the file `.github/workflows/channel-risk-monitor.yaml`
in your repository with the following content:

```yaml
name: channel-risk-monitor

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
    uses: canonical/robotics-actions-workflows/.github/workflows/channel-risk-sync-monitor.yaml@main
```

The workflow infers the snap name from your `snapcraft.yaml`.
The `schedule` trigger runs the check every day at 06:00 UTC;
adapt the cron expression to your needs.
The `workflow_dispatch` trigger lets you run the check manually
from the **Actions** tab.

```{note}
The calling job must grant `issues: write`,
otherwise the workflow cannot open the reminder issue.
```

## Tune the comparison

The default configuration compares `latest/candidate`
against `latest/stable`
and raises an issue after 10 days.
Adjust the channels, the snap and the threshold to your release process:

```yaml
    with:
      snap-name: my-snap
      snap-track: "5.x"
      snap-risk-aspirant: candidate
      snap-risk-target: stable
      threshold: 14
```

Provide `snap-name` when the snap is not defined in the repository.

## Verify the monitoring

Run the workflow manually once:

1. On GitHub, open your repository and go to the **Actions** tab.
2. Select the **channel-risk-monitor** workflow in the sidebar.
3. Select **Run workflow** and confirm.

If the revision on the aspirant channel is newer
than the one on the target channel
and has been waiting for at least the threshold,
a new issue appears in your repository,
titled
`[CI] Consider promoting '<aspirant-channel>' to '<target-channel>'.`.
Running the workflow again does not create a duplicate
while that issue is still open.

## Next steps

When an issue is opened,
promote the waiting revision with the
{ref}`promotion guide <how-to-guides-packaging-promote-snap-from-candidate-to-stable>`.

To automate a similar follow-up for upstream releases,
see the
{ref}`version-bump guide <how-to-guides-packaging-automate-version-bump-pull-requests>`,
which turns upstream monitoring issues into version-bump pull requests.
