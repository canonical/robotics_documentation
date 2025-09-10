# Send rosbags to {{ COS_ROB }}

In this how-to,
we detail how to set up and configure a robot to send
rosbags to the {{ COS_ROB }} server.

We thus assume that a {{ COS_ROB }} server is up and running.
You may refer to the tutorial
['Deploy {{ COS_ROB }} server in the cloud'](../../tutorials/observability/deploy-cos-for-robotics-server-in-the-cloud.md).
to do so.

In addition, a cloud storage must be deployed and integrated with {{ COS_ROB }}.
Pick the tab below corresponding to the storage solution you deployed.

`````{tab-set}

````{tab-item} Microceph

The following assumes that a Microceph storage solution
is deployed and integrated with {{ COS_ROB }}.
You may refer to the how-to
['Deploy Microceph for {{ COS_ROB }}'](deploy-ceph.md).
to do so.

## Creating the RadosGW user

In order to upload rosbags to the server,
we must first create an S3 credential.

To do so, issue the command:

```console
$ juju exec --unit microceph/leader -- radosgw-admin user create --uid=my-user --display-name=my-user
{
    "user_id": "my-user",
    "display_name": "my-user",
    "email": "",
    "suspended": 0,
    "max_buckets": 1000,
    "subusers": [],
    "keys": [
        {
            "user": "my-user",
            "access_key": "<MY_USER_ACCESS_KEY>",
            "secret_key": "<MY_USER_SECRET_KEY>",
            "active": true,
            "create_date": "2024-12-10T17:03:53.196001Z"
        }
    ],
...
```

Take not of the `access_key` as well as the `secret_key`.
They are the credentials we are going to configure on the device.

Before moving on to the device,
the last step is to create an S3 bucket for our user to upload the rosbags.

To do so we are going to use the S3 client `rclone`,
but any other client of your choice should do.

Install `rclone` with:

```console
sudo snap install rclone
```

After installation,
create the bucket with:

```console
$ export RCLONE_CONFIG_COSROB_ACCESS_KEY_ID=<MY_USER_ACCESS_KEY>
$ export RCLONE_CONFIG_COSROB_SECRET_ACCESS_KEY=<MY_USER_SECRET_KEY>
$ export RCLONE_CONFIG_COSROB_TYPE=s3
$ export RCLONE_CONFIG_COSROB_PROVIDER=Ceph
$ export RCLONE_CONFIG_COSROB_ENDPOINT="$(sudo snap get rob-cos-demo-configuration rob-cos-base-url)"
$
$ rclone mkdir "cosrob:$(sudo snap get rob-cos-demo-configuration device-uid)$"
```

This command will create a bucket named after the robot uid that is acessible to it.

## Setting up the agent

With the server side ready to receive rosbags,
we shall now set up the device side.

### Configuring the credentials

The first step is to configure the RadosGW credentials we've just created.
To do so, use the commands:

```console
sudo snap set rob-cos-demo-configuration access-key-id <MY_USER_ACCESS_KEY>
sudo snap set rob-cos-demo-configuration secret-access-key <MY_USER_SECRET_KEY>
```

### Installing the agent

Finally, we can install the snap on the robot:

```console
sudo snap install ros2-exporter-agent --channel=latest/beta
```

Once installed, we shall verify that its interface is connected:

```console
$ snap connections ros2-exporter-agent
Interface     Plug                                     Slot                                           Notes
content       ros2-exporter-agent:configuration-read   rob-cos-demo-configuration:configuration-read  -
```

In case it is not, or if you are using your own configuration snap,
use the command:

```console
sudo snap connect ros2-exporter-agent:configuration-read <my-configuration>:configuration-read
```

Once the interface is connected,
the exporter agent will automatically start recording rosbags and
send them to the file server on {{ COS_ROB }}.

You can start/stop either from their respective command:

```console
sudo snap stop ros2-exporter-agent.recorder
```

and:

```console
sudo snap stop ros2-exporter-agent.synchronization
```

````

````{tab-item} Caddy

The following assumes that a file server
is deployed and integrated with {{ COS_ROB }}.
You may refer to the how-to
['Deploy a file server for {{ COS_ROB }}'](deploy-caddy.md).
to do so.

## Setting up the agent

With the server side ready to receive rosbags,
we shall now set up the device side.

The setup is as simple as installing the snap on the robot:

```console
sudo snap install ros2-exporter-agent --channel=latest/beta
```

Once installed, we shall verify that its interfaces are connected:

```console
$ snap connections ros2-exporter-agent
Interface     Plug                                     Slot                                           Notes
content       ros2-exporter-agent:configuration-read   rob-cos-demo-configuration:configuration-read  -
content       ros2-exporter-agent:rob-cos-common-read  rob-cos-data-sharing:rob-cos-common-read       -
```

and that its services have automatically started:

```console
$ snap services ros2-exporter-agent
Service                                 Startup   Current   Notes
ros2-exporter-agent.auto-clean          enabled   active    timer-activated
ros2-exporter-agent.daily-rotation      enabled   active    timer-activated
ros2-exporter-agent.read-configuration  enabled   active    -
ros2-exporter-agent.recorder            enabled   active    -
ros2-exporter-agent.synchronization     enabled   active    timer-activated
```

In case the interfaces are not connected,
or if you are using your own configuration snap,
you can connect them with:

```console
sudo snap connect ros2-exporter-agent:rob-cos-common-read <my-data-sharing>:rob-cos-common-read
```

And:

```console
sudo snap connect ros2-exporter-agent:configuration-read <my-demo-configuration>:configuration-read
```

Once both interface are connected,
the exporter agent will automatically start recording rosbags and
send them to the file server on {{ COS_ROB }}.

They can be start/stop with their respective command:

```console
sudo snap stop ros2-exporter-agent.recorder
```

and:

```console
sudo snap stop ros2-exporter-agent.synchronization
```

````

`````
