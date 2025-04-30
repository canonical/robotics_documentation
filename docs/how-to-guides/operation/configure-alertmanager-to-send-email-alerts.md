# Configure Alertmanager to send email alerts

```{warning}
**Beta Notice**: The observability documentation is currently in `beta`. 
Content and features may change, and some functionality may be incomplete or experimental. 
Feedback is welcome as we continue to improve.
```

Once an alert is triggered by Prometheus or Loki,
the alert is received and distributed by Alertmanager.

Alertmanager can be configured to send notifications on multiple
[receivers](https://prometheus.io/docs/alerting/latest/configuration/#general-receiver-related-settings)

In this how-to guide,
you will configure the Alertmanager application to send emails on alerts.

## Alertmanager configuration

The configuration of Alertmanager is done by a YAML file later loaded in the application.
The YAML file follows the
[scheme defined in the official documentation](https://prometheus.io/docs/alerting/latest/configuration/#file-layout-and-global-settings).

### Get the app password

Before configuring the Alertmanager, you must get a token called "app password",
to let Alertmanager send emails from your account.

While logged into your Gmail account, go to the [App passwords page](https://myaccount.google.com/apppasswords) and generate a new app password.
visit the [Gmail app password page](https://myaccount.google.com/apppasswords),
and create a new app password.

Make sure to copy the created code, and place it in the `alert-manager.yaml`
configuration file.

### Write the configurations file for Alertmanager

Alertmanager is configured via a YAML file.
To get a starting point for the file,
you can get the actual `alert-manager.yaml` by going on your Alertmanager instance.
In the "status" tab, you will find at the bottom, the actual config to use as a starting point:

![image](https://assets.ubuntu.com/v1/15a945f0-alertmanager-status.png)

In addition to the default configuration,
you will add two entry: `route` and `receivers`.

#### Route

The [route attribute](https://prometheus.io/docs/alerting/latest/configuration/#route-related-settings) defines where and how the alerts are dispatched.
Here, the idea is to group alerts not only from devices but also from Juju applications.
The alerts are sent in batches in order to prevent continuous notifications.

Additionally, the route defines to which receiver the alerts are then forwarded.
In this case, it will be emails.

The route is defined as follows:

```YAML
route:
  receiver: 'email'
  group_by:
    - juju_model_uuid
    - juju_application
    - juju_model
  continue: false
  group_wait: 30s
  group_interval: 5m
  repeat_interval: 1h
  routes:
    - receiver: 'email'
      group_wait: 10s
      match_re:
        severity: critical|warning|none
      continue: true
```

#### Receiver

The [receiver attribute](https://prometheus.io/docs/alerting/latest/configuration/#receiver-integration-settings)
defines the integration with specific receivers (email, chat, web-hooks, etc).
Receivers usually require an authentication token,
which, in the case of Gmail, is the app password.

In the receiver you must declare the sender's email (the one associated to the app password),
and the recipient's email.

The receiver is defined as follows:

```YAML
receivers:
  - name: 'email'
    email_configs:
      - to: 'all@my-company.com'
        from: 'user.name@gmail.com'
        smarthost: 'smtp.gmail.com:587'
        auth_username: 'user.name@gmail.com'
        auth_password: 'APP_TOKEN'
        auth_identity: 'user.name@gmail.com'
```

### Apply the Alertmanager configuration

With the previously defined Alertmanager configuration in an `alert-manager.yaml`,
you can apply the configuration to the Juju application.

The `alertmanager-k8s` declares a [`config_file` configuration](https://charmhub.io/alertmanager-k8s/configurations#config_file) that can be used with the following command:

```BASH
juju config alertmanager config_file='@./alert-manager.yaml'
```

You can verify that the configuration got applied by going in the status tab of Alertmanager.

Since the Alertmanager Juju application has a watchdog alert, you will receive your first alert right after.

## Email alert template

Now that the configuration of the application is done,
you can also configure the [email notification template](https://prometheus.io/docs/alerting/latest/notifications/#notification-template-reference)
used for sending notifications.
The template lets you customize both the appearance and the data in your notification.

In the case of an email notification, the template is an HTML file.
You can get the [default template from GitHub](https://github.com/prometheus/alertmanager/blob/main/template/email.html) with the following command:

```BASH
wget https://raw.githubusercontent.com/prometheus/alertmanager/refs/heads/main/template/email.html
```

Similarly to the `config_file` configuration,
`alertmanager-k8s` has a
[`template-config`](https://charmhub.io/alertmanager-k8s/configurations#templates_file)

You can then apply the new template with the following command:

```BASH
juju config alertmanager templates_file='@./email.html'
```

You must now update your Alertmanager configuration, so the receiver uses the new template:

```BASH
receivers:
  - name: 'email'
    email_configs:
      - to: 'all@my-company.com'
        from: 'user.name@gmail.com'
        smarthost: 'smtp.gmail.com:587'
        auth_username: 'user.name@gmail.com'
        auth_password: 'APP_TOKEN'
        auth_identity: 'user.name@gmail.com'
        html: '{{ template "templates.tmpl" . }}'
```

Make sure to run the `juju config` command again with the updated `alert-manager.yaml`.

Now, when an alert will trigger you will receive a customized notification!
