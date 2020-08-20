"""
Parse FGDC metadata
"""
import re
from pathlib import Path

import geopandas as gpd
import pandas as pd
from bs4 import BeautifulSoup
from shapely.geometry import box


def parse_xml(xml, fields):
    soup = BeautifulSoup(xml)

    # Field names must be unique within the FGDC metadata
    data = {}
    for field in fields:
        xml_field = soup.find(field)
        data[field] = xml_field and xml_field.text

    return data


def parse_meta(meta_dir):
    meta_dir = Path(meta_dir)
    xy_regex = re.compile(r'x(\d{2})y(\d{3})')

    data = []
    i = 0
    for meta_file in meta_dir.glob('**/*.xml'):
        name = meta_file.stem
        x, y = xy_regex.search(name).groups()

        project_dir = meta_file.parents[1].name

        with meta_file.open() as f:
            d = parse_xml(
                f.read(),
                fields=['utmzone', 'westbc', 'eastbc', 'northbc', 'southbc'])

        d['name'] = name
        d['x'] = x
        d['y'] = y
        d['project_dir'] = project_dir

        data.append(d)

        i += 1
        if i % 1000 == 0:
            print(i)

    return pd.DataFrame(data)


def meta_to_wgs84(df):
    """Convert meta file with multiple UTM zones to WGS84

    TODO check that projected position is near WGS bounds from metadata file. At
    least a couple occurences of elevation in the ocean. Probably should be utm
    11 instead of 10.
    """
    df['x'] = pd.to_numeric(df['x'])
    df['y'] = pd.to_numeric(df['y'])

    wgs84_dfs = []
    for utmzone, group in df.groupby('utmzone'):
        group['geometry'] = group.apply(
            lambda row: create_box(row['x'], row['y']), axis=1)
        utm_epsg = f'epsg:269{utmzone}'
        group_gdf = gpd.GeoDataFrame(group, crs=utm_epsg)

        wgs84 = group_gdf.to_crs(epsg=4326)
        wgs84_dfs.append(wgs84)

    concat_gdf = pd.concat(wgs84_dfs)
    return concat_gdf


def create_box(x, y):
    """Create UTM shapely geometry from top left corner
    """
    minx = x * 10000
    miny = (y - 1) * 10000
    maxx = (x + 1) * 10000
    maxy = y * 10000
    return box(minx, miny, maxx, maxy)
