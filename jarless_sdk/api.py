"""
The module that is wrapper to the JARLESS backend API
"""
import os
import json
import requests

JARLESS_SERVER_URL = os.getenv("JARLESS_SERVER_URL", "http://localhost:5000")
_8MB = 8192


def api_create_package(tar_path, yaml_path):
    """Send the image (tar) to be created"""
    if not os.path.exists(yaml_path):
        raise RuntimeError(f"The YAML package is missing: {yaml_path}")

    if not os.path.exists(tar_path):
        raise RuntimeError(f"Build the image first! The TAR file not found: {tar_path}")

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


def api_get_package_image(package_name, save_to="/tmp"):
    """get the package image (tar)"""
    resp = requests.get(
        f"{JARLESS_SERVER_URL}/api/packages/{package_name}/images/download"
    )
    if resp.status_code != 200:
        raise RuntimeError("something went wrong!")

    json_data = resp.json()
    image_name = json_data["url"].split("?")[0].split("/")[-1]

    target_path = f"{save_to}/{image_name}"

    with requests.get(json_data["url"], stream=True) as data:
        data.raise_for_status()
        with open(target_path, "wb") as target_file:
            for chunk in data.iter_content(chunk_size=_8MB):
                target_file.write(chunk)
    return target_path
