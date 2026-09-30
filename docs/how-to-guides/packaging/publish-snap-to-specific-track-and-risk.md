(how-to-guides-packaging-publish-snap-to-specific-track-and-risk)=

# Publish a snap to a specific track and risk

By default,
the {ref}`snap CI <references-snap-ci>` publishes to the `latest` track:
to the `edge` risk on pushes, and to the `candidate` risk on tags.
To publish elsewhere, set the `snap-track` and `snap-risk` inputs of the
{ref}`snap <references-snap-ci-snap>`
or {ref}`publish <references-snap-ci-publish>` workflow.

## Prerequisites

- A GitHub repository containing a snap project
  with a snap CI workflow set up,
  for example from the
  {ref}`snap CI tutorial <tutorials-snap-ci-with-github-actions>`.
- A `SNAPSTORE_LOGIN` repository secret holding your store credential.
- The target [track](https://snapcraft.io/docs/channels)
  must exist on the Snap Store.
  Request it through the
  [store requests forum](https://forum.snapcraft.io/c/store-requests/19)
  if it does not.

## Publish to a specific risk

Set `snap-risk` to the target risk.
This value takes precedence over the default `edge`/`candidate` behavior:

```yaml
jobs:
  snap:
    permissions:
      contents: read
    uses: canonical/robotics-actions-workflows/.github/workflows/snap.yaml@main
    with:
      snap-risk: beta
    secrets:
      snapstore-login: ${{ secrets.SNAPSTORE_LOGIN }}
```

Every publishable run now releases the snap to `latest/beta`.

```{warning}
Setting `snap-risk` overrides the default channel resolution entirely:
even tag-triggered runs publish to the given risk
instead of `candidate`.
```

## Publish to a specific track

Set `snap-track` to the target track:

```yaml
    with:
      snap-track: "5.x"
```

The default risk resolution still applies on that track:
pushes publish to `5.x/edge` and tags to `5.x/candidate`.
Combine both inputs to control the full channel:

```yaml
    with:
      snap-track: "5.x"
      snap-risk: stable
```

```{note}
All snaps built from the same `git-ref` in one run
are published to the same channel.
```

See the {ref}`publish workflow reference <references-snap-ci-publish>`
for the details of channel resolution.
