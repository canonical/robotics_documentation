(tutorials-snaps-core-building-ros-snaps-with-content-sharing)=

# Part 4: Build ROS snaps with content sharing

The {ref}`Part 2 snap <tutorials-snaps-core-packaging-complex-robotics-software-with-snaps>`
ships the drivers, navigation stack and teleoperation together. A keyboard
controller does not need the lidar driver or the maps. In this tutorial you
will move the keyboard node into its own snap and share a Lyrical runtime
instead of shipping another copy of ROS with it.

## Build a standalone controller first

On Ubuntu 26.04, create a project containing the {download}`teleoperation
recipe <examples/turtlebot3-teleop/snap/snapcraft.yaml>` at
`snap/snapcraft.yaml`. The upstream package is `ament_python`; its entry
point is installed under `opt/ros/snap/lib/turtlebot3_teleop`, not in the
base system's PATH.

```{literalinclude} examples/turtlebot3-teleop/snap/snapcraft.yaml
:language: yaml
```

For a baseline, temporarily replace `ros2-lyrical-ros-base` with
`ros2-lyrical` in the recipe. From the project directory:

```bash
export SNAPCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=1
arch=$(dpkg --print-architecture)
snapcraft pack --use-lxd
mv "turtlebot3-lyrical-teleop_0.1_${arch}.snap" standalone.snap
```

## Build with a shared runtime

Restore `ros2-lyrical-ros-base` in the recipe. The extension adds a build-time
SDK for colcon and a runtime content plug whose default provider is
`ros-lyrical-ros-base`. The two have different jobs: the SDK is not required
on the robot. Inspect the configuration rather than copying a mount path
from another ROS distribution:

```bash
snapcraft expand-extensions
snapcraft pack --use-lxd
ls -lh standalone.snap "turtlebot3-lyrical-teleop_0.1_${arch}.snap"
```

Compare the two files on the same architecture. A smaller consumer does not
by itself mean a smaller installation: count the provider once per device,
not once per consumer.

## Connect and test

On the target, install the provider and your shared controller:

```bash
sudo snap install ros-lyrical-ros-base
sudo snap install --dangerous "./turtlebot3-lyrical-teleop_0.1_$(dpkg --print-architecture).snap"
snap connections turtlebot3-lyrical-teleop
```

If the content plug's slot is `-`, connect it explicitly:

```bash
sudo snap connect turtlebot3-lyrical-teleop:ros-lyrical-ros-base ros-lyrical-ros-base:ros-lyrical-ros-base
```

Start the Part 2 simulation but **not** its keyboard app. Run
`turtlebot3-lyrical-teleop.key` in a terminal. Confirm that the robot
responds and that stopping teleoperation stops command publication. The
content interface supplies files; it does not transport `/cmd_vel`. The two
processes still need the same ROS domain and compatible DDS settings.

You can now update the controller without updating the drivers. Keep using
the Part 2 snap for bringup, mapping and navigation; only run one keyboard
publisher. The next tutorial seeds both application snaps and the shared
runtime into a Raspberry Pi image.
