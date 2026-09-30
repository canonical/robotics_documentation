(how-to-guides-packaging-build-igh-ethercat-cli-snap-from-modified-checkout)=

# Build the IgH EtherCAT CLI snap from a modified checkout

By the end of this guide, you will have built the `ighethercat` snap
from a local checkout of the IgH EtherCAT source containing your own changes,
installed and run it on your host.

````{important} Before you start, you'll need:

- Familiarity with snaps and Snapcraft
  (see the {ref}`snaps and Ubuntu Core tutorials <tutorials-snaps-core-learning-roadmap>`).
- Snapcraft and LXD installed and operational on your host.
- Your own checkout of the IgH EtherCAT source (`stable-1.6`)
  containing the changes you want to package.
  All commands below must be run from its root directory.
````

<!-- vale Canonical.400-Enforce-inclusive-terms = NO -->
<!-- "IgH EtherCAT Master" is the upstream project's official name, so the
     master/slave inclusive-terms check is disabled for this paragraph only. -->

The [IgH EtherCAT Master](https://gitlab.com/etherlab.org/ethercat) (EtherLab)
is an open-source EtherCAT MainDevice implementation for Linux.
Alongside its kernel modules, it ships `ethercat`,
a user-space command-line tool for listing SubDevices,
reading and writing SDOs, and diagnosing the bus.
The `ighethercat` snap packages that tool
along with the `libethercat` user-space library,
allowing it to be installed like any snap
as a single versioned artifact.

<!-- vale Canonical.400-Enforce-inclusive-terms = YES -->

```{note}
IgH predates the current EtherCAT terminology,
so its commands and paths still use the older names
(for example `ethercat slaves` and `master/`).
This guide uses MainDevice and SubDevice in prose
and keeps the IgH names where they are literal commands or paths.
```

The snap contains only the user-space CLI and library.
The IgH kernel MainDevice, kernel modules, and NIC drivers remain on the host,
and the packaged tool communicates with it via `/dev/EtherCAT0`:

```text
ighethercat snap                    Ubuntu host
+-----------------------+           +--------------------------+
| ethercat CLI          |           | ec_master kernel module  |
| libethercat userspace | <-------> | /dev/EtherCAT0           | <-> EtherCAT bus
+-----------------------+           +--------------------------+
```

## Add the snap recipe

Save the following as `snap/snapcraft.yaml` in the root of your IgH checkout:

```yaml
name: ighethercat
base: core24
version: '1.6.9-dev1'
summary: IgH EtherCAT command-line tool (CLI) for SDO access and bus diagnostics
description: |
  The ethercat command-line tool and libethercat userspace library from the
  IgH EtherCAT Master. It needs a running IgH kernel MainDevice on the host,
  reachable through /dev/EtherCAT0.
license: GPL-2.0+
grade: stable
confinement: strict

plugs:
  ethercat-master:
    interface: custom-device
    custom-device: ethercat-master

slots:
  ethercat-master-slot:
    interface: custom-device
    custom-device: ethercat-master
    devices:
      - /dev/EtherCAT[0-9]*
    udev-tagging:
      - kernel: EtherCAT[0-9]*
        subsystem: EtherCAT

parts:
  ethercat:
    plugin: autotools
    source: .
    override-build: |
      ./bootstrap
      craftctl default
    autotools-configure-parameters:
      - --prefix=/usr
      - --disable-kernel
      - --disable-eoe
      - --disable-initd
    build-packages:
      - autoconf
      - automake
      - libtool
      - pkg-config
      - build-essential
    build-attributes:
      - enable-patchelf

apps:
  ethercat:
    command: usr/bin/ethercat
    plugs:
      - ethercat-master
```

The `ethercat` part builds the checkout it lives in (`source: .`)
using the `autotools` plugin, after running the IgH `./bootstrap` script.
Kernel support is disabled,
so only changes under `tool/` (the CLI) and `lib/` (the user-space library)
affect the snap;
changes under `master/` or `devices/` are not included in the build.
The snap is strictly confined and exposes one app, `ighethercat.ethercat`.
Its [`custom-device` interface](https://snapcraft.io/docs/reference/interfaces/custom-device-interface/)
grants access exclusively to the host's `/dev/EtherCATn` character devices.
The matching slot lets you connect the interface locally without a gadget snap.
Unlike a filesystem-only interface,
`custom-device` grants both AppArmor and device control group access to matching devices.

## Build the snap

After making your changes, from the repository root, run:

```bash
snapcraft pack
```

The result is `ighethercat_1.6.9-dev1_<arch>.snap`,
for example `ighethercat_1.6.9-dev1_amd64.snap`.
After making further edits under `tool/` or `lib/`, run `snapcraft pack` again.

## Install, connect and run the snap

A locally built snap is unsigned,
so installation requires `--dangerous`:

```bash
sudo snap install --dangerous ./ighethercat_1.6.9-dev1_*.snap
```

Connect the `custom-device` plug to the snap's matching slot:

```bash
sudo snap connect \
  ighethercat:ethercat-master \
  ighethercat:ethercat-master-slot
```

The manual connection keeps the snap strictly confined
while permitting access to `/dev/EtherCATn`.
`custom-device` is a [super-privileged interface](https://snapcraft.io/docs/explanation/interfaces/super-privileged-interfaces/#reference-operations-interfaces-super-privileged-interfaces),
so distributing this snap through the Snap Store
and making the connection automatic requires Store review.

Run the CLI using its snap-qualified name
so an `ethercat` binary installed on the host is not selected by mistake:

```bash
snap run ighethercat.ethercat version
```

Expected output:

```text
IgH EtherCAT master 1.6.9 unknown
```

`unknown` is expected:
IgH derives the revision from a generated `revision` file or `git describe`,
neither of which is available in a local-source build.

## Connect to an EtherCAT bus

Bus commands need a running IgH MainDevice on the host.
First, check that the interface is connected and its device exists:

```bash
snap connections ighethercat
test -e /dev/EtherCAT0 && echo 'EtherCAT device is available'
```

Then use the packaged CLI as usual, for example:

```bash
snap run ighethercat.ethercat slaves
snap run ighethercat.ethercat sdos --position 0
snap run ighethercat.ethercat upload --position 0 --type uint32 0x1000 0
```

Avoid SDO writes (`ethercat download`), register writes, state changes, and SII writes,
unless you understand the target hardware and how to recover it.

## Troubleshooting

### Your change is missing from the installed snap

Confirm that `snap/snapcraft.yaml` is in the root of your checkout
and that you ran Snapcraft from there,
then run a full clean and rebuild:

```bash
snapcraft clean
snapcraft pack
```

### The CLI reports an ioctl version mismatch

```{warning}
The user-space CLI and the host kernel MainDevice
must use compatible ioctl API versions.
Build the CLI from an IgH revision that matches the host MainDevice,
or use a matching host MainDevice.
```

For general Snapcraft and snap installation problems,
see the {ref}`snap FAQ and troubleshooting page <reference-snapcraft-faq-troubleshooting>`.
