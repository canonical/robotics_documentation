# How to enable ROS ESM

ROS ESM builds on two Canonical ESM products: ESM-infra and ESM-apps. As a result, there are three steps to enabling ROS ESM:

1. Obtaining your token
2. Enabling ESM-infra and ESM-apps
3. Enabling ROS ESM.

Note that ESM-infra and ESM-apps are required dependencies of ROS ESM.

## Obtain your authentication token

Access to ESM is controlled by a token associated with your Ubuntu Single Sign-on `(SSO)` account. If you already purchased ROS ESM, then you will have the token and you can review it on:

<https://ubuntu.com/pro>

Ubuntu Advantage is now Ubuntu Pro. Ubuntu Pro expands our famous ten-year security coverage to an additional 23,000 packages beyond the main operating system.

If you haven’t purchased ROS ESM yet, please [contact us](https://ubuntu.com/robotics/ros-esm#get-in-touch) and a sales representative will get in touch with you.

## Enable ESM-infra and ESM-apps

In order to enable these services, you will need:

* An Ubuntu LTS machine with a version similar to or above 16.04 LTS
* Sudo access
* An email address, or an existing Ubuntu One account
* Ubuntu Pro client version 27.11.2 or newer

Once you have your contract token, make sure your Pro client is up to date:

```bash
sudo apt update && sudo apt upgrade
sudo apt install -y ubuntu-advantage-tools
```

For more information, please visit [Ubuntu Pro Client Guide](https://discourse.ubuntu.com/t/ubuntu-pro-client/31027).

### Confirm your Ubuntu Pro client version

Regardless of your Ubuntu distribution, make sure you are running the latest version of the Ubuntu Pro client. To check it, run:

```bash
sudo pro --version
```

You should have a version greater than or equal to 27.11.2.

### Attach the Pro client

Use the client to attach this machine to your contract using your token:

```bash
sudo pro attach YOUR_TOKEN
```

Note, if you had previously attached a `UA token`, you might see a message like this:

```bash
This machine is already attached to YOUR_EMAIL
To use a different subscription first run: sudo pro detach.
 ```

In that case, detach your token as indicated, and try attaching your Ubuntu Pro token again.

You should see some of the Ubuntu Pro services, such as Expanded Security Maintenance for Infrastructure `(esm-infra)` automatically enabled, while others will remain disabled until you switch them on. You can check this with:

```bash
sudo pro status
```

If it’s not, enter the following:

```bash
sudo pro enable esm-infra
```

Then, enable ESM Apps with:

```bash
sudo pro enable esm-apps --beta
```

At any time, you can check how many deb packages are installed on your machine and from which source using:

```bash
pro security-status
```

Congratulations, you now have ESM-infra and ESM-apps enabled! Run an upgrade to install available security updates, if any:

```bash
sudo apt update
sudo apt upgrade
```

More information at: <https://ubuntu.com/security/esm>

## Enable ROS ESM

ROS ESM is exposed in the Pro client similar to ESM-infra and ESM-apps and is controlled by that same token. However, ROS ESM is disabled by default and not listed in the common service list. First, let’s make sure that the Pro client is up-to-date:

```bash
sudo pro version
```

Should return version `27.11.2` or greater.

Then, let’s make sure that your token is entitled to enabling ROS ESM with:

```bash
sudo pro status --all
```

You should now see the following ROS ESM services: ‘ros’ and ‘ros-updates’. Make sure that the ‘entitled’ column displays a ‘yes’ in front of these services.  If not, please reach out to customer service as shown in your welcome email.

Now you have everything needed to enable ROS ESM. There are two suites available:

* **ros**: only security-related updates for ROS-related software.
* **ros-updates**: security and non-security-related updates for ROS-related software. These are security updates and bug fixes.

**To enable the ROS security updates**, run the following command:

```bash
sudo pro enable ros --beta
```

**To enable non-security updates**, run the following command:

```bash
sudo pro enable ros-updates --beta
```

Note that if you enter directly:

```bash
sudo pro enable ros-updates --beta
```

You will be prompted to enable the ‘ros’ service first, as ‘ros-updates’ depends on ‘ros’.
