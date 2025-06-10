from typing import Dict, Any
from infrahub_sdk.transforms import InfrahubTransform
from .helperfunctions import HelperFunctions
from pathlib import Path

""" This Public Module provides:
- Get Information from the GraphQL
- Compare the Values with the Default YAML Templates
"""


class TransformVirtuellMaschine(InfrahubTransform):
    """Transform data into a YAML string format based on a template."""

    query = "GetVirtuellMaschine"

    async def transform(self, data: Dict[str, Any]) -> str:
        """Transform the input data into a string format based on a YAML template.

        Replacing values with the matching keys from the data.
        """
        currentpath = Path(__file__).resolve()
        pathfile = str(currentpath.parents[1]) + "/YAML_Templates/virtuellmaschine.yaml"
        resultstring = ""

        try:
            with open(pathfile, "r") as yamlfile:
                # Filter and extract the relevant keys from the input data
                customizedkeyvalue = HelperFunctions.filternesteddict(data)
                if not customizedkeyvalue:
                    raise ValueError("No matching keys found in the input data.")

                # Iterate through each line in the YAML template
                for line in yamlfile:
                    if ":" in line:
                        lineprefix = line.split(":")
                        lineresult = HelperFunctions.process_line(
                            "".join(str(element) for element in lineprefix[1:]),
                            customizedkeyvalue,
                        )
                        resultstring += lineprefix[0] + ":" + lineresult
                    else:
                        resultstring += line

        except FileNotFoundError:
            raise FileNotFoundError("YAML template file not found.")
        except Exception as e:
            raise RuntimeError(f"An error occurred during the transformation: {e}")

        return resultstring
