# Registering and activating ROS-ESM

As part of [Ubuntu Pro](https://documentation.ubuntu.com/pro/) for Applications subscription,
[ROS ESM](https://ubuntu.com/robotics/ros-esm) gives you a hardened
and long-term supported ROS system for robots and its applications.
Even if your ROS distribution hasn’t reached its end-of-life `(EoL)`,
you can count on `backports` for critical security updates and `CVEs` fixes for your environment.
In addition, all upstream changes are evaluated by hand to minimise breaking changes.
By enabling our repositories, you will get trusted and stable binaries for your environment.
If you are a standard or advanced customer, you also get ROS support.
This provides you with a single point of contact to log ROS bugs.

## Benefits

ROS ESM provides four key benefits:

- 10 year LTS release lifetime for ROS bringing the highest level of security and compliance
- Security patching for over 25,000 packages in ROS, Ubuntu Universe and Ubuntu main
- Better security `KPIs` as critical `CVEs` patches are applied on average in less than 24h
- Single point of contact to log bugs and propose fixes to guarantee timely and quality fixes

For more information,
please visit [Ubuntu Pro Service Description, Extended Security Maintenance (ESM) page,](https://ubuntu.com/security/esm)
and [ROS ESM Specialist service description](https://ubuntu.com/legal/ubuntu-pro-description/ros-esm-service-description)
or [contact us for more information](https://ubuntu.com/robotics/ros-esm#get-in-touch).

After you finish this tutorial,
you may want to look at more specific how-to guides on day-to-day usages of ROS ESM,
such as [this how-to](../../how-to-guides/security/combine-esm-and-upstream-ros.md).

---

## Enabling ROS ESM

ROS ESM builds on two Canonical ESM products: `ESM-infra` and `ESM-apps`.
As a result, there are three steps to enabling ROS ESM:

1. Obtaining your token
2. Enabling ESM-infra and ESM-apps
3. Enabling ROS ESM.

Note that `ESM-infra` and `ESM-apps` are required dependencies of ROS ESM.

### Obtain your authentication token

Access to ESM is controlled by a token associated with your Ubuntu Single Sign-on `(SSO)` account.
To obtain a token go to this page <https://ubuntu.com/pro/subscribe>.
You can register for free up to 5 tokens to try out Ubuntu Pro and ROS ESM.
If you already purchased ROS ESM or Ubuntu Pro, then you will have the token and you can review it at:

<https://ubuntu.com/pro>

[Get in touch with us](https://ubuntu.com/robotics/ros-esm#get-in-touch) if you need a personalised offer.

### Enabling ESM-infra and ESM-apps

In order to enable these services, you will need:

- An Ubuntu LTS machine with a version similar to or above 16.04 LTS
- Sudo access
- An email address, or an existing Ubuntu One account
- Ubuntu Pro client version `27.11.2` or newer

Once you have your Ubuntu Pro token, make sure your Pro client is up to date:

``````{tabs}

`````{tab}  Ubuntu 20.04 and later

```bash

sudo apt update && sudo apt upgrade
sudo apt install -y ubuntu-pro-client
```

This is because the `ubuntu-advantage-tools` package has been deprecated in favour of the `ubuntu-pro-client` package.

> See More: For more information, please visit [Ubuntu Pro Client Guide](https://ubuntu.com/pro/tutorial).

`````

`````{tab} Ubuntu 18.04 and below

```bash
sudo apt update && sudo apt upgrade
sudo apt install -y ubuntu-advantage-tools
```

`````

``````

#### Confirm your Ubuntu Pro client version

Regardless of your Ubuntu distribution,
make sure you are running the latest version of the Ubuntu Pro client.
To check it, run:

```bash
sudo pro --version
```

You should have a version greater than or equal to `27.11.2`.

#### Attach the Pro client

Use the client to attach this machine to your contract using your token:

```bash
sudo pro attach YOUR_TOKEN
```

In order to see which Ubuntu Pro services are enabled you can run:

```bash
sudo pro status
```

```bash
$ pro status
SERVICE          ENTITLED  STATUS       DESCRIPTION
anbox-cloud      yes       disabled     Scalable Android in the cloud
esm-apps         yes       enabled      Expanded Security Maintenance for Applications
esm-infra        yes       enabled      Expanded Security Maintenance for Infrastructure
fips             yes       disabled     NIST-certified FIPS crypto packages
fips-updates     yes       disabled     FIPS compliant crypto packages with stable security updates
livepatch        yes       enabled      Canonical Livepatch service
ros              yes       disabled     Security Updates for the Robot Operating System
usg              yes       disabled     Security compliance and audit tools
```

You should see some of the Ubuntu Pro services,
such as Expanded Security Maintenance for Infrastructure `(esm-infra)` automatically enabled,
while others will remain disabled until you switch them on.

If it’s not, enter the following:

```bash
sudo pro enable esm-infra
```

Then, enable ESM Apps with:

```bash
sudo pro enable esm-apps
```

At any time, you can check how many deb packages are installed on your machine and from which source using:

```bash
pro security-status
```

Congratulations, you now have ESM-infra and ESM-apps enabled!
Run an upgrade to install available security updates, if any:

```bash
sudo apt update
sudo apt upgrade
```

### Enabling ROS ESM

ROS ESM is exposed in the Pro client similar to `ESM-infra` and `ESM-app`s and is controlled by that same token.
However, ROS ESM is disabled by default and not listed in the common service list.
First, let’s make sure that the Pro client is up-to-date:

```bash
sudo pro version
```

Should return version `27.11.2` or greater.

Then, let’s make sure that your token is entitled to enabling ROS ESM with:

```bash
sudo pro status --all
```

You should now see the following ROS ESM services: `ros` and `ros-updates`.
Make sure that the `entitled` column displays a `yes` in front of these services.
If not, please reach out to customer service.

Now you have everything needed to enable ROS ESM.
There are two suites available:

- **ros**: only security-related updates for ROS-related software.
- **ros-updates**: security and non-security-related updates for ROS-related software. These are security updates and bug fixes.

**To enable the ROS security updates**, run the following command:

```bash
sudo pro enable ros
```

**To enable non-security updates**, run the following command:

```bash
sudo pro enable ros-updates
```

Note that if you enter directly:

```bash
sudo pro enable ros-updates
```

You will be prompted to enable the `ros` service first, as `ros-updates` depends on `ros`.

### Rosdep set up

ROS ESM provides its own distribution and `rosdep` files.
Let's make sure you install `rosdep` from ESM and re-initialise it as follows:

``````{tabs}

`````{tab}  Noetic/Foxy (Python3)

```bash
sudo apt install python3-rosdep
sudo rm /etc/ros/rosdep/sources.list.d/20-default.list
sudo rosdep init
rosdep update
```
`````

`````{tab} Kinetic/Melodic (Python2)

```bash
sudo apt install python-rosdep
sudo rm /etc/ros/rosdep/sources.list.d/20-default.list
sudo rosdep init
rosdep update
```

`````
``````

## Using ROS ESM

Congratulations, you’re now set up to use ROS ESM!
From here, you can either install the complete ROS distro variant offered by ROS ESM (`ros_base`),
or you can use rosdep to install the specific dependencies required by your ROS project.
Let's quickly explore the two options for this tutorial.

For more information on what happens behind the scenes,
take a look at [this explanation](../../explanations/security/ros-esm-ppa-rosdep.md).

### Installing ROS ESM base variant

ROS ESM offers the upstream `metapackage` variant called `ros_base`,
which facilitates the installation of all ROS packages included in this variant.
For example, if you are working with `20.04 Focal` and its corresponding version ROS Noetic,
run the command:

```bash
sudo apt install ros-noetic-ros-base
```

```{important}
You have to remember that the Ubuntu version and ROS version are co-dependent, so you have to choose a pair.
For example, Ubuntu 16.04 LTS and ROS Kinetic,
Ubuntu 18.04 LTS and ROS Melodic,
Ubuntu 20.04 LTS and ROS 2 Foxy or ROS 1 Noetic.
Here you can find more information for [ROS distributions](http://wiki.ros.org/Distributions)
and [ROS 2 distributions](https://docs.ros.org/en/foxy/Releases.html).

```

For a more personalised installation of specific packages and to see how you can mix ROS-ESM with upstream packages,
please take a look at [this how-to](../../how-to-guides/security/combine-esm-and-upstream-ros.md).

### Installing ROS ESM project-specific dependencies

Typically, when utilising ROS ESM, your ROS workspace would already be configured with the relevant source code.
In such cases, it is highly recommended to accurately define the dependencies of your packages in the `package.xml` file
and proceed by installing all the required ROS ESM dependencies by executing the following command:

```bash
cd ros-ws
rosdep install –ignore-src –from-paths src
```

By doing so, the packages required for your project will be fetched and installed from the `ROS ESM ppa`, ensuring smooth operation.

Congratulations!
You can now compile your private packages as usual with catkin or colcon and the output binaries will be based on top of our ROS ESM,
so that you can extend the lifetime of your robots by 5 more years!

### ESM and non-ESM components

A given ROS distribution includes a huge number of packages with wildly varying levels of quality.
ROS ESM does not attempt to support them all (such a thing would be disingenuous), and instead focuses on core functionality.
Besides, it’s not unusual for upstream ROS components to break backward compatibility, while ESM will not.
One ramification of this is that ROS packages in ESM might fall behind their upstream counterparts in order to retain stability.

We of course realise that everyone’s needs are different,
and are very open to receiving feedback about anything that should be added to ROS ESM.
While such additions will need to pass some scrutiny,
we fully expect the number of ROS packages included in ESM to grow over time.

If you’d like to suggest a package or learn more,
feel free to reach out at [ubuntu-robotics-community-group@canonical.com](mailto:ubuntu-robotics-community-group@canonical.com).
