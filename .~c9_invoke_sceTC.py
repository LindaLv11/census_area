"""
Your module description
"""
import pandas as pd
import json
import shapely
from shapely.geometry import Polygon
from shapely.geometry import Point
import pandas
import census
import census_area
MY_API_KEY = '475e7ac8120a6caa3641a5bb4b305ac92128eaac'
fname = '/home/ec2-user/environment/census_area/water_district_boundary_sample.geojson'
with open(fname) as infile:
    my_shape_geojson = json.load(infile)

c = /census_area/census_area/__init__.py.Census()