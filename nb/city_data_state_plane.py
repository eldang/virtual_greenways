import pandas as pd
import shapefile
import pyproj


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


def read_shape_state_plane(filename):
    sf = shapefile.Reader(filename)
    shapes = sf.shapes()

    keys = [f[0] for f in sf.fields[1:]] + ['points']

    sf_dict = {idx: dict(zip(keys, row.record + [project_points2(row.shape.points)]))
               for idx,row in enumerate(sf.iterShapeRecords())}


    segment_df = pd.DataFrame.from_dict(sf_dict, orient='index')
 
    return segment_df