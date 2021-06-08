#!/usr/bin/env python
import warnings
import click

from .dockerpy import build_image, save_image
from .helpers import get_current_config, get_current_folder
from .api import api_create_package

warnings.filterwarnings("ignore")


@click.group()
def cli():
    pass


@cli.command("build-package")
def build_package():
    config = get_current_config()

    image = build_image(get_current_folder(), config["image_name"])
    click.secho(f"\nImage '{image}' created!", fg="yellow")

    image_tar = save_image(
        get_current_folder(), config["image_name"], config["image_tar_name"]
    )
    click.secho(f"\nImage saved to: '{image_tar}'!", fg="yellow")


@cli.command("create-package")
def create_package():
    config = get_current_config()

    directory = get_current_folder()
    image_tar_name = config["image_tar_name"]

    response = api_create_package(
        f"{directory}/dist/{image_tar_name}", f"{directory}/.jarless.yml"
    )
    click.secho(response)


if __name__ == "__main__":
    cli()
