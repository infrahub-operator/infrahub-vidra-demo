import sys
import os
from typing import Any


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
from helperfunctions import _HelperFunctions


def createwebserver(name: str, description: str, namespace: str, image: str) -> Any:
    """Create the Webserver with the given Attributes."""
    graphgql = "CreateWebserver"
    payload = {
        "variables": {
            "name": name,
            "description": description,
            "namespace": namespace,
            "image": image,
        }
    }
    json_data = _HelperFunctions._send_graphql(
        graphgql, payload, branch=namespace + name
    )
    return json_data["data"]["KubernetesWebserverCreate"]["object"]["host"]["value"]


def createvirtuellmaschine(
    name: str, description: str, namespace: str, url: str
) -> Any:
    """Create the Webserver with the given Attributes."""
    graphgql = "CreateVirtuellMaschine"
    payload = {
        "variables": {
            "name": name,
            "description": description,
            "namespace": namespace,
            "url": url,
        }
    }
    json_data = _HelperFunctions._send_graphql(
        graphgql, payload, branch=namespace + name
    )
    return f"ssh {name}@10.8.36.20 -p {json_data['data']['KubernetesVirtuellMaschineCreate']['object']['port']['value']}"
