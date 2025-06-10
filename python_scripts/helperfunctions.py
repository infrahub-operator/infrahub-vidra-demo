from typing import Dict, Any
from requests.auth import HTTPBasicAuth
import json
import requests


class _HelperFunctions:
    @staticmethod
    def _send_graphql(
        graphql: str, payload: Dict[str, Any], branch: str = "main"
    ) -> dict[str, Any]:
        responsebranch = _HelperFunctions._createbranch(branch)
        if responsebranch != 200:
            raise ValueError("An Error occurred in the Creation of the Branch")

        graphqlurl = f"http://localhost:8000/api/query/{graphql}?&branch={branch}"
        headers = {"X-INFRAHUB-KEY": "06438eb2-8019-4776-878c-0941b1f1d1ec"}
        payload = payload
        response = requests.post(
            graphqlurl,
            auth=HTTPBasicAuth("g_createservice", "g_createservice"),
            headers=headers,
            data=json.dumps(payload),
        )
        if response.status_code != 200:
            raise ValueError("An Error occurred in the Creation of the Branch")

        if "name" in payload["variables"]:
            name = f"New Proposed Change for a Webserver {payload['variables']['name']}"
        description = f"{payload['variables']}"
        responseproposedchange = _HelperFunctions._createproposedchange(
            branch, name, description
        )
        if responseproposedchange  != 200:
            raise ValueError("An Error occurred in the Creation of the Proposed Change")

        return response.json()  # type: ignore 

    @staticmethod
    def _createbranch(branchname: str) -> int:
        graphqlurl = "http://localhost:8000/api/query/CreateBranch"
        headers = {"X-INFRAHUB-KEY": "06438eb2-8019-4776-878c-0941b1f1d1ec"}
        payload = {"variables": {"branchname": branchname}}
        response = requests.post(
            graphqlurl,
            auth=HTTPBasicAuth("admin", "infrahub"),
            headers=headers,
            data=json.dumps(payload),
        )
        return response.status_code

    @staticmethod
    def _createproposedchange(
        sourcebranch: str,
        name: str = "New Proposed Change!",
        description: str = "New Proposed Change. Please review it.",
    ) -> int:
        graphqlurl = "http://localhost:8000/api/query/CreateProposedChange"
        headers = {"X-INFRAHUB-KEY": "06438eb2-8019-4776-878c-0941b1f1d1ec"}
        payload = {
            "variables": {
                "sourcebranch": sourcebranch,
                "name": name,
                "description": description,
            }
        }
        response = requests.post(
            graphqlurl,
            auth=HTTPBasicAuth("admin", "infrahub"),
            headers=headers,
            data=json.dumps(payload),
        )

        return response.status_code
