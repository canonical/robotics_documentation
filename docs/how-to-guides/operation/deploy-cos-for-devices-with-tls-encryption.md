# Deploy {{COS_ROB}} for devices with TLS encryption

```{warning}
**Beta Notice**: {{COS_ROB}} is currently in `beta`.
Content and features may change,
and some functionality may be incomplete or experimental.
Feedback is welcome as we continue to improve.
```

{{COS_ROB}} devices offers flexible deployment options,
allowing for either an unencrypted configuration or a more secure setup with TLS termination enabled.
With TLS termination enabled,
the Traefik charm acts as the TLS termination point by integrating to a self signed certificate charm or to an external CA charm.

This guide details the deployment of {{COS_ROB}} with TLS termination. It outlines the necessary steps to set up a {{COS_ROB}}, enabling it to successfully register and establish secure communication with the server.


## Server side
This guide assumes that {{COS_ROB}} has been deployed as outlined in the [main tutorial]((../../tutorials/observability/deploy-cos-for-robotics-server-in-the-cloud.md))
.
Next, we’ll set up TLS for the deployment using the [self-signed-certificates charm](https://charmhub.io/self-signed-certificates).
To keep things organized,
we’ll deploy the TLS components in a separate Juju model called `tls`.

```bash
juju add-model tls
juju switch tls
```

Deploy the charm in the `tls` model with:

```bash
juju deploy self-signed-certificates --channel=latest/edge
```

This charm will manage the certificate authority (CA) and issue self-signed certificates to Traefik.
In order to make the TLS charm endpoints available to our other model,
we need to setup [cross-models relations](https://documentation.ubuntu.com/juju/3.6/reference/relation/).
This is achieved by offering the charm relations:

```bash
juju offer self-signed-certificates:send-ca-cert send-ca-cert
juju offer self-signed-certificates:certificates certificates
```

In this way,
those relations can be consumed by the charms in our robotics model,
such as Traefik.

Now, let's switch back to the `cos-robotics-model` and consume the relations:

```bash
juju switch cos-robotics-model
juju consume -m cos-robotics-model admin/tls.certificates
juju consume -m cos-robotics-model admin/tls.send-ca-cert
```

Finally, integrate the relations with Traefik and Grafana to enable TLS:

```bash
juju integrate traefik certificates
juju integrate traefik send-ca-cert
juju integrate grafana send-ca-cert
```

The `send-ca-cert` relation provides the public root CA certificate that is used to sign all certificates issued by the `self-signed-certificates` charm.
Prometheus and Loki are accessed by Grafana through Traefik,
which means Grafana must trust the CA that issued Traefik’s certificates.
Without the `send-ca-cert` relation,
Grafana would see Traefik’s certificates as untrusted,
breaking secure communication.

That’s it for the server side,
you can verify that now traefik is serving endpoints on `https` with:

```bash
juju run traefik/0 show-proxied-endpoints
```

The output should look like this:

```bash
Running operation 12 with 1 task
  - task 13 on unit-traefik-0

Waiting for task 13...
proxied-endpoints: '{"traefik": {"url": "https://10.239.43.60"}, "ros2bag-fileserver/0":
  {"url": "10.239.43.60:2222"}, "prometheus/0": {"url": "https://10.239.43.60/cos-robotics-model-prometheus-0"},
  "loki/0": {"url": "https://10.239.43.60/cos-robotics-model-loki-0"}, "alertmanager":
  {"url": "https://10.239.43.60/cos-robotics-model-alertmanager"}, "catalogue": {"url":
  "https://10.239.43.60/cos-robotics-model-catalogue"}, "foxglove-studio": {"url":
  "https://10.239.43.60/cos-robotics-model-foxglove-studio"}, "cos-registration-server":
  {"url": "https://10.239.43.60/cos-robotics-model-cos-registration-server"}, "ros2bag-fileserver":
  {"url": "https://10.239.43.60/cos-robotics-model-ros2bag-fileserver"}}'
```

## Device side

When TLS termination is enabled,
each device must trust the certificate provided by Traefik for the registration and communication to work.

### Set the certificate on the device

First, retrieve the CA certificate from the `self-signed-certificates` charm on the server:

```bash
 juju run self-signed-certificates/0 get-ca-certificate
```

Copy the output and save it to a file.
On Ubuntu Desktop or Server,
certificates are typically installed in `/usr/local/share/ca-certificates` and activated with:

```bash
sudo update-ca-certificates
```

In this way,
the certificate will be available system wide and the agents running on the robot will automatically trust the certificate.

```
Note: this works only on Ubuntu Desktop and Server. For Ubuntu Core a system wide solution is not available yet.
```

### Install the agents

The [main tutorial](../../tutorials/observability/deploy-cos-for-robotics-agent-on-your-robot.md) shows how to deploy {{COS_ROB}} on your robot.
That setup does not involve the use of TLS.
The configuration of the agents on the robot is achieved via a configuration snap.
We prepared two configurations snaps with with different levels of configuration:
- **basic**: Provides a basic setup to quickly start monitoring and collecting data from a device. ⚠️ Not production ready - intended only for testing and development.
- **advanced**: Provides an extended setup with additional features such as TLS, identity management and Ceph storage.
In order to set up the robot with TLS the advanced configuration must be installed.
Here the various agents are configured to use the certificates installed on the device.

An helper script to setup TLS is available for download:


```bash
curl -L https://raw.githubusercontent.com/canonical/rob-cos-device-setup/advanced-setup/setup-robcos-device.sh -O
```

And run it with:

```bash
sudo bash setup-robcos-device.sh
```

The script will initiate prompts for the robot UID and the rob-cos-server URL.
While the robot UID is optional,
the URL is mandatory (make sure to set the URL with HTTPS).
The queries and response will look as follows:

```bash
Please enter the device-uid:
my-new-tls-robot

Please enter the rob-cos-server-url:
https://<rob-cos-server-ip>/rob-cos-model
```

Your device should now be successfully registered with {{COS_ROB}}, with TLS enabled.

### Enable Foxglove Bridge WSS

The Foxglove Bridge agent running on the device uses WebSockets to exchange data with Foxglove Studio served by the browser.
To establish a secure WebSocket connection (wss://),
the device needs a certificate and a key that can be supplied to the application and validated by the browser.
The `advanced` branch of the configuration snap sets the `generate-device-tls-certificate` flag in the device.yaml.
This flag triggers the generation of a TLS certificate and key,
which are then stored in the device's `rob-cos-data-sharing` snap.
The Foxglove Bridge configuration subsequently uses this certificate by referencing the relevant paths.
Currently, the certificate generated for the Foxglove Bridge must be manually trusted by your browser. 
To do this in Google Chrome:
- Open a new tab and navigate to `chrome://certificate-manager/localcerts/usercerts`.
- The certificate is avilable on the device at: `/var/snap/foxglove-bridge/common/rob-cos-shared-data/device.crt`
- Click on `Import` and select the certificate file from your device.
- Once imported, the certificate should appear under the `Installed by You` section.
After these steps, your browser will trust the certificate,
allowing for secure WebSocket communication with the Foxglove Bridge.
