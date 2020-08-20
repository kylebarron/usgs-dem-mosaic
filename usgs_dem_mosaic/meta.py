"""
Parse FGDC metadata
"""
import re
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup


def parse_xml(xml, fields=['utmzone']):
    soup = BeautifulSoup(xml)

    # Field names must be unique within the FGDC metadata
    return {field: soup.find(field).text for field in fields}


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
            d = parse_xml(f.read(), fields=['utmzone'])

        d['name'] = name
        d['x'] = x
        d['y'] = y
        d['project_dir'] = project_dir

        data.append(d)

        i += 1

        if i == 1000:
            break

    return pd.DataFrame(data)
