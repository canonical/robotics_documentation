(tutorials-snaps-core-distribute-ros-apps-with-snap-store)=

# Distribute ROS applications with the Snap Store

In Part 3, you will publish a strictly confined ROS 2 Lyrical talker and
listener to the Snap Store, install it as a user would, then deliver an update.
You do not need a robot or the build directory from Part 1.

## Build the talker and listener

Start on Ubuntu 26.04 with [LXD initialised](https://documentation.ubuntu.com/lxd/latest/tutorial/first_steps/)
and [Snapcraft installed](https://snapcraft.io/snapcraft). You do not need ROS
on the host. Check that `snapcraft extensions` lists `ros2-lyrical` for `core26`.
If it does not, update Snapcraft to a version that provides the extension before
continuing.

Create an empty project and save {download}`the example recipe
<examples/talker-listener/snap/snapcraft.yaml>` as `snap/snapcraft.yaml` inside
it. Run the remaining commands from the project directory.

```{literalinclude} examples/talker-listener/snap/snapcraft.yaml
:language: yaml
```

The `colcon` plugin builds the `demo_nodes_cpp` ament package from a pinned
revision of the [ROS 2 demos](https://github.com/ros2/demos/tree/3bc83863f1135cfaea0dfda1483d2c4645a7c0d6/demo_nodes_cpp).
The `ros2-lyrical` extension configures the build and runtime environments.
The application uses `ros2 launch` to start both nodes.

Choose an available snap name. Use that name both in the recipe's `name`
field and in the shell variable below. Keep the same shell for the tutorial.

```bash
name=yourname-test-ros2-snapstore
arch=$(dpkg --print-architecture)
export SNAPCRAFT_ENABLE_EXPERIMENTAL_EXTENSIONS=1
snapcraft pack --use-lxd
sudo snap install --dangerous "./${name}_0.1_${arch}.snap"
snap run "$name.ros2-talker-listener"
```

Look for both the talker's `Publishing:` line and the listener's `I heard:`
line with the same message. Press **Ctrl+C**. Remove the local installation
so the next install tests the Store revision:

```bash
sudo snap remove "$name"
```

## Register and release a test revision

Sign in with a [Snap Store developer account](https://snapcraft.io/account).
Only upload software you are entitled to publish. This example uses
`latest/edge` rather than the stable channel because it is a test release.
An edge channel is **not private**.

```bash
snapcraft login
snapcraft register "$name"
snapcraft upload --release=latest/edge "${name}_0.1_${arch}.snap"
```

If the name is taken, choose a new name, update the recipe and shell variable,
and repeat the build and local test. Once the Store review and release finish,
install the signed revision without `--dangerous`:

```bash
sudo snap install "$name" --channel=latest/edge
snap list "$name"
snap run "$name.ros2-talker-listener"
```

Check for the message exchange again, then stop the application with **Ctrl+C**.
Note the revision in `snap list`: the Store assigns this number, whereas you
set the version (`0.1`) in the recipe.

## Deliver an update

In `snap/snapcraft.yaml`, change `version` to `'0.2'` and change the command's
final argument from `talker_listener_launch.py` to `talker_listener_launch.xml`.
Both launch files ship with the same Lyrical package. The update should
preserve the exchange of messages while changing the installed version.

```bash
snapcraft pack --use-lxd
snapcraft upload --release=latest/edge "${name}_0.2_${arch}.snap"
```

After the release, `snap info "$name"` should show `0.2` in `latest/edge`.
Devices tracking that channel will receive it on refresh. To test immediately:

```bash
sudo snap refresh "$name"
snap list "$name"
snap run "$name.ros2-talker-listener"
```

Verify that the version is `0.2`, the revision differs from the one you noted,
and the listener still receives messages. You have now tested distribution and
an update without changing the install command on the target device.
See [managing updates](https://snapcraft.io/docs/managing-updates) and
[channels](https://snapcraft.io/docs/channels) before promoting a snap for
production use.
