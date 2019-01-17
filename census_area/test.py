from core import *
from _init_ import *
from lodes import *
from variables import *
from shapely.geometry import LineString
from shapely.geometry import Polygon
from shapely.geometry import Point
import json
from math import sqrt


fname = 'census_area/census_area/water_district_boundary_sample.geojson'
with open(fname) as infile:
    my_shape_geojson = json.load(infile)

# Geometry should be a water district json file
def variable_reaggregagion(census_API_key, target_variable, geometry, type_of_statistic, type_of_aggregation):
    '''
    census_API_key is the API key
    target_variable is the variable we need to calculate
    geometry should be a water district json file      
    type of statistic can be : count, per_capita, per_household.  
    type of aggregation can be: sum, average, moe_sum.
    '''
    c = Census(MY_API_KEY, year = 2010)
    features = []
    MoE_variable = target_variable[0: len(target_variable) - 1] + 'M'
    pop_variable = 'B01003_001E'
    household_variable = 'DP02_0001E'
    old_homes = c.acs5.geo_tract(('NAME', pop_variable, household_variable, target_variable, MoE_variable), geometry['features'][0]['geometry'])
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
        
        weight[weight_id]['household_intersect'] = tract_data[household_variable] * wei
        
        weight[weight_id]['variable_whole'] = tract_data[target_variable]
        population += weight[weight_id]['popu_intersect']
        moe_square += tract_data[MoE_variable] ** 2
        total_household += weight[weight_id]['household_intersect']
        
    # calclate the population weight and the household weight in another for loop:            
    for wei_ids in weight:
    
        weight[wei_ids]['popul_weight'] = weight[wei_ids]['popu_intersect'] / population
        weight[wei_ids]['household_weight'] = weight[wei_ids]['household_intersect'] / total_household


    # calculate the statistic in a new for loop.
    
        # calculate a simple average in this for loop:
        # multiply population weight and areal weight
    
        # type of statistics:
    if type_of_statistic == 'count':
        for wei_ids in weight:
            weight[wei_ids]['variable_intersection'] = weight[wei_ids]['variable_whole'] * weight[wei_ids]['areal_weight']
    elif type_of_statistic == 'per_capita':
        for wei_ids in weight:
            weight[wei_ids]['variable_intersection'] = weight[wei_ids]['variable_whole'] * weight[wei_ids]['popul_weight']
    elif type_of_statistic == 'per_household':
        for wei_ids in weight:
            weight[wei_ids]['variable_intersection'] = weight[wei_ids]['variable_whole'] * weight[wei_ids]['household_weight']
    else:
        raise ValueError('incorrect type_of_statistic')
     
    average, total_sum = 0, 0    
    if type_of_aggregation == 'sum':
        for wei_ids in weight:
            total_sum += weight[wei_ids]['variable_intersection']
        return total_sum
    if type_of_aggregation == 'average':
        for wei_ids in weight:
            average += weight[wei_ids]['variable_whole'] *  weight[wei_ids]['popul_weight'] * weight[wei_ids]['areal_weight']
        return average
        
    if type_of_aggregation == 'moe_sum':
        moe = sqrt(moe_square)
        return moe
    else:
        raise ValueError('incorrect type_of_aggregation')
