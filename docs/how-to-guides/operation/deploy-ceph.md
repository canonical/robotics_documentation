# Deploy Microceph for {{ COS_ROB }}

```{warning}
**Beta Notice**: {{COS_ROB}} is currently in `beta`.
Content and features may change,
and some functionality may be incomplete or experimental.
Feedback is welcome as we continue to improve.
```

In this How-To-Guide,
we will walk through the deployment of a Ceph-based storage with
an S3 endpoint in the **Canonical Observability Stack (COS) for robotics**.
We therefore assume that a {{ COS_ROB }} stack is up and running.
You may refer to the tutorial
['Deploy {{ COS_ROB }} server in the cloud'](../../tutorials/observability/deploy-cos-for-robotics-server-in-the-cloud.md).
to do so.

By the end of this guide,
We will have a cloud storage available in {{ COS_ROB }} so that devices
can push rosbags for later use.

## Setting up the cloud

For this deployment,
we rely on [**Microceph**](https://canonical-microceph.readthedocs-hosted.com/stable/)
deployed on an
[**LXD**](https://documentation.ubuntu.com/server/how-to/containers/lxd-containers/)
cloud.

Let us start by setting up the **LXD** cloud.

### Install **LXD**

Install the **LXD** snap with:

```console
sudo snap install lxd
```

and initialize it with:

```console
lxd init --minimal
```

Once **LXD** is initialized, we expose it to the network:

```console
lxc config set core.https_address :8443
```

Exposing it to the network allows us to use a single **Juju** controller,
the `cos-robotics-controller` deployed in the tutorial,
to operate both clouds.
Mind that other deployment strategies are possible.

### Bootstrapping **LXD**

While **LXD** automatically appears in the list of
local clouds available to **Juju** (`juju clouds`),
we are not going to rely on this integration to bootstrap it.
Instead, we are going to add it to Juju as if it was a remote cloud.
To do so, we use the following interactive command:

```console
$ juju add-cloud --client --controller cos-robotics-controller
Cloud Types
  lxd
  maas
  manual
  openstack
  vsphere

Select cloud type: lxd

Enter a name for your lxd cloud: lxd-local

Enter the API endpoint url for the remote LXD server: https://HOST_IP_ADDRESS

Auth Types
  certificate

Enter region [default]:

Enter the API endpoint url for the region [use cloud api url]:

Enter another region? (y/N):

Cloud "lxd-local" successfully added to your local client.
You will need to add a credential for this cloud (`juju add-credential lxd-local`)
before you can use it to bootstrap a controller (`juju bootstrap lxd-local`) or
to create a model (`juju add-model <your model name> lxd-local`).

Cloud "" added to controller "cos-robotics-controller".
WARNING loading credentials: credentials for cloud lxd-local not found
To upload a credential to the controller for cloud "lxd-local", use
* 'add-model' with --credential option or
* 'add-credential -c lxd-local'.
```

This command enrolls the **LXD** cloud both to the **Juju** client as well as
the existing controller through it local IP address.
Note that in this configuration, the **LXD** cloud could be running on a different
machine on a local network.

We also note the final warning about credentials.
Fortunately, to address it we can benefit from the **LXD** integration to **Juju**
this time around and have it (somewhat) automatically load the certificate.
To do so, enter the following command and follow along the interactive process:

```console
$ juju autoload-credentials --client --controller cos-robotics-controller
Looking for cloud and credential information on local client...

Looking for cloud information on controller "cos-robotics-controller"...

1. LXD credential "localhost" (new)
Select a credential to save by number, or type Q to quit: 1

Select the cloud it belongs to, or type Q to quit [localhost]: lxd-local

Saved LXD credential "localhost" to cloud lxd-local locally

1. LXD credential "localhost" (existing, will overwrite)
Select a credential to save by number, or type Q to quit: Q

Controller credential "localhost" for user "admin" for cloud "lxd-local" on controller "cos-robotics-controller" loaded.
For more information, see ‘juju show-credential lxd-local localhost’.
```

Juju has now loaded the ‘localhost’ cloud credential through its
integration with the LXD snap and associated it
with the manually registered ‘lxd-local’ cloud.

Let’s verify that the cloud was indeed added to the controller,

```console
$ juju clouds --client --controller cos-robotics-controller

Clouds available on the controller:
Cloud      Regions  Default    Type
lxd-local  1        localhost  lxd
microk8s   1        localhost  k8s

Clouds available on the client:
Cloud      Regions  Default    Type  Credentials  Source    Description
localhost  1        localhost  lxd   0            built-in  LXD Container Hypervisor
lxd-local  1        default    lxd   1            local     LXD Container Hypervisor
microk8s   1        localhost  k8s   1            built-in  A Kubernetes Cluster
```

Both our clouds are set up,
we can now continue with the deployment.

## Deploy **Microceph**

The deployment relies on a Terraform plan that can be found
in the repository used in the tutorial.
You can retrieve it again with:

```console
git clone https://github.com/ubuntu-robotics/rob-cos-overlay.git
```

We then move to the sub-directory containing the **Microceph** plan:

```console
cd path/to/rob-cos-overlay/terraform/microceph

and initialize the project:

```console
terraform init
```

In order to deploy, we must create a new Juju project on the **LXD** cloud:

```console
juju add-model cos-robotics-microceph-model lxd-local
```

Let's check on those models:

```console
$ juju models
Controller: cos-robotics-controller

Model                           Cloud/Region        Type        Status     Machines  Units  Access  Last connection
controller                      microk8s/localhost  kubernetes  available         0      1  admin   just now
cos-robotics-microceph-model*   lxd-local/default   lxd         available         0      0  admin   2025-08-28
cos-robotics-model              microk8s/localhost  kubernetes  available         5      5  admin   2025-08-22
```

Finally, we can deploy the stack with:

```bash
terraform apply -var="model=cos-robotics-microceph-model"
```

Now you can sit back and watch the deployment take place:

```bash
juju status --watch 5s --color --relations --model cos-robotics-microceph-model
```

Once all the machines are active,
we have to attach some storage to the **Microceph** cluster:

```console
juju run microceph/0 add-osd loop-spec="10G,1"
juju run microceph/1 add-osd loop-spec="10G,1"
juju run microceph/2 add-osd loop-spec="10G,1"
```

This will create a storage pool of ~30G to store our rosbags.

## Integrate **Microceph**

With the storage deployed,
we shall now integrate it to {{ COS_ROB }}.
To do so, we start by creating a Juju offer:

```console
$ juju offer microceph:ingress --model cos-robotics-microceph-model
Application "microceph" endpoints [ingress] available at "admin/cos-robotics-microceph-model.microceph"
```

We then consume this offer in the {{ COS_ROB }} model:

```console
juju consume admin/cos-robotics-microceph-model.microceph --model cos-robotics-model
```

Once the offer consumed,
the `microceph` application should appear as a ‘SAAS’ ,

```console
$ juju status --model cos-robotics-model
Model               Controller               Cloud/Region       Version  SLA          Timestamp
cos-robotics-model  cos-robotics-controller  lxd-local/default  3.6.0    unsupported  15:28:30+01:00

SAAS      Status  Store                   URL
microceph active  cos-robotics-controller admin/cos-robotics-microceph-model.microceph
...
```

We can then integrate **Microceph** to the {{ COS_ROB }} ingress:

```console
juju integrate microceph traefik --model cos-robotics-model
```

From there we can query **Microceph** about its **RadosGW** IP,

```console
$ juju run microceph/leader get-rgw-endpoints --model cos-robotics-microceph-model
Running operation 2 with 1 task
  - task 3 on unit-microceph-1

Waiting for task 3...
s3: http://100.83.155.248
swift: http://100.83.155.248/swift/v1
```

Let’s check if this IP is actually up,

```console
$ curl http://100.83.155.248
<?xml version="1.0" encoding="UTF-8"?><ListAllMyBucketsResult xmlns="http://s3.amazonaws.com/doc/2006-03-01/"><Owner><ID>anonymous</ID></Owner><Buckets></Buckets></ListAllMyBucketsResult>
```

The cloud storage is up and running.

## Create a RadosGW user

The last step is to create a shared-user to upload the rosbags to the S3 buckets.
To do so use the command:

```console
$ juju exec --unit microceph/leader -- radosgw-admin user create --uid=fleet-a --display-name=fleet-a
{
    "user_id": "fleet-a",
    "display_name": "fleet-a",
    "email": "",
    "suspended": 0,
    "max_buckets": 1000,
    "subusers": [],
    "keys": [
        {
            "user": "fleet-a",
            "access_key": "MY_ACCESS_KEY",
            "secret_key": "MY_SECRET_KEY",
            "active": true,
            "create_date": "2024-12-10T17:03:53.196001Z"
        }
    ],
...
```

where `fleet-a` is the name of the shared user across a fleet.

Make sure to note the `access_key` and `access_key` as we will use them later.
You can always retrieve them with the command
`juju exec --unit microceph/leader -- radosgw-admin user info --uid=fleet-a`.

Our storage is ready to receive rosbags from the devices.

---

## Next steps: device setup

Now that the storage is set up,
let’s see how to configure a device to upload rosbags.
