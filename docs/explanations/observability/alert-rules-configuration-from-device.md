# Alert rules configuration from device

Alerts rule file can be defined in Prometheus and Loki to trigger notifications on the Alertmanager.

These alert rule files can be provided by the devices directly and then hosted on the
[`COS-registration-server`](https://charmhub.io/cos-registration-server-k8s).

This allows devices to deploy the alert configurations they need specifically
or configurations that could be used by any other device.

## Rules uploaded on the COS-registration-server

The `COS-registration-server` can host alert rule files.
The supported rule files applications are Prometheus and Loki.

The server currently supports two types of rules:
- standard alert rule files: directly passed to the corresponding applications
- templated alert rule files: Jinja2 templated rule file to render against specific devices

The templated rule files are designed to allow the creation of an alert that will only affect
a defined list of devices.
The templated rule will be rendered for the devices that explicitly
declared it in the `device-loki-alert-rule-files` or `device-prometheus-alert-rule-files`
while registering on the `COS-registration-server` with the
[`COS-registration-agent`](https://snapcraft.io/cos-registration-agent).

### Templated alert rule files format

The templated rule files are [`Jinja2`](https://jinja.palletsprojects.com/en/stable/)
templates.
In the context of alert rules with COS, the Jinja2 start and stop variable are: `%%`.

The current supported variable is: `%%juju_device_uuid%%`.

Below is an example of a templated alert rule file:

```
groups:
  - name: low-memory/%%juju_device_uuid%%
    rules:
    - alert: 5GBLowMemory%%juju_device_uuid%%
      annotations:
        description: "Low memory alert specific to {{ $labels.device_instance }}"
        summary: "Robot {{ $labels.device_instance }} has less than 5 GB of memory free."
      expr: (node_memory_MemFree_bytes{device_instance="%%juju_device_uuid%%"})/1e9 < 5
      for: 5m
      labels:
        severity: critical
```
``` {note}
The name of the **group** as well as the name of the alert must be templated to
ensure its uniqueness.
```

## Alert rule files' flow from device to COS-registration-server and the applications

In the following diagram, we can see that the alert rule files distributed with the "Device-1"
are getting uploaded to the `COS-registration-server` by the `COS-registration-agent`.

After that, the "Device-2" is also registering to the server and explicitly referring to the templated rule without having to upload it.

The `COS-registration-server` renders the templated files for the devices that specified them, depending on the type of alert rule file.
It then sends the rendered files as well as the non-template ones to the various applications.

![image](https://assets.ubuntu.com/v1/b8fe6537-Alert%20rule%20files%20flow.jpg)
