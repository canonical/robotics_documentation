# Check if a CVE is fixed in your environment

If you're running ROS in production, it's important to know whether a specific CVE
has been patched in your environment. One of the simplest ways to check this
is by using the Ubuntu CVE Tracker. To do that, follow these steps:

## 1. Look up the CVE

Go to the [Ubuntu CVE Tracker website](https://ubuntu.com/security/cves)
and search for the CVE ID, for example: `CVE-2025-3753`.
You'll find details about the vulnerability, including:

- Affected packages
- Impacted Ubuntu releases
- Fix status (e.g., Released, Needed, Not affected)
- Links to the associated public CVE entries in the NVD database

## 2. Find the fixed version

Look for the version number where the fix was released.
Make a note of the package name and the patched version for your ROS ESM release.
For example, you will find [CVE-2025-3753](https://ubuntu.com/security/CVE-2025-3753),
affecting the `ros-comm` package has been fixed for ROS ESM Noetic from version `1.17.4+2`:

![image](../../assets/images/how-to-guides-maintenance-check-cves-1.png)

## 3. Compare with your system

If you're using **Ubuntu Pro with ROS ESM**,
first make sure security updates are enabled:

```bash
pro status
```

Check which version is currently installed in your system:

```bash
apt list --installed | grep package-name
```

Replace *package-name* with the relevant name,
like `ros-noetic-ros-comm` or any other affected package.

## 4. Update if needed

If your installed version is older than the fixed one, run:

```bash
sudo apt update
sudo apt upgrade
```

This quick check helps you confirm whether potentially critical vulnerabilities
have been addressed in your ROS-based systems.
If you still **need to enable Ubuntu Pro and ROS ESM**, check out our [step-by-step guide](enable-ros-esm.md).
