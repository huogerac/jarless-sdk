"""
Directory helper
"""
import os
from pathlib import Path
import yaml


def get_current_folder():
    """the current project folder"""
    return os.getcwd()


def get_current_config():
    """the current jarless YAML file"""
    config_file_path = f"{get_current_folder()}/.jarless.yml"
    if not os.path.exists(config_file_path):
        raise RuntimeError(f"The '{config_file_path}' is missing")

    with open(config_file_path) as config_file:
        config = yaml.load(config_file)
        image_name = f"{config['name']}:{config.get('version', 'latest')}"
        config["image_name"] = image_name
        config["image_tar_name"] = image_name.replace(":", "__") + ".tar"
        return config


def get_dist_folder_for(folder):
    """the current dist folder"""
    dist_folder = Path(f"{folder}/dist")
    dist_folder.mkdir(exist_ok=True)
    return dist_folder
