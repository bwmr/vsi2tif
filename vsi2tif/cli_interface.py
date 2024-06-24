import click

from vsi2tif import utils


@click.command()
@click.option(
    "--bleach-correct",
    is_flag=True,
    default=False,
    help="Correct intensity for photo-bleaching.",
)
@click.option(
    "--split-colors",
    is_flag=True,
    default=False,
    help="Save one (simple) tiff per channel, instead of one ome-tiff for all.",
)
@click.argument(
    "input_files",
    nargs=-1,
    type=click.Path(exists=True, file_okay=True, dir_okay=False),
)
def vsi2tif_cli(bleach_correct: bool, split_colors: bool, input_files: []):
    """
    Convert one or many vsi-files to ome-tiff.

    Bleach-correct by histogram matching if desired (XYZ only!)

    Split by color if desired.

    """
    utils._vsi2tif(bleach_correct, split_colors, input_files)

    return
