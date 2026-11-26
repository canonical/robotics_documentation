# Part 5: Create an Ubuntu Core image for the TurtleBot3

Build an Ubuntu Core 26 image for a Raspberry Pi 4 (arm64) that boots with
the Part 2 robot snap, the Part 4 teleoperation snap, and its Lyrical runtime
already installed. An amd64 Ubuntu 26.04 VM can assemble this image; it
cannot boot the Pi gadget or verify the OpenCR and lidar connections.

## Gather the inputs

Build and locally test the Part 2 and Part 4 recipes **on arm64**. Copy
`turtlebot3-lyrical_0.1_arm64.snap` and
`turtlebot3-lyrical-teleop_0.1_arm64.snap` into an empty image directory.
Do not substitute snaps produced by a native amd64 build.

On the image builder, install `jq` and `ubuntu-image`:

```bash
sudo apt install jq
sudo snap install ubuntu-image --classic
```

Use an Ubuntu One account with a registered SSH public key for first boot.
Log in with `snap login` and obtain your developer ID from `snapcraft whoami`
after `snapcraft login`. If you do not yet have a registered model signing
key, create one:

```bash
snap create-key turtlebot3-model
snapcraft register-key turtlebot3-model
```

## Create and sign the model

Start from the official Core 26 **Pi arm64** model. It selects compatible
tracks for the `pi` gadget and `pi-kernel`, and declares `core26` as its base.
Keep these entries. Set both publisher fields to your own developer ID.
Use `grade: dangerous` only for this development image: it allows the two
locally built, unasserted snaps.

```bash
curl -fLo pi-model.json https://raw.githubusercontent.com/snapcore/models/dc34064508c7df17b38c7fd44d235d4d525383e9/ubuntu-core-26-pi-arm64.json
developer_id=YOUR_DEVELOPER_ID
jq --arg id "$developer_id" --arg now "$(date -u +%FT%TZ)" '
  .model = "turtlebot3-lyrical-pi" | ."brand-id" = $id | ."authority-id" = $id |
  .timestamp = $now | .grade = "dangerous" |
  (.snaps[] | select(.name == "console-conf")).presence = "required" |
  .snaps += [
    {"name":"ros-lyrical-ros-base","type":"app","default-channel":"latest/stable",
     "id":"r4G1mfGSqkLOLL9jPKEe51vIQzyhd2Ha"},
    {"name":"turtlebot3-lyrical","type":"app"},
    {"name":"turtlebot3-lyrical-teleop","type":"app"}
  ]' pi-model.json > turtlebot3-model.json
snap sign -k turtlebot3-model turtlebot3-model.json > turtlebot3.model
```

The content snap is a runtime requirement, not the build-time SDK.
`console-conf` is required here so you can configure networking and your
account from an attached display and keyboard.

## Assemble the image

```bash
ubuntu-image snap --output-dir image \
    --snap ./turtlebot3-lyrical_0.1_arm64.snap \
    --snap ./turtlebot3-lyrical-teleop_0.1_arm64.snap \
    turtlebot3.model
ls -lh image/*.img
```

Use Raspberry Pi Imager's **Use custom** option to write the resulting disk
image to a spare SD card. Confirm the destination: writing the image erases
that card. Insert the card in the Pi, boot with a network connection, and
complete console-conf. Use the SSH address shown on the console.

## Verify first boot and hardware access

```bash
snap model
snap list
snap connections turtlebot3-lyrical-teleop
snap interface serial-port
snap services turtlebot3-lyrical
```

Check that the model is `turtlebot3-lyrical-pi`, all three ROS snaps are
present, and the controller's runtime content plug is connected as described
in Part 4. The robot services should not start until you enable them.

The reference gadget does not guarantee slots for arbitrary USB serial
devices. Identify the slots for the attached OpenCR and LDS-01. If neither
the gadget nor snapd exposes them, **stop here**: add device-specific
[serial-port slots](https://snapcraft.io/docs/serial-port-interface) in a
custom gadget based on the [Core 26 Pi gadget](https://github.com/snapcore/pi-gadget/tree/26).
Do not bypass confinement or connect to unrelated ports. Confirm the device
paths match the upstream launch defaults (`/dev/ttyACM0` for OpenCR and
`/dev/ttyUSB0` for the lidar).

With the wheels clear of the ground, replace the two slot placeholders with
the actual `snap:slot` identifiers:

```bash
sudo snap connect turtlebot3-lyrical:opencr OPENCR_SLOT
sudo snap connect turtlebot3-lyrical:lidar LIDAR_SLOT
sudo snap set turtlebot3-lyrical use-sim-time=false
sudo snap start --enable turtlebot3-lyrical.bringup
sudo snap logs turtlebot3-lyrical.bringup
turtlebot3-lyrical-teleop.key
```

Verify that the hardware driver and laser initialise, that teleoperation
responds to the stop command, and that bringup still works after reboot.
Before shipping a production image, publish signed arm64 revisions of the
application snaps, use their Store IDs and channels in a signed-grade
model, and validate the gadget connections on each supported hardware revision.
