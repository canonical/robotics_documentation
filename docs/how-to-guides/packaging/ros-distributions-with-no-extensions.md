ROS distributions with no extensions
====================================

The snapcraft ROS extensions help you snap ROS applications for the different ROS distributions. However, this does not mean that you cannot build a snap for a ROS distribution that does not have a dedicated extension. In this document, you will see how to do that.

## How to snap a ROS application without extension?

The ROS extensions facilitate the deployment of ROS applications with snaps. What does a ROS extension do?

ROS extensions, as all other snapcraft extensions, factorize some of the YAML entries found in the snapcraft.yaml file that are common and necessary for building ROS applications. For ROS extensions these entries are,

* The ROS APT package repository and its GPG key.
* The following build-packages:
  * ros-ROS-DISTRO-ros-environment
  * ros-ROS-DISTRO-ros-workspace
  * ros-ROS-DISTRO-ament-index-cpp
  * ros-ROS-DISTRO-ament-index-python
* The build-environment variables:
  * ROS_VERSION = ros-version
  * ROS_DISTRO = ros-distro
* The command-chain command script which takes care of sourcing the ROS environment prior to launching your application.

All of these additional YAML entries can be revealed from your snapcraft.yaml file with the command `snapcraft expand-extensions`.

With this in mind, let us see how you can replicate what the extension is doing for other ROS distributions.

