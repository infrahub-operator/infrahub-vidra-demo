# infrahub-vidra-demo
Demo of Infrahub meets Kubernetes by using Vidra 

## Installation, provision infrahub and run Webserver
```bash
task init
```

Check if the Vidra operator is installed and running
```bash
kubectl get pod -n vidra-system
```
Apparently completion and the alias `k` are not working in Codespaces

## Frontend and Infrahub
Infrahub and the self-service Frontend can be accessed by opening the ports tab, clicking on the globe icon in the Forwarded Address column of port 8000 and 5001.

- In the frontend you can now create a webserver request.
- This will generate a proposed change on a new branch in Infrahub. 
- Login to Infrahub (User: `admin`; Password: `infrahub`) and merge the proposed change. It will now create the Artifacts.

## Vidra Sync
Now you can add a [InfrahubSync](https://infrahub-operator.github.io/vidra/guides/usage) 

There is the sync to main branch Webserver Artifact prepared using `vidra-cli`:
```bash
host_ip=$(hostname -I | awk '{print $1}')
vidra-cli credentials apply https://${host_ip} --username admin --password infrahub
vidra-cli infrahubsync apply "http://${host_ip}:8000" -a Webserver_Manifest -b main -N default -e
```

or simply (does not work in codespaces)
```bash
task vidra-add-sync
```

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

HAVE FUN!