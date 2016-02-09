import fiona
import shapefile
import pandas as pd
import pyproj
from functools import partial
from shapely.geometry import Point
from shapely.ops import transform
import folium_test
from folium_test import UNCLASSIFIED, INTERMEDIATE, DIFFICULT, ALL_ABILITIES,\
    segments_to_map
import os

# http://stackoverflow.com/questions/31900600/python-and-shapefile-very-large-coordinates-after-importing-shapefile
def project_points(points, projection):
    points_wgs84 = (transform(projection, Point(p)) for p in points)
    
    points_transformed = [(p.y, p.x) for p in points_wgs84]
    
    return points_transformed

def project_points2(points):
    state_plane = pyproj.Proj(init='epsg:2926', preserve_units=True)
    wgs = pyproj.Proj(proj='latlong', datum='WGS84', ellps='WGS84')
    longlat = [pyproj.transform(state_plane, wgs, x, y) for x, y in points]
    
    return [(lat, lon) for (lon, lat) in longlat]

# see http://pandas.pydata.org/pandas-docs/stable/indexing.html
def select_segments(segment_df):
    selected_df = segment_df.query('Existing == "Y"')
    return selected_df
    

def segments_to_folium(segment_df):
    folium_df = pd.DataFrame(segment_df.loc[:,['STNAME',
                                               'FType_1023',
                                               'points']])
    folium_df.rename(columns={'STNAME': 'name',
                              'FType_1023': 'description',
                              'points': 'polyline'},
                     inplace=True)
    folium_df['district'] = 'Current'
    folium_df['difficulty'] = UNCLASSIFIED
    folium_df['difficulty_code'] = 'u'
    return folium_df


def classify_segments(folium_df):
    query_string = 'description == "In street major separation"' 
    rows = folium_df.query(query_string).index
    folium_df.loc[rows,['difficulty']] = INTERMEDIATE
    folium_df.loc[rows,['difficulty_code']] = 'i'

    query_string = 'description == "Multi use Trail" or description == "Enhanced Street"' 
    rows = folium_df.query(query_string).index
    folium_df.loc[rows,['difficulty']] = ALL_ABILITIES
    folium_df.loc[rows,['difficulty_code']] = 'e'
    
    query_string = 'description == "Sharrows" or description == "In street minor separation"' 
    rows = folium_df.query(query_string).index
    folium_df.loc[rows,['difficulty']] = DIFFICULT
    folium_df.loc[rows,['difficulty_code']] = 'd'
    
    
def read_projection(shapefilename):
    shp = fiona.open(shapefilename)
    #p_in = pyproj.Proj(shp.crs)
    # see: http://www.seattle.gov/dpd/cityplanning/populationdemographics/geographicfilesmaps/intro/
    # and: http://www.spatialreference.org/ref/?search=Washington
    # EPSG:2926: NAD83(HARN) / Washington North (ftUS)
    p_in = pyproj.Proj({'init': 'EPSG:2926'})   # 
    p_out = pyproj.Proj({'init': 'EPSG:4326'})  # aka WGS84
    projection = partial(pyproj.transform, p_in, p_out)
    shp.close()
    
    return projection
    
def read_shape(filename):
    #projection = read_projection(filename)
    sf = shapefile.Reader("BMP_bob.shp")
    shapes = sf.shapes()

    print(len(shapes))
    print(sf.fields)
    
    keys = [f[0] for f in sf.fields[1:]] + ['points']

    sf_dict = {idx: dict(zip(keys, row.record + [project_points2(row.shape.points)]))
               for idx,row in enumerate(sf.iterShapeRecords())}

    
    segment_df = pd.DataFrame.from_dict(sf_dict, orient='index')
 
    return segment_df

if __name__ == '__main__':
    segment_df = read_shape(os.path.join("BMP", "BMP_Bob.shp"))
    selected_df = select_segments(segment_df)
    folium_df = segments_to_folium(selected_df)
    classify_segments(folium_df)

    coords = [47.6131746,-122.4878834] # Seattle
    
    segments_to_map(coords, folium_df,
                    included=['e'],
                    filename='greenways_green.html')
    segments_to_map(coords, folium_df,
                    included=['e', 'i'],
                    filename='greenways_yellow.html')
    segments_to_map(coords, folium_df,
                    included=['e', 'i', 'd'],
                    filename='greenways_red.html') 
    segments_to_map(coords, folium_df,
                    included=['e', 'i', 'd', 'u'],
                    filename='greenways_all.html')   
    print('done')