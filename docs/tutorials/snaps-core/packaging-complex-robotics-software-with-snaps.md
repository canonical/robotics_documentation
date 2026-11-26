(tutorials-snaps-core-packaging-complex-robotics-software-with-snaps)=

# Package a TurtleBot3 application as a snap

In Part 2 you will package the ROBOTIS TurtleBot3 Waffle Pi stack for ROS 2
Lyrical on Ubuntu 26.04. Start with a simulated robot; the same snap contains
an optional hardware bringup service for a Waffle Pi with an OpenCR and LDS-01.
Only the simulator or the hardware driver should publish odometry and scans
at any one time.

(identification-of-robot-components)=
## Decide which processes belong in the snap

* **Bringup** launches the robot state publisher, base driver and lidar driver.
  Leave it stopped for simulation: Gazebo supplies those functions.
* **Teleoperation** needs a terminal, not a background service. The keyboard
  node publishes `geometry_msgs/msg/TwistStamped` on `/cmd_vel`.
* **Mapping** uses SLAM Toolbox to build an occupancy grid. **Navigation**
  loads a saved map into Nav2. Run one service at a time so that they do not
  both publish the map-to-odometry transform.

## Build the workspace

Use an Ubuntu 26.04 build machine with Git, Snapcraft and an initialised LXD.
Check that `snapcraft extensions` lists `ros2-lyrical` for `core26`. Work from
the `docs/tutorials/snaps-core/examples/turtlebot3` directory of the
[tutorial source](https://github.com/canonical/robotics_documentation).

```bash
./prepare-workspace
export SNAPCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=1
snapcraft pack --use-lxd
sudo snap install --dangerous "./turtlebot3-lyrical_0.1_$(dpkg --print-architecture).snap"
snap services turtlebot3-lyrical
```

The preparation script puts pinned ROBOTIS packages in one colcon workspace.
In particular it includes the LDS-01 driver as source rather than assuming
there is a Lyrical binary for it. The plugin builds the ament packages and
installs the overlay under `opt/ros/snap`. The extension configures the ROS
environment before starting each app.

```{literalinclude} examples/turtlebot3/snap/snapcraft.yaml
:language: yaml
```

Notice `install-mode: disable`: installation alone must not start the robot.
The {download}`launcher <examples/turtlebot3/scripts/robot-app>` reads its
clock setting through `snapctl`. The {download}`configure hook
<examples/turtlebot3/snap/hooks/configure>` rejects invalid settings. Restart
active services after changing this setting.

## Drive the simulated robot

Use a graphical Ubuntu 26.04 session (a VM with a desktop is sufficient).
The simulator and RViz run **outside** the snap. After configuring the Lyrical
APT repository on that system, install the simulator and ROS command-line tools:

```bash
sudo apt install ros-lyrical-turtlebot3-gazebo ros-lyrical-desktop
source /opt/ros/lyrical/setup.bash
export TURTLEBOT3_MODEL=waffle_pi
ros2 launch turtlebot3_gazebo turtlebot3_world.launch.py
```

In another terminal, select simulation time and start teleoperation:

```bash
sudo snap set turtlebot3-lyrical use-sim-time=true
turtlebot3-lyrical.key
```

Use the keys displayed by the program. Verify that the simulated robot moves
and stops. In a separate terminal with Lyrical sourced, inspect
`ros2 topic info /cmd_vel --verbose`: the keyboard publisher and simulator
subscriber should agree on `geometry_msgs/msg/TwistStamped`. Check that
`/scan`, `/odom` and `/clock` are publishing before starting SLAM.

## Map the world and navigate

```bash
sudo snap start turtlebot3-lyrical.mapping
sudo snap logs turtlebot3-lyrical.mapping
```

Drive around the simulated obstacles until `/map` covers an area you want to
navigate. Stop the robot and save the map:

```bash
sudo turtlebot3-lyrical.save-map
ls -l /var/snap/turtlebot3-lyrical/common/map
sudo snap stop turtlebot3-lyrical.mapping
sudo snap start turtlebot3-lyrical.navigation
sudo snap logs turtlebot3-lyrical.navigation
```

The map saver writes a PGM image and its YAML metadata under `$SNAP_COMMON`,
which is shared between the save command and the system services and survives
snap refreshes. `current_map.yaml` points to the last successful save.
In RViz, set the fixed frame to `map`, add a Map display for `/map`, then use
**2D Pose Estimate** to initialise localisation and **Nav2 Goal** to select a
reachable point on the map. Check that the robot reaches the goal.

For hardware, stop navigation and the simulator, set `use-sim-time=false`
and connect the snap's `opencr` and `lidar` serial plugs to the appropriate
device slots before starting `turtlebot3-lyrical.bringup`. Do not reuse a
simulation map for the real robot.

```{toctree}
:hidden:

exercises/exercise_2
```

Next, try the {ref}`map cleanup exercise <tutorials-snaps-core-exercises-exercise-2>`
or continue to {ref}`Part 3 <tutorials-snaps-core-distribute-ros-apps-with-snap-store>`.
