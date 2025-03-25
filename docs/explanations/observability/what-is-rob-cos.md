# What is ROB COS

ROB COS stands for Robotics Canonical Observability Stack and is a superset of
[COS Lite](https://charmhub.io/topics/canonical-observability-stack/editions/lite).
ROB COS brings [observability](https://ubuntu.com/observability/what-is-observability)
to your robots and devices.

When deploying robots, the need to collect data arises sooner than expected. One might need to visualize
live or previously stored data. The necessity for data can have multiple causes: debugging, statistics
analysis, monitoring, data collection for machine learning, etc.

Moreover, as new devices are deployed, the observability capacity has to scale effortlessly.
For all these reasons ROB COS has been developed, offering an observability infrastructure
and solution for devices.

On the following drawing, we can see a fleet of devices using snaps to push data to the ROB COS server, which is then available to the user for visualization.

[!image](https://assets.ubuntu.com/v1/f4e74173-What_is_ROB_COS.png)

## How ROB COS works

The ROB COS consists of two main components:
- the server side: which hosts applications for monitoring, analysis and visualisation extending COS lite.
- the device side: a set of snaps that allow the robot to interface and communicate with the server.
consisting of a set of snaps.

The ROB COS is already including a set of applications on the server and device side.
By the modular nature of [COS](https://charmhub.io/topics/canonical-observability-stack),
you can easily select a subset of applications or even extend it with open source or even proprietary
applications.

The ROB COS is extending COS Lite in the sense that it can handle robotics data and that the clients can be deployed on devices via snaps.

### The server side

The server side (which can run on the cloud, a laptop, or any capable machine) [Juju](https://juju.is/docs/juju/tutorial), an open source orchestration engine, to easily deploy applications at any scale and [Microk8s](https://microk8s.io/docs/getting-started), a lightweight Kubernetes cluster.
bringing stability, security and scalability.

Every application running in Juju is a
[charmed operator (charm)](https://canonical-juju.readthedocs-hosted.com/en/latest/user/reference/charm/).
This means the server side can also benefit from [charmhub.io](https://charmhub.io/)
to get seamless updates over time.

The ROB COS consists of a
[Juju bundle](https://canonical-juju.readthedocs-hosted.com/en/latest/user/reference/bundle/)
ready to be deployed on any
[Juju k8s machine](https://canonical-juju.readthedocs-hosted.com/en/latest/user/explanation/kubernetes-in-juju/).

This bundle can easily be extended by the mean of an
[overlay](https://canonical-juju.readthedocs-hosted.com/en/latest/user/reference/bundle/).

Charms bundled in the ROB COS are responsible for data visualization and data storage.
The applications expected on the servers can be:

- Data processing
- Data analytics and visualization
- Monitoring system and data models
- Alert manager
- Logs aggregator
- Anomaly detector
- VPN server

### The device side

On devices, the ROB COS consists of a set of [snap](https://snapcraft.io/docs) packages.
Snaps packages are particularly suited for [robotics](https://ubuntu.com/robotics/docs)
and their limited resources reducing the need for on device operations.
Installed snaps will benefit from seamless updates and rollback from the
[Snap Store](https://snapcraft.io/store).
Additionally,
thanks to snaps, the device side can run completely from the [Ubuntu Core](https://ubuntu.com/core/docs)
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

## Who is ROB COS for

The ROB COS stack is fully open source, so anyone can use it.
Since the ROB COS is meant to observe devices,
the typical use case is to observe a fleet of devices.
Thanks to the P2P VPN, devices can be on the same site or not.

ROB COS is deployed with Juju,
meaning anyone can deploy ROB COS as a secure, scalable and resilient server.

The typical use case of ROB COS is for a company to deploy a complete observability stack
for a fleet of devices.

Whether deployed on self-hosted infrastructure or in the cloud, ROB COS can meet all the observability needs of an organization.

Additionally, Canonical offers a managed version of ROB COS so you can focus on your business.
We will run the best-in-class open source monitoring tools you need for the observability
of your applications.

You can learn more about open source observability on
[ubuntu.com/observability](http://ubuntu.com/observability).

The generic COS documentation can be found on
[charmhub.io](https://charmhub.io/topics/canonical-observability-stack).
