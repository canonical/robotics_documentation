# Enable TLS encryption in {{ COS_ROB }}

```{warning}
**Beta Notice**: {{ COS_ROB }} is currently in `beta`.
Content and features may change,
and some functionality may be incomplete or experimental.
Feedback is welcome as we continue to improve.
```

{{ COS_ROB }} offers flexible deployment options,
allowing for either an unencrypted configuration
or a more secure setup with TLS termination enabled.
With TLS termination enabled,
the Traefik charm acts as the TLS termination point
by integrating to a self signed certificate charm
or to an external certificate authority charm.

This guide details the deployment of {{ COS_ROB }} with TLS termination.
It outlines the necessary steps to set up a {{ COS_ROB }} device,
enabling it to successfully register and establish secure communication with the server.
The first part will detail how to setup the Server side,
while the second will focus on the device.

## Server side

First, we will proceed by setting up TLS on the server side.
This guide assumes that {{ COS_ROB }} is up an running.
You can follow the [main tutorial](../../tutorials/observability/deploy-cos-for-robotics-server-in-the-cloud.md)
to do so.
From there, we’ll set up TLS for the deployment
using the [self-signed-certificates charm](https://charmhub.io/self-signed-certificates),
which provides self-signed X.509 certificates to charms.

To keep things organized,
We deploy the TLS components in a separate Juju model called `tls`.
Let us start by creating this model:

```bash
juju add-model tls
juju switch tls
```

Deploy the charm in the `tls` model with:

```bash
juju deploy self-signed-certificates --channel=1/stable
```

This charm will manage the certificate authority (CA)
and issue self-signed certificates to Traefik and devices.
In order to make the TLS charm endpoints available to other models,
we need to setup [cross-models relations](https://documentation.ubuntu.com/juju/3.6/reference/relation/).
This is achieved by offering the charm relations:

```bash
juju offer self-signed-certificates:send-ca-cert send-ca-cert
juju offer self-signed-certificates:certificates certificates
```

The output will look as follows:

```bash
Application "self-signed-certificates" endpoints [send-ca-cert] available at "admin/tls.send-ca-cert"
Application "self-signed-certificates" endpoints [certificates] available at "admin/tls.certificates"
```

In this way,
those relations can be consumed by the charms in our {{ COS_ROB }} model,
such as Traefik.

Now,
let's switch back to the `cos-robotics-model` and consume the relations:

```bash
juju switch cos-robotics-model
juju consume admin/tls.certificates
juju consume admin/tls.send-ca-cert
```

Finally,
integrate the relations with Traefik and Grafana to enable TLS:

```bash
juju integrate traefik certificates
juju integrate traefik send-ca-cert
juju integrate grafana send-ca-cert
```

The `send-ca-cert` relation
provides the public root CA certificate
that is used to sign all certificates issued
by the `self-signed-certificates` charm.
Prometheus and Loki are accessed by Grafana through Traefik,
which means Grafana must trust the CA that issued Traefik’s certificates.
Without the `send-ca-cert` relation,
Grafana would see Traefik’s certificates as not trusted,
preventing secure communication from being established.

That’s it for the server side,
you can verify that Traefik is now serving endpoints on `https` with:

```bash
juju run traefik/leader show-proxied-endpoints
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

We can see in this output that the proxied-endpoints URLs are using the https protocol.

## Device side

When TLS termination is enabled,
each device must trust the certificate provided by Traefik
for the registration and communication to work.
Below,
the steps to install the self-signed certificate generated on the server
onto the device are outlined.

### Set the certificate on the device

First,
retrieve the CA certificate from the `self-signed-certificates` charm on the server:

```bash
juju run self-signed-certificates/0 get-ca-certificate
```

The output will show the public CA as follows:

```bash
Running operation 11 with 1 task
  - task 12 on unit-self-signed-certificates-0

Waiting for task 12...
ca-certificate: |
  -----BEGIN CERTIFICATE-----
  MIIDZzCCA....
  -----END CERTIFICATE-----

```

Copy the certificate content and save it into a file ending with `.crt`, for example:

```bash
nano traefik-ca.crt
```

```{warning}
Note: When copying the certificate from the output above,
Make sure you *do not* include any leading spaces before the certificate lines.
The file should start exactly with `-----BEGIN CERTIFICATE-----` at the beginning of the line.
If the certificate lines are indented, the certificate will be invalid.
```

Move this file into the system’s trusted CA directory:

```bash
sudo mv traefik-ca.crt /usr/local/share/ca-certificates/
```

Finally activate the certificate by updating the certificates trust store with:

```bash
sudo update-ca-certificates
```

In this way,
the certificate will be available system wide,
and the agents running on the robot can trust the certificate.

### Verify connectivity

Now that the certificate is installed,
verify that you can successfully connect over HTTPS:

```bash
curl -vvv https://<cos-robotics-server-ip>/cos-robotics-model-catalogue
```

If the setup is correct,
you should see a valid TLS handshake and the expected response from the server.

```{warning}
Note: this process of making the certificates available system-wide,
works only on Ubuntu Desktop and Server.
For Ubuntu Core a system wide solution is not available yet.
```

### Install the agents

The [main tutorial](../../tutorials/observability/deploy-cos-for-robotics-agent-on-your-robot.md)
shows how to register a device with {{ COS_ROB }} without TLS,
using the [basic](https://github.com/canonical/rob-cos-demo-configuration)
configuration snap.
This configuration provides a basic setup
to quickly start monitoring and collecting data from a device.

In this guide,
we use the
[advanced](https://github.com/canonical/rob-cos-demo-configuration/tree/advanced)
configuration snap instead.
This extended setup enables TLS
and configures all agents to use the certificates installed on the device.

The [advanced](https://github.com/canonical/rob-cos-demo-configuration/tree/advanced)
branch of the [demo configuration snap](https://snapcraft.io/rob-cos-demo-configuration),
sets the `generate-device-tls-certificate` flag in the device configuration YAML.
This flag triggers the generation of a private key and a certificate signing request,
which is sent to the registration server upon [registration](https://github.com/canonical/cos-registration-agent?tab=readme-ov-file#setup).
The server generates a leaf certificate
to be stored in the device's `rob-cos-data-sharing` snap.

The Foxglove bridge running on the device
uses WebSockets to exchange data with Foxglove Studio served by the browser.
To establish a secure WebSocket connection (**wss://**),
the [Foxglove bridge configuration](https://github.com/canonical/rob-cos-demo-configuration/blob/advanced/snap/local/configuration/foxglove-bridge.yaml)
then uses this certificate by referencing the relevant paths.

Before proceeding, let's make sure that the Foxglove bridge snap can read
the certificates from the `rob-cos-data-sharing` snap.
Let's connect the bridge to it by executing the following command:

```bash
sudo snap connect foxglove-bridge:rob-cos-common-read rob-cos-data-sharing:rob-cos-common-read
```

Now, disconnect the device by removing the cos-registration-agent snap:

```bash
sudo snap remove cos-registration-agent
```

Next, refresh the configuration snap to switch to the advanced configuration channel:

```bash
sudo snap refresh rob-cos-demo-configuration --channel=advanced/beta
```

Reset the configuration to ensure the advanced settings are applied:

```bash
sudo rob-cos-demo-configuration.reset-config
```

Configure the base URL for the model, making sure to use the https schema:

```bash
snap set rob-cos-demo-configuration rob-cos-base-url=https://<rob-cos-server-ip>/cos-robotics-model
```

Finally, reinstall the cos-registration-agent snap to register the device with TLS:

```bash
sudo snap install cos-registration-agent --edge
```

```{warning}
Note: The generation of the leaf certificate for the device is asynchronous.
As soon as the registration is started a private key and a CSR are generated,
the CSR is sent to the registration server.
Then the agent will keep polling for a signed certificate to be available on the database.
This might take up to 5 minutes.
```

Your device should now be successfully registered with {{ COS_ROB }},
with TLS enabled.

## Laptop Side

Now that our server and device are setup with the correct certificates,
we need to make sure our laptop and browser trust them.
The only certificate that has to be trusted
is the CA certificate issued by the self-signed-certificates charm,
since the device certificate are leaf certificates.

First, let's create a `traefik-ca.crt` file on our laptop.
The content is the same of the CA we installed on the device earlier,
obtained by running the following command on the server:

```bash
juju run self-signed-certificates/0 get-ca-certificate
```

```{warning}
Note: When copying the certificate from the output above,
Make sure you *do not* include any leading spaces before the certificate lines.
The file should start exactly with `-----BEGIN CERTIFICATE-----` at the beginning of the line.
If the certificate lines are indented, the certificate will be invalid.
```

Finally, import the file in Google Chrome as follows:

- Open a new tab and navigate to `chrome://certificate-manager/localcerts/usercerts`.
- Click on **Import** and select the certificate files from your laptop.
- Once imported, the certificate should appear under the
  **Installed by You** section.

After these steps,
your browser will trust the certificate,
allowing for full TLS.

## Security considerations

### Handle CA distribution carefully

The root CA certificate must be manually distributed to every device
and operator laptop, as shown in this guide.
Take care to transfer the CA file over a secure channel,
verify its integrity before installing it,
and never skip certificate validation to work around distribution issues —
doing so defeats the purpose of TLS entirely.
In large fleets or organisations with many operators,
the overhead of maintaining this process securely is worth considering
when choosing a TLS provider.
Refer to the [Security with X.509 certificates](https://charmhub.io/topics/security-with-x-509-certificates)
topic on Charmhub for guidance.

### Protect access to the Juju TLS model

The CA private key managed by the `self-signed-certificates` charm
is the root of trust for the entire deployment.
Any operator with write access to the `tls` Juju model
can issue certificates that will be trusted by all registered devices.
Apply the principle of least privilege to Juju user permissions
and restrict access to the `tls` model to authorised operators only.

### Understand the scope of system-wide CA trust on devices

Installing the CA certificate into `/usr/local/share/ca-certificates/`
and running `update-ca-certificates` extends trust to **every process**
running on that device, not only the COS agents.
Any certificate signed by this CA will be accepted as valid by the entire OS.
This is the intended behaviour for this deployment,
but it means the CA private key must be kept secure.
If the CA is compromised, all devices that have installed it must be considered at risk.

### Device leaf certificates are not automatically renewed

The `self-signed-certificates` charm handles automatic renewal
of server-side certificates (Traefik, Grafana).
Device leaf certificates, however, are issued at registration time
and are not automatically renewed.
By default, device leaf certificates are valid for 90 days.
If a device leaf certificate expires,
the device will need to re-register with the server to obtain a new one.
Monitor certificate validity in long-running deployments,
and consider adjusting the default validity period to suit your fleet's operational cycle.

### There is no certificate revocation mechanism for devices

There is currently no certificate revocation list (CRL) or OCSP responder
for device leaf certificates.
If a device is decommissioned or suspected to be compromised,
be aware of the following limitations:

- The registration server is a configuration and listing service only.
  Removing a device from it does not prevent a compromised device
  from continuing to publish data, as there is no identity-based
  access control on data ingestion.
- If the device's private key may have been exposed,
  the only way to invalidate all issued certificates is to rotate the CA
  using the [`rotate-private-key`](https://charmhub.io/self-signed-certificates/actions) action
  on the `self-signed-certificates` charm.
  This requires reinstalling the new CA certificate on every device and operator laptop,
  and re-registering all devices.

### Device private key is protected by snap isolation, not encryption at rest

During registration, a private key and a CSR are generated on the device
and the private key is stored in the `rob-cos-data-sharing` snap data directory.
Snap data directories are owned by root and isolated between snaps
through AppArmor and seccomp policies,
which provides process-level protection.
Physical access to the device remains a risk:
consider enabling full-disk encryption on the robot's storage
when the threat model requires it.

### Foxglove bridge WebSocket is accessible on the local network

The Foxglove bridge listens for WSS (WebSocket over TLS) connections
using the device leaf certificate.
By default, this port may be reachable by any host on the local network.
Use firewall rules to restrict access to the Foxglove bridge port
to trusted hosts only.

### Ubuntu Core devices cannot use system-wide CA distribution

The `update-ca-certificates` mechanism used in this guide
works only on Ubuntu Desktop and Server.
Devices running Ubuntu Core do not support this system-wide approach yet,
and a suitable solution for Ubuntu Core is not yet available.
Take this into account when planning your fleet's operating system.
