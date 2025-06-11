from typing import Dict, Any
from requests.auth import HTTPBasicAuth
import requests
import json
import time


def creategroup() -> None:
    """Upsert new group called 'g_webserver'."""
    payload = {
        "query": """
        mutation {
          CoreStandardGroupUpsert(
            data: {
              name: {value: "g_webserver"}
            }
          ) {
            ok
          }
        }
      """
    }
    send_graphql(payload)
    print("Object Gruppe 'g_webserver' was created")

    """Create a new group called 'g_virtuellmaschine'."""
    payload = {
        "query": """
        mutation {
          CoreStandardGroupUpsert(
            data: {
              name: {value: "g_virtuellmaschine"}
            }
          ) {
            ok
          }
        }
      """
    }
    send_graphql(payload)
    print("Object Gruppe 'g_virtuellmaschine' was created")


def createtemplate() -> None:
    """Create a new Kubernetes template for webserver."""
    payload = {
        "query": """
        mutation {
          TemplateKubernetesWebserverUpsert(
            data: {
              template_name: {value: "tem-webserver"},
              port: {value: 80},
              containerport: {value: 80},
              version: {value: 1},
              namespace: {value: "default"},
              replicas: {value: 1}
            }
          ) {
            ok
          }
        }
      """
    }
    send_graphql(payload)
    print("Template was created")

    """Create a new Kubernetes template for g_virtuellmaschine."""
    payload = {
        "query": """
        mutation {
          TemplateKubernetesVirtuellMaschineUpsert(
            data: {
              template_name: {value: "tem-virtuellmaschine"},
              cores: {value: 2},
              namespace: {value: "default"}
            }
          ) {
            ok
          }
        }
      """
    }
    send_graphql(payload)
    print("Template was created")


def createrole() -> None:
    """Create a new role named 'role_createkubernetes'."""
    payload = {
        "query": """
        mutation {
          CoreAccountRoleUpsert(
            data: {
              name: {value: "role_createkubernetes"},
            }
          ) {
            ok
          }
        }
      """
    }
    send_graphql(payload)
    print("Role was created")


def createobjectpermission() -> None:
    """Create a new object permission for Kubernetes."""
    payload = {
        "query": """
        mutation {
          CoreObjectPermissionUpsert(
            data: {
              namespace: {value: "Kubernetes"},
              name: {value: "*"}, # All Objects in this Namespace
              action: {value: "create"},
              decision: {value: 4 }, # 4 is the enum value for "allow_other"
              roles: [{hfid: "role_createkubernetes"}]
            }
          ) {
            ok
          }
        }
      """
    }
    send_graphql(payload)
    print("Permission was created")


def createusergroup() -> None:
    """Create a new user group named 'g_createkubernetesobjects'."""
    payload = {
        "query": """
        mutation {
          CoreAccountGroupUpsert(
            data: {
              name: {value: "g_createkubernetesobjects"},
              roles: [{hfid: "role_createkubernetes"}]
            }
          ) {
            ok
          }
        }
      """
    }
    send_graphql(payload)
    print("Usergroup was created")


def createserviceuser() -> None:
    """Create a new service user for Kubernetes with role 'g_createkubernetesobjects'."""
    payload = {
        "query": """
        mutation {
          CoreAccountUpsert(
            data: {
              name: {value: "g_createservice"},
              password: {value: "g_createservice"},
              member_of_groups: {hfid: "g_createkubernetesobjects"}
            }
          ) {
            ok
          }
        }
      """
    }
    send_graphql(payload)
    print("User was created")


def creategitintegration() -> None:
    """Create a new GitLab integration for Kubernetes deployment."""
    payload = {
        "query": """
        mutation {
          CoreReadOnlyRepositoryUpsert(
            data: {
              name: { value: "Gitlab Inventory" },
              location: { value: "https://github.com/infrahub-operator/infrahub-vidra-demo.git" },
              ref: { value: "main" },
            }
          ) {
            ok
          }
        }
      """
    }

    send_graphql(payload)
    print("Git Integration was created")


def createpool() -> Any:
    """Upserta new service user for Kubernetes with role 'g_createkubernetesobjects'."""
    payload = {
        "query": """
      mutation {
        CoreNumberPoolCreate(data:{
          name: {value: "portpool"},
          node: {value: "KubernetesVirtuellMaschine"},
          node_attribute: {value: "port"},
          start_range: {value: 30000},
          end_range: {value: 32767}
        })
        {
          ok
          object {
            hfid
            id
          }
        }
      }
    """
    }
    id = send_graphql(payload)
    print("Addresspool was created")
    return id


def send_graphql(payload: Dict[str, Any]) -> Any:
    """Send a GraphQL request to the API endpoint."""
    graphql_url = "http://localhost:8000/graphql/main"
    headers = {
        "X-INFRAHUB-KEY": "06438eb2-8019-4776-878c-0941b1f1d1ec",
        "Content-Type": "application/json",
    }

    response = requests.post(
        graphql_url,
        auth=HTTPBasicAuth("admin", "infrahub"),
        headers=headers,
        data=json.dumps(payload),
    )

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Fehler {response.status_code}: {response.text}")


if __name__ == "__main__":
    print("📥 Abfrage läuft...")
    creategroup()
    creategitintegration()
    print("Wait 60sec for Git Synchro")
    time.sleep(60)  # Wait for Git Integration
    createrole()
    createobjectpermission()
    createusergroup()
    createserviceuser()
    createpool()
    createtemplate()
    print("Provisioning Done")
