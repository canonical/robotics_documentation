(tutorials-snaps-core-packaging-complex-robotics-software-with-snaps)=

# Packaging complex robotics software with snaps

```{important}

 **Before you start**

1. Make sure you have completed {ref}`Tutorial 1: Packaging our first ROS application as a snap <tutorials-snaps-core-packaging-ros-application-getting-started>`
before starting this tutorial.
This tutorial builds on key concepts introduced earlier,
including the benefits of snaps for ROS applications and
the essential features of Snapcraft.

2. This guide is meant for ROS snap beginners and
advanced users looking for guidelines.

3. This is not a quick guide  nor a ROS tutorial.
A new developer will take approximately **one full day** to cover the entire guide.
```

The first step for deploying a robotics application is to package it.
Snaps are specifically designed to confine embedded Linux applications,
making it easier to install and manage software versions.
They offer useful features for deployment, such as over-the-air (OTA) updates,
delta updates, automatic rollback, security policies, and more.
While bundling all software dependencies,
snaps provide a comprehensive deployment infrastructure for robotics software.

While snaps adapt to the way ROS developers work,
they bring new concepts and tools that we need to understand first.

## How to use this developer guide

In {ref}`Tutorial 1: Packaging our first ROS application as a snap <tutorials-snaps-core-packaging-ros-application-getting-started>`
of our developer guide series,
we introduced the main concepts and learned what snaps can do for ROS applications.
We also explored the most important features of Snapcraft.

In this developer guide,
we will explore advanced snap topics and tools that will show you how to structure,
package, and test complex robotics applications.

While this developer guide is meant to be read completely,
a second-time reader or an experienced snapcraft developer
might come back to a specific section.
Some sections can be used independently to learn how to solve a specific problem.

## What we will learn

Deploying robotics software is usually tackled when a project reaches certain maturity.
We need a fast and reliable way to distribute software and subsequent updates.
Additionally, we need the deployed software to be fully isolated in its sandbox,
thus minimizing security risks.

Addressing those points and more,
snaps represent an ideal solution to deploy ROS applications to devices and users.

Snapping a simple talker-listener in
{ref}`Tutorial 1: Packaging our first ROS application as a snap <tutorials-snaps-core-packaging-ros-application-getting-started>`
was good enough to see the potential of snaps.
However, when packaging a more complex application, one might wonder:

- Should we build one snap for our entire robot?
- Should we have one part per ROS package?
- What should a final robot snap look like?

Snap and snapcraft contain tons of features that will come in handy when
defining our robot application.
This guide will help you understand these features and how to use them.

In this second part, we will learn:

- How to create a snap for a robot software stack.
- How to take the decisions that a ROS snap developer has to take to design a snap.
- We will introduce new features and
  concepts associated with snaps that will be useful in a robot application.
- The different means to debug a snap package and its snapped applications.

While covering the theoretical aspects of ROS snaps,
we will apply all this knowledge to [TurtleBot3](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/)
for a more interesting real-world scenario.

## Requirements

1. You will need basic ROS knowledge.
  Ideally, you will already understand how to build packages, call a service,
  and know what a launch file is.
  You should also be familiar with the process of creating a map and
  using it to navigate.
2. A basic understanding of the Linux environment (Ubuntu) is also required.
3. You should have a working knowledge of snaps.
  This means either previous experience with snap and snapcraft,
  or having followed the
  {ref}`tutorials-snaps-core-packaging-ros-application-getting-started`.

### Setup

Since this developer guide builds a snap for a robot, we will need:

