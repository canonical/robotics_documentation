(tutorials-snaps-core-building-ros-snaps-with-content-sharing)=

# Part 4: Building ROS snaps with content sharing

## How to use this developer guide

In {ref}`part 2 <tutorials-snaps-core-packaging-complex-robotics-software-with-snaps>`
of our developer guide series,
we saw in fine detail how to create a single snap for a complete robot stack,
including things like controllers, sensor drivers,
but also functionalities such as autonomous navigation.

While {ref}`part 3 <tutorials-snaps-core-distribute-ros-apps-with-snap-store>`
of our series focused on the snap store and the snap release process,
this developer guide, part 4,
draws from the example shown in part 2 to exemplify one specific feature of snaps,
[content sharing](https://snapcraft.io/docs/content-interface).
We will therefore revisit the entire example in order
to make use of this feature – after introducing it, of course.

This guide is meant for ROS snap beginners and
advanced users looking for insights and
guidelines on implementing ROS snap content sharing.
This is not a quick tutorial, but rather an in-depth guide.
Furthermore, these steps assume that you have completed {ref}`part 2 <tutorials-snaps-core-packaging-complex-robotics-software-with-snaps>`
of this series.

## Packaging complex robotics software with multiple snaps

We have established in {ref}`part 2 <tutorials-snaps-core-packaging-complex-robotics-software-with-snaps>`
the importance of packaging your applications for deployment.
We also demonstrated this packaging by building a single snap
that contains the entire software stack for the TurtleBot 3.
While this monolithic solution is convenient,
it also has several drawbacks such as its size and
the resultant resources it consumes when installed and updated.
More importantly, it also ties the whole stack to a specific robot model.

Ideally, parts of the entire software stack should be reusable on other robot models;
the teleoperation application and the navigation stack are two such examples.
This could be achieved by breaking down the monolithic design into several smaller snaps,
each enabling a specific functionality.

For instance, we could design a single robot-specific snap,
containing all of the robot-specific stack components such as drivers,
controllers, robot model and so on.
Alongside this snap we can add a plethora of other snaps which are robot agnostic,
each enabling a given functionality.
These snaps could then be used on a variety of different robots,
potentially varying only slightly in their configuration.

This multi-snap design is exactly the theme of this guide.
For a detailed comparison of the [different architectures with snaps](#explanations-snaps-ros-architectures-with-snaps)
you can check the documentation.

## Rationalising a multi-snap deployment with content sharing

A snap being self-contained is a powerful feature.
But sharing resources, such as the same ROS packages, can also be useful.
Not only does sharing avoid duplication,
it also helps to ensure related applications share the same version of the ROS stack.

Such design – sharing a common set of libraries among multiple snaps –
is readily available through a feature called content sharing.
However, using it is anything but straightforward.
We must make sure that all dependencies are available
at build time but not shipped in the final artefact.
We must also make sure that the `ROS workspaces` are properly sourced,
wherever they are and whenever they are needed. This can quickly become a headache.

Fortunately, new ROS extensions for snapcraft have been
developed precisely to enable seamless content sharing.
We’ll be using those extensions in this guide.

## What we will learn

Just like in {ref}`part 2 <tutorials-snaps-core-packaging-complex-robotics-software-with-snaps>`,
we will be deploying a robotics software stack using snaps and snapcraft.
Following the [TurtleBot3](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/)
example, we will split the monolithic snap presented in part 2 into a system
of four (4) snaps, namely:

* turtlebot3-lyrical-bringup: The robot specific snap required to bring the robot up.
  We may also refer to it as the ‘brain’ snap.
* turtlebot3-lyrical-teleop: A teleoperation snap allowing us to drive our robot.
* turtlebot3-lyrical-nav: A snap that contains both the mapping and
  autonomous navigation functionality.
* A foundational snap.

The foundational snap is the basis for the content sharing design and,
as its name suggests, it's a snap by itself.
While we haven’t yet dug into the inner workings of content sharing,
we briefly suggested that the common bits live outside the application snaps.
As a matter of fact, they live in a separate snap of their own,
a snap that only contains libraries and
a few executables (think ros2 run/launch) but exposes no applications.

We will design the four snaps so that they are standalone,
yet loosely integrated to one another offering some ease of use for the final user.
We will build the three application snaps standalone first, then connect
them to the same foundational snap.
The image below shows a preliminary idea of what we will build in this tutorial.

![TurtleBot3c multi snap system diagram](https://assets.ubuntu.com/v1/f2b8ff8f-tb3_multi_snap_system.png)

In this fourth part, we will learn:

* How to draw a line and separate functionalities in their own snap.
* How to build a ROS snap using content sharing.
* New snap features and concepts that will be useful in a robotics context.

### Requirements

The main requirement is that you have already completed {ref}`part 2 <tutorials-snaps-core-packaging-complex-robotics-software-with-snaps>`
of this guide.
This implies that you are familiar with ROS, Linux and snap/snapcraft.

### Setup

Since we are reusing part 2 examples, the setup is the same.
Please {ref}`refer back <tutorials-snaps-core-packaging-complex-robotics-software-with-snaps>`
for the details of the setup either on your machine or in a virtual machine.

The ROS 2 Lyrical content sharing extension we are going to employ later
requires Snapcraft 9 with experimental extensions enabled.
Make sure that you have the right version of snapcraft installed with:

```bash
snapcraft version
```

## Identification of robot components

When creating a monolithic snap for an entire robot stack,
we end up placing many different applications and functionalities in the same blob.
As we want to split that monolithic snap into smaller chunks
that are as standalone as possible,
we need to consider where to draw the line.

Fortunately, the job of identifying the high level functionalities was mostly done in
{ref}`part 2 <identification-of-robot-components>`
where we identified the different applications to be exposed by the snap.
Following the same dotted lines, we will consider the following functionalities:

1. BringUp, or the obvious need to bring the robot up to a functioning state.
  This includes things such as spawning controllers and drivers,
  and advertising the robot state and model.
2. Teleoperation, or the possibility to drive the robot from a keyboard,
  a `gamepad`, a virtual joystick or similar device.
3. Navigation and Mapping,
  or the ability for the robot to create a representation of
  its environment and autonomously navigate in it.

As a matter of fact, we will reuse the very same
[TurtleBot3](https://github.com/ROBOTIS-GIT/turtlebot3)
project’s source code from part 2.
We will also reuse our tutorial's launchers and configuration so that the
aforementioned functionalities can be launched individually.

### Snapping the TurtleBot3

With the functionalities clearly identified,
we shall now move on to creating the snaps.

We can follow the same template from our previous tutorial,
change the names of the 3 snaps and include only the respective apps and daemons.

In the following sections we will copy the `snapcraft.yaml`
defined in the developer guide part 2 and adapt it to generate 3 different snaps;
"Bringup", "Teleoperation", and "Navigation and Mapping".

Use the prepared Part 2 project under
`docs/tutorials/snaps-core/examples/turtlebot3` as the starting point.
The `prepare-split` helper copies the launchers and hooks, filters the colcon
workspace and runtime packages, and writes each component's `snapcraft.yaml`.
Install the YAML module for this helper:

```bash
sudo apt install python3-yaml
export SNAPCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=1
```

#### BringUp

First, change the name to `turtlebot3-lyrical-bringup` and
adapt the summary and description based on the separation we described before.

```yaml
name: turtlebot3-lyrical-bringup
summary: TurtleBot3 ROS 2 Lyrical bringup
description: The bringup component of the TurtleBot3 tutorial stack.
```

Next, we can simplify the workspace craft part because we only need
the upstream robot driver, model and lidar packages. For the `colcon` plugin,
keep only those packages in `src`.

Remove everything related to the teleoperation,
navigation and mapping from the original file.
In fact, in the BringUp snap we want to keep the `core` app and nothing else.
Keep the two serial plugs so the drivers can access OpenCR and the lidar.
The resulting app is still a disabled-by-default daemon.

```yaml
apps:
  core:
    command: bin/robot-app bringup
    extensions: [ros2-lyrical]
    plugs: [network, network-bind, opencr, lidar]
    daemon: simple
    install-mode: disable
```

```bash
./prepare-split bringup ../bringup-project
(cd ../bringup-project && snapcraft pack --use-lxd)
```

Note that we have not enabled content sharing just yet.
The `ros2-lyrical` extension includes the required ROS dependencies inside the snap.
Let’s continue with the other 2 snaps and
afterwards we will show how to enable content sharing.

#### Teleoperation

Apply the snap rename and adapt the summary and the description:

```yaml
name: turtlebot3-lyrical-teleop
summary: TurtleBot3 ROS 2 Lyrical teleop
description: The teleop component of the TurtleBot3 tutorial stack.
```

Keep only `turtlebot3_teleop` in the colcon workspace.

We can now remove all the `navigation` and `mapping` sections,
as well as the `core` which is now in the `bringup` snap.

This leaves us with the `teleop`, `key` and `joy` sections.
The `joy` app keeps the `joystick` interface, and all three apps keep their
network plugs.

The final result looks like this:

```yaml
apps:
  teleop:
    command: bin/robot-app teleop
    extensions: [ros2-lyrical]
    plugs: [network, network-bind]
    daemon: simple
  key:
    command: bin/robot-app key
    extensions: [ros2-lyrical]
    plugs: [network, network-bind]
  joy:
    command: bin/robot-app joy
    extensions: [ros2-lyrical]
    plugs: [network, network-bind, joystick]
```

```bash
./prepare-split teleop ../teleop-project
(cd ../teleop-project && snapcraft pack --use-lxd)
```

#### Mapping and Navigation

Our third snap will contain the mapping and navigation bits.
The steps are the same as before.
First change the name and the description:

```yaml
name: turtlebot3-lyrical-nav
summary: TurtleBot3 ROS 2 Lyrical nav
description: The nav component of the TurtleBot3 tutorial stack.
```

Keep the `turtlebot3_navigation2` package in `src` and stage the SLAM Toolbox
and Nav2 tools.
Remove the unrelated apps and keep only `mapping`, `navigation` and `save-map`.
Keep both services' disabled install mode and the map-saving stop commands.
The map now belongs to this snap's `$SNAP_COMMON`.

```yaml
apps:
  mapping:
    command: bin/robot-app mapping
    extensions: [ros2-lyrical]
    plugs: [network, network-bind]
    daemon: simple
    install-mode: disable
    stop-command: bin/robot-app save-map
    post-stop-command: bin/robot-app install-map
  save-map:
    command: bin/robot-app save-map
    extensions: [ros2-lyrical]
    plugs: [network, network-bind]
  navigation:
    command: bin/robot-app navigation
    extensions: [ros2-lyrical]
    plugs: [network, network-bind]
    daemon: simple
    install-mode: disable
```

```bash
./prepare-split nav ../nav-project
(cd ../nav-project && snapcraft pack --use-lxd)
```

Before rebuilding, keep a copy of each standalone artifact so you can compare
sizes. The component recipes are generated from the same Part 2 recipe:

```{literalinclude} examples/turtlebot3/prepare-split
:language: python
```

## Using content sharing

Up to this point in the tutorial,
the snaps we have created are self-sufficient and
are not using the ROS foundational snap.

The snaps are working and could be already used in a robot,
but in order to gain the advantages of the content sharing we need to change
the extensions from `ros2-lyrical` to `ros2-lyrical-ros-base`.
It’s a single line of change,
but it enables a different extension that will make sure all
the ROS packages contained in the `ros-lyrical-ros-base` snap are
connected from the foundational snap into your newly created multiple snaps.

```diff
-   extensions: [ros2-lyrical]
+   extensions: [ros2-lyrical-ros-base]
```

[The Ubuntu Robotics Community](https://snapcraft.io/publisher/ubuntu-robotics-community)
maintains multiple ROS foundational variants based on [REP-2001](https://ros.org/reps/rep-2001.html)
such as `ros-core`, `ros-base`, and `desktop` for multiple ROS distributions.

For more details and
all the possible extensions you can use as foundational please check
[the documentation](https://snapcraft.io/docs/supported-extensions)
and look for the ROS 2 Lyrical content-sharing extensions.

After changing the extension to make use of content sharing,
rebuild all three projects with `snapcraft pack --use-lxd`.
Keep the first builds in a separate directory so the new builds do not
overwrite them. Install the content provider and the three new builds
with `snap install --dangerous` for the local files.
Once done, let us verify that the content sharing interface is connected.
With the turtlebot3-lyrical-bringup snap as an example run,

```bash
$ snap connections turtlebot3-lyrical-bringup
Interface            Plug                              Slot                         Notes
content[ros-lyrical-ros-base]  turtlebot3-lyrical-bringup:ros-lyrical-ros-base  ros-lyrical-ros-base:ros-lyrical-ros-base  -
network              turtlebot3-lyrical-bringup:network       :network                     -
network-bind         turtlebot3-lyrical-bringup:network-bind  :network-bind                -
serial-port          turtlebot3-lyrical-bringup:opencr       -                            -
```

The `content[ros-lyrical-ros-base]` interface connects our snap's plug
to the slot of the `ros-lyrical-ros-base` snap that supplies the ROS 2 Lyrical
runtime. If the slot column is `-`, install and connect the provider:

```bash
sudo snap install ros-lyrical-ros-base
sudo snap connect turtlebot3-lyrical-bringup:ros-lyrical-ros-base ros-lyrical-ros-base:ros-lyrical-ros-base
```

### Your ROS snap with and without content sharing

It’s worth looking more in detail at what happens when the content sharing method
is used by the `ros2-lyrical-ros-base` extension.

![ROS snap w/o content sharing](https://assets.ubuntu.com/v1/a8b2c915-ros_snap_w-o_content-sharing.png)

Remember that when using the `ros2-lyrical` extension,
all the dependencies of your ROS packages are read from the `package.xml` files and
installed using `apt`.
They will be shipped with your snap as usual.

When you switch to the new foundational snaps,
such as `ros-lyrical-ros-base`,
most of the basic ROS packages are already installed,
so when reading the `package.xml` files the snapcraft process skips those and
only installs the missing ones inside the snap.

When the snap is installed and started in your robot it will connect to
the content from the foundational snap and get all the ROS packages in there,
as if they were shipped with your own snap.

There are some very important advantages to this approach:

* The foundational snap is rarely updated,
  this reduces the bandwidth during OTA updates.
* Your snaps all fetch content from the same foundational snap,
  meaning there are no longer copies of the same packages across multiple snaps.
  This reduces disk usage and ensures the same versions are being used across snaps.

See below for a size comparison of the snaps before and
after the use of content sharing that we described in this guide.

| Snap | Standalone size | Content-sharing size |
| --- | --- | --- |
| `turtlebot3-lyrical-bringup` | Measure | Measure |
| `turtlebot3-lyrical-nav` | Measure | Measure |
| `turtlebot3-lyrical-teleop` | Measure | Measure |
| `ros-lyrical-ros-base` | Not installed | Count once |

Measure the files with `ls -lh` after building both versions on the same
architecture. Include one copy of the provider in the second total.

Do not run the monolithic snap at the same time. To repeat the Part 2 test in
simulation, leave `core` stopped, set `simulation=true` on
`turtlebot3-lyrical-nav`, and use `turtlebot3-lyrical-teleop.key` to drive.
Use the split `mapping` and `navigation` services to save and reload the map.
For Part 5, build the component snaps on arm64 and publish those revisions to
a test channel under snap names you own, as in Part 3.

## Conclusion

We have reached the end of this developer guide that explores the use of
content sharing for ROS snaps.

### What have we achieved

What we achieved in the developer guide is no small feat.
Starting from the example detailed in part 2 of the developer guide series,
we have built a multi-snap schema to deploy the TurtleBot3 software stack.
In doing so, we have practised how to split a stack into several independent,
yet integrated, functionalities.
This enables a clear separation of concerns and
turns several of our snaps into robot agnostic functionalities that
can be deployed on different platforms.

We have also learnt about the snap content sharing feature and
experienced how this feature can be seamlessly employed for ROS snaps.

### What’s next?

This guide is part of a larger series covering different aspects of the snap ecosystem.
While you should have gone through part 2 to end up here,
you may have skipped part 3 which covers the [Snap Store](https://snapcraft.io/store).

The next developer guide will cover [Ubuntu Core](https://ubuntu.com/core),
a secure, `application-centric` OS for embedded devices.
We will explore how we can use Ubuntu Core to create production images with
our application snaps to simplify the deployment of robots to market.
It will also cover various aspects of the security,
operation and management of snaps.

You can also visit the [robotics documentation](#docs-index)
to find out more about snaps and the other services offered by Canonical,
such as [ROS ESM](https://ubuntu.com/robotics/ros-esm).
If you have any questions or need help,
you can visit and post your question on the [snapcraft forum](https://forum.snapcraft.io/).
