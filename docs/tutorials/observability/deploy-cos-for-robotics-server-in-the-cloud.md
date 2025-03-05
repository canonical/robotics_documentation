# Deploy COS for robotics server in the cloud

COS for Robotics is a light-weight, highly-integrated, observability stack running on Kubernetes, offering a plug and play observability solution tailored for monitoring robotics devices. The server infrastructure integrates robotics-specific applications with the ones provided by [COS-lite](https://charmhub.io/topics/canonical-observability-stack/editions/lite).
The server side is designed for the Edge and capable of running alongside MicroK8s and Juju with limited computing resources (around 8 GB of memory).
On the device side, different agents in the form of Snaps are provided to simplify the process of registering devices on the server. These agents enable users to connect their robots to the COS for Robotics applications and immediately initiate monitoring operations.
Each robot in your fleet can be set up with the snap agents, registered and observed, allowing for efficient management across an entire fleet.

![image](https://assets.ubuntu.com/v1/64dae60b-cos-for-robotics.png)

COS for Robotics is designed for anyone requiring robotics device monitoring, offering straightforward deployment and management. It is open-source, user-friendly and lightweight, ensuring access to anyone.
Moreover, it is designed with customization in mind. It offers the flexibility to add new applications in the form of charms or OCI images and enhance existing ones.
The goal of COS for Robotics is to provide the robotics community with an ecosystem of observability applications for robotics that is open, easy to use and deploy and fully customizable.
The purpose of this tutorial is to showcase how to set up the COS for Robotics application on a server and how to easily register a ROS 2 device on it and start monitoring it. Now, let’s go and deploy that bundle!

## Server Side

The COS for Robotics lite bundle is a Juju-based observability stack, running on Kubernetes. The bundle consists of [Foxglove-Studio](https://charmhub.io/foxglove-studio-k8s), [Ros2BagFileserver](https://charmhub.io/ros2bag-fileserver-k8s), [COS-registration-server](https://charmhub.io/cos-registration-server-k8s), [Prometheus](https://charmhub.io/prometheus-k8s), [Loki](https://charmhub.io/loki-k8s), [Alertmanager](https://charmhub.io/alertmanager-k8s) and [Grafana](https://charmhub.io/grafana-k8s).

### Install prerequisites

This tutorial assumes you have a Juju controller bootstrapped on a MicroK8s cloud that is ready to use. Let’s proceed with the installation.

#### Install MicroK8s

Install the microk8s snap with:
```bash
sudo snap install microk8s --channel 1.31-strict
```

Add the user to the microk8s group for unprivileged access and give use permission to read the `~/.kube` director:

```bash
sudo adduser $USER snap_microk8s
sudo chown -f -R $USER ~/.kube
```

Wait for microk8s to finish initialising with:

```bash
sudo microk8s status --wait-ready
```

Enable the storage and dns addons which are required for the Juju controller:

```bash
sudo microk8s enable hostpath-storage dns
```

Finally, ensure your new group membership is apparent in the current terminal (Not required once you have logged out and back in again):

```bash
newgrp snap_microk8s
```

#### Install Juju

Install the Juju snap with:

```
sudo snap install juju --channel 3.5/stable
```

Since the juju package is strictly confined, you also need to manually create a path:

```
mkdir -p ~/.local/share
```

Now bootstrap a Juju controller into your MicroK8s
juju bootstrap microk8s rob-cos-controller.
If successful the terminal will show the following message:

```
Bootstrap complete, controller "rob-cos-controller" is now available in namespace "controller-rob-cos-controller"
```

#### Configure and enable Metallb

The bundle comes with Traefik to provide ingress, for which the `metallb` addon must be enabled. [Metallb](https://metallb.universe.tf/) provides LoadBalancer functionality and requires the source IP address of the host system for outbound connections. Run the following command to retrieve the IP address:

```
sudo apt update && sudo apt install -y jq
IPADDR=$(ip -4 -j route get 2.2.2.2 | jq -r '.[] | .prefsrc')
```

Then, enable metallb with the following command:

```
sudo microk8s enable metallb:$IPADDR-$IPADDR
```

### Deploy the COS for Robotics Lite bundle

Now, let’s create a dedicated model for the COS Lite bundle with the following:

```
juju add-model cos-robotics-model
juju switch cos-robotics-model
```

Next, download the robotics overlay with:

```
curl -L https://raw.githubusercontent.com/canonical/rob-cos-overlay/main/robotics-overlay.yaml -O
```

Finally, deploy it with:

```
juju deploy cos-lite --trust --overlay ./robotics-overlay.yaml
```

Now you can sit back and watch the deployment take place:

```bash
juju status --watch 5s --color --relations
```

COS will  be ready to use when the juju status shows all the machines active and the agents idle as follow:

![image](https://assets.ubuntu.com/v1/97b37234-juju_status.png)

Now COS for Robotics is good to go: you can register devices to it to begin the monitoring!
Browse endpoints and catalogue
When all the charms are deployed, you can head over to browse their built-in web-UIs. You can find out their addresses from the [`show-proxied-endpoints`](https://charmhub.io/traefik-k8s/actions#show-proxied-endpoints) `Traefik` action. In your terminal type:

```bash
juju run traefik/0 show-proxied-endpoints
```

The catalogue endpoint can be visualised on your browser and it will list the catalogue of applications offered by COS for Robotics. From the proxied endpoints, the catalogue URL should be similar to:

```bash
"catalogue":{"url": http://<cos-robotics-server-ip>/cos-robotics-model-catalogue"}
```

Now by navigating to the catalogue URL in your browser, the catalogue of all the available application will be displayed:

![image](https://assets.ubuntu.com/v1/32e58421-catalogue.png)


#### Grafana Login

Clicking on the **Grafana** application will prompt you for username and password as follows:

![image](https://assets.ubuntu.com/v1/bf1fa2db-grafana_welcome.png)

The default password for Grafana is automatically generated for every installation. To access Grafana’s web interface, use the username `admin`, and the password obtained from the `[get-admin-password](https://charmhub.io/grafana-k8s/actions)` action as follows:

```bash
juju run grafana/0 get-admin-password
```

Now that the server is set up, let’s see how to deploy and register a device for monitoring.
