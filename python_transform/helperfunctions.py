from typing import Dict, Any, cast
import re


class HelperFunctions:
    """Helper functions to process nested dictionaries and lines in text."""

    singledict: Dict[str, str] = {}

    @staticmethod
    def filternesteddict(nesteddict: Dict[str, Any], key: str = "") -> Dict[str, str]:
        """Filter nested dictionaries and store the result in a global dictionary."""
        for nestedkey, value in nesteddict.items():
            # Check if Dictionary is nested
            if isinstance(value, dict):
                HelperFunctions.filternesteddict(value, nestedkey)
                continue
            if isinstance(value, list) and (
                isinstance(value[0], dict) or isinstance(value[0], list)
            ):
                HelperFunctions.filternesteddict(
                    cast(Dict[str, Any], value[0]), nestedkey
                )
                continue

            # Write the key-value pair to the global single dictionary
            HelperFunctions.singledict[key.lower()] = str(value).lower()

        return HelperFunctions.singledict

    @staticmethod
    def match_key_in_line(line: str, key: str) -> bool:
        """Check if a specific key is present in the line (case-insensitive)."""
        pattern = rf"\W{re.escape(key)}\W"  # Searching for a non-word Character (like -), de key word and non-word character.
        return bool(re.search(pattern, line, re.IGNORECASE))

    @staticmethod
    def process_line(line: str, customizedkeyvalue: Dict[str, Any]) -> str:
        """Process each line, replacing matching keys with values from the input data."""
        for key, value in customizedkeyvalue.items():
            if HelperFunctions.match_key_in_line(line, key):
                line = line.replace(key, value)
        return line
