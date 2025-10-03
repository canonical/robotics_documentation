# The `ros2` SDK

The `ros2` SDK is used to set up a ROS 2 development environment.

In Workshop, it sets up a bare minimum ROS 2 environment
before also attempting to install the project dependencies using Rosdep.
We detail hereafter what the `ros2` SDK contains and what does it configure.

## How it works

The `ros2` SDK retrieves the ROS 2 GPG key from the Ubuntu key server and
sets up the ROS 2 repository.

It then installs the following packages:

- ros-dev-tools
- python3-colcon-argcomplete
- python3-colcon-alias
- python3-colcon-clean
- python3-colcon-mixin
- ros-${ROS_DISTRO}-ros-environment
- ros-${ROS_DISTRO}-ros-workspace
- ros-${ROS_DISTRO}-ament-index-cpp
- ros-${ROS_DISTRO}-ament-index-python
- ros-${ROS_DISTRO}-ros2run
- ros-${ROS_DISTRO}-ros2launch

And initializes Rosdep.

It then configures Colcon's auto-completion as well as its default
`~/.colcon/defaults.yaml` configuration file and
retrieve and configures the default Colcon mixins.

The SDK sets up the ROS 2 workspace at `~/workspace/src` and
automatically source the ROS 2 installation in `~/.profile`.

Last but not least,
it installs the project dependencies using `rosdep install`.

## Example

Please refer to the tutorial
['ROS 2 development using Workshop'](../tutorials/ros-2-dev-workshop.md)
for a complete example of using the `ros2` SDK.
