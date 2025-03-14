# What is ROB COS?

ROB COS stands for Robotics Canonical Observability Stack and is a superset of
[COS Lite](https://charmhub.io/topics/canonical-observability-stack/editions/lite).
ROB COS brings [observability](https://ubuntu.com/observability/what-is-observability)
to your robots and devices.

When deploying robots, the need to collect data arises sooner than expected. One might need to visualize
live or previously stored data. The necessity for data can have multiple causes: debugging, statistics
analysis, monitoring, data collection for machine learning, etc.

Over the deployment of new devices, the observability capacity has to scale effortlessly.
This is for all these reasons that the ROB COS has been developed, offering an observability infrastructure
and solution for devices.

On the following drawing, we can see the fleet devices using snaps to push data to the ROB COS server and then the user

[!image](https://assets.ubuntu.com/v1/f4e74173-What_is_ROB_COS.png)

## ROB COS

The ROB COS can be separated in two: the server side, overlaying the
[COS Lite](https://charmhub.io/topics/canonical-observability-stack/editions/lite) and the device side,
consisting of a set of snaps.

The ROB COS is already including a set of applications on the server and device side.
By the modular nature of [COS](https://charmhub.io/topics/canonical-observability-stack),
you can easily select a subset of applications or even extend it with open source or even proprietary
applications.

The ROB COS is extending the
[COS Lite](https://charmhub.io/topics/canonical-observability-stack/editions/lite) in the sense that it can
handle robotics data and that the clients can be deployed on devices via snaps.

### The server side

Since ROB COS is extending the
[COS Lite](https://charmhub.io/topics/canonical-observability-stack/editions/lite),
the server side is running reliably alongside [MicroK8s](https://microk8s.io/) and [Juju](https://juju.is/)
bringing stability, security and scalability.

Every application running in Juju is a
[charmed operator (charm)](https://juju.is/docs/juju/charmed-operator).
This means the server side can also benefit from [charmhub.io](https://charmhub.io/)
to get seamless updates over time.

The ROB COS consists of a [Juju bundle](https://juju.is/docs/juju/bundle)
ready to be deployed on any [Juju k8s machine](https://juju.is/docs/juju/kubernetes-in-juju).

This bundle can easily be extended by the mean of an
[overlay](https://juju.is/docs/sdk/charm-bundles#heading--overlay-bundle).

Charms bundled in the ROB COS are responsible for data visualization and data storage.
The applications expected on the servers can be:
- Data processing
- Data analytics and visualization
- Monitoring system and data models
- Alert manager
- Logs aggregator
- Anomaly detector
- VPN server
- Etc

### The device side

On devices, the ROB COS consists of a set of [snaps](https://snapcraft.io/docs) packages.
Snaps packages are particularly suited for [robotics](https://ubuntu.com/robotics/docs)
and their limited resources reducing the need for on device operations.
Installed snaps will benefit from seamless updates and rollback from the
[Snap Store](https://snapcraft.io/store).
Additionally,
the device side can run completely from the [Ubuntu Core](https://ubuntu.com/core/docs)
Operating system engineered for IoT and embedded.

Snaps running on the device are responsible for collecting data and syncing them to the server side.
By the mean of configuration,
device’s snaps could collect and synchronize data according to the bandwidth and storage available.

The applications expected on the devices can be:
- Telemetry collectors
- Data collectors (i.e: ROS 2 data)
- Logs collectors
- VPN client
- Device manager client
- Etc

## For who?

The ROB COS stack is fully open source, so anyone can use it.
Since the ROB COS is meant to observe devices,
the typical use case is to observe a fleet of devices.
Thanks to the P2P VPN, devices can be on the same site or not.

ROB COS is deployed with Juju,
meaning anyone can deploy ROB COS as a secure, scalable and resilient server.

The typical use case of ROB COS is for a company to deploy a complete observability stack
for a fleet of devices.

Being deployable on a self-hosted or cloud infrastructure,
ROB COS will meet all needs required by an organization.

Additionally, Canonical offers a managed version of ROB COS so you can focus on your business.
We will run the best-in-class open source monitoring tools you need for the observability
of your applications.

You can learn more about open source observability on
[ubuntu.com/observability](http://ubuntu.com/observability).

The generic COS documentation can be found on
[charmhub.io](https://charmhub.io/topics/canonical-observability-stack).
