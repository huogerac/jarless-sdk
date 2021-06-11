#!/usr/bin/env python
# pylint: disable=W0703,C0114,C0116
import warnings
import click

from .dockerpy import build_image, save_image, load_image
from .helpers import get_current_config, get_current_folder
from .api import api_create_package, api_get_package_image

warnings.filterwarnings("ignore")


@click.group()
def cli():
    pass


@cli.command("build-package")
def build_package():
    """
    It uses the `Dockerfile` to build the DOCKER IMAGE (using the `docker build`)
    Then it uses the IMAGE to build a binary image (using the `docker save`)
    """
    try:
        config = get_current_config()

        image = build_image(get_current_folder(), config["image_name"])
        click.secho(f"\nImage '{image}' created!", fg="yellow")

        image_tar = save_image(
            get_current_folder(), config["image_name"], config["image_tar_name"]
        )
        click.secho(f"\nImage saved to: '{image_tar}'!", fg="yellow")

    except Exception as error:
        click.secho(error, fg="red")


@cli.command("create-package")
def create_package():
    """
    It uses the binary image (generate by the build)
    for sending the IMAGE (tar file) to the JARLESS SERVER (STORAGE)
    """
    try:
        config = get_current_config()

        directory = get_current_folder()
        image_tar_name = config["image_tar_name"]

        response = api_create_package(
            f"{directory}/dist/{image_tar_name}", f"{directory}/.jarless.yml"
        )
        click.secho(response)

    except Exception as error:
        click.secho(error, fg="red")


@cli.command("load-package")
@click.option("--version", required=True, help="The package version to be loaded.")
def load_package(version):
    """
    It gets the binary image (tar) from JARLESS SERVER (STORAGE)
    and load it to the local docker images,
    the result is the same as the package build
    """
    try:

        click.secho(
            f"TODO: It's missing save/load images using the package {version}",
            fg="yellow",
        )
        config = get_current_config()
        image_name = config["name"]  # f"{config['name']}:{version}"
        target_folder = f"{get_current_folder()}/dist"

        image_path = api_get_package_image(image_name, save_to=target_folder)
        img_name, img_id = load_image(image_path)
        click.secho(f"Package image loaded: {img_name} --> {img_id}")

    except Exception as error:
        click.secho(error, fg="red")


if __name__ == "__main__":
    cli()
