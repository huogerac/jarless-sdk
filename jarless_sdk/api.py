import os
import json
import requests

JARLESS_SERVER_URL = os.getenv("JARLESS_SERVER_URL", "http://localhost:5000")


def api_create_package(tar_path, yaml_path):

    files = {
        "tardata": open(tar_path, "rb"),
        "yamldata": open(yaml_path, "rb"),
    }

    resp = requests.post(
        f"{JARLESS_SERVER_URL}/api/packages?overwrite=true", files=files
    )
    if resp.status_code != 201:
        raise RuntimeError("something went wrong!")

    return json.dumps(resp.json(), indent=2)
