from core import *
from __init__ import *
from lodes import *
from variables import *
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import Point
import json
import pandas
from math import sqrt

MY_API_KEY = #INSERT API KEY

fname = 'census_area/census_area/water_district_boundary_sample.geojson'
with open(fname) as infile:
    my_shape_geojson = json.load(infile)


def func(MY_API_KEY, target_variable, MoE_variable): 
    
    c = Census(MY_API_KEY, year = 2010)
    features = []
    pop_variable = 'B01003_001E'
    old_homes = c.acs5.geo_tract(('NAME',pop_variable, target_variable, MoE_variable), my_shape_geojson['features'][0]['geometry'])
    weight = {}
    population, moe_square= 0, 0
    variables = []
    for tract_geojson, tract_data, wei in old_homes:
        points = []
        for point in tract_geojson['geometry']['coordinates'][0]:
            points.append((point))
        tract_area = Polygon(points).area
        weight_id = tract_data['tract']
        weight[weight_id] = {}
        weight[weight_id]['area_in_tract'] =  tract_area
        weight[weight_id]['population'] = tract_data[pop_variable]
        weight[weight_id]['geometry'] =  Polygon(points)
        weight[weight_id]['areal_weight'] = wei
        weight[weight_id]['popu_intersect'] = wei * tract_data[pop_variable]
        weight[weight_id]['variable_whole'] = tract_data[target_variable]
        population += weight[weight_id]['popu_intersect']
        moe_square += tract_data[MoE_variable] ** 2

    # calclate the population weight in another for loop:            
    for wei_ids in weight:
    
        weight[wei_ids]['popul_weight'] = weight[wei_ids]['popu_intersect'] / population


    # calculate the statistic in a new for loop.
    average, total_sum = 0, 0
    for wei_ids in weight:
        # if target_variable_weight == 'Areal':
        #     weight[weight_id]['variable_intersection'] = tract_data[target_variable] * wei
        # if target_variable_weight == 'Population':
        #     weight[weight_id]['variable_intersection'] = tract_data[target_variable] * weight[wei_ids]['popul_weight'] 
        # else:
        #     raise ValueError('the name of the weight has to be Population or Areal')
            
        # calculate a simple average in this for loop:
        # multiply population weight and areal weight
        weight[wei_ids]['variable_intersection'] = weight[wei_ids]['variable_whole'] * weight[wei_ids]['areal_weight']
        average += weight[wei_ids]['variable_whole'] *  weight[wei_ids]['popul_weight'] * weight[wei_ids]['areal_weight']
        total_sum += weight[wei_ids]['variable_intersection']
            
    moe = sqrt(moe_square)
    

    return (population, average, moe, total_sum)
