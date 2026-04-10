# Get started with ROS 2 snaps

When creating a snap for a ROS 2 application (or any snap for that matter),
the very first step is to create a `snapcraft.yaml` file for the project and
file it up with some boilerplate before we can actually get to the specifics
of the project at hand.
In the case of ROS 2-based applications,
we can actually make use of a template to get us started faster.

```{note}
If you are new to the whole topic of creating snaps for ROS 2 applications,
I'd encourage you to start with the tutorial series:
{doc}`From zero to hero: deploy a robot with snaps and Ubuntu Core </tutorials/snaps-core/index>`.
as this particular how-to touches on one single specific aspect:
creating the `snapcraft.yaml` file from a template.
```

To get started with ROS 2 snaps and create a `snapcraft.yaml` from the template,
use the command:

```bash
snapcraft init --name my-ros2-project --profile ros2
```

This command will generate the `snapcraft.yaml` file
inside a `snap` folder in the current directory:

```bash
$ tree
.
└── snap
    └── snapcraft.yaml
```

This is nice and all, but simply creating a file is not all that interesting.
The real value lies in that said file is
a functioning snap recipe for an actual ROS 2 demo.

Let us see what it contains:

```yaml
# The name of the snap.
name: my-ros2-project
# Just for humans, typically '1.2+git' or '1.3.2'
version: "0.0.1"
# 79 char long summary
summary: Single-line elevator pitch for your amazing snap
description: |
  This is my-ros2-project's description. You have a paragraph or two to tell the
  most important story about your snap. Keep it under 100 words though,
  so that it looks good in the snap store.

# The base snap is the runtime environment for this snap.
# Each ROS 2 LTS distribution has a corresponding base in the core** series.
# View the compatible bases at:
# https://documentation.ubuntu.com/snapcraft/stable/reference/extensions/ros-2-extensions
base: core24

# use 'strict' once you have the right plugs and slots
confinement: devmode
# must be 'stable' to release into candidate/stable channels
grade: devel

# The applications exposed by the snap.
apps:
  ros2-talker-listener:
    command: ros2 launch demo_nodes_cpp talker_listener.launch.py
    # The ROS extensions establish common settings for all ROS snaps.
    # Learn more about it at https://canonical-robotics.readthedocs-hosted.com/en/latest/references/snapcraft/extensions/
    extensions: [ros2-jazzy-ros-core]

# The parts to build the snap.
parts:
  ros-demos:
    # The colcon plugin builds parts for ROS 2.
    # Learn more about the plugin at https://documentation.ubuntu.com/snapcraft/stable/reference/plugins/colcon_plugin
    plugin: colcon
    source: https://github.com/ros2/demos.git
    source-branch: jazzy
    source-subdir: demo_nodes_cpp
```

The recipe comes with most expected directives pre-filed with default values
that are informative and commented.
Note that the template packages a talker-listener demo from the upstream `ros2/demos`
GitHub repository.
It retrieves the source code from a specific branch and packages only a sub-directory
of this large collection of demos.
It then invokes a plain `ros2 launch` command to start the talker-listener demo.
The last point to which I would like to draw your attention to is that this template
uses `core24` and ROS 2 Jazzy.
If you are targeting ROS 2 Lyrical instead, replace `core24` with `core26` and swap
the extension and branch name from `ros2-jazzy-ros-core` / `jazzy` to
`ros2-lyrical-ros-core` / `lyrical`.
Should you be using a different ROS 2 distribution,
you will find links to the documentation right at your fingertip to help you
in your endeavor.
