(explanations-snaps-snap-ci-workflows-use-cases)=

# Snap CI reusable workflows: intended use cases

The {ref}`snap CI reusable workflows <references-snap-ci>`
build, test and release snaps.
Taken individually, the
{ref}`build <references-snap-ci-build>`,
{ref}`test <references-snap-ci-test>`
and {ref}`publish <references-snap-ci-publish>` workflows
are fairly generic building blocks.
Put together in the
{ref}`snap <references-snap-ci-snap>` workflow,
they form an opinionated pipeline
that encodes a specific release model
designed around two ways in which a snap project is usually organized.

Understanding these two use cases helps you decide whether
the workflows fit your project and how to configure them.

## The `snapcraft.yaml` lives alongside the source code

This is the main use case.
The snap packaging and the application source code share the same repository,
so every change to the code can immediately be validated as a snap.

The workflow behaves differently depending on the event:

- On **pull requests**, the snap is built and tested.
  The resulting snap can be retrieved as a workflow artifact
  for further local testing and tinkering. Nothing is published.
- On **pushes** and manual triggers (`workflow_dispatch`),
  the snap is built,
  tested and released on the Snap Store on the `edge` risk channel.
- On **tags**, the snap is additionally released
  on the `candidate` risk channel.

Promotion from `candidate` to `stable`
is deliberately left out of the automation.
It is a manual step,
expected to happen after thorough testing —
either with the `snapcraft promote` command
or with the {ref}`promote <references-snap-ci-promote>` workflow.

This design keeps every change on `main` available on
`edge` for early adopters,
while releases intended for a wider audience
go through the `candidate` gate first.

## The `snapcraft.yaml` lives in its own repository

Sometimes the packaging is maintained separately
from the upstream source code,
for example when snapping a third-party project.
In this case the repository only contains the `snapcraft.yaml`.

Here, the snap version is expected to be updated
with respect to the upstream code.
Since such a snap is only republished
when a new upstream version lands,
every published revision is a release candidate by nature.
The intended release schema is therefore
to publish on the `candidate` channel by default —
by setting the `snap-risk` input to `candidate` —
and to promote to `stable` manually after validation,
either with the `snapcraft promote` command
or with the {ref}`promote <references-snap-ci-promote>` workflow.

Keeping the `snapcraft.yaml`, its git history and its CI
in sync with upstream can prove tedious.
The recommended approach is
to pin the source code version at a given tag
(`parts.<part>.source-tag` in the `snapcraft.yaml`)
and to solely update the snap on new upstream tags.

Two monitoring workflows support this maintenance model:

- The
  {ref}`upstream-gh-tag-monitor <references-snap-ci-upstream-gh-tag-monitor>`
  workflow (or its generic variant,
  {ref}`generic-upstream-monitor <references-snap-ci-generic-upstream-monitor>`)
  watches upstream releases
  and opens an issue when a new version is available.
- The
  {ref}`bump-snap-version <references-snap-ci-bump-snap-version>`
  workflow turns such an issue
  into a pull request that updates the `snapcraft.yaml`.

Together with the
{ref}`channel-risk-sync-monitor <references-snap-ci-channel-risk-sync-monitor>`
workflow,
which reminds you when a revision has been waiting
for promotion for too long,
the whole lifecycle of an externally packaged snap
can be managed from the packaging repository.

## Why this design

The composition trades flexibility for consistency.
By fixing the release schema —
pull requests build and test,
pushes publish to `edge`,
tags publish to `candidate`,
promotion to `stable` stays manual —
the `snap` workflow makes every snap repository behave the same way.
Maintainers can move between repositories
without relearning each project's CI,
and the store channels always carry the same meaning.

Projects that need a different release model
can still reuse the individual
{ref}`build <references-snap-ci-build>`,
{ref}`test <references-snap-ci-test>`
and {ref}`publish <references-snap-ci-publish>` workflows
and compose them as they see fit,
instead of calling the integrated
{ref}`snap <references-snap-ci-snap>` workflow.
