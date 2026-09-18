# Choose a ROS 2 development environment

ROS 2 developers can work directly on a host or use several kinds of managed
development environment.
Each approach makes a different trade-off between host
integration, isolation, reproducibility, platform coverage,
and operational complexity.

This explanation compares [Workshop](https://ubuntu.com/workshop/docs/)
with a bare-metal workspace,
Vagrant, Docker, Dev Containers, and Pixi.
It compares their general ROS 2 and IDE integration, ease of use,
reproducibility, main benefits, and limitations.

In this comparison, reproducibility means that the environment is controlled
and minimally affected by the host, not that every environment is identical.

## Quick comparison

<!-- pyml disable-num-lines 8 line-length -->
| Approach | ROS 2 support | Main benefit | Main limitation |
| --- | --- | --- | --- |
| [Workshop](#workshop-main-benefits-and-limitations) | Canonical's ROS 2 SDKs | Integrated Ubuntu environment with controlled host access | No macOS or Windows support |
| [Bare metal](#workshop-compared-with-bare-metal) | Official ROS 2 packages | Direct access to devices, graphics, and networking | Cannot use multiple ROS 2 LTS releases simultaneously |
| [Docker](#workshop-compared-with-docker) | Official ROS container images | Mature images, CI, and ecosystem | Requires manual setup of all integrations, device access, GUIs, and networking |
| [Dev Containers](#workshop-compared-with-dev-containers) | No dedicated support; can use the official ROS 2 Docker images | Declarative configuration and strong editor-integrated onboarding | Runtime behaviour and specification support depend on the backend |
| [Pixi](#workshop-compared-with-pixi) | ROS 2 packages provided by RoboStack | Lightweight, lock-file-based cross-platform environments | No OS isolation and ROS 2 dependencies use the Conda and RoboStack ecosystem |
| [Vagrant](#workshop-compared-with-vagrant) | No dedicated support | Reproducible environment with VM-level isolation when using a VM provider | Resource use and host, device, network, and IDE integration depend on the provider and box |

## Workshop: main benefits and limitations

**Main benefits:**

- Runs multiple Ubuntu-based development environments that can be discarded and recreated.
- Simplifies access to selected host devices and desktop resources via [interfaces](https://ubuntu.com/workshop/docs/explanation/interfaces/concepts/).
- Supports CLI workflows, [VS Code extension](https://ubuntu.com/workshop/docs/how-to/develop-with-workshops/connect-vscode/#how-vscode-connect-remote)
  and editor workflows over SSH.
- Adds low overhead thanks to LXD system containers.

**Limitations:**

- Supports Linux and WSL2, but not native macOS or Windows.
- Places ROS 2 nodes behind a virtual network by default.
  See [ROS 2 networking with Workshop](../../how-to-guides/development/ros2-networking-workshop.md)
  for supported communication topologies.
- May require explicit connections for privileged host resources,
  and mounts may need to be remounted to the desired host location.

## Workshop comparison

The following sections compare Workshop with each alternative in more detail,
covering only the aspects relevant to each comparison.

(workshop-compared-with-bare-metal)=

### Workshop compared with bare metal

Bare metal provides direct access to hardware and networking, but shares host
state and makes supporting multiple ROS 2 LTS releases and reproducing
environments difficult.

<!-- pyml disable-num-lines 7 line-length -->
| Aspect | Workshop | Bare metal |
| --- | --- | --- |
| *ROS 2* | Runs any ROS 2 distribution in its own Ubuntu, independently of the host version | Uses binary packages for ROS 2 releases supported by the host Ubuntu release |
| *Environment lifecycle* | Keeps project dependencies inside refreshable, disposable environments | Installs dependencies on the shared host, where state accumulates and requires manual maintenance |
| *Hardware & GUI access* | Explicitly exposes selected host devices and desktop resources | Provides direct access to devices and graphics |
| *Networking* | Exposed to the host through an LXD bridge | Uses the host LAN interfaces directly |
| *Reproducibility* | Workshop definition controls the base, SDKs, and integrations | Requires installation automation or a managed host image |

(workshop-compared-with-docker)=

### Workshop compared with Docker

Docker provides repeatable images and a mature ecosystem,
but requires manual setup for integrations, devices, GUIs, and networking.

<!-- pyml disable-num-lines 8 line-length -->
| Aspect | Workshop | Docker |
| --- | --- | --- |
| *Environment model* | Development-focused Ubuntu system container | Container created to run an application |
| *ROS 2* | Provided by ROS 2 SDKs | Official ROS images |
| *Hardware & GUI access* | Standardised through [Workshop interfaces](https://ubuntu.com/workshop/docs/explanation/interfaces/concepts/) | Configured through devices, capabilities, mounts, sockets, etc |
| *Environment lifecycle* | Launch, refresh, and restore lifecycle | Requires recreating the container and defining runtime configuration in Docker Compose or equivalent |
| *Deployment alignment* | Reproduces the target Ubuntu deployment environment | Strong alignment with CI and deployment images |
| *Host* | Linux with snapd and WSL2 | Linux, macOS, and Windows, depending on Docker Engine support |

(workshop-compared-with-dev-containers)=

### Workshop compared with Dev Containers

Dev Containers provide declarative configuration and strong editor-integrated onboarding,
but runtime behaviour and specification support depend on the selected backend.

<!-- pyml disable-num-lines 8 line-length -->
| Aspect | Workshop | Dev Containers |
| --- | --- | --- |
| *Environment definition* | Workshop definition and SDK channels | `devcontainer.json`, and an image or Dockerfile |
| *Runtime model* | LXD system container managed by Workshop | Behaviour comes from the selected container backend (mostly Docker) |
| *ROS 2* | Provided by ROS 2 SDKs | Can use the official ROS images |
| *IDE integration* | CLI, VS Code extension, and SSH-based editor workflows | Strong editor-integrated onboarding with VS Code |
| *Hardware & GUI access* | Standardised through [Workshop interfaces](https://ubuntu.com/workshop/docs/explanation/interfaces/concepts/) | Requires maintaining custom configurations in `devcontainer.json` |
| *Host* | Linux with snapd and WSL2 | Same host support as the selected container runtime, plus browser-based environments through GitHub Codespaces |

To get the best experience with Workshop and VS Code,
see the [Workshop VS Code documentation](https://ubuntu.com/workshop/docs/how-to/develop-with-workshops/connect-vscode/#how-vscode-connect-remote).

(workshop-compared-with-pixi)=

### Workshop compared with Pixi

Pixi offers lightweight, cross-platform environments,
but provides no OS isolation and uses the Conda and RoboStack ecosystem
rather than Ubuntu packages and `rosdep`.
On Linux,
some packages require minimum host `glibc` and kernel versions,
which can prevent the environment from running on older hosts.

<!-- pyml disable-num-lines 10 line-length -->
| Aspect | Workshop | Pixi |
| --- | --- | --- |
| *Environment model* | Ubuntu-based system container | Cross-platform package environment |
| *ROS 2* | Provided by ROS 2 SDKs | Only the subset of ROS 2 packages from the RoboStack ecosystem |
| *Reproducibility* | Workshop definition and SDK channels | Manifest and lock file |
| *Host* | Linux with snapd and WSL2 | Linux, macOS, and Windows on supported architectures |
| *Hardware & GUI access* | Explicitly exposed from the host | Direct host access |
| *Networking* | Exposed to the host through an LXD bridge | Direct host access |
| *Isolation* | OS-level environment boundary | No OS-level isolation boundary |
| *IDE integration* | CLI, VS Code extension, and SSH-based editor workflows | Native editor integrations |

(workshop-compared-with-vagrant)=

### Workshop compared with Vagrant

Vagrant offers containers or VMs for isolation.
Access to hardware, network,
and IDE integration depend on the selected provider and the user's Vagrantfile.
Vagrant does not provide or maintain any ROS 2 boxes,
so the entire ROS 2 environment must be provisioned and maintained manually.

<!-- pyml disable-num-lines 9 line-length -->
| Aspect | Workshop | Vagrant |
| --- | --- | --- |
| *Isolation* | LXD system container | Usually a VM, provider-dependent |
| *ROS 2* | Provided by ROS 2 SDKs | No official ROS 2 boxes, must be maintained manually |
| *Environment lifecycle* | Refreshable and resettable workshops | VM lifecycle managed through Vagrant commands |
| *Hardware & GUI access* | Explicit interface connections | USB, PCI, graphics, and networking depend on the provider |
| *Networking* | Exposed to the host through an LXD bridge | Must be configured in the `Vagrantfile`; available networking modes depend on the selected provider |
| *Host* | Linux with snapd and WSL2 | Depends on provider, host architecture, and box availability |
| *IDE integration* | CLI, VS Code extension, and SSH-based editor workflows | Usually remote development over SSH |

