# Part 5: Create an Ubuntu Core image for the TurtleBot3

When developing a robot,
one might want to have an Ubuntu image ready to be flashed on a robot.
With Ubuntu Core,
developers can prepare an image embedding all
the software necessary for a robot as well as configurations,
so the robot is ready to be used from the first boot without manual intervention.

This tutorial will guide you through the steps required
to create your own Ubuntu Core image for a TurtleBot3,
with all the necessary snaps, and install it on a Raspberry Pi 4.

## Requirements

For this tutorial, you will need:

* [A developer account](https://documentation.ubuntu.com/snapcraft/stable/how-to/publishing/authenticate/),
  and be logged in with snapcraft
* Some basic snap/snapcraft knowledge
* A [TurtleBot3](https://emanual.robotis.com/docs/en/platform/turtlebot3/overview/)
  with a Raspberry[Pi 4](https://www.raspberrypi.com/products/raspberry-pi-4-model-b/)
* An additional screen or, alternatively, a serial adaptor.
* [Snapd](https://snapcraft.io/snapd) and
  [snapcraft](https://snapcraft.io/snapcraft) installed

## The goal

For this tutorial,
our goal will be to create an Ubuntu Core image that is
ready to be installed and used on a TurtleBot3 robot equipped with a Raspberry Pi 4.

The image will include all the TurtleBot3c snaps that we prepared in the
[Tutorial part 4: Building ROS snaps with content sharing](#tutorials-snaps-core-building-ros-snaps-with-content-sharing):

* `turtlebot3-lyrical-bringup`:
  The core components for the TurtleBot3
* `turtlebot3-lyrical-nav`:
  The navigation components for the TurtleBot3
* `turtlebot3-lyrical-teleop`:
  The teleoperation components of the Turtlebot3

Additionally, for convenience,
the robot should create its own hotspot so that we can connect
to the robot and teleoperate it from our laptop.
For that matter, we will also embed:

* [Wifi-hotspot-config](https://snapcraft.io/wifi-hotspot-config):
  Configure the network manager for the hotspot
* [Network-manager](https://snapcraft.io/network-manager):
  The network manager
* [Avahi](https://snapcraft.io/avahi):
  The Avahi daemon so we can ping by hostname and not IP address.

With all these snaps installed and configured in our image,
after booting the SD card in the Raspberry Pi,
we will be able to teleoperate the robot from a computer connected to the hotspot.

If you are looking for a more generic tutorial about Ubuntu Core image creation,
and additional information,
please visit: [ubuntu.com/core/docs/build-an-image](https://ubuntu.com/core/docs/build-an-image).

## Create the assertion model

When building an Ubuntu Core image,
the very first step is to write an assertion model.

The model is a recipe that describes the components that comprise a complete image.
An assertion is provided as JSON in a text file.
> See more: [Assertion model](https://ubuntu.com/core/docs/reference/assertions)

The model contains:

* Identification information, such as the developer-id and model name.
* Which [essential snaps](https://documentation.ubuntu.com/core/explanation/core-elements/snaps-in-ubuntu-core/)
  make up the device system.
* Other required or optional snaps that implement the device functionalities.

In our case, we will build a Raspberry Pi 4 image,
and we will pick Ubuntu Core 26.
While the Ubuntu Core version can be chosen independently
of the base version of the snaps,
it will still include the corresponding version of the base snap.
In this example, our TurtleBot3 snaps use `core26` for ROS 2 Lyrical.
We thus pick the corresponding Ubuntu Core image,
to spare the installation of a different core snap.

### Metadata

First, we get the reference model for the Raspberry Pi 4.
Provided as a reference, it will serve as a good starting point for our own model:

```bash
wget -O turtlebot3c-model.json https://raw.githubusercontent.com/snapcore/models/dc34064508c7df17b38c7fd44d235d4d525383e9/ubuntu-core-26-pi-arm64.json
```

Open the file `turtlebot3c-model.json` and
change the `model` field with the name `turtlebot3c-pi-arm64`:

```diff
-    "model": "ubuntu-core-26-pi-arm64",
+    "model": "turtlebot3c-pi-arm64",
```

In the same file, change `authority-id` and `brand-id` to your own ID.
It can be retrieved with:

```bash
snapcraft whoami
```

### List of snaps

From the snaps already listed in the model,
we leave the Raspberry Pi `gadget`, `pi-kernel`, `snapd` and `core26` snaps.
Set the `console-conf` entry's `presence` to `required` for first-boot setup.

When adding snaps to the model, an ID is requested.
This is the unique ID provided by the [Snap Store](https://snapcraft.io/store).
We use the command `snap info` to get ID:

```bash
$ snap info core26
name:   core26
[...]
snap-id:   cUqM61hRuZAJYmIS898Ux66VY61gBbZf
[...]
```

Here, the snap ID is `cUqM61hRuZAJYmIS898Ux66VY61gBbZf`.

#### TurtleBot3c snaps

Let’s add the TurtleBot3c snaps to our `turtlebot3c-model.json`.
Use the names and Store IDs of your Part 4 snaps, not the IDs of older
Noetic snaps. Replace the three placeholders below with those IDs.
Make sure the specified channel contains the Lyrical revision for arm64.

```json
    {
    "name": "ros-lyrical-ros-base",
    "type": "app",
    "default-channel": "latest/stable",
    "id": "r4G1mfGSqkLOLL9jPKEe51vIQzyhd2Ha"
    },
   {
   "name":"turtlebot3-lyrical-bringup",
   "type":"app",
   "default-channel":"latest/beta",
   "id":"BRINGUP_SNAP_ID"
   },
   {
   "name":"turtlebot3-lyrical-nav",
   "type":"app",
   "default-channel":"latest/beta",
   "id":"NAV_SNAP_ID"
   },
   {
   "name":"turtlebot3-lyrical-teleop",
   "type":"app",
   "default-channel":"latest/beta",
   "id":"TELEOP_SNAP_ID"
   }
```

Note that we’ve also added the `ros-lyrical-ros-base` snap.
We need it since we are using the TurtleBot3c [ROS snap content-sharing approach](#explanations-snaps-ros-architectures-with-snaps-multi-snaps-using-content-sharing)
that depends on `ros-lyrical-ros-base` to provide the ROS libraries.

#### Networking snaps

Since we want the TurtleBot3 to create a hotspot,
we will need the `network-manager` snap as well as our [`wifi-hotspot-config`](https://snapcraft.io/wifi-hotspot-config)
snap that will talk to the `network-manager` to create the hotspot on boot.

Additionally, for convenience, we also add `avahi`.
This way, we will be able to ping the robot by hostname and
not have to look for its IP address.

We add the networking snaps to the `turtlebot3c-model.json`:

```json
{ "name": "network-manager",
  "type": "app",
  "default-channel": "26/stable",
  "id": "RmBXKl6HO6YOC2DE4G2q1JzWImC04EUy"
},
{ "name": "wifi-hotspot-config",
  "type": "app",
  "default-channel": "latest/beta",
  "id": "9s6xjXubw4a2yA0TE1aIyK90kewEzhYf"
},
{ "name": "avahi",
  "type": "app",
  "default-channel": "26/stable",
  "id": "dVK2PZeOLKA7vf1WPCap9F8luxTk9Oll"
}
```

The model now contains all the TurtleBot3c snaps as well as all the networking snaps.
With all the applications that we need listed in the model, our model is ready.

## Sign the model

To certify our model and modify it later on, we need to sign it.

This ensures the model cannot be altered without the key,
and also links the created image to both the signed version
of the model and an Ubuntu One account.

> See more: [Sign a model assertion](https://ubuntu.com/core/docs/sign-model-assertion)

First, we check whether we have a key or not:

```bash
snapcraft list-keys
```

If not, we generate one:

```bash
snapcraft create-key turtlebot3c-key
```

Then we register it to the Snap Store with
the details of our [Ubuntu One](https://login.ubuntu.com/) account:

```bash
snapcraft register-key turtlebot3c-key
```

The key should now appear when entering:

```bash
$ snapcraft list-keys

The following keys are available on this system:
    Name              SHA3-384 fingerprint
*   turtlebot3c-key   XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```

With the key ready, we update the timestamp entry in the `turtlebot3c-model.json`.
To generate a valid timestamp at the present moment, use the command:

```bash
date -Iseconds --utc
```

Note that we generated the timestamp after creating the key which is mandatory.

And report the change in the `turtlebot3c-model.json`:

```diff
-"timestamp": "2020-03-31T12:00:00.0Z",
+"timestamp": "2024-08-06T12:22:26+00:00",
```

We can now sign the model with our key `turtlebot3c-key`:

```bash
snap sign -k turtlebot3c-key turtlebot3c-model.json > turtlebot3c.model
```

We now have our signed model:
`turtlebot3c.model` that we generated from our model `turtlebot3c-model.json`
signed with our private `turtlebot3c-key`.

## Create our gadget snap

The [gadget snap](https://ubuntu.com/core/docs/gadget-snaps)
is responsible for defining and configuring system properties specific to our device.

The gadget content can define the layout of the volumes of the device storage,
default configuration options for snaps or even interface connections.

Thus, we will customise snap parameters as well as snap interface connections
in our gadget snap for the TurtleBot3c snaps.

### Get the template

Let us retrieve the template of the `pi-gadget` snap to kickstart our own:

```bash
git clone https://github.com/snapcore/pi-gadget.git -b 26
```

We picked branch `26` for the `core26` gadget targeting arm64.

In the `snapcraft.yaml` of the pi-gadget snap that we’ve just cloned,
change the name to “turtlebot3-pi”:

```diff
-name: pi
+name: turtlebot3c-pi
```

Note that at the end of the `snapcraft.yaml`,
all the slots available are declared (serial, `spi`, `i2c`, etc.).
For security consideration, we should remove the one that we don’t need.
However, we leave this as an exercise to the reader.

Add two serial slots under the existing `slots` mapping in `snapcraft.yaml`.
These paths are the launch defaults for OpenCR and LDS-01.
Confirm the paths on your robot before building the gadget.

```yaml
  opencr:
    interface: serial-port
    path: /dev/ttyACM0
  lidar:
    interface: serial-port
    path: /dev/ttyUSB0
```

We can now proceed with the gadget connections customisation.

### Connections

In our snaps, some plugs are auto-connect.
For those who are not, we manually connect them in the `gadget` snap.

Similarly to the model, we must specify the snaps by their ID.

Append the following connections at the end of the `gadget.yaml` file
to connect the various interfaces.

```diff
volumes:
  [...]
+connections:
+  # turtlebot3-lyrical-bringup
+  - plug: BRINGUP_SNAP_ID:opencr
+    slot: system:opencr
+  - plug: BRINGUP_SNAP_ID:lidar
+    slot: system:lidar

+  # turtlebot3-lyrical-teleop
+  - plug: TELEOP_SNAP_ID:joystick

+  # wifi-hotspot-config
+  - plug: 9s6xjXubw4a2yA0TE1aIyK90kewEzhYf:network-manager
+    slot: RmBXKl6HO6YOC2DE4G2q1JzWImC04EUy:service
```

Doing so, all the interfaces of our snap stack
are automatically plugged for this specific Ubuntu Core image.

### Configurations

The WiFi hotspot snap requires some configurations.
More specifically, we want to configure a custom `SSID` and password,
as well as the WiFi interface.

Similarly, we refer to the snap by their unique ID.

In the `gadget.yaml`,
we configure the hotspot with the `SSID` "turtlebot3c" and
the password "turtlebot3c":

```diff
connections:
  [...]
+defaults:
+  9s6xjXubw4a2yA0TE1aIyK90kewEzhYf:
+    ssid: "turtlebot3c"
+    password: "turtlebot3c"
+    wifi-interface: "wlan0"
```

With this, the `wifi-hotspot-config` snap will create
a hotspot called "turtlebot3c" so we can connect to it.

## Build the gadget snap

Building a gadget snap is no different from any other snap.

On Ubuntu 26.04 amd64, build the gadget for arm64 using the Pi gadget's
`rpi-amd64` platform:

```bash
snapcraft pack --use-lxd --platform=rpi-amd64
```

On an arm64 build host, use `--platform=rpi` instead.

We now have our gadget snap: `turtlebot3c-pi_26-1_arm64.snap`.
Let’s integrate it in our model!

In the `turtlebot3-model.json`,
replace the previous gadget snap with our custom one:

```diff
-    {
-        "name": "pi",
-        "type": "gadget",
-        "default-channel": "26/stable",
-        "id": "YbGa9O3dAXl88YLI6Y1bGG74pwBxZyKg"
-    },
+    {
+        "name": "turtlebot3c-pi",
+        "type": "gadget"
+    },
```

Here we don’t define the `id` since we are providing the gadget snap
locally and not from the [Snap Store](https://snapcraft.io/store).
Additionally, because we use a local gadget snap that is unsigned,
we must set the grade in `turtlebot3c-model.json` to `dangerous`:

```diff
-"grade": "signed",
+"grade": "dangerous",
```

Since we modified the model, let’s sign it again:

```bash
snap sign -k turtlebot3c-key turtlebot3c-model.json > turtlebot3c.model
```

The Ubuntu Core model is now fully customised for the TurtleBot3c.

As we see in the following diagram,
we have in the image the basic `snapd`, `turltebot3c-pi` and `pi-kernel` snaps.
Additionally, we have the `network-manager`,
`avahi` and `wifi-hotspot-config` snaps to set up and manage the network.
Finally, we have the `ros-lyrical-ros-base` snap providing the ROS libraries to our
`turtlebot3-lyrical-bringup`, `turtlebot3-lyrical-teleop`, and
`turtlebot3-lyrical-nav` snaps.

![TurtleBot3c Ubuntu Core image](https://assets.ubuntu.com/v1/ce66139b-TurtleBot3c%20Ubuntu%20Core%20image.png)

## Generating the image

To generate the image,
we use the [`ubuntu-image`](https://snapcraft.io/ubuntu-image) tool.
It generates an image ready to be written
on an SD card from the model that we prepared.

Install the tool as a snap:

```bash
sudo snap install ubuntu-image --classic
```

In our case, we provide the `turtlebot3c.model`
that we signed as well as our local gadget snap:

```bash
ubuntu-image snap turtlebot3c.model --snap ./pi-gadget/turtlebot3c-pi_26-1_arm64.snap
```

This generates the `pi.img` file.
The image file already contains all the snaps we specified in our model,
as well as the configurations and connections from the gadget snap.

### Write the image

To flash the image on the SD card,
we use [`rpi-imager`](https://snapcraft.io/rpi-imager)
which is conveniently distributed as a snap.

To install it:

```bash
snap install rpi-imager
```

Next, insert an SD card in your computer and start the `rpi-imager`.

We choose raspberry-pi 4 as the device.
For the OS, go down the list and select “use custom”:

![`rpi-imager`](https://assets.ubuntu.com/v1/55dfe56f-rpi-imager.png)

Then select the `pi.img` file we’ve just created.

In the “choose storage”, select your SD card.

Select no when asked if you want to apply custom OS settings,
and yes when asked to clear the SD card.

This writing can take some time,
and the `rpi-imager` will let you know once your SD card is ready.

## First boot

Once the SD card is ready, we can insert it in the Raspberry Pi 4.

Ubuntu Core does not ship with a user by default and
since we didn’t create one explicitly,
we won’t be able to interact with the OS by plugging a screen and a keyboard,
but we can still do some monitoring.

### Monitoring of the first boot

In case we still want to monitor the logs and
what’s happening during the boot, we can connect a screen.

We can also connect a serial to USB adaptors for monitoring purposes.

To do so, connect the ground, `Rx` and `Tx` from your adaptor respectively
[to the pins 6, 8 and 10 of the Raspberry pi](https://www.raspberrypi.com/documentation/computers/raspberry-pi.html#gpio).

We use `picocom` to monitor the serial, we can install it with:

``` bash
apt install picocom
```

You can now monitor the serial port with:

```bash
picocom /dev/ttyUSB0 -b 115200
```

### Connect to the robot

The first boot creates the filesystem as well as
decompresses the snaps and configures them.
Meaning that the first boot can take up to 2 minutes.

Once finished, we can find the WiFi hotspot "turtlebot3c" available and
connect to it with the password “turtlebot3c”.

Make sure to have `avahi-daemon` installed on your host machine and
once connected to the WiFi hotspot, we can ping our robot with the command:

```bash
ping turtlebot3c.local
```

The TurtleBot3 is now ready to operate!

### Teleoperate the robot

Now that we are connected to the robot,
we can teleoperate it from our computer over the network.

First, we need to install the Lyrical `turtlebot3-lyrical-teleop` snap
on our computer from the same channel as the image.

```bash
sudo snap install turtlebot3-lyrical-teleop --channel=latest/beta
```

Disable the laptop's `teleop` daemon so only the robot runs the multiplexer.
On the robot, verify the serial connections and start its `core` service.
Substitute your actual snap names if they differ.

```bash
sudo snap stop --disable turtlebot3-lyrical-teleop.teleop
```

On the robot:

```bash
snap connections turtlebot3-lyrical-bringup
sudo snap start --enable turtlebot3-lyrical-bringup.core
```

By default, ROS 2 nodes discover each other through DDS without a central server.
Keep the robot and computer on the same hotspot network, use the same
`ROS_DOMAIN_ID` on both, and make sure discovery is not restricted to localhost.
With the same default domain on both devices, no address needs to be set.
We can then use the keyboard to teleoperate our robot with:

```bash
turtlebot3-lyrical-teleop.key
```

If the robot responds to keyboard commands and stops on command, the
teleoperation test for our custom Ubuntu Core image passed.

## Conclusion

When we booted the robot the first time no manual intervention was necessary,
everything was planned in advance by the means of the gadget snap and the model.
We have seen not only how to pre-install our application on an Ubuntu Core image,
but also how to customise the image and our application for a specific use case.
Ubuntu Core is meant for devices in production.

Thanks to the [security and `sandboxing` features](https://ubuntu.com/core/docs/security-and-sandboxing),
Ubuntu Core is not only lightweight and customised but also secured,
making it ready for an industrial application.
Combined with [landscape](https://documentation.ubuntu.com/landscape),
it offers the perfect solution to deploy robot software at scale.

> More generic documentation about Ubuntu Core
  can be found on [ubuntu.com/core/docs](http://ubuntu.com/core/docs).
