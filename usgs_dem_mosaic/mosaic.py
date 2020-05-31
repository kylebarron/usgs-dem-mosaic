from cogeo_mosaic.mosaic import MosaicJSON
from geojson import Feature
from shapely.geometry import box

from .s3 import list_s3

DEFAULT_ZOOMS = {'1': [8, 12], '13': [8, 13], '1m': [11, 17], '2': [8, 12]}
BUCKET = 'prd-tnm'


def create_mosaic(urls=None, res=None):
    allowed_res = ['1', '13', '1m', '2']
    if res and res not in allowed_res:
        raise ValueError(f'res must be in {allowed_res}')

    urls = find_urls_for_res(res)

    features = []
    for url in urls:
        key = url.split('/')[4]
        geom = box(*parse_grid(key))
        full_s3_path = f's3://{BUCKET}/{url}'
        feature = Feature(geometry=geom, properties={'path': full_s3_path})
        features.append(dict(feature))

    minzoom, maxzoom = DEFAULT_ZOOMS[res]
    mosaic = MosaicJSON.from_features(
        features, minzoom, maxzoom, accessor=lambda x: x['properties']['path'])


def find_urls_for_res(res):
    assert res != '1m', 'Use spatial metadata file for 1m data'

    ext = '.tif'
    prefix = f'StagedProducts/Elevation/{res}/'
    return list(list_s3(BUCKET, prefix, ext))


def parse_grid(key):
    """Parse standard 1-arc-second filename grid
    """
    minx, miny, maxx, maxy = [None] * 4

    if key[0] == 'n':
        maxy = int(key[1:3])
        miny = maxy - 1
    else:
        maxy = -1 * int(key[1:3])
        miny = maxy - 1

    if key[3] == 'w':
        minx = -1 * int(key[4:])
        maxx = minx + 1
    else:
        minx = int(key[4:])
        maxx = minx + 1

    return minx, miny, maxx, maxy
