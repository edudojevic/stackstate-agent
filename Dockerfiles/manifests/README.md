# Kubernetes Setup

### Cluster creation

If you want to create a cluster using AWS EKS please follow the `manifests/aws/tf/Readme.md` on how to spin that up with Terraform.

### Configure RBAC 

If your Kubernetes has role-based access control (RBAC) enabled, configure RBAC permissions for your StackState Agent service account.  

Create the appropriate ClusterRole, ServiceAccount, and ClusterRoleBinding:

```
kubectl create -f stackstate-serviceaccount.yaml
```

### Enable Kubernetes state

To gather your kube-state metrics:
* Download the [Kube-State manifests folder](https://github.com/kubernetes/kube-state-metrics/tree/master/kubernetes)
* Apply them to your Kubernetes cluster:

```
kubectl apply -f <NAME_OF_THE_KUBE_STATE_MANIFESTS_FOLDER>
```

## Deploy the DaemonSet

Before deploying the agent there are few configuration settings to take care of, open the `stackstate-agent.yaml` and:

* replace `<STACKSTATE_BACKEND_IP>` with your Stackstate backend IP
* if you want to collect only containers information (and no processes) remove the env variable `DD_PROCESS_AGENT_ENABLED`
* if you want to disable connections gathering remove the env variable `DD_CONNECTIONS_CHECK` (or set it to `false`)

Now you can deploy the DaemonSet with the following command:

```
kubectl create -f stackstate-agent.yaml
```
