# Kubernetes e2e Bundle

## Overview

This is Juju bundle designed to run e2e tests against the cluster.

# Usage

Deploy the bundle and run the conformance test on the `kubernetes-e2e` charm. 

## Deploy the bundle

```
juju deploy kubernetes-e2e
```

This bundle exposes the kubernetes-worker charm by default. This means that
it is accessible through its public address.

If you would like to remove external access, unexpose the application:

```
juju unexpose kubernetes-worker
```

To get the status of the deployment, run `juju status`. For a constant update,
this can be used with `watch`.

```
watch -c juju status --color
```

### Alternate deployment methods


#### Usage with your own binaries

In order to support restricted-network deployments, the charms in this bundle
support
[juju resources](https://jujucharms.com/docs/2.0/developer-resources#managing-resources).

This allows you to `juju attach` the resources built for the architecture of
your cloud.

```
juju attach kubernetes-master kubernetes=~/path/to/kubernetes-master.tar.gz
```

## Interacting with the Kubernetes cluster

After the cluster is deployed you may assume control over the Kubernetes cluster
from any kubernetes-master, or kubernetes-worker node.

To download the credentials and client application to your local workstation:

Create the kubectl config directory.

```
mkdir -p ~/.kube
```

Copy the kubeconfig to the default location.

```
juju scp kubernetes-master/0:config ~/.kube/config
```

Fetch a binary for the architecture you have deployed. If your client is a
different architecture you will need to get the appropriate `kubectl` binary
through other means.

```
juju scp kubernetes-master/0:kubectl ./kubectl
```

Query the cluster.

```
./kubectl cluster-info
```

### Accessing the Kubernetes Dashboard

With `kubectl` placed in your `$PATH` and having the config placed, you may
establish a secure tunnel to your cluster with the following command:

```
./kubectl proxy
```

By default, this establishes a proxy running on your local machine and the
kubernetes-master unit. To reach the Kubernetes dashboard, visit
`http://localhost:8001/ui`


### Control the cluster

kubectl is the command line utility to interact with a Kubernetes cluster.


#### Minimal getting started

To check the state of the cluster:

```
./kubectl cluster-info
```

List all nodes in the cluster:

```
./kubectl get nodes
```

Now you can run pods inside the Kubernetes cluster:

```
./kubectl create -f example.yaml
```

List all pods in the cluster:


```
./kubectl get pods
```

List all services in the cluster:

```
./kubectl get services
```

For expanded information on kubectl beyond what this README provides, please
see the
[kubectl overview](http://kubernetes.io/docs/user-guide/kubectl-overview/)
which contains practical examples and an API reference.

Additionally if you need to manage multiple clusters, there is more information
about configuring kubectl with the
[kubectl config guide](http://kubernetes.io/docs/user-guide/kubectl/kubectl_config/)


### Scaling kubernetes-worker

The kubernetes-worker nodes are the load-bearing units of a Kubernetes cluster.

By default pods are automatically spread throughout the kubernetes-worker units
that you have deployed.

To add more kubernetes-worker units to the cluster:

```
juju add-unit kubernetes-worker
```

or specify machine constraints to create larger nodes:

```
juju add-unit kubernetes-worker --constraints "cpu-cores=8 mem=32G"
```

Refer to the
[machine constraints documentation](https://jujucharms.com/docs/stable/charms-constraints)
for other machine constraints that might be useful for the kubernetes-worker units.


### Scaling Etcd

Etcd is used as a key-value store for the Kubernetes cluster. The bundle
defaults to one instance in this cluster.

For reliability and more scalability, we recommend between 3 and 9 etcd nodes.
If you want to add more nodes:

```
juju add-unit etcd
```

The CoreOS etcd documentation has a chart for the
[optimal cluster size](https://coreos.com/etcd/docs/latest/admin_guide.html#optimal-cluster-size)
to determine fault tolerance.

## Known Limitations and Issues

 The following are known issues and limitations with the bundle and charm code:

 - kubernetes-master, kubernetes-worker, kubeapi-load-balancer and etcd are not
 supported on LXD at this time.
 - Destroying the the easyrsa charm will result in loss of public key
 infrastructure (PKI).

## Kubernetes details

- [Kubernetes User Guide](http://kubernetes.io/docs/user-guide/)
- [The Canonical Distribution of Kubernetes](https://jujucharms.com/canonical-kubernetes/bundle/)
- [Bundle Source](https://github.com/juju-solutions/bundle-kubernetes-e2e)
- [Bug tracker](https://github.com/juju-solutions/bundle-canonical-kubernetes/issues)
