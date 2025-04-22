# Observe {{ COS_ROB }}

{{ COS_ROB }} provides valuable insights about one's fleet of devices.
Maybe more importantly it also alerts the fleet operators should anything dysfunction.
As such, {{ COS_ROB }} can be seen as a critical piece of infrastructure.
And while it is resilient, it can be subject to failure and disrupts the monitoring of the fleet.

For this reason, {{ COS_ROB }} is itself observable as well, using most of the tools
already used for observing the robots fleets.
While {{ COS_ROB }} could perfectly observe itself, this wouldn't make much sense in case
of a large outage.
Instead, we recommend deploying a separate
[{{ COS }}](https://charmhub.io/topics/canonical-observability-stack/editions/lite)
stack in production which responsibility is to monitor {{ COS_ROB }}.

We assume hereafter that both {{ COS_ROB }} and {{ COS }} are deployed and set up.
{{ COS }} deployment is very similar to that of {{ COS_ROB }} and a tutorial can be found on
[{{ COS }} documentation website](https://charmhub.io/topics/canonical-observability-stack/tutorials).
We also assume that {{ COS }} deployment includes support for
[distributed tracing support with Tempo](https://charmhub.io/topics/canonical-observability-stack/how-to/add-distributed-tracing)
as well as the [Blackbox Exporter](https://charmhub.io/blackbox-exporter-k8s/docs/using)
for probing of endpoints.

```{note}
There are multiple strategies for the topology of this double deployment.
For the sake of this how-to, we assume that {{ COS }} and {{ COS_ROB }} live
in their respective models and that both are controlled by the same Juju controller.
Make sure to read Juju's documentation about
[coss-model relations](https://documentation.ubuntu.com/juju/3.6/reference/relation/#cross-model)
as we are using this feature and since it may impact the very boostrapping of the controllers
depending on the topology.
```

## Prelude

For good measure, let us start by making sure that everything is fine.
We first check the {{ COS_ROB }} stack:

```bash
$ juju status --model robcos-model
Model         Controller         Cloud/Region        Version  SLA          Timestamp
robcos-model  robcos-controller  microk8s/localhost  3.6.4    unsupported  14:39:49Z

App                      Version  Status  Scale  Charm                        Channel        Rev  Address         Exposed  Message
alertmanager             0.27.0   active      1  alertmanager-k8s             latest/stable  156  10.152.183.200  no
catalogue                         active      1  catalogue-k8s                latest/stable   81  10.152.183.111  no
cos-registration-server           active      1  cos-registration-server-k8s  latest/edge      8  10.152.183.235  no
foxglove-studio                   active      1  foxglove-studio-k8s          latest/edge      1  10.152.183.96   no
grafana                  9.5.3    active      1  grafana-k8s                  latest/stable  139  10.152.183.182  no
loki                     2.9.6    active      1  loki-k8s                     latest/stable  187  10.152.183.140  no
prometheus               2.52.0   active      1  prometheus-k8s               latest/stable  232  10.152.183.148  no
ros2bag-fileserver                active      1  ros2bag-fileserver-k8s       latest/edge      3  10.152.183.83   no
traefik                  2.11.0   active      1  traefik-k8s                  latest/stable  234  10.152.183.242  no       Serving at 100.83.155.248

Unit                        Workload  Agent  Address       Ports  Message
alertmanager/0*             active    idle   10.1.105.131
catalogue/0*                active    idle   10.1.105.135
cos-registration-server/0*  active    idle   10.1.105.167
foxglove-studio/0*          active    idle   10.1.105.173
grafana/0*                  active    idle   10.1.105.149
loki/0*                     active    idle   10.1.105.136
prometheus/0*               active    idle   10.1.105.155
ros2bag-fileserver/0*       active    idle   10.1.105.139
traefik/0*                  active    idle   10.1.105.133         Serving at 100.83.155.248

Offer    Application  Charm        Rev  Connected  Endpoint       Interface      Role
traefik  traefik      traefik-k8s  234  1/1        traefik-route  traefik_route  provider
```

The {{ COS_ROB }} stack is ready.
What about the {{ COS }} stack:

```bash
$ juju status --model cos-model
Model      Controller         Cloud/Region       Version  SLA          Timestamp
cos-model  robcos-controller  cos-k8s/localhost  3.6.4    unsupported  09:55:08Z

App           Version                Status  Scale  Charm                  Channel        Rev  Address         Exposed  Message
alertmanager  0.27.0                 active      1  alertmanager-k8s       latest/stable  156  10.152.183.87   no
blackbox      0.24.0                 active      1  blackbox-exporter-k8s  latest/stable   25  10.152.183.83   no
catalogue                            active      1  catalogue-k8s          latest/stable   81  10.152.183.144  no
grafana       9.5.3                  active      1  grafana-k8s            latest/stable  139  10.152.183.247  no
loki          2.9.6                  active      1  loki-k8s               latest/stable  187  10.152.183.62   no
minio         res:oci-image@220b31a  active      1  minio                  ckf-1.9/edge   419  10.152.183.64   no
prometheus    2.52.0                 active      1  prometheus-k8s         latest/stable  232  10.152.183.50   no
s3                                   active      1  s3-integrator          latest/edge    145  10.152.183.29   no
tempo                                active      1  tempo-coordinator-k8s  latest/edge     73  10.152.183.237  no       metrics-generator disabled. Add a relation over send-remote-write
tempo-worker  2.7.1                  active      1  tempo-worker-k8s       latest/edge     53  10.152.183.161  no       metrics-generator disabled. No prometheus remote-write relation configured on the coordinator
traefik       2.11.0                 active      1  traefik-k8s            latest/stable  234  10.152.183.73   no       Serving at 100.83.164.181

Unit             Workload  Agent  Address       Ports          Message
alertmanager/0*  active    idle   10.1.128.139
blackbox/0*      active    idle   10.1.128.133
catalogue/0*     active    idle   10.1.128.141
grafana/0*       active    idle   10.1.128.155
loki/0*          active    idle   10.1.128.137
minio/0*         active    idle   10.1.128.132  9000-9001/TCP
prometheus/0*    active    idle   10.1.128.138
s3/0*            active    idle   10.1.128.145
tempo-worker/0*  active    idle   10.1.128.134                 metrics-generator disabled. No prometheus remote-write relation configured on the coordinator
tempo/0*         active    idle   10.1.128.140                 metrics-generator disabled. Add a relation over send-remote-write
traefik/0*       active    idle   10.1.128.191                 Serving at 100.83.164.181
```

Alright, we're all setup and we can get to relating the stacks.

## Deploy the Grafana agent

With both {{ COS_ROB }} and {{ COS }} deployed in their respective models,
we must now 'relate' them through Juju
[relations](https://documentation.ubuntu.com/juju/latest/reference/relation/).

Since the stacks live in separate models, we must establish a so called
[coss-model relations](https://documentation.ubuntu.com/juju/3.6/reference/relation/#cross-model).
These are two folds, firstly, we need to expose some applications from one model to the other,
secondly, we can relate applications as we normally would using Juju.

To ease the setup, we deploy the [Grafana agent](https://charmhub.io/grafana-agent-k8s)
in the {{ COS_ROB }} model.
This allows for connecting our applications in {{ COS_ROB }} to
the Grafana instance in {{ COS }} in a simpler manner as we will see later on.
Not only is this simplifying the deployment but it also offer more flexibility
when it comes to modifying the overall deployment topology.
This setup is depicted in [the following diagram](#cos-cosrob-diagram):

```{mermaid}
:name: cos-cosrob-diagram
:caption: A bi-model deployment of {{ COS }} observing {{ COS_ROB }}.
:config: {"fontFamily": "ubuntu", "theme": "dark"}
:align: center
graph LR;
    subgraph Cloud 1 [COS for Robotics]
        A(Grafana)
        B(Prometheus)
        C(Foxglove Studio)
        K(COS registration server)
        L(rosbag server)
        D(...)
        E(Grafana Agent)
        A --> E
        B --> E
        D --> E
        K --> E
        L --> E
        C --> E
    end

    subgraph Cloud 2 [COS Lite]
        F(Grafana)
        H(Prometheus)
        G(Loki)
        I(Tempo)
        J(...)
    end

    E --> F
    E --> H
    E --> G
    E --> I
```

To deploy the agent, issue the command:

```bash
juju deploy grafana-agent-k8s
```

## Relating to the agent

Now that the agent is deployed, we can connect all the observability endpoints to it.
And there are quite a few of them:

```bash
# alermanager
juju relate alermanager:grafana-dashboard grafana-agent:grafana-dashboards-consumer
juju relate alermanager:self-metrics-endpoint grafana-agent:metrics-endpoint
juju relate alermanager:tracing grafana-agent:tracing-provider
# catalogue
juju relate catalogue:tracing grafana-agent:tracing-provider
# cos-registration-server
juju relate cos-registration-server:logging grafana-agent:logging-provider
juju relate cos-registration-server:tracing grafana-agent:tracing-provider
juju relate cos-registration-server:grafana-dashboard grafana-agent:grafana-dashboards-consumer
# foxglove-studio
juju relate foxglove-studio:logging grafana-agent:logging-provider
juju relate foxglove-studio:tracing grafana-agent:tracing-provider
juju relate foxglove-studio:grafana-dashboard grafana-agent:grafana-dashboards-consumer
# grafana
juju relate grafana:charm-tracing grafana-agent:tracing-provider
juju relate grafana:workload-tracing grafana-agent:tracing-provider
juju relate grafana:metrics-endpoint grafana-agent:metrics-endpoint
# loki
juju relate loki:metrics-endpoint grafana-agent:metrics-endpoint
juju relate loki:grafana-dashboard grafana-agent:grafana-dashboards-consumer
juju relate loki:charm-tracing grafana-agent:tracing-provider
juju relate loki:workload-tracing grafana-agent:tracing-provider
# prometheus
juju relate prometheus:self-metrics-endpoint grafana-agent:metrics-endpoint
juju relate prometheus:grafana-dashboard grafana-agent:grafana-dashboards-consumer
juju relate prometheus:charm-tracing grafana-agent:tracing-provider
juju relate prometheus:workload-tracing grafana-agent:tracing-provider
# traefik
juju relate traefik:metrics-endpoint grafana-agent:metrics-endpoint
juju relate traefik:grafana-dashboard grafana-agent:grafana-dashboards-consumer
juju relate traefik:charm-tracing grafana-agent:tracing-provider
juju relate traefik:workload-tracing grafana-agent:tracing-provider
```

With all the relations established to the agent,
we can now move on to exposing the {{ COS }} endpoints to the {{ COS_ROB }} model
in order to connect them.
<!-- we can now 'offer' the {{ COS }} endpoints to the {{ COS_ROB }} model. -->

## Making an offer

As we mentioned earlier, the first step is to issue 'offers'.
To do so, issue the commands:

```bash
juju offer cos-model.grafana:grafana-dashboard cos-grafana
juju offer cos-model.loki:logging cos-loki
juju offer cos-model.prometheus:receive-remote-write cos-prometheus
juju offer cos-model.tempo:tracing cos-tempo
juju offer cos-model.blackbox:probes cos-blackbox
```

These create the offers from the `cos-model` model,
where the {{ COS }} lives,
to be consumed in another model.

They are then 'consumed' on the {{ COS_ROB }} model with:

```bash
juju consume cos-model.cos-grafana
juju consume cos-model.cos-loki
juju consume cos-model.cos-prometheus
juju consume cos-model.cos-tempo
juju consume cos-model.cos-blackbox
```

Once consumed, they appears in the `juju status` output as `SAAS` entries:

```bash
$ juju status
Model         Controller         Cloud/Region        Version  SLA          Timestamp
robcos-model  robcos-controller  microk8s/localhost  3.6.4    unsupported  12:44:19Z

SAAS            Status  Store              URL
cos-blackbox    active  robcos-controller  admin/cos-model.cos-blackbox
cos-grafana     active  robcos-controller  admin/cos-model.cos-grafana
cos-loki        active  robcos-controller  admin/cos-model.cos-loki
cos-prometheus  active  robcos-controller  admin/cos-model.cos-prometheus
cos-tempo       active  robcos-controller  admin/cos-model.cos-tempo
...
```

## Relating to {{ COS }}

With the {{ COS }} endpoints now available in the {{ COS_ROB }} model,
all we have to do is to relate them to the Grafana agent.

We proceed with:

```bash
juju relate grafana-agent:grafana-dashboards-provider cos-grafana:grafana-dashboard
juju relate grafana-agent:logging-consumer cos-loki:logging
juju relate grafana-agent:send-remote-write cos-prometheus:receive-remote-write
juju relate grafana-agent:tracing cos-tempo:tracing
```

We also relate our applications to Blackbox:

```bash
juju relate cos-registration-server:probes cos-blackbox:probes
juju relate foxglove-studio:probes cos-blackbox:probes
```

Voila.

The {{ COS_ROB }} stack is now observable by {{ COS }}.
