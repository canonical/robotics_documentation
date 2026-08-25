(how-to-guides-packaging-build-igh-ethercat-cli-snap-from-modified-checkout)=

# Build the IgH EtherCAT CLI snap from a modified checkout

<!-- vale Canonical.400-Enforce-inclusive-terms = NO -->

The [IgH EtherCAT Master](https://gitlab.com/etherlab.org/ethercat) (EtherLab)
is an open-source EtherCAT MainDevice implementation for Linux.
Alongside its kernel modules it ships `ethercat`,
a userspace command-line tool for listing SubDevices,
reading and writing SDOs and diagnosing the bus.
The `ighethercat` snap packages that tool,
together with the `libethercat` userspace library,
so that it can be installed on any snap-enabled Ubuntu system
as a single versioned artifact.

<!-- vale Canonical.400-Enforce-inclusive-terms = YES -->

IgH predates the current EtherCAT terminology,
so its commands and paths still use the older names
(for example `ethercat slaves` and `master/`).
This guide uses MainDevice and SubDevice in prose
and keeps the IgH names where they are literal commands or paths.

The `ighethercat` snap is defined by a Snapcraft recipe, `snap/snapcraft.yaml`,
kept in a fork of the IgH EtherCAT repository.
By default that recipe fetches the upstream `stable-1.6` sources from GitLab,
so any edits you make to the IgH code in your own checkout
are not included in the snap.
This guide shows how to build the `ighethercat` snap from your local checkout instead,
confirm that your change reached the packaged binary,
and install and run the result.
Use it when you are developing or patching the `ethercat` CLI
and want to deploy the modified tool as a snap.

The snap carries only the userspace CLI and library.
The IgH kernel MainDevice, kernel modules and NIC drivers stay on the host,
and the packaged tool talks to it through `/dev/EtherCAT0`:

```text
ighethercat snap                    Ubuntu host
+-----------------------+           +--------------------------+
| ethercat CLI          |           | ec_master kernel module  |
| libethercat userspace | --------> | /dev/EtherCAT0           | --> EtherCAT bus
+-----------------------+           +--------------------------+
```

````{important} Before you start
1. This guide assumes you are familiar with snaps and Snapcraft.
  If you are new to snaps, start with the
  {ref}`snaps and Ubuntu Core tutorials <tutorials-snaps-core-learning-roadmap>`,
  in particular
  [What is a snap?](/tutorials/snaps-core/packaging-ros-application-as-snap.md#what-is-a-snap).
2. Snapcraft and LXD are installed and working on your Ubuntu host,
  as set up in the tutorials above.
3. You have a clone of the IgH EtherCAT repository that contains
  the `ighethercat` snap recipe:

   ```bash
   git clone https://github.com/florcabral/ethercat.git
   cd ethercat
   ```

   The recipe is `snap/snapcraft.yaml`,
   and all commands below run from the repository root.

The artifact checks also use `unsquashfs` and `strings`,
from the `squashfs-tools` and `binutils` packages.

````

## The snap recipe

`snap/snapcraft.yaml` has a single `ethercat` part that pulls the upstream Git source,
runs the IgH `./bootstrap` script,
and builds with the `autotools` plugin using:

```text
--prefix=/usr
--disable-kernel
--disable-eoe
--disable-initd
```

Because kernel support is disabled,
only changes under `tool/` (the CLI) and `lib/` (the userspace library)
affect the snap.
Changes under `master/` or `devices/` are not built into it.

The snap is classic confined so that the CLI can open
the host's custom `/dev/EtherCAT0` device.
It exposes one app, `ighethercat.ethercat`.

## Point the recipe at the local checkout

As committed, the recipe fetches a clean `stable-1.6` tree from GitLab
and ignores edits in your checkout.
In the `ethercat` part of `snap/snapcraft.yaml`, replace:

```yaml
    source: https://gitlab.com/etherlab.org/ethercat.git
    source-type: git
    source-branch: stable-1.6
```

with:

```yaml
    source: .
```

`source-type` and `source-branch` describe Git sources
and must be removed for a local directory.
Snapcraft must be run from the repository root:
`.` then selects the whole repository,
and a path outside the project directory
(such as `..` from inside `snap/`)
is not copied into the LXD build environment.

Give the build a distinguishable version
so the artifact is not confused with a release build, for example:

```yaml
version: '1.6.9-dev1'
```

Keep the snap name unchanged.

## Make your change

Edit the IgH source under `tool/` or `lib/`.

To have a change that is easy to verify without an EtherCAT MainDevice,
add an output line to `CommandVersion::execute()` in `tool/CommandVersion.cpp`,
after the existing `IgH EtherCAT master` line:

```cpp
cout << "Dev build: local IgH source packaged by Snapcraft" << endl;
```

`ethercat version` does not open `/dev/EtherCAT0`,
so this marker lets you test the packaging path independently of hardware state.

Review the changes before building:

```bash
git diff -- snap/snapcraft.yaml tool/
```

## Build the snap

From the repository root:

```bash
snapcraft clean --use-lxd
snapcraft pack --use-lxd
```

Cleaning is required when switching from the remote source to `source: .`,
otherwise a previously pulled upstream tree can be reused.

The result is `ighethercat_1.6.9-dev1_<arch>.snap`,
for example `ighethercat_1.6.9-dev1_amd64.snap`.

## Verify the change reached the snap

Check the packaged metadata:

```bash
unsquashfs -cat ighethercat_1.6.9-dev1_*.snap meta/snap.yaml
```

It should report `version: 1.6.9-dev1` and `confinement: classic`.

Check that the compiled CLI contains the marker:

```bash
unsquashfs -cat ighethercat_1.6.9-dev1_*.snap usr/bin/ethercat \
  | strings \
  | grep -F 'Dev build: local IgH source packaged by Snapcraft'
```

If nothing is printed, see [Troubleshooting](#troubleshooting) before installing.

## Install and run the snap

A locally built snap is unsigned, and this one is classic confined,
so installation needs both `--dangerous` and `--classic`:

```bash
sudo snap install --dangerous --classic ./ighethercat_1.6.9-dev1_*.snap
```

```{warning}
`--dangerous` skips Snap Store signature verification
and classic confinement gives the application broad host access.
Only install local snaps you built yourself or received from a trusted source.
```

If a previous local revision of `ighethercat` is installed,
remove it first with `sudo snap remove ighethercat`.

Run the CLI through its snap-qualified name
so an `ethercat` binary installed on the host cannot be selected by mistake:

```bash
snap run ighethercat.ethercat version
```

Expected output:

```text
IgH EtherCAT master 1.6.9 unknown
Dev build: local IgH source packaged by Snapcraft
```

`unknown` is expected:
IgH derives the revision from a generated `revision` file or `git describe`,
neither of which is available in a local-source build.

## Connect to an EtherCAT bus

Bus commands need a running IgH MainDevice on the host.
Check that its device exists:

```bash
test -e /dev/EtherCAT0 && echo 'EtherCAT device is available'
```

Then use the packaged CLI as usual, for example:

```bash
snap run ighethercat.ethercat slaves
snap run ighethercat.ethercat sdos --position 0
snap run ighethercat.ethercat upload --position 0 --type uint32 0x1000 0
```

Avoid `download`, register writes, state changes and SII writes
unless you understand the target hardware and how to recover it.

## Rebuild after further changes

After editing more files under `tool/` or `lib/`,
rebuild only the `ethercat` part
instead of discarding the whole build environment:

```bash
snapcraft clean ethercat --use-lxd
snapcraft pack --use-lxd
```

Bump the `version` in `snap/snapcraft.yaml`
when you need artifacts that can coexist.
Do a fully clean build (`snapcraft clean --use-lxd`) before a release
to rule out cached inputs.

## Restore the release recipe

If the local-source changes are not meant to be committed, restore them:

```bash
git restore snap/snapcraft.yaml tool/CommandVersion.cpp
```

The recipe then fetches `stable-1.6` from upstream again.

## Troubleshooting

### The marker is missing from the snap

Confirm that the `ethercat` part contains exactly `source: .`
with no `source-type` or `source-branch` lines,
then run a full clean and rebuild:

```bash
snapcraft clean --use-lxd
snapcraft pack --use-lxd
```

### Snapcraft cannot access LXD

Confirm that your user can run `lxc list`.
If you were just added to the `lxd` group,
log out and back in before retrying.

### Installation says classic confinement is required

Install with both flags:

```bash
sudo snap install --dangerous --classic ./ighethercat_*.snap
```

### `slaves` cannot open `/dev/EtherCAT0`

The snap does not provide or start the kernel MainDevice.
Configure and start a compatible IgH MainDevice on the host
and check that `/dev/EtherCAT0` exists.
`ethercat version` works without the device.

### The CLI reports an ioctl version mismatch

The userspace CLI and the host kernel MainDevice
must use compatible ioctl API versions.
Build the CLI from an IgH revision that matches the host MainDevice,
or use a matching host MainDevice.
