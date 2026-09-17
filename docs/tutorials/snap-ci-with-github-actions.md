(tutorials-snap-ci-with-github-actions)=

# Set up a CI pipeline for your snap with reusable GitHub workflows

% Include start summary

Learn how to build, test and publish a snap
on pull requests, pushes to `main` and release tags
using the reusable GitHub workflows from the
[canonical/robotics-actions-workflows](https://github.com/canonical/robotics-actions-workflows)
repository.

% Include stop summary

## What you will learn

In this tutorial, you will:

- Add a complete CI pipeline to a snap project with a single workflow file.
- Build your snap on every pull request and push to `main`.
- Verify that the built snap installs and runs.
- Publish your snap to the Snap Store `edge` channel on every push to `main`.
- Publish your snap to the `candidate` channel when you tag a release.

No prior experience with GitHub Actions is required.

## Prerequisites

- A GitHub repository containing a snap project.
  This tutorial assumes a `snapcraft.yaml` file at the root of the repository
  or in the `snap/` directory.
- A snap name [registered on the Snap Store](https://snapcraft.io/docs/registering-your-app-name)
  that matches the `name` field of your `snapcraft.yaml`.
- The Snapcraft command-line tool [installed on your machine](https://documentation.ubuntu.com/snapcraft/stable/how-to/set-up-snapcraft/).

## Export your Snap Store credentials

Publishing to the Snap Store requires a store credential.
Rather than a user name and password,
the workflows expect the data produced by `snapcraft export-login`,
as documented in the
[action-publish store login](https://github.com/canonical/action-publish#store-login)
section.

Export one with Snapcraft:

```bash
snapcraft export-login --snaps=<your-snap-name> \
  --acls package_access,package_push,package_update,package_release \
  login.txt
```

Replace `<your-snap-name>` with the name of your snap.
The command writes the credential to the file `login.txt`.
Restricting the credential with `--acls` limits it
to the access the pipeline requires.
You can restrict it further with the `--channels` and `--expires` arguments.

```{warning}
Treat `login.txt` like a password.
Anyone holding this file can publish revisions of your snap.
```

## Add the credentials to your repository

Add the credential to your repository as an encrypted secret:

1. On GitHub, open your repository and go to
   **Settings > Secrets and variables > Actions**.
2. Select **New repository secret**.
3. Set the name to `SNAPSTORE_LOGIN`.
4. Paste the entire content of `login.txt` as the value.
5. Select **Add secret**.

Delete the local file afterward:

```bash
rm login.txt
```

## Create the workflow

Create the file `.github/workflows/snap.yaml` in your repository
with the following content:

```yaml
name: snap

on:
  push:
    branches:
      - main
    tags:
      - '*'
  pull_request:
    branches:
      - main
  workflow_dispatch:

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

Let us break this file down:

- The `on` section triggers the pipeline on pushes to `main`,
  on new tags, on pull requests against `main`
  and on manual triggers from the GitHub web interface.
- The top-level `permissions: {}` denies all `GITHUB_TOKEN` permissions by default.
  The `snap` job grants back `contents: read`,
  the minimum the reusable workflow needs.
- The `uses` keyword calls the reusable
  {ref}`snap <references-snap-ci-snap>` workflow
  hosted in the `canonical/robotics-actions-workflows` repository.
- The `secrets` section forwards the store credential
  you stored in the previous step.

```{note}
This tutorial pins the reusable workflow to the `main` branch
with `@main`.
For production use, pin a specific commit hash instead
to protect your pipeline from upstream changes.
```

Commit the file and push it to a new branch:

```bash
git switch -c add-snap-ci
git add .github/workflows/snap.yaml
git commit -m "ci: add snap CI pipeline"
git push origin add-snap-ci
```

## Verify the build on a pull request

Open a pull request from the `add-snap-ci` branch to `main`.

On the pull request page, the `snap` check starts automatically.
It first builds your snap, then installs it and runs `snap info` on it.
The snap is not published on pull requests.

Once the check succeeds, download the built snap
from the workflow run summary page,
under **Artifacts**.
The artifact name starts with `workflow-build-snap-`.

Install it locally to confirm it works:

```bash
sudo snap install --dangerous <snap-file>
```

Replace `<snap-file>` with the downloaded file name.

Merge the pull request.

## Verify the publication to edge

Merging the PR triggers the pipeline again on the `main` branch.
This time, after the build and test succeed,
the pipeline publishes the snap to the `latest/edge` channel of the Snap Store.

Wait for the workflow run to complete,
then verify the publication:

```bash
snap info <your-snap-name>
```

The output lists a new revision on the `latest/edge` channel.

## Release a candidate

When pushing a git tag to the repository,
it publishes to the `candidate` channel instead of `edge`.

Tag a release on the `main` branch and push the tag:

```bash
git switch -c main
git pull origin main
git tag v0.1.0
git push origin v0.1.0
```

Once the workflow run completes, verify the new revision:

```bash
snap info <your-snap-name>
```

The output now lists the new revision on the `latest/candidate` channel.

## What you have achieved

You now have a complete CI pipeline for your snap:

- Pull requests build and test the snap.
- Pushes to `main` additionally publish the snap to `latest/edge`.
- Tags additionally publish the snap to `latest/candidate`.

## Next steps

- Promote tested revisions from `candidate` to `stable`
  with the {ref}`promote <references-snap-ci-promote>` workflow.
- Monitor upstream projects for new releases with the
  {ref}`upstream-gh-tag-monitor <references-snap-ci-upstream-gh-tag-monitor>`
  workflow.
- Explore all available options in the
  {ref}`Snap CI workflow reference <references-snap-ci>`.