> ℹ️ Core18 does not support Snapcraft Extensions. If you are developing a ROS snap based on ROS Melodic distro, then all the extensions entries are handled by the [catkin plugin](https://snapcraft.io/docs/catkin-plugin#heading--core18). To check an example see the core18 example [here](https://snapcraft.io/docs/ros-applications).

## Writing the snap

As an example, the process of creating a simple talker-listener snap based on ROS 2 Galactic will be shown hereafter.

### Building ROS

ROS installation requires the following steps:

* adding the ROS package repositories
* setting up the GPG keys
* installing the ROS Debian package
* source ROS workspace

Let’s see how to achieve each step with Snaps.

Adding the required package repository and setting up the keys is done by using the Snapcraft [package repository keyword](https://snapcraft.io/docs/package-repositories) as follows:

```
# Add ROS 2 repository
package-repositories:
  - components: [main]
    formats: [deb]
    key-id: C1CF6E31E6BADE8868B172B4F42ED6FBAB17C654
    key-server: keyserver.ubuntu.com
    suites: [focal]
    type: apt
    url: http://repo.ros2.org/ubuntu/main
```

Now, let’s proceed to install the ROS Debian packages. The ROS Debian packages are installed by defining a snap [part](https://snapcraft.io/docs/snapcraft-yaml-schema). Snap parts are recipes to build a piece of software and are driven via [plugins](https://snapcraft.io/docs/snapcraft-plugins). For ROS, you solely want to install the ROS Debian package, no source code involved, you can use the [nil plugin](https://snapcraft.io/docs/nil-plugin) as follows:

```
parts:
  ros2-galactic-extension:
    plugin: nil
```

To add the packages that are needed to build our ROS project you can use the build-packages keyword, which allows for the installation of build-time dependencies. You can learn more about [build and staging dependencies](https://snapcraft.io/docs/build-and-staging-dependencies) in the documentation. For a ROS project, the bare minimum packages required are those setting up a ROS workspace, hence they are added to the list of build-packages as follows:

```
parts:
  ros2-galactic-extension:
    plugin: nil
    build-packages:
      - ros-galactic-ros-environment
      - ros-galactic-ros-workspace
      - ros-galactic-ament-index-cpp
      - ros-galactic-ament-index-python
```

It’s important to emphasize that build-packages are only used for building and won’t be packaged in the final snap.

Finally, the ROS workspace has to be sourced for ROS applications to run. To ease this process, snapcraft provides a [script](https://github.com/snapcore/snapcraft/blob/main/extensions/ros2/launch) to do so. You can pull the script from the snapcraft source and install it. Following the example above, the ros2-galactic-extension will look like this:

```
parts:
  ros2-galactic-extension:
    plugin: nil
      build-packages:
        - ros-galactic-ros-environment
        - ros-galactic-ros-workspace
        - ros-galactic-ament-index-cpp
        - ros-galactic-ament-index-python
      override-build: |
        install -D -m 0755 $SNAP/share/snapcraft/extensions/ros2/launch ${SNAPCRAFT_PART_INSTALL}/snap/command-chain/ros2-launch
```

Read more about [overriding the build step](https://snapcraft.io/docs/overrides) in the documentation. This is the process to set up ROS in a snap, and the process is the same for every ROS distribution.

### Building the demo application

Now that ROS has been dealt with, let’s proceed with building the ROS application source code. This is done by creating a new snap part. ROS 2 provides some demos in the [demos GitHub repository](https://github.com/ros2/demos.git). ROS packages are built by cloning the source code, installing its dependencies via rosdep and compiled with colcon. In snapcraft, all of this is handled via the [colcon plugin](https://snapcraft.io/docs/colcon-plugin) which you can add to the part as follows:

```
ros-demos:
  after: [ros2-galactic-extension]
  plugin: colcon
  source: https://github.com/ros2/demos.git
  source-branch: galactic
  source-subdir: demo_nodes_cpp
```

Our application requires the roslaunch package as a run dependency however this is not included as a `run_dependency` in the package.xml file of our example Therefore, you need to also include it in the part by using the stage-packages keyword as follows:

```
ros-demos:
  after: [ros2-galactic-extension]
  plugin: colcon
  source: https://github.com/ros2/demos.git
  source-branch: galactic
  source-subdir: demo_nodes_cpp
  stage-packages: [ros-galactic-ros2launch]
```

Finally, for the part to install all the correct dependencies versions and build, it is necessary to define the ROS version and distro. This is done by defining the build-environment variables as follows:

```
# Define the ROS 2 environment variable necessary for install and build time
build-environment:
  - ROS_VERSION: '2'
  - ROS_DISTRO: galactic
```

This is it, you can now proceed in defining the application that will be launched by your snap.

### Running the application

When deploying a ROS application you can identify three main components that must be defined:

* command; launch file or node to be run
* enabling access to the necessary host resources (such as cameras, GPIO pins, network connections, and drivers), defining the launch file or rosnode to run
* sourcing ROS and the workspace

Snaps effectively allows you to define and isolate the pieces of your application that you want to expose to the rest of the system via the [apps](https://snapcraft.io/docs/snapcraft-yaml-schema) tag.

After having identified the command that launch your application you can add it with the command keyword as follows:

```
apps:
  ros2-talker-listener:
  command: opt/ros/galactic/bin/ros2 launch demo_nodes_cpp talker_listener.launch.py
```

By default, snap applications are confined and are not allowed to access any of the host resources. [Interfaces and plugs](https://snapcraft.io/docs/interface-management) allow the user to define the resources on the host that the application will have access to. You can have a look at the list of [supported interfaces](https://snapcraft.io/docs/supported-interfaces).

For a generic ROS application that communicates with other ROS components via topics, you will need the “network” plug to grant the snap access to the host’s network, and also the “network-bind” plug, which provides the snap with the ability to bind to a specific IP address and port as required for ROS communication. You can add those to the application as follows:

```
apps:
  ros2-talker-listener:
    command: opt/ros/galactic/bin/ros2 launch demo_nodes_cpp talker_listener.launch.py
    plugs: [network, network-bind]
```

In order to source the ROS environment, you can use the command-chain keyword, which allows us to list commands to be executed before our main command. In this case, you will execute the script that was pulled in the Snap in the ROS part as follows:

```
apps:
  ros2-talker-listener:
    command-chain: [snap/command-chain/ros2-launch]
    command: opt/ros/galactic/bin/ros2 launch demo_nodes_cpp talker_listener.launch.py
    plugs: [network, network-bind]
```

Finally, to run the application it is necessary to source the ROS environment and define the necessary ROS variables such as the PYTHONPATH, ROS_DISTRO, ROS_VERSION:

```
environment:
  PYTHONPATH: $SNAP/opt/ros/galactic/lib/python3.8/site-packages:$SNAP/usr/lib/python3/dist-packages:${PYTHONPATH}
  ROS_DISTRO: galactic
  ROS_VERSION: '2'
```

This is it, now you can run your ROS application with snap. You can look at the full snapcraft.yaml file described in this document [here](https://github.com/ubuntu-robotics/ros-snaps-examples/blob/main/non_lts_galactic/snap/snapcraft.yaml).

## See also

* [Snapcraft ROS Noetic extension](https://snapcraft.io/docs/ros-noetic): The Snapcraft extension to snap ROS Noetic applications.
* [Snapcraft ROS Foxy extension](https://snapcraft.io/docs/ros2-foxy-extension): The Snapcraft extension to snap ROS Foxy applications.
* [Snapcraft ROS Humble extension](https://snapcraft.io/docs/ros2-humble-extension): The Snapcraft extension to snap ROS Humble applications.
* [Snapcraft supported extensions](https://snapcraft.io/docs/supported-extensions): Complete list of Snapcraft extensions available to developers.
