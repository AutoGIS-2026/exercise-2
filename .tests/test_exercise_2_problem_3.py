#!/usr/bin/env python3


"""Test the submitted solutions for exercise 2, problem 3 of AutoGIS."""

import pytest

import geopandas
import pandas
import pyproj

from points_decorator import points


# Sorting by the `timestamp` strings, by parsed datetimes (invalid dates, e.g. 2015-02-29,
# become NaT and sort last), or by parsed datetimes after dropping NaT rows, are all
# reasonable solutions, and lead to slightly different results.
TIMESTAMP_VARIANTS = [
    {"rows": 9026, "mean": 107133.51202944393, "max": 6970668.816343962},
    {"rows": 9026, "mean": 106874.48244489935, "max": 7025053.420056544},
    {"rows": 8937, "mean": 106321.92698874186, "max": 6768931.490425182},
]


class Test_Exercise_2_Problem_3:
    @points(
        1,
        "Problem 3: Did you read the shapefile into a `GeoDataFrame` named "
        "`kruger_points`, and did you re-project it to EPSG:32735?"
    )
    def test_read_reproject(self, problem3):
        assert isinstance(problem3.kruger_points, geopandas.GeoDataFrame)
        assert len(problem3.kruger_points) == 81379
        assert problem3.kruger_points.crs == pyproj.CRS("EPSG:32735")

    @points(
        1,
        "Problem 3: Check again whether you grouped the points correctly!"
    )
    def test_grouped(self, problem3):
        assert isinstance(
            problem3.grouped_by_users,
            pandas.core.groupby.generic.DataFrameGroupBy
        )
        assert (
            len(problem3.grouped_by_users.groups)
            == problem3.kruger_points["userid"].nunique()
        )

    @points(
        2,
        "Problem 3: Have you created a data frame `movements` "
        "that contains LineStrings? "
        "Is it in the correct reference system?"
    )
    def test_movements_linestrings(self, problem3):
        assert isinstance(problem3.movements, geopandas.GeoDataFrame)
        assert problem3.movements.geometry.geom_type.unique() == ["LineString"]
        assert problem3.movements.crs == pyproj.CRS("EPSG:32735")

    @points(
        1,
        "Problem 3: Remember to calculate the distances between "
        "each user’s points (in `movements[\"distance\"])"
    )
    def test_movements_distance(self, problem3):
        assert "distance" in problem3.movements.columns
        assert not problem3.movements["distance"].hasnans
        assert problem3.movements["distance"].dtype == "float64"

    @points(
        0.67,
        "Problem 3: Calculate the shortest distance a user "
        "travelled between all their posts"
    )
    def test_shortest_distance(self, problem3):
        assert problem3.shortest_distance == pytest.approx(0.0)

    @points(
        0.67,
        "Problem 3: Calculate the mean distance travelled per user"
    )
    def test_mean_distance(self, problem3):
        assert any(
            problem3.mean_distance == pytest.approx(variant["mean"])
            for variant in TIMESTAMP_VARIANTS
        )

    @points(
        0.66,
        "Problem 3: Calculate the longest distances a user travelled"
    )
    def test_max_distance(self, problem3):
        assert any(
            problem3.longest_distance == pytest.approx(variant["max"])
            for variant in TIMESTAMP_VARIANTS
        )

    @points(
        1,
        "Problem 3: Did you save the output into a "
        "shapefile `movements.shp` inside `DATA_DIRECTORY`?"
    )
    def test_shapefile(self, problem3):
        assert (problem3.DATA_DIRECTORY / "movements.shp").exists()
        df = geopandas.read_file(problem3.DATA_DIRECTORY / "movements.shp")
        assert len(df) in [variant["rows"] for variant in TIMESTAMP_VARIANTS]
