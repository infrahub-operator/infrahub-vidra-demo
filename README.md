# Infrahub + Vidra Demo

This repository provides a GitOps demo environment showcasing how [Infrahub](https://github.com/opsmill/infrahub) and [Vidra](https://github.com/infrahub-operator/vidra) work together in harmony to declaratively manage Kubernetes resources. It showcases deploying a webserver consisting of a Service, Deployment, Ingress, and a Namespace with just a few clicks onto k8s.

Use this demo to explore how infrastructure models defined in Infrahub can be synchronized to a cluster using Vidra and how our Infrahub transformer creates k8s manifest artifacts.

---

## Quick Start (GitHub Codespaces)

1. **Open this repo in GitHub Codespaces or in Visual Studio Code and start the devcontainer**
2. Run the following to initialize everything:

```bash
task init
```
This sets up:

- A local Kubernetes cluster via [Kind](https://kind.sigs.k8s.io) (incl. kubectl, Helm, and k9s)
- Infrahub (incl. git sync, k8s schema, k8s transformation, GraphQL queries, and k8s YAML templates)
- A custom self-service UI (for easily requesting new webservers)
- Vidra Operator and CLI

Check Vidra is running:
```bash
kubectl get pods -n vidra-system
```
💡 Shell convenience features like the `k` alias for `kubectl` and completions may not work in Codespaces.

## 🔧 Infrastructure Modeling via UI

Access UIs via the Ports tab:
- Port `8000`: Infrahub (login: admin / infrahub)
- Port `5001`: Self-service frontend
> **Note:** Virtual machine resources are not working in this demo, as KubeVirt is not installed in the cluster. Only standard Kubernetes resources (such as Deployments, Services, and Ingresses) are supported.

This triggers:
- A new Infrahub branch with the proposed change
- Adding the requested webserver to that branch and to the correct group within Infrahub
- After merging: k8s mainfest artifact generation in Infrahub

## 🔁 Apply Vidra Sync

To sync the model to your cluster, use the CLI:
```bash
host_ip=$(hostname -I | awk '{print $1}')
vidra-cli credentials apply https://${host_ip} --username admin --password infrahub
vidra-cli infrahubsync apply "http://${host_ip}:8000" -a Webserver_Manifest -b main -N default -e
```
If running locally (not in Codespaces), you can also use:
```bash
task vidra-add-sync
```

Now your webserver is deployed to the cluster following GitOps principles (changes to the webserver resources are detected and synced again with the source of truth—Infrahub).

## Explore Vidra
```bash
kubectl get infrahubsyncs.infrahub.operators.com -o yaml
```
```bash
kubectl get vidraresources.infrahub.operators.com
```
```bash
kubectl get vidraresources.infrahub.operators.com -o yaml
```
Get the managed resources:
```bash
kubectl get <kind> <name> -n <namespace>
```
or simply use 
```bash
k9s
```
Access the Webserver:
```bash
kubectl port-forward -n <namespace> <svc/service-name> 8080:80
```
## 📚 Available Tasks
To view available helper commands:
```bash
task
```

## Final Thoughts

This demo isn’t just a quickstart—it’s a glimpse into the future of infrastructure management. Model your systems in Infrahub, let Vidra automate the deployment, and manage everything through intuitive UIs. Whether you’re a platform engineer or just exploring GitOps, this Codespaces-powered demo is the fastest way to experience the workflow.

HAVE FUN! 🥳

