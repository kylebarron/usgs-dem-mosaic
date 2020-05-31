import sys

import click

from usgs_dem_mosaic.s3 import list_s3 as _list_s3


@click.command()
@click.option(
    '-b',
    '--bucket',
    type=str,
    default='prd-tnm',
    show_default=True,
    help='Bucket name')
@click.option(
    '-p',
    '--prefix',
    type=str,
    default='StagedProducts/Elevation/13/TIFF/',
    show_default=True,
    help='Prefix to list within')
@click.option(
    '--ext',
    type=str,
    default='.tif',
    show_default=True,
    help=
    'Suffix/file extension to filter for. To turn off filtering, pass None or an empty string'
)
def list_s3(bucket, prefix, ext):
    """Get listing of files on S3 with prefix and extension
    """
    counter = 0
    for key in _list_s3(bucket, prefix, ext):
        counter += 1
        if counter % 5000 == 0:
            print(f'Found {counter} items so far', file=sys.stderr)

        print(key)


if __name__ == '__main__':
    list_s3()
