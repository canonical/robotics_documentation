Interaction between ROS ESM and ROS upstream
=========================

When enabling ROS ESM using `pro enable ros` as described in this tutorial [TODO link]() some changes are made to `apt` configuration and it's important to be aware of those details. 

# Changes to PPAs

If you followed the official ROS 1 or ROS 2 installation instructions for [ROS 1](https://wiki.ros.org/noetic/Installation/Ubuntu) or [ROS 2](https://docs.ros.org/en/rolling/Installation/Ubuntu-Install-Debs.html) you now have some additional files in your `/etc/apt/sources.list.d` folder.

These files are telling to your apt software which server is able to provide specific packages. For the ROS ecosystem the files are usually called:
- `/etc/apt/sources.list.d/ros-latest.list` for ROS 1
- `/etc/apt/sources.list.d/ros2.list` for ROS 2

For example when you request apt to install `ros-noetic-std-msgs` it will fetch it from the server written inside the ros-latest.list file.
When you enable ROS ESM you will notice that a new configuration file is added inside your `sources.list.d` folder. 
The file is called `ubuntu-ros.list` and tells apt to fetch packages from [esm.ubuntu.com](https://esm.ubuntu.com).
Our ESM packages can be distinguished because their version follows the pattern `X.Y.Z+<ubuntu-version>-<counter>` where X.Y.Z is the usual ROS versioning system, <ubuntu-version> is an LTS name such as 20.04.1 and counter is a single integer. 
After enabling ROS ESM you can inspect a package with apt-cache. For example:

```
apt-cache policy ros-foxy-std-msgs
ros-foxy-std-msgs:
  Installed: 2.0.5-1focal.20230527.044919
  Candidate: 2.0.5+20.04.1-0
  Version table:
     2.0.5+20.04.1-0 500
        500 https://esm.ubuntu.com/ros/ubuntu focal-security/main amd64 Packages
 *** 2.0.5-1focal.20230527.044919 500
        500 http://packages.ros.org/ros2/ubuntu focal/main amd64 Packages
        500 http://repo.ros2.org/ubuntu/main focal/main amd64 Packages
        100 /var/lib/dpkg/status
```
This shows that ros.org has a version of ros-foxy-std-msgs at `2.0.5-1focal` while ROS ESM has a version of `2.0.5+20.04.1-0`.

Apt automatically decides to upgrade from upstream ros.org to ROS ESM if both are available, you can confirm this by running

```
apt list --upgradable
ros-foxy-std-msgs/focal-security 2.0.5+20.04.1-0 amd64 [upgradable from: 2.0.5-1focal.20230527.044919]
```

# Changes to rosdep

ROS ESM is its own ROS distribution, and thus provides its own distribution and `rosdep` files. If you already have upstream ROS installed and initialised (e.g. you previously ran `sudo rosdep init`), you’ll need to make sure you install `rosdep` from ESM and re-initialise it as follows:

```bash
sudo apt install python-rosdep
sudo rm /etc/ros/rosdep/sources.list.d/20-default.list
sudo rosdep init
rosdep update
```

