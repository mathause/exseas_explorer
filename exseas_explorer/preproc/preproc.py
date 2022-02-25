"""
This sub-module contains pre-processing functionality.
"""

import geopandas as gpd
# from shapely.geometry import Polygon
# from skimage import measure
import matplotlib.pyplot as plt
import numpy as np
import xarray as xr
from rasterio import features


def extract_contours():
    """
    Extract contours
    """

    contour_data = []

    # Make an object generator
    contours = features.shapes(mask.sel(step=step).values,
                               transform=self.affine_transform,
                               connectivity=4)

    # Get init time and step
    _init_time = getattr(self.intensity.init_time, 'values',
                         self.intensity.init_time)
    _step = getattr(step, 'values', step)

    # Iterate over object generator
    for geom, val in contours:

        # Avoid passing entire domain as final polygon
        if val != 0:

            geometry = shape(geom)
            contour_data.append([_init_time, _step, geometry])

    return contour_data


def update_patches(work_dir='/ytpool/data/ETH/INTEXseas/',
                   patch_file='patches_40y_era5_RTOT_djf_ProbDry.nc'):
    """Read extreme season patches from NetCDF file, convert to polygons, and
    save as GeoJSON files

    TODO
    - Add ability to control this function using click, e.g. using different files

    Parameters
    ----------
    work_dir : str
        Working directory
    patch_file : str
        Input file to process
    """

    # Read file
    in_file = xr.open_dataset(work_dir + patch_file)

    # Convert lables to polygons
    lab_contours = []

    # Re-name key xarray
    in_file = in_file.rename({'key': 'year'})

    # Define NA
    # in_file = xr.where(in_file==0, np.NaN, in_file)

    for year in in_file.year:
        labels = np.unique(in_file.lab.sel(year=year).data)
        labels = np.delete(labels, np.where(labels == 0))
        for label in labels:
            contours = measure.find_contours(in_file.lab.sel(year=year), label)
            polygons = []
            for contour in contours:
                polygons.append(Polygon(contour))
            gdf = gpd.GeoDataFrame(index=[label],
                                   crs='epsg:4326',
                                   geometry=polygons)

    # Save labels as GeoJSON file


test = xr.where(
    in_file.lab.sel(year=year) == 5073, in_file.lab.sel(year=year), 0)

# Display the image and plot all contours found
fig, ax = plt.subplots()
ax.imshow(in_file.lab.sel(year=year), cmap="Spectral")

for contour in test:
    ax.plot(contour[:, 1], contour[:, 0], linewidth=2)

ax.axis('image')
ax.set_xticks([])
ax.set_yticks([])
plt.show()
