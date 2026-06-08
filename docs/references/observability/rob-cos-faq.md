# FAQ & Troubleshooting

```{warning}
**Beta Notice**: {{COS_ROB}} is currently in `beta`.
Content and features may change,
and some functionality may be incomplete or experimental.
Feedback is welcome as we continue to improve.
```

## Can I use {{ COS_ROB }} without Juju and charms?

While this is not a supported use case,
you can redeploy the server side without Juju and charms
by deploying and integrating all the server side applications manually.

## Can I use {{ COS_ROB }} without snaps?

While this is not a supported use case,
you can redeploy the device side without snaps by repackaging and
managing yourself the installation,
configuration and orchestration of the different agents on the device.

## Is Canonical maintaining Foxglove Studio 1?

No, we are not.
The development of {{ COS_ROB }} started before Foxglove Studio 1 got discontinued.
We are only providing a packaged version of
the latest open source Foxglove studio 1 release,
along with a patch to support passing layout by URL.
We are not guaranteeing the support of our packaged version of Foxglove studio.

## Is {{ COS_ROB }} compatible with Foxglove Studio 2?

No, Foxglove Studio 2 is not currently supported in {{ COS_ROB }}.
Since it’s closed source it’s up to the Foxglove company to integrate it if they want.

## Is Canonical providing a managed instance of {{ COS_ROB }}?

Yes, Canonical provides a service of managed instances of {{ COS_ROB }} for companies.

## Is {{ COS_ROB }} going to be deployable completely open source?

Yes, all the charms and snaps are open source.

## Can I integrate a custom/private application in {{ COS_ROB }}?

Yes, in the case of a server side application,
the application [must be charmed](https://juju.is/docs/sdk/from-zero-to-hero-write-your-first-kubernetes-charm).
Depending on the desired visibility of your charm,
you might upload it to charmhub.io or by
[deploying your own charmstore](https://github.com/juju/charmstore).
Additionally, you could keep your charm local.

In the case of a device application,
the application [must be snapped](https://documentation.ubuntu.com/snapcraft/stable/tutorials/craft-a-snap/).
It can then be deployed publicly to the [Snap Store](https://snapcraft.io/store) or
privately on the [dedicated Snap Store](https://documentation.ubuntu.com/dedicated-snap-store/).

## How can I suggest features to the {{ COS_ROB }}?

You can reach [ubuntu-robotics-community-group@canonical.com](mailto:ubuntu-robotics-community-group@canonical.com).
Once publicly released,
suggestions can be made on <https://discourse.ubuntu.com/> as well as
with tickets in the different repositories.

## Who is maintaining the charms and snaps?

The robotics team at Canonical.
All contributions and suggestions are welcome in all the repositories.

## For how long, {{ COS_ROB }} is going to be maintained?

We currently commit to our rolling releases.

## When is {{ COS_ROB }} going to be publicly released?

The first public release of {{ COS_ROB }} will happen in the 6 months
after the closing of the private beta testing.

## Are old revisions of charms and snaps going to receive security updates?

No, all the charms and snaps are only going to be updated on their latest version.
Thanks to Juju and snapd, all the updates will be seamless and automatic.

## Can I use another VPN than NetBird?

Yes you can, multiple VPNs are available on the Snap Store.
The role of the VPN is to secure the connections and
provide direct connectivity between the devices and the server.

## Does my device need to use Ubuntu?

No, although {{ COS_ROB }} is recommended for [Ubuntu Core](https://ubuntu.com/core).
{{ COS_ROB }} is supported on Ubuntu Server,
Desktop and all the Linux distributions
[supporting the snapd daemon](https://snapcraft.io/docs/installing-snapd).

## Does my server need to use Ubuntu?

No, although {{ COS_ROB }} is recommended for Ubuntu server.
{{ COS_ROB }} is supported on all the Linux distributions
[supporting the snapd daemon](https://snapcraft.io/docs/installing-snapd).
