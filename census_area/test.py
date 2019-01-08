from core import *
from __init__ import *
from lodes import *
from variables import *
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import Point
import json
import pandas

MY_API_KEY = '475e7ac8120a6caa3641a5bb4b305ac92128eaac'

fname = 'census_area/census_area/water_district_boundary_sample.geojson'
with open(fname) as infile:
    my_shape_geojson = json.load(infile)

c = Census(MY_API_KEY, year = 2010)

features = []
old_homes = c.acs5.geo_tract(('NAME','B01003_001E', 'B25034_010E'), my_shape_geojson['features'][0]['geometry'])
weight = {}
for tract_geojson, tract_data, wei in old_homes:
    points = []
    for point in tract_geojson['geometry']['coordinates'][0]:
        points.append((point))
    tract_area = Polygon(points).area
    weight_id = tract_data['tract']
    weight[weight_id] = {}
    weight[weight_id]['area_in_tract'] =  tract_area
    weight[weight_id]['population'] = tract_data['B01003_001E']
    weight[weight_id]['geometry'] =  Polygon(points)
    weight[weight_id]['areal_weight'] = wei
# a = AreaFilter()