- TurtleBot3 [Gazebo](https://gazebosim.org/) simulation running under ROS 2 Lyrical.
- Git to prepare our workspace, and Snapcraft and LXD as in Part 1.
- Depending on our current OS,
  we can choose between the following Native setup and the Multipass setup.

`````{tabs}
````{group-tab} Option 1: Native Setup

The Native setup will need Ubuntu 26.04.
This is because we will need the TurtleBot3 simulation to run.
We don’t intend to embed the simulation into our snap.

With the running Ubuntu 26.04, configure the Lyrical APT repository using the
[ROS 2 Lyrical installation instructions](https://docs.ros.org/en/lyrical/Get-Started/Installation/Ubuntu-Install-Debs.html).
Install the simulator and desktop tools:

```bash
sudo apt update
sudo apt install git ros-lyrical-desktop ros-lyrical-turtlebot3-gazebo \
    ros-lyrical-nav2-rviz-plugins
```

````

````{group-tab} Option 2: Multipass

Install [Multipass](https://documentation.ubuntu.com/multipass/stable/) and
launch a VM:

```bash
multipass launch 26.04 --cpus 4 --disk 30G --memory 8G --name workshop-part2
multipass shell workshop-part2
```

Follow the native installation steps inside the VM. For the Gazebo and RViz
windows, use a graphical session or X11 forwarding. If your VM provider
cannot forward graphics, run the simulator on a graphical Ubuntu 26.04
system and ensure that ROS 2 discovery works between the simulator and VM.

````
`````

### Setup Check

We can make sure that everything is properly installed by launching:

```bash
source /opt/ros/lyrical/setup.bash
TURTLEBOT3_MODEL=waffle_pi ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

We should then see the TurtleBot3 simulated in the `turtlebot3_world` environment.
We can now press **Ctrl+C** to stop the Gazebo launch.

Check that `snapcraft extensions` lists `ros2-lyrical` for `core26`.
The extension requires explicit opt-in while experimental.

We are now all set up for this developer guide.

(identification-of-robot-components)=

## Identification of robot components

While we can find many examples to snap various applications,
robots might sound more complicated.
A robot is usually composed of multiple applications, background services,
and applications to call.

Snaps are designed to deploy applications.
Thus, **we must think of our robot software as an application and**
**not as a set of launch files**
to call in 5 different terminals.

To start snapping our stack we first need to
[identify the various functionalities and applications of our robot application](#explanations-snaps-identify-functionalities-and-apps-of-robotics-snap).

We are going to apply the methodology to the TurtleBot3.
This way, we will have a clear example of the functionalities and snap
entries for a robot,
as well as the process to identify these entries.

For this guide,
we will focus on the monolithic snap approach since
it is the simplest for a first robot snap.
All the possible architectures for ROS snap applications are described
{ref}`in the documentation <explanations-snaps-ros-architectures-with-snaps>`.

### Functionalities of our robot snap

Before defining our applications,
we must define the final functionalities that the snap should bring to our robot.
We want the user to do three things:

1. Teleoperate the robot with a keyboard or a joystick.
2. Create a map of our environment.
3. Navigate into our mapped environment.

These are the three functionalities that we want our users
to be able to perform with our robot.

Additionally, we don’t want our snap to be compatible only with our physical TurtleBot3.
We also want our snap to be compatible with the simulation.

Note that **we won’t need the snap to run the simulation itself**,
since the simulation is a substitute for the real robot.
**The snap should simply interface with the simulation.**

### Defining the TurtleBot3 applications

Now that we have defined the functionalities of the robot,
let’s have a look at the applications we need to cover them.

We want most of it to be ready as quickly as possible on the robot.
Hence, the common set of nodes for these functionalities must be always up and running.
We will call it the **core** application.

The diagram below summarises all these different applications inside our
TurtleBot3 snap and how they will be used by the final user.
The snap contains all the system and ROS dependencies for our applications.
The `teleop` daemon starts automatically. We enable `core` explicitly when
deploying to a real robot.
`joy` and `key` apps are applications that can be called from the terminal by
a user to be able to control the robot manually.
Finally, `mapping` and `navigation` are background applications that can be
enabled or disabled.
Once enabled they will act exactly like `core` and
simply automatically start at boot.
All these applications are communicating with each other with ROS.

<https://assets.ubuntu.com/v1/2529db37-tb3snap.png>

Let’s break down what each of these applications will do and the requirements they have.

#### Core

Core is going to be our common set of nodes always running in the background.
In the case of the TurtleBot3,
we are talking about all the nodes to interface with the hardware
(mobile base and lidar)
as well as the `robot_state_publisher` to have the model of the robot available.
This `core` snap application must be running in the background.

#### Teleoperation applications

TurtleBot3 should have the functionality to be
teleoperated with a joystick or a keyboard.
We want to be able to do that from a controller connected to the robot.
We also want another computer on the network to be able to control our robot.

To be able to manage so many different ways of teleoperating the robot,
we will need an application to be able to route all this traffic.
Similarly to the core app enabling the common part of all functionalities,
the `teleop` app will be starting the common part necessary
for all teleoperation scenarios.

On the contrary,
we don’t want the joystick or keyboard specific apps to be running all the time.

We will then need three different snap applications:

- The first one called `teleop` simply runs the teleoperation basics in the background.
  This way, a controller application running on the robot or
  remotely can always control the robot.
- The second application will be called `joy` and
  will be a command to call whenever we want to control the robot with a joystick.
  Meaning that every node and
  configuration specific to the joystick control should be launched in the application.
- The third application, `key`, will be similar to the `joy` application,
  but for the keyboard control.

You can see all of them in the diagram above.
This is an example of how we can split our applications.
Depending on the use case one might decide for a different split.

With these three different snap applications,
we will be able to have all the teleoperation functionality that we wanted.

#### Mapping

We will use TurtleBot3 to create a map of its environment.
Thus, we want a `mapping` application that we can call to start mapping our environment.
We also want this application to automatically save the map when we stop the application.
This way there will be no need to manipulate any file or to call a service of any kind.

Remember that the idea is to think of creating an application for deployment.
The final user of our snap will understand what creating a map of the environment means.
On the contrary, our end-user might not know ROS and thus how to save a map the ROS way
(calling the Nav2 map saver).

With `teleop` and either `core` or the simulator running,
launching `joy` or `key` along with `mapping` will be all we need to start
creating a map of any environment.

#### Navigation

After mapping, we navigate in our freshly mapped environment.

Hence, we will need another application called `navigation`.
This application will be launching everything we need for
the navigation (localization + navigation).
This application should make sure to load the last map that
we created (with the `mapping` application).
While the mapping is done on rare occasions, the navigation will be rather standard.

Thus, our `navigation` should be running as a daemon in the background.
With the specificity that it should be shipped as disabled (we can enable it)
since we won’t have a map created on the very first install.

#### TurtleBot3 ROS workspace presentation

We have now seen the different applications that the TurtleBot3 snap will
have to make its applications easy and error-proof to use.

In the section above we covered the methodology used to define our snap application.
**We must think in terms of functionalities once deployed**.
The usage of a deployed application can differ from the usage that a developer
would have of the same ROS workspace.

It’s now time to look at what’s inside the TurtleBot3 repositories.
This way we will identify how to expand a traditional ROS workspace into
an application-oriented workspace.

Some packages come from pinned source and the rest come from the Lyrical
package repository. Snapcraft puts the required runtime packages in the snap.

#### TurtleBot3

This is the [official repository from ROBOTIS](https://github.com/ROBOTIS-GIT/turtlebot3),
which contains most of the TurtleBot3 packages. The main packages for this demo are:

- `turtlebot3_bringup`: Contains robot launch files for different configurations.
- `turtlebot3_description`: Contains URDF files as well as meshes.
- `turtlebot3_node`: Interfaces with the physical TurtleBot3.
- `turtlebot3_navigation2`: Contains launch files and parameters for Nav2.
- `turtlebot3_teleop`: Contains the node to control TurtleBot3 with a keyboard.

All these ROS packages contain `package.xml`,
effectively listing all the build time and run-time dependencies.
Recall that these `package.xml` files are used by Snapcraft to
automatically pull dependencies.
If we were to use a different robot stack we should make sure that similarly,
the `package.xml` is properly listing the dependencies.

We also build the upstream LDS-01 driver for the physical robot. For simulation,
Gazebo replaces the hardware bringup, so we leave `core` stopped.

#### TurtleBot3 messages

Additionally, the [`turtlebot3_msgs`](https://github.com/ROBOTIS-GIT/turtlebot3_msgs)
repository is another official repository from ROBOTIS and
contains the TurtleBot3 message definitions.
The `turtlebot3_msgs` interface package is available as a Lyrical binary.
Snapcraft resolves it from the `package.xml` dependencies. The keyboard,
joystick, and navigation publishers use `geometry_msgs/msg/TwistStamped`
so the multiplexer and TurtleBot3 agree on the type of the velocity command.

#### TurtleBot3c

Instead of using a TurtleBot3c fork for Lyrical, we provide the
{download}`TurtleBot3 snap recipe <examples/turtlebot3/snap/snapcraft.yaml>`
and the tutorial's launcher to expose applications for bringup,
teleoperation, mapping and navigation.

We indeed use a topic multiplexer called `topic_tools/mux`
responsible for routing the desired robot control topic to
the `/cmd_vel` topic (see figure below).
This way our TurtleBot3 could be controlled by a joystick, a keyboard,
or even the navigation depending on what we desire without interfering with each other.

![/cmd_vel mux](https://assets.ubuntu.com/v1/c59f2f80-teleop-mux.png)

Selecting the topic which is going to be redirected
can be done with the following command:

```bash
ros2 service call /mux/select topic_tools_interfaces/srv/MuxSelect "{topic: '/key_vel'}"
```

## Snapping our software

In the previous section, we have defined the applications that our snap must expose.
We have also seen the different repositories from TurtleBot3 that
we will need to implement those applications.
This is the first step to writing our `snapcraft.yaml` file.

The following section is going to cover how to snap applications, step by step.
The complete example is in `docs/tutorials/snaps-core/examples/turtlebot3`
in the tutorial repository.
We can refer to it at any time in case we have questions
regarding the content of a file.

### Completing our snapcraft.yaml

From the [tutorial source repository](https://github.com/canonical/robotics_documentation),
change to `docs/tutorials/snaps-core/examples/turtlebot3`.
As in Part 1, we first need to complete the metadata along with the base
and [`strict` confinement](https://snapcraft.io/docs/explanation/security/snap-confinement/).
The full recipe is below; we'll go through each part and app in turn.

```{literalinclude} examples/turtlebot3/snap/snapcraft.yaml
:language: yaml
```

#### Build the workspace

The recipe builds a colcon workspace containing the ROBOTIS packages used
by our apps. The source packages declare build and runtime dependencies in
`package.xml`, which the `colcon` plugin resolves for Lyrical. We leave
Gazebo and RViz on the host for the simulation.

##### Writing our turtlebot3 part

Run the workspace preparation script once per checkout. It updates the
pinned TurtleBot3 source for the ROS 2 Lyrical C++ headers and the
`message_filters` subscriber API:

```bash
./prepare-workspace
export SNAPCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=1
```

```{literalinclude} examples/turtlebot3/prepare-workspace
:language: sh
```

The `robot` part builds the `src` directory. We explicitly stage tools
called by our snap launchers, such as `ros-lyrical-ros2launch`,
`ros-lyrical-ros2service`, and `ros-lyrical-nav2-map-server`. The
`ros2-lyrical` extension sets up the environment for ROS 2.

##### Building the core app

`core` calls `ros2 launch turtlebot3_bringup robot.launch.py` to start the
hardware drivers and robot state publisher.
This application must be running in the background when we want to use the
physical robot. Remember that since it’s a ROS application we will need a
ROS environment, which the extension sets up for us.

The `opencr` and `lidar` plugs
give the app access to the serial ports. Connect them to the matching slots
before enabling the service on hardware. We use `install-mode: disable`
so installation alone does not start the robot.

In simulation Gazebo provides the corresponding robot state and sensors,
so leave `core` stopped.

##### Building the teleop app

The `teleop` app will be running our teleoperation multiplexer.
The ROS 2 `topic_tools` multiplexer
has three input topics and a single `/cmd_vel` output. This service starts
at installation so the keyboard and joystick apps can use it when needed.
It uses the `network` and `network-bind` plugs because control commands
can also originate on a different device.

#### Building the key app

This app must publish a `/key_vel` topic based on the keyboard input.
`key` calls the upstream `teleop_keyboard` executable, installed by colcon
under `opt/ros/snap/lib/turtlebot3_teleop`. It remaps `cmd_vel` to `/key_vel`
and selects that input. This app needs a terminal, not a daemon.

##### Building the joy app

The major differences are that this is going to be published on the
`/joy_vel` topic and that we need access to the joystick.
`joy` uses `teleop_twist_joy` and the `joy` node. The launch argument
`publish_stamped_twist:=true` matches the other publishers and
`joy_vel:=/joy_vel` gives the joystick a separate input to the multiplexer.
The snap's [joystick interface](https://snapcraft.io/docs/reference/interfaces/joystick-interface/)
allows it to read the controller. Check `snap connections turtlebot3-lyrical`
and connect the `joystick` plug if needed.

Now we have all the applications necessary for teleoperation whether we
use a keyboard or a joystick.

##### Building the mapping app

`mapping` launches SLAM Toolbox's `online_async_launch.py`. It runs as a
daemon so that the stop command can save a map. Mapping is disabled on
install because it is only needed while surveying a new environment.

##### Building the navigation app

Finally, our last application, `navigation`.
It starts Nav2 using the selected model's parameters and the last saved map.
It also starts disabled.
The reason is that when we first install our snap, we won’t have created any map.
This way we can create our first map and then activate our navigation daemon:

```bash
sudo snap start turtlebot3-lyrical.navigation
```

## Application scripts

So far we have defined our parts as well as our different applications in our snap.
Nothing there was new.
It was simply an application of the basic ROS/snap knowledge to the TurtleBot3 case.

Let’s say that we want our snap `navigation` daemon to
always use the latest recorded map.
Or that we want the mapping to automatically save the map without
having to manually call a ROS service to save the map.

For these, we can use additional features of `snap` and `snapcraft`.
These features will make our applications much more
integrated and easier for the final user.
The features that we will describe below are:

- Environment variables.
- Local file parts.
- Launcher scripts.
- Daemon scripts.

### Snap environment variables

Environment variables are widely used across Linux to provide convenient access
to system and application properties.
Both `snapcraft` and `snapd` consume, set,
and pass-through specific environment variables to support building and running snaps.

There are snap environment variables,
like `$SNAP` and `$SNAP_INSTANCE_NAME` used to identify the snap and its location.
The [*Snap environment variables*](#explanations-snaps-snap-environment-variables)
documentation is a great place to learn about these.

Additionally, snaps define environment variables specific to data and file storage.
The [*Snap data and file storage documentation*](#explanations-snaps-snap-data-and-file-storage-topic-guide)
is a great place to learn about these.
We keep our maps in `$SNAP_COMMON`, whose data is shared across snap revisions.

### Local files part

In order to create additional behaviour for a snap, we need to add scripts.
These scripts could be for example responsible for calling
the ROS node in charge of saving the map.

To import all these local files into our snap we will need an additional
`snapcraft` [part](https://documentation.ubuntu.com/snapcraft/stable/reference/snapcraft-yaml/index.html).
They are used to declare pieces of code that will be pulled into your snap package.

Our `robot` part uses the `colcon` plugin to build and install our ROS packages.
In order to simply import scripts into our snap we will need a different plugin,
the
[`dump` plugin](https://documentation.ubuntu.com/snapcraft/stable/common/craft-parts/reference/plugins/dump_plugin/).

As its name suggests, the `dump` plugin is simply used to
"dump" the specified sources in a specified location into our snap.
Usually, the dumped files are scripts, configuration files, binaries etc.

### Adding scripts to our snap’s part

In our case we will simply need to dump our launcher from `scripts` into
the `bin` of our snap.

We will then need to add the following part to the `snapcraft.yaml`:

```yaml
commands:
  plugin: dump
  source: scripts
  organize:
    robot-app: bin/robot-app
```

The `organize` keyword is a key/value pair,
the key represents the path of a file inside the selected source of
the part and the value represents the file's destination in the stage area.

### Launcher scripts

Since the core application is a daemon,
we cannot pass it extra arguments with `snap start`.
For this reason we will use a launcher script.
This way, we will not only be able to specify ROS arguments,
but also do some extra work before starting the application.
For example, verifying that a file exists before calling a command.

#### Adding scripts’ launcher

The example provides a launcher with a subcommand for each app:

```{literalinclude} examples/turtlebot3/scripts/robot-app
:language: sh
```

#### Using scripts

Now, let’s use our script in `snapcraft.yaml` instead of the “raw” commands.
Each app calls `bin/robot-app` with the corresponding subcommand.
For example, `navigation` uses `command: bin/robot-app navigation`.
The app's ROS extension, network plugs and daemon settings still belong
in the snap recipe, not in the launcher.

#### Daemon scripts

In TurtleBot3 we already have a few daemons.
These snap services can use multiple new features that
will come in handy for our application.

`Snap` and `snapcraft` offer great features to orchestrate daemon applications.
The [*Application orchestration*](#explanations-snaps-application-orchestration)
documentation is a great place to learn more about orchestration.

`stop-command` runs before stopping the service, and `post-stop-command`
runs afterward. This distinction matters because a map saver must receive
the map while the mapping node is still publishing it.

#### Applying daemon scripts to TurtleBot3

We have already made our applications run in the background,
but we don’t want the user to have to call ROS nodes manually to save a map.
Let’s make this automatic!

Use the first lifecycle command to save the map and the second to install it.
That makes an ordinary `snap stop` sufficient to finish a mapping session.

#### Save the map

The Nav2 `map_saver_cli` writes a PGM image and its YAML metadata. The
`stop-command: bin/robot-app save-map` calls it with a temporary file prefix.
The script creates a readiness marker only once the map saver succeeds, so
a failed save does not replace the previous map.

Now our map will be saved automatically whenever we stop our
mapping service with `sudo snap stop turtlebot3-lyrical.mapping`.
It would be better to keep all the maps created and simply mark one as the current one.
This way we could even restore a previous one later.

#### Install the last map

The `post-stop-command: bin/robot-app install-map` moves a completed pair
to timestamped names and updates `current_map.yaml` to point to the newest map.
The timestamp preserves earlier maps; the symlink gives navigation a stable
path. Both service commands use `$SNAP_COMMON/map`.

#### Navigation launcher adaptation

The launcher checks that `current_map.yaml` exists before launching Nav2.
It passes the path with `map:=` along with the model's navigation parameters.
It sends Nav2's final stamped velocity output to `/nav_vel`, so only the
multiplexer publishes `/cmd_vel`.

#### Velocity multiplexer selection

Before starting the keyboard, joystick, or navigation app, the launcher
calls `/mux/select` with a `topic_tools_interfaces/srv/MuxSelect` request.
The selected input is `/key_vel`, `/joy_vel`, or `/nav_vel`, respectively.
Once selected the topic is forwarded to `/cmd_vel`.
For example, the service call for joystick control is:

```bash
ros2 service call /mux/select topic_tools_interfaces/srv/MuxSelect "{topic: '/joy_vel'}"
```

Stop the robot before changing publishers. In a ROS 2 terminal, check
`ros2 topic info /cmd_vel --verbose` to confirm that the multiplexer and
the robot use `geometry_msgs/msg/TwistStamped`.

## Turtlebot3 configurations

We want to change the robot model and switch between simulation and hardware
without rebuilding the snap. These are configuration values we can store
using `snap set` and read inside the snap with `snapctl`.

### Adding TurtleBot3 hooks

The `configure` hook runs after `snap set`. If it fails, snapd rejects the
configuration transaction. Keep it executable in `snap/hooks/configure`:

```{literalinclude} examples/turtlebot3/snap/hooks/configure
:language: sh
```

#### Simulation parameter

##### Hooks

The hook accepts `true` or `false` for `simulation`. An unset value means
hardware mode.

##### Use the configuration

Stop the hardware `core` service if it is running, then select simulation:

```bash
sudo snap set turtlebot3-lyrical simulation=true
```

The launcher passes this as `use_sim_time` to SLAM Toolbox and Nav2.
Restart any active mapping or navigation service for it to use the new
setting. Gazebo supplies `/clock` in simulation.

#### Turtlebot3 model

##### Hooks

The hook validates `turtlebot3-model` against `burger`, `waffle`, and
`waffle_pi`. The default is `waffle_pi`.

###### Use the configuration

Set the model that matches the real robot or the simulated world:

```bash
sudo snap set turtlebot3-lyrical turtlebot3-model=waffle_pi
```

The launcher exports `TURTLEBOT3_MODEL` for the upstream launch files and
uses the corresponding navigation parameters. Restart any active services
and relaunch Gazebo with the same model if needed.

### Final test

Build the snap from the prepared workspace:

```bash
export SNAPCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=1
snapcraft pack --use-lxd
```

If you already installed the tutorial snap and want to reproduce a first
install, remove it with `sudo snap remove turtlebot3-lyrical --purge`.
This also deletes its maps and configuration, so first save anything
you want to keep.

1. Install the newly built snap with `sudo snap install --dangerous ./turtlebot3-lyrical_0.1_amd64.snap`
   (adjust the architecture for your build).
2. Set `sudo snap set turtlebot3-lyrical simulation=true turtlebot3-model=waffle_pi`.
3. In a terminal with Lyrical sourced, start the simulation:

   ```bash
   TURTLEBOT3_MODEL=waffle_pi ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
   ```

4. Ensure the `teleop` service is running, then start `sudo snap start turtlebot3-lyrical.mapping`.
5. Drive around the world with `turtlebot3-lyrical.key` and stop the robot.
6. Run `sudo snap stop turtlebot3-lyrical.mapping`. Verify that
   `/var/snap/turtlebot3-lyrical/common/map/current_map.yaml` points to a new map.
7. Start `sudo snap start turtlebot3-lyrical.navigation`.
8. Run `rviz2`. Set the fixed frame to `map`, add a Map display for `/map`,
   and use **2D Pose Estimate** to set an initial pose.
9. Send a reachable Nav2 goal and check that the robot reaches it.

Once you have a map and navigation works, you can enable the navigation
daemon at boot with `sudo snap start --enable turtlebot3-lyrical.navigation`.
Use `sudo snap disable turtlebot3-lyrical` to stop all of the snap's apps and
services. Check them with `snap services turtlebot3-lyrical`.

We have now presented every single step to snap a TurtleBot3 software stack.
We went from application identification to actual snapping and
finally added some advanced behaviour to automate map management.

## Exercise

Now that we have learned the ins and outs of the TurtleBot3 snap,
we can apply some of our fresh knowledge for a quick exercise.
The exercise as well as the solution are available in the
{ref}`Developer guide part 2 - exercise <tutorials-snaps-core-exercises-exercise-2>`.

```{toctree}
:hidden:
:maxdepth: 1

Part 2 exercise <exercises/exercise_2>
```

## Next Steps: Debugging

If an app fails to start or the robot does not respond, check its service
logs, snap connections and ROS topics. For help investigating packaging or
confinement, see {ref}`how-to-guides-packaging-debugging-snap-applications`.

## Conclusion

We have prepared a ROS 2 workspace and packaged the robot's drivers,
teleoperation, mapping and navigation in one snap.

### What we achieved

In this developer guide,
 we went through the creation of the TurtleBot3 snap.
We have covered all the steps that one must go through when creating a snap for a robot.

First, we identified the different applications and
daemons that our snap must expose.
We also identified the scope of our snap.
Then we applied the knowledge of the first part of the developer guide to
build the first draft of our snap.
By discovering new features of snaps we were able to implement features to
manage our maps and to select the right velocity topic.
We implemented these features to simplify and automate the usage of the snap.

We finally covered the snap debugging aspect.
This helped us to solve all the different issues we encountered while testing the snap.

Now the whole stack of TurtleBot3 for the simulation or
the real robot is packed in a single snap.
