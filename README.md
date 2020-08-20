# usgs-dem-mosaic

Create MosaicJSONs for USGS Cloud-Optimized GeoTIFF DEMs

## Notes

```bash
mkdir -p data/
python usgs_dem_mosaic/scripts/list_s3.py \
    --bucket 'prd-tnm' \
    --prefix 'StagedProducts/Elevation/13/TIFF/' \
    --ext '.tif' \
    > data/geotiff_13_files.txt
```

## 1 meter

Download current spatial metadata

```bash
aws s3 cp s3://prd-tnm/StagedProducts/Elevation/1m/FullExtentSpatialMetadata/FESM_1m.gpkg data/
# or
wget https://prd-tnm.s3-us-west-2.amazonaws.com/StagedProducts/Elevation/1m/FullExtentSpatialMetadata/FESM_1m.gpkg -O data/FESM_1m.gpkg
```


1. Download XML metadata

Note, it's important to download the entire folder so that the processing script
works correctly.

```bash
aws s3 cp \
    s3://prd-tnm/StagedProducts/Elevation/1m/Projects/ \
    . \
    --recursive --exclude="*" --include="*xml"
```

2. Process XML metadata

Code in `meta.py` not yet a CLI

### Notes

- If you use "first" pixel selection, then you always want the lower-resolution image as a fallback.


