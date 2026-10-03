#!/usr/bin/env python3


"""Test the submitted solutions for exercise 2, problem 2 of AutoGIS."""

import geopandas
import pandas
import pyproj
import shapely.wkt

from points_decorator import points


def plotted_extents(figures):
    """Yield the (xmin, xmax, ymin, ymax) of all axes in `figures` that show data."""
    for figure in figures:
        for axes in figure.axes:
            if axes.collections or axes.patches or axes.lines or axes.images:
                yield axes.get_xlim() + axes.get_ylim()


def plot_shows(figures, x, y):
    """Is there a plot whose extent contains the point (x, y)?"""
    return any(
        xmin <= x <= xmax and ymin <= y <= ymax
        for xmin, xmax, ymin, ymax in plotted_extents(figures)
    )


class Test_Exercise_2_Problem_2:
    @points(
        1,
        "Problem 2: Did you read the CSV file"
        " into a data frame called `data`?"
    )
    def test_csv_read(self, problem2):
        assert isinstance(problem2.data, pandas.DataFrame)
        assert len(problem2.data) == 81379
        for column in ("lon", "lat", "timestamp", "userid"):
            assert column in problem2.data.columns

    @points(
        2,
        "Problem 2: `data` does not have a `geometry` column, "
        "or the geometry column does not contain `shapely.geometry.Points`"
    )
    def test_geometry_column(self, problem2):
        assert isinstance(problem2.data, pandas.DataFrame)
        assert "geometry" in problem2.data.columns
        assert problem2.data.geometry.apply(
            lambda g: isinstance(g, shapely.geometry.Point)
        ).unique() == [True]

    @points(
        1,
        "Problem 2: Did you convert `data` into a `geopandas.GeoDataFrame`?"
    )
    def test_gdf(self, problem2):
        assert isinstance(problem2.data, geopandas.GeoDataFrame)

    @points(
        1,
        "Problem 2: `data` does not seem to have a coordinate"
        " reference system defined."
    )
    def test_gdf_crs(self, problem2):
        assert problem2.data.crs == pyproj.CRS("EPSG:4326")

    @points(
        1,
        "Problem 2: Save the data to a Shapefile "
        "`kruger_points.shp` in `DATA_DIRECTORY`"
    )
    def test_shapefile(self, problem2):
        assert (problem2.DATA_DIRECTORY / "kruger_points.shp").exists()
        df = geopandas.read_file(problem2.DATA_DIRECTORY / "kruger_points.shp")
        assert len(df) == 81379

    @points(1, "Problem 2: Did you plot the data set?")
    def test_plot(self, problem2):
        assert plot_shows(problem2._FIGURES, 31.5, -24.0)
