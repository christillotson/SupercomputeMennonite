import os
import sys
from pathlib import Path

import numpy as np
import rasterio

sys.path.append(str(Path(__file__).resolve().parent))
from Sentinel2Indices import INDICES

BAND_FILES = ["B01", "B02", "B03", "B04", "B05", "B06", "B07", "B8A", "B09", "B11", "B12"]


def load_bands(scene_dir):
    bands = []
    profile = None
    shape = None
    transform = None
    crs = None

    for band_name in BAND_FILES:
        jp2_path = os.path.join(scene_dir, f"{band_name}.jp2")
        if not os.path.exists(jp2_path):
            raise FileNotFoundError(f"Missing band file: {jp2_path}")

        with rasterio.open(jp2_path) as src:
            if profile is None:
                profile = src.profile.copy()
                shape = (src.height, src.width)
                transform = src.transform
                crs = src.crs
            else:
                if (src.height, src.width) != shape:
                    raise ValueError(f"Band {band_name} has mismatched dimensions.")
                if src.transform != transform:
                    raise ValueError(f"Band {band_name} has mismatched transform.")
                if src.crs != crs:
                    raise ValueError(f"Band {band_name} has mismatched CRS.")

            arr = src.read(1).astype(np.float32)

            if np.nanmax(arr) > 1.5:
                arr = arr / 10000.0

            bands.append(arr)

    return bands, profile


def build_output_profile(src_profile):
    profile = src_profile.copy()
    profile.update(
        driver="GTiff",
        dtype=rasterio.float32,
        count=1,
        nodata=np.nan,
        compress="deflate",
        predictor=3,
        zlevel=6,
    )
    return profile


def process(scene_dir, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    print(f"Loading bands from '{scene_dir}'...")
    bands, profile = load_bands(scene_dir)
    print(f"Loaded {len(bands)} bands.")
    out_profile = build_output_profile(profile)

    for index_func in INDICES:
        name = index_func.__name__
        out_path = os.path.join(output_dir, f"{name}.tif")

        print(f"Computing {name}...")
        index_array = index_func(*bands).astype(np.float32)

        with rasterio.open(out_path, "w", **out_profile) as dst:
            dst.write(index_array, 1)

        print(f"  Saved -> {out_path}")

    print(f"\nDone. Wrote {len(INDICES)} index GeoTIFFs to '{output_dir}'.")


def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_index_tiffs.py <scene_dir> [output_dir]")
        sys.exit(1)

    scene_dir = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) >= 3 else os.path.join(scene_dir, "indices")

    process(scene_dir, output_dir)


if __name__ == "__main__":
    main()
