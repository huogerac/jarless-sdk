"""
The module that encapsulate the docker operations
"""
import logging
import docker

from .helpers import get_dist_folder_for

client = docker.from_env()
client_api = docker.APIClient(base_url="unix://var/run/docker.sock")
logger = logging.getLogger(__name__)


def build_image(folder, image_name):
    """Builds the project image using its Dockerfile"""
    for line in client_api.build(path=folder, rm=True, tag=image_name, decode=True):
        logger.warning(line.get("stream", "").rstrip("\n"))
    return image_name


def save_image(folder, image_name, image_tar_name):
    """Generates the project image (tar)"""
    dist_folder = get_dist_folder_for(folder)
    target_image = f"{dist_folder}/{image_tar_name}"

    image = client.images.get(image_name)
    with open(target_image, "wb") as target_file:
        for chunk in image.save(named=True):
            target_file.write(chunk)
    return target_image


def load_image(image_tar_path):
    """Load and image file (tar)"""
    with open(image_tar_path, "rb") as tar_file:
        image = client.images.load(tar_file)
        return image[0].tags[0], image[0].short_id
