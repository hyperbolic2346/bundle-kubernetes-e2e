# Kubernetes e2e

This is Juju bundle used for running e2e tests against a Juju deployed
Kubernetes cluster. In addition to the Kubernetes charms this bundle includes
a specific kubernetes-e2e charm that is only used for testing. 

This bundle allocates additional resources to testing and should not be used 
for deploying normal Kubernetes clusters. Use the 
[Canonical Distribution of Kubernetes](https://jujucharms.com/canonical-kubernetes/)
or the
[Kubernetes core](https://jujucharms.com/kubernetes-core/) bundles if you 
only want to deploy a Kubernetes cluster. The source for these bundles can be 
found in [github](https://github.com/juju-solutions/bundle-canonical-kubernetes)

# Usage

Deploy the bundle and run the conformance test on the kubernetes-e2e charm. 
That exercises the upstream conformance tests of a running cluster. 

## Deploy the kubernetes-e2e bundle

```
juju deploy kubernetes-e2e
```

The charms in this bundle provide status messages to indicate their current 
status. Monitor the progress of the deployment with:

```
watch -c juju status --color
```

## Run the e2e test

Once all the charms are in an "active" state, and the Kubernetes cluster has 
"kube-dns" running you can execute the e2e tests with a Juju action.

```
juju run-action kubernetes-e2e/0 test
```

Capture the action identifier, and run the command to wait for the action
output.

```
juju show-action-output --wait 0 <action id>
```

This will wait for the action to complete. The results are saved to 2 files in
the `/home/ubuntu` directory which you can download using `juju scp` commands.

```
juju scp kubernetes-e2e/0 <action-id>.log.tar.gz e2e.log.tar.gz
juju scp kubernetes-e2e/0 <action-id>-junit.tar.gz e2e-junit.tar.gz
```

## Kubernetes details

- [Kubernetes User Guide](http://kubernetes.io/docs/user-guide/)
- [Canonical Distribution of Kubernetes](https://jujucharms.com/canonical-kubernetes/)
- [Kubernetes core](https://jujucharms.com/kubernetes-core/)
- [Bundle Source](https://github.com/juju-solutions/bundle-kubernetes-e2e)
- [Bug tracker](https://github.com/juju-solutions/bundle-kubernetes-e2e/issues)
