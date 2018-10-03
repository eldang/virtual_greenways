import pandas as pd
import shapefile


st_codes = {
    'Multipurpose Trail': 22
}


vehicle_use_codes = {
    'micromobility': 2 # non-motorized
}


def flip_points(points):
    return [(lat, lon) for (lon, lat) in points]


def read_shape(filename):
    sf = shapefile.Reader(filename)
    shapes = sf.shapes()
    
    keys = [f[0] for f in sf.fields[1:]] + ['points']

    sf_dict = {idx: dict(zip(keys, row.record + [flip_points(row.shape.points)]))
               for idx,row in enumerate(sf.iterShapeRecords())}


    segment_df = pd.DataFrame.from_dict(sf_dict, orient='index')
 
    return segment_df


#selected_df = segment_df[(segment_df.ARTERIAL_C==1) & (segment_df.R_ZIP=='98125')]
#selected_df = segment_df[segment_df.ST_CODE==st_codes['Multipurpose Trail']]
#selected_df = segment_df[segment_df.VEHICLE_US==vehicle_use_codes['micromobility']]
#segment_df['ARTERIAL_C']